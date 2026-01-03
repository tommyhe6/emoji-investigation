import modal

app = modal.App("qwen3-patching")

MODEL_ID = "Qwen/Qwen3-4B-Instruct-2507"

# Prompts for patching experiments

CLEAN = f"""<|im_start|>user
Is there an official bee emoji in Unicode? Only reply Yes or No.<|im_end|>
<|im_start|>assistant
"""
CORRUPT = f"""<|im_start|>user
Is there an official butterfly emoji in Unicode? Only reply Yes or No.<|im_end|>
<|im_start|>assistant
"""


def download_model():
    from huggingface_hub import snapshot_download

    snapshot_download(MODEL_ID)


image = (
    modal.Image.debian_slim(python_version="3.13")
    .uv_sync(".")
    .run_function(download_model)
)


@app.cls(image=image, gpu="A100", timeout=600)
class Qwen3Model:
    @modal.enter()
    def load_model(self):
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_ID).to("cuda")

    @modal.method()
    def activation_patching_sweep(self, clean_prompt: str, corrupt_prompt: str) -> dict:
        """
        Activation patching: run corrupt prompt but patch in clean activations
        at the final token position for each layer's MLP and attention outputs,
        plus residual stream patching at various points.

        Returns logits and probs for Yes/No under each patching condition.
        """
        import torch

        # Get Yes/No token IDs
        yes_id = self.tokenizer.encode("Yes", add_special_tokens=False)[0]
        no_id = self.tokenizer.encode("No", add_special_tokens=False)[0]

        # Tokenize both prompts
        clean_inputs = self.tokenizer([clean_prompt], return_tensors="pt").to(self.model.device)
        corrupt_inputs = self.tokenizer([corrupt_prompt], return_tensors="pt").to(self.model.device)

        num_layers = len(self.model.model.layers)

        # First, cache clean activations (components + residual stream)
        clean_cache = {}
        hooks = []

        def cache_clean(name):
            def hook(module, input, output):
                out = output[0] if isinstance(output, tuple) else output
                clean_cache[name] = out.detach().clone()
            return hook

        def cache_clean_input(name):
            def hook(module, input):
                # For residual stream, we want the input to the layer
                inp = input[0] if isinstance(input, tuple) else input
                clean_cache[name] = inp.detach().clone()
            return hook

        # Cache embedding output
        hooks.append(self.model.model.embed_tokens.register_forward_hook(cache_clean("embed")))

        for i, layer in enumerate(self.model.model.layers):
            # Cache residual stream at input to each layer (resid_pre)
            hooks.append(layer.register_forward_pre_hook(cache_clean_input(f"resid_pre_L{i}")))
            # Cache component outputs
            hooks.append(layer.self_attn.register_forward_hook(cache_clean(f"L{i}_attn")))
            hooks.append(layer.mlp.register_forward_hook(cache_clean(f"L{i}_mlp")))
            # Cache residual stream after attention, before MLP (resid_mid)
            hooks.append(layer.mlp.register_forward_pre_hook(cache_clean_input(f"resid_mid_L{i}")))

        # Cache final norm input (residual stream after last layer)
        hooks.append(self.model.model.norm.register_forward_pre_hook(cache_clean_input("resid_post_final")))

        with torch.no_grad():
            self.model(input_ids=clean_inputs["input_ids"])

        for hook in hooks:
            hook.remove()

        # Get baseline logits for clean and corrupt
        with torch.no_grad():
            clean_logits = self.model(input_ids=clean_inputs["input_ids"]).logits[0, -1, :]
            corrupt_logits = self.model(input_ids=corrupt_inputs["input_ids"]).logits[0, -1, :]

        clean_probs = torch.softmax(clean_logits, dim=-1)
        corrupt_probs = torch.softmax(corrupt_logits, dim=-1)

        results = {
            "baseline": {
                "clean": {
                    "yes_logit": clean_logits[yes_id].item(),
                    "no_logit": clean_logits[no_id].item(),
                    "yes_prob": clean_probs[yes_id].item(),
                    "no_prob": clean_probs[no_id].item(),
                    "logit_diff": (clean_logits[yes_id] - clean_logits[no_id]).item(),
                },
                "corrupt": {
                    "yes_logit": corrupt_logits[yes_id].item(),
                    "no_logit": corrupt_logits[no_id].item(),
                    "yes_prob": corrupt_probs[yes_id].item(),
                    "no_prob": corrupt_probs[no_id].item(),
                    "logit_diff": (corrupt_logits[yes_id] - corrupt_logits[no_id]).item(),
                },
            },
            "patched_components": {},
            "patched_resid": {},
        }

        # Helper to run patching and get results
        def get_patched_result(patched_logits):
            patched_probs = torch.softmax(patched_logits, dim=-1)
            return {
                "yes_logit": patched_logits[yes_id].item(),
                "no_logit": patched_logits[no_id].item(),
                "yes_prob": patched_probs[yes_id].item(),
                "no_prob": patched_probs[no_id].item(),
                "logit_diff": (patched_logits[yes_id] - patched_logits[no_id]).item(),
            }

        # Patch each component: run corrupt, but substitute clean activation at final token
        for layer_idx in range(num_layers):
            for component in ["attn", "mlp"]:
                patch_name = f"L{layer_idx}_{component}"
                clean_act = clean_cache[patch_name]

                def make_patch_hook(clean_activation):
                    def hook(module, input, output):
                        out = output[0] if isinstance(output, tuple) else output
                        out[:, -1, :] = clean_activation[:, -1, :]
                        if isinstance(output, tuple):
                            return (out,) + output[1:]
                        return out
                    return hook

                if component == "attn":
                    target = self.model.model.layers[layer_idx].self_attn
                else:
                    target = self.model.model.layers[layer_idx].mlp

                hook = target.register_forward_hook(make_patch_hook(clean_act))

                with torch.no_grad():
                    patched_logits = self.model(input_ids=corrupt_inputs["input_ids"]).logits[0, -1, :]

                hook.remove()

                results["patched_components"][patch_name] = get_patched_result(patched_logits)

        # Patch entire layers (attn + mlp together)
        results["patched_layers"] = {}
        for layer_idx in range(num_layers):
            patch_name = f"L{layer_idx}"
            clean_attn = clean_cache[f"L{layer_idx}_attn"]
            clean_mlp = clean_cache[f"L{layer_idx}_mlp"]

            def make_patch_hook(clean_activation):
                def hook(module, input, output):
                    out = output[0] if isinstance(output, tuple) else output
                    out[:, -1, :] = clean_activation[:, -1, :]
                    if isinstance(output, tuple):
                        return (out,) + output[1:]
                    return out
                return hook

            hook_attn = self.model.model.layers[layer_idx].self_attn.register_forward_hook(
                make_patch_hook(clean_attn)
            )
            hook_mlp = self.model.model.layers[layer_idx].mlp.register_forward_hook(
                make_patch_hook(clean_mlp)
            )

            with torch.no_grad():
                patched_logits = self.model(input_ids=corrupt_inputs["input_ids"]).logits[0, -1, :]

            hook_attn.remove()
            hook_mlp.remove()

            results["patched_layers"][patch_name] = get_patched_result(patched_logits)

        # Windowed layer patching (2, 3, 4 layers together)
        results["patched_windows"] = {}
        for window_size in [2, 3, 4]:
            for start_idx in range(num_layers - window_size + 1):
                end_idx = start_idx + window_size
                patch_name = f"L{start_idx}-L{end_idx - 1}"

                hooks = []
                for layer_idx in range(start_idx, end_idx):
                    clean_attn = clean_cache[f"L{layer_idx}_attn"]
                    clean_mlp = clean_cache[f"L{layer_idx}_mlp"]

                    def make_patch_hook(clean_activation):
                        def hook(module, input, output):
                            out = output[0] if isinstance(output, tuple) else output
                            out[:, -1, :] = clean_activation[:, -1, :]
                            if isinstance(output, tuple):
                                return (out,) + output[1:]
                            return out
                        return hook

                    hooks.append(
                        self.model.model.layers[layer_idx].self_attn.register_forward_hook(
                            make_patch_hook(clean_attn)
                        )
                    )
                    hooks.append(
                        self.model.model.layers[layer_idx].mlp.register_forward_hook(
                            make_patch_hook(clean_mlp)
                        )
                    )

                with torch.no_grad():
                    patched_logits = self.model(input_ids=corrupt_inputs["input_ids"]).logits[0, -1, :]

                for hook in hooks:
                    hook.remove()

                results["patched_windows"][patch_name] = get_patched_result(patched_logits)

        # Patch residual stream at different points
        # resid_pre_L{i}: residual stream entering layer i (before attn)
        # resid_mid_L{i}: residual stream after attn, before MLP

        def make_resid_pre_patch_hook(clean_activation):
            def hook(module, input):
                inp = input[0] if isinstance(input, tuple) else input
                inp[:, -1, :] = clean_activation[:, -1, :]
                if isinstance(input, tuple):
                    return (inp,) + input[1:]
                return (inp,)
            return hook

        for layer_idx in range(num_layers):
            # Patch residual stream before layer (resid_pre)
            patch_name = f"resid_pre_L{layer_idx}"
            clean_resid = clean_cache[patch_name]

            hook = self.model.model.layers[layer_idx].register_forward_pre_hook(
                make_resid_pre_patch_hook(clean_resid)
            )

            with torch.no_grad():
                patched_logits = self.model(input_ids=corrupt_inputs["input_ids"]).logits[0, -1, :]

            hook.remove()

            results["patched_resid"][patch_name] = get_patched_result(patched_logits)

            # Patch residual stream mid-layer (after attn, before MLP)
            patch_name = f"resid_mid_L{layer_idx}"
            clean_resid = clean_cache[patch_name]

            hook = self.model.model.layers[layer_idx].mlp.register_forward_pre_hook(
                make_resid_pre_patch_hook(clean_resid)
            )

            with torch.no_grad():
                patched_logits = self.model(input_ids=corrupt_inputs["input_ids"]).logits[0, -1, :]

            hook.remove()

            results["patched_resid"][patch_name] = get_patched_result(patched_logits)

        # Patch final residual stream (after last layer, before final norm)
        patch_name = "resid_post_final"
        clean_resid = clean_cache[patch_name]

        hook = self.model.model.norm.register_forward_pre_hook(
            make_resid_pre_patch_hook(clean_resid)
        )

        with torch.no_grad():
            patched_logits = self.model(input_ids=corrupt_inputs["input_ids"]).logits[0, -1, :]

        hook.remove()

        results["patched_resid"][patch_name] = get_patched_result(patched_logits)

        return results

    @modal.method()
    def head_patching_sweep(self, clean_prompt: str, corrupt_prompt: str) -> dict:
        """
        Head-level patching and ablation for ALL layers and heads.
        - Ablation: zero out each head's output individually
        - Activation patching: patch in clean head output for each head
        Reports delta logit_diff from corrupt baseline.
        """
        import torch

        yes_id = self.tokenizer.encode("Yes", add_special_tokens=False)[0]
        no_id = self.tokenizer.encode("No", add_special_tokens=False)[0]

        clean_inputs = self.tokenizer([clean_prompt], return_tensors="pt").to(
            self.model.device
        )
        corrupt_inputs = self.tokenizer([corrupt_prompt], return_tensors="pt").to(
            self.model.device
        )

        config = self.model.config
        num_layers = len(self.model.model.layers)
        num_heads = config.num_attention_heads
        head_dim = config.hidden_size // num_heads

        # Cache clean attention outputs for all layers
        clean_attn_cache = {}

        def make_cache_hook(layer_idx):
            def hook(module, input, output):
                attn_out = output[0] if isinstance(output, tuple) else output
                clean_attn_cache[layer_idx] = attn_out.detach().clone()
            return hook

        hooks = []
        for i, layer in enumerate(self.model.model.layers):
            hooks.append(layer.self_attn.register_forward_hook(make_cache_hook(i)))

        with torch.no_grad():
            self.model(input_ids=clean_inputs["input_ids"])

        for hook in hooks:
            hook.remove()

        # Get baseline logits
        with torch.no_grad():
            clean_logits = self.model(input_ids=clean_inputs["input_ids"]).logits[0, -1, :]
            corrupt_logits = self.model(input_ids=corrupt_inputs["input_ids"]).logits[0, -1, :]

        clean_probs = torch.softmax(clean_logits, dim=-1)
        corrupt_probs = torch.softmax(corrupt_logits, dim=-1)

        clean_diff = (clean_logits[yes_id] - clean_logits[no_id]).item()
        corrupt_diff = (corrupt_logits[yes_id] - corrupt_logits[no_id]).item()

        def get_result(logits):
            probs = torch.softmax(logits, dim=-1)
            logit_diff = (logits[yes_id] - logits[no_id]).item()
            return {
                "yes_logit": logits[yes_id].item(),
                "no_logit": logits[no_id].item(),
                "yes_prob": probs[yes_id].item(),
                "no_prob": probs[no_id].item(),
                "logit_diff": logit_diff,
                "delta_from_corrupt": logit_diff - corrupt_diff,
            }

        results = {
            "num_layers": num_layers,
            "num_heads": num_heads,
            "head_dim": head_dim,
            "baseline": {
                "clean": {
                    "yes_logit": clean_logits[yes_id].item(),
                    "no_logit": clean_logits[no_id].item(),
                    "yes_prob": clean_probs[yes_id].item(),
                    "no_prob": clean_probs[no_id].item(),
                    "logit_diff": clean_diff,
                },
                "corrupt": {
                    "yes_logit": corrupt_logits[yes_id].item(),
                    "no_logit": corrupt_logits[no_id].item(),
                    "yes_prob": corrupt_probs[yes_id].item(),
                    "no_prob": corrupt_probs[no_id].item(),
                    "logit_diff": corrupt_diff,
                },
            },
            "ablated_heads": {},
            "patched_heads": {},
        }

        # Sweep all layers and heads
        for layer_idx in range(num_layers):
            attn = self.model.model.layers[layer_idx].self_attn
            clean_attn_out = clean_attn_cache[layer_idx]

            for head_idx in range(num_heads):
                start_idx = head_idx * head_dim
                end_idx = (head_idx + 1) * head_dim
                key = f"L{layer_idx}H{head_idx}"

                # Ablation: zero out head
                def make_ablate_hook(start, end):
                    def hook(module, input, output):
                        attn_out = output[0] if isinstance(output, tuple) else output
                        attn_out[:, -1, start:end] = 0.0
                        if isinstance(output, tuple):
                            return (attn_out,) + output[1:]
                        return attn_out
                    return hook

                hook = attn.register_forward_hook(make_ablate_hook(start_idx, end_idx))
                with torch.no_grad():
                    ablated_logits = self.model(input_ids=corrupt_inputs["input_ids"]).logits[0, -1, :]
                hook.remove()

                results["ablated_heads"][key] = get_result(ablated_logits)

                # Patching: patch in clean head
                def make_patch_hook(start, end, clean_act):
                    def hook(module, input, output):
                        attn_out = output[0] if isinstance(output, tuple) else output
                        attn_out[:, -1, start:end] = clean_act[:, -1, start:end]
                        if isinstance(output, tuple):
                            return (attn_out,) + output[1:]
                        return attn_out
                    return hook

                hook = attn.register_forward_hook(make_patch_hook(start_idx, end_idx, clean_attn_out))
                with torch.no_grad():
                    patched_logits = self.model(input_ids=corrupt_inputs["input_ids"]).logits[0, -1, :]
                hook.remove()

                results["patched_heads"][key] = get_result(patched_logits)

        return results


volume = modal.Volume.from_name("emoji-results", create_if_missing=True)
VOLUME_PATH = "/results"


def plot_patching_results(results: dict, output_dir: str):
    """Generate charts for activation patching results."""
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    os.makedirs(output_dir, exist_ok=True)

    baseline = results["baseline"]
    clean_diff = baseline["clean"]["logit_diff"]
    corrupt_diff = baseline["corrupt"]["logit_diff"]
    total_effect = clean_diff - corrupt_diff

    def calc_recovery(data):
        return (data["logit_diff"] - corrupt_diff) / total_effect * 100 if total_effect != 0 else 0

    # Plot 1: Component patching heatmap (layers x components)
    patched_comp = results["patched_components"]
    num_layers = len([k for k in patched_comp.keys() if "_attn" in k])

    attn_recovery = []
    mlp_recovery = []
    for i in range(num_layers):
        attn_recovery.append(calc_recovery(patched_comp[f"L{i}_attn"]))
        mlp_recovery.append(calc_recovery(patched_comp[f"L{i}_mlp"]))

    fig, ax = plt.subplots(figsize=(16, 4))
    data = np.array([attn_recovery, mlp_recovery])

    im = ax.imshow(data, aspect="auto", cmap="RdBu_r", vmin=-100, vmax=100)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Attention", "MLP"])
    ax.set_xticks(range(0, num_layers, 2))
    ax.set_xticklabels([f"L{i}" for i in range(0, num_layers, 2)])
    ax.set_xlabel("Layer")
    ax.set_title(f"Component Patching Recovery % (clean_diff={clean_diff:.2f}, corrupt_diff={corrupt_diff:.2f})")

    plt.colorbar(im, ax=ax, label="Recovery %")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/component_patching_heatmap.png", dpi=150)
    plt.close()

    # Plot 2: Layer patching bar chart
    patched_layers = results["patched_layers"]
    layer_recovery = [calc_recovery(patched_layers[f"L{i}"]) for i in range(num_layers)]

    fig, ax = plt.subplots(figsize=(16, 5))
    colors = ["forestgreen" if r > 0 else "salmon" for r in layer_recovery]
    ax.bar(range(num_layers), layer_recovery, color=colors, edgecolor="black", linewidth=0.5)
    ax.axhline(y=0, color="black", linewidth=0.5)
    ax.axhline(y=100, color="gray", linestyle="--", linewidth=0.5, label="Full recovery")
    ax.set_xlabel("Layer")
    ax.set_ylabel("Recovery %")
    ax.set_title("Layer Patching (Attn + MLP together)")
    ax.set_xticks(range(0, num_layers, 2))
    ax.set_xticklabels([f"L{i}" for i in range(0, num_layers, 2)])
    plt.tight_layout()
    plt.savefig(f"{output_dir}/layer_patching_bar.png", dpi=150)
    plt.close()

    # Plot 3: Residual stream patching
    patched_resid = results["patched_resid"]

    resid_pre_recovery = []
    resid_mid_recovery = []
    for i in range(num_layers):
        resid_pre_recovery.append(calc_recovery(patched_resid[f"resid_pre_L{i}"]))
        resid_mid_recovery.append(calc_recovery(patched_resid[f"resid_mid_L{i}"]))

    fig, ax = plt.subplots(figsize=(16, 5))
    x = np.arange(num_layers)
    width = 0.4

    ax.bar(x - width/2, resid_pre_recovery, width, label="resid_pre (before attn)", color="steelblue")
    ax.bar(x + width/2, resid_mid_recovery, width, label="resid_mid (after attn, before mlp)", color="darkorange")

    ax.axhline(y=0, color="black", linewidth=0.5)
    ax.axhline(y=100, color="gray", linestyle="--", linewidth=0.5)
    ax.set_xlabel("Layer")
    ax.set_ylabel("Recovery %")
    ax.set_title("Residual Stream Patching")
    ax.set_xticks(range(0, num_layers, 2))
    ax.set_xticklabels([f"L{i}" for i in range(0, num_layers, 2)])
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{output_dir}/residual_patching_bar.png", dpi=150)
    plt.close()

    # Plot 4: Cumulative recovery by layer (resid_pre shows cumulative effect)
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(range(num_layers), resid_pre_recovery, marker="o", linewidth=2, markersize=4, label="resid_pre")
    ax.axhline(y=0, color="black", linewidth=0.5)
    ax.axhline(y=100, color="gray", linestyle="--", linewidth=0.5, label="Full recovery")
    ax.set_xlabel("Layer")
    ax.set_ylabel("Recovery %")
    ax.set_title("Cumulative Recovery (patching residual stream before each layer)")
    ax.set_xticks(range(0, num_layers, 2))
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{output_dir}/cumulative_recovery.png", dpi=150)
    plt.close()

    # Plot 5: Top patches summary
    all_patches = []
    for patch_name, data in patched_comp.items():
        all_patches.append((patch_name, calc_recovery(data), "component"))
    for patch_name, data in patched_layers.items():
        all_patches.append((patch_name, calc_recovery(data), "layer"))
    for patch_name, data in patched_resid.items():
        all_patches.append((patch_name, calc_recovery(data), "resid"))

    # Top 20 by absolute recovery
    sorted_patches = sorted(all_patches, key=lambda x: abs(x[1]), reverse=True)[:20]

    fig, ax = plt.subplots(figsize=(12, 8))
    names = [p[0] for p in sorted_patches]
    recoveries = [p[1] for p in sorted_patches]
    colors = ["forestgreen" if r > 0 else "salmon" for r in recoveries]

    y_pos = np.arange(len(names))
    ax.barh(y_pos, recoveries, color=colors, edgecolor="black", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    ax.axvline(x=0, color="black", linewidth=0.5)
    ax.axvline(x=100, color="gray", linestyle="--", linewidth=0.5)
    ax.set_xlabel("Recovery %")
    ax.set_title("Top 20 Most Impactful Patches")
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(f"{output_dir}/top_patches.png", dpi=150)
    plt.close()

    print(f"Saved patching charts to {output_dir}")


def plot_head_results(results: dict, output_dir: str):
    """Generate charts for head-level patching results."""
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    os.makedirs(output_dir, exist_ok=True)

    num_layers = results["num_layers"]
    num_heads = results["num_heads"]
    baseline = results["baseline"]

    clean_diff = baseline["clean"]["logit_diff"]
    corrupt_diff = baseline["corrupt"]["logit_diff"]
    total_effect = clean_diff - corrupt_diff

    def calc_recovery(data):
        return (data["logit_diff"] - corrupt_diff) / total_effect * 100 if total_effect != 0 else 0

    # Plot 1: Head patching heatmap (layers x heads)
    patched_heads = results["patched_heads"]
    patching_matrix = np.zeros((num_layers, num_heads))

    for layer_idx in range(num_layers):
        for head_idx in range(num_heads):
            key = f"L{layer_idx}H{head_idx}"
            patching_matrix[layer_idx, head_idx] = calc_recovery(patched_heads[key])

    fig, ax = plt.subplots(figsize=(20, 10))
    im = ax.imshow(patching_matrix, aspect="auto", cmap="RdBu_r", vmin=-50, vmax=50)
    ax.set_xlabel("Head")
    ax.set_ylabel("Layer")
    ax.set_title(f"Head Patching Recovery % (clean_diff={clean_diff:.2f}, corrupt_diff={corrupt_diff:.2f})")
    ax.set_xticks(range(0, num_heads, 2))
    ax.set_yticks(range(0, num_layers, 2))

    plt.colorbar(im, ax=ax, label="Recovery %")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/head_patching_heatmap.png", dpi=150)
    plt.close()

    # Plot 2: Head ablation heatmap
    ablated_heads = results["ablated_heads"]
    ablation_matrix = np.zeros((num_layers, num_heads))

    for layer_idx in range(num_layers):
        for head_idx in range(num_heads):
            key = f"L{layer_idx}H{head_idx}"
            ablation_matrix[layer_idx, head_idx] = calc_recovery(ablated_heads[key])

    fig, ax = plt.subplots(figsize=(20, 10))
    im = ax.imshow(ablation_matrix, aspect="auto", cmap="RdBu_r", vmin=-50, vmax=50)
    ax.set_xlabel("Head")
    ax.set_ylabel("Layer")
    ax.set_title(f"Head Ablation Recovery % (zeroing out head)")
    ax.set_xticks(range(0, num_heads, 2))
    ax.set_yticks(range(0, num_layers, 2))

    plt.colorbar(im, ax=ax, label="Recovery %")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/head_ablation_heatmap.png", dpi=150)
    plt.close()

    # Plot 3: Top heads by patching
    all_heads_patch = [(k, calc_recovery(v)) for k, v in patched_heads.items()]
    sorted_heads_patch = sorted(all_heads_patch, key=lambda x: abs(x[1]), reverse=True)[:30]

    fig, ax = plt.subplots(figsize=(12, 10))
    names = [h[0] for h in sorted_heads_patch]
    recoveries = [h[1] for h in sorted_heads_patch]
    colors = ["forestgreen" if r > 0 else "salmon" for r in recoveries]

    y_pos = np.arange(len(names))
    ax.barh(y_pos, recoveries, color=colors, edgecolor="black", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    ax.axvline(x=0, color="black", linewidth=0.5)
    ax.set_xlabel("Recovery %")
    ax.set_title("Top 30 Heads by Patching Impact")
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(f"{output_dir}/top_heads_patching.png", dpi=150)
    plt.close()

    # Plot 4: Per-layer summary (mean and max recovery across heads)
    layer_mean_patch = []
    layer_max_patch = []
    layer_mean_ablate = []

    for layer_idx in range(num_layers):
        layer_recoveries_patch = [patching_matrix[layer_idx, h] for h in range(num_heads)]
        layer_recoveries_ablate = [ablation_matrix[layer_idx, h] for h in range(num_heads)]
        layer_mean_patch.append(np.mean(layer_recoveries_patch))
        layer_max_patch.append(np.max(np.abs(layer_recoveries_patch)))
        layer_mean_ablate.append(np.mean(layer_recoveries_ablate))

    fig, axes = plt.subplots(1, 2, figsize=(16, 5))

    ax = axes[0]
    ax.bar(range(num_layers), layer_mean_patch, color="steelblue", edgecolor="black", linewidth=0.5)
    ax.axhline(y=0, color="black", linewidth=0.5)
    ax.set_xlabel("Layer")
    ax.set_ylabel("Mean Recovery %")
    ax.set_title("Mean Head Patching Recovery by Layer")
    ax.set_xticks(range(0, num_layers, 4))

    ax = axes[1]
    ax.bar(range(num_layers), layer_max_patch, color="darkorange", edgecolor="black", linewidth=0.5)
    ax.set_xlabel("Layer")
    ax.set_ylabel("Max |Recovery| %")
    ax.set_title("Max Head Patching Impact by Layer")
    ax.set_xticks(range(0, num_layers, 4))

    plt.tight_layout()
    plt.savefig(f"{output_dir}/head_layer_summary.png", dpi=150)
    plt.close()

    print(f"Saved head patching charts to {output_dir}")


@app.function(image=image, volumes={VOLUME_PATH: volume}, timeout=600)
def save_patching_charts(results: dict, head_results: dict, clean_prompt: str, corrupt_prompt: str):
    """Save all patching charts to the Modal volume."""
    import json
    import os

    output_dir = f"{VOLUME_PATH}/patching_results"
    os.makedirs(output_dir, exist_ok=True)

    # Save raw results as JSON
    with open(f"{output_dir}/patching_results.json", "w") as f:
        json.dump(results, f, indent=2)

    with open(f"{output_dir}/head_patching_results.json", "w") as f:
        json.dump(head_results, f, indent=2)

    # Save prompts
    with open(f"{output_dir}/prompts.txt", "w") as f:
        f.write(f"CLEAN:\n{clean_prompt}\n\nCORRUPT:\n{corrupt_prompt}\n")

    # Generate charts
    plot_patching_results(results, output_dir)
    plot_head_results(head_results, output_dir)

    volume.commit()
    print(f"Saved all patching results and charts to {output_dir}")


def print_head_results(results: dict):
    """Print head-level patching/ablation results for all layers."""
    num_layers = results["num_layers"]
    num_heads = results["num_heads"]
    baseline = results["baseline"]

    print("=" * 100)
    print("HEAD-LEVEL PATCHING/ABLATION (ALL LAYERS)")
    print(f"Layers: {num_layers}, Heads per layer: {num_heads}, Head dim: {results['head_dim']}")
    print("=" * 100)

    print("\nBASELINE:")
    print("-" * 80)
    print(f"{'':15} {'Yes_logit':>10} {'No_logit':>10} {'Diff':>10} {'Y_prob':>10} {'N_prob':>10}")
    print("-" * 80)

    for name, data in baseline.items():
        print(
            f"{name:15} {data['yes_logit']:>10.4f} {data['no_logit']:>10.4f} "
            f"{data['logit_diff']:>10.4f} {data['yes_prob']:>10.4f} {data['no_prob']:>10.4f}"
        )

    clean_diff = baseline["clean"]["logit_diff"]
    corrupt_diff = baseline["corrupt"]["logit_diff"]
    total_effect = clean_diff - corrupt_diff

    print(f"\nTotal effect (clean - corrupt logit_diff): {total_effect:.4f}")

    ablated = results["ablated_heads"]
    patched = results["patched_heads"]

    # Sort by distance to clean_diff (smallest = best recovery)
    def distance_to_clean(data):
        return abs(data["logit_diff"] - clean_diff)

    # Top 30 heads by ablation (closest to clean)
    print("\n" + "=" * 100)
    print(f"TOP 30 HEADS BY ABLATION (sorted by closeness to clean_diff={clean_diff:.4f}):")
    print("-" * 100)

    ablation_list = [(k, d) for k, d in ablated.items()]
    sorted_ablation = sorted(ablation_list, key=lambda x: distance_to_clean(x[1]))[:30]

    for i, (key, data) in enumerate(sorted_ablation, 1):
        dist = distance_to_clean(data)
        print(
            f"{i:2}. {key:8} diff={data['logit_diff']:>+8.4f} | dist_to_clean={dist:>6.4f} | "
            f"Y_prob={data['yes_prob']:.4f} N_prob={data['no_prob']:.4f}"
        )

    # Top 30 heads by patching (closest to clean)
    print("\n" + "=" * 100)
    print(f"TOP 30 HEADS BY PATCHING (sorted by closeness to clean_diff={clean_diff:.4f}):")
    print("-" * 100)

    patching_list = [(k, d) for k, d in patched.items()]
    sorted_patching = sorted(patching_list, key=lambda x: distance_to_clean(x[1]))[:30]

    for i, (key, data) in enumerate(sorted_patching, 1):
        dist = distance_to_clean(data)
        print(
            f"{i:2}. {key:8} diff={data['logit_diff']:>+8.4f} | dist_to_clean={dist:>6.4f} | "
            f"Y_prob={data['yes_prob']:.4f} N_prob={data['no_prob']:.4f}"
        )


def print_results(results: dict):
    """Print patching results in a readable format."""
    print("=" * 100)
    print("ACTIVATION PATCHING RESULTS")
    print("=" * 100)

    baseline = results["baseline"]
    print("\nBASELINE:")
    print("-" * 80)
    print(f"{'':20} {'Yes_logit':>12} {'No_logit':>12} {'Diff':>12} {'Yes_prob':>12} {'No_prob':>12}")
    print("-" * 80)

    for name, data in baseline.items():
        print(
            f"{name:20} {data['yes_logit']:>12.4f} {data['no_logit']:>12.4f} "
            f"{data['logit_diff']:>12.4f} {data['yes_prob']:>12.4f} {data['no_prob']:>12.4f}"
        )

    clean_diff = baseline["clean"]["logit_diff"]
    corrupt_diff = baseline["corrupt"]["logit_diff"]
    total_effect = clean_diff - corrupt_diff

    print(f"\nTotal effect (clean - corrupt logit_diff): {total_effect:.4f}")

    def calc_recovery(data):
        return (data["logit_diff"] - corrupt_diff) / total_effect * 100 if total_effect != 0 else 0

    # Component patching
    print("\n" + "=" * 100)
    print("COMPONENT PATCHING (corrupt -> patch in clean attn/mlp output at final token)")
    print("=" * 100)
    print(f"\n{'Component':15} {'Yes_logit':>10} {'No_logit':>10} {'Diff':>10} {'Y_prob':>8} {'N_prob':>8} {'Recovery':>10}")
    print("-" * 85)

    patched_comp = results["patched_components"]

    def sort_key_component(x):
        parts = x.split("_")
        layer = int(parts[0][1:])
        comp = parts[1]
        return (layer, comp)

    sorted_keys = sorted(patched_comp.keys(), key=sort_key_component)

    for patch_name in sorted_keys:
        data = patched_comp[patch_name]
        recovery = calc_recovery(data)
        print(
            f"{patch_name:15} {data['yes_logit']:>10.4f} {data['no_logit']:>10.4f} "
            f"{data['logit_diff']:>10.4f} {data['yes_prob']:>8.4f} {data['no_prob']:>8.4f} "
            f"{recovery:>9.1f}%"
        )

    # Layer patching (attn + mlp together)
    print("\n" + "=" * 100)
    print("LAYER PATCHING (corrupt -> patch in clean attn+mlp at final token)")
    print("=" * 100)
    print(f"\n{'Layer':15} {'Yes_logit':>10} {'No_logit':>10} {'Diff':>10} {'Y_prob':>8} {'N_prob':>8} {'Recovery':>10}")
    print("-" * 85)

    patched_layers = results["patched_layers"]
    sorted_keys = sorted(patched_layers.keys(), key=lambda x: int(x[1:]))

    for patch_name in sorted_keys:
        data = patched_layers[patch_name]
        recovery = calc_recovery(data)
        print(
            f"{patch_name:15} {data['yes_logit']:>10.4f} {data['no_logit']:>10.4f} "
            f"{data['logit_diff']:>10.4f} {data['yes_prob']:>8.4f} {data['no_prob']:>8.4f} "
            f"{recovery:>9.1f}%"
        )

    # Windowed layer patching
    print("\n" + "=" * 100)
    print("WINDOWED LAYER PATCHING (corrupt -> patch multiple consecutive layers)")
    print("=" * 100)

    patched_windows = results["patched_windows"]

    for window_size in [2, 3, 4]:
        print(f"\n--- Window size: {window_size} layers ---")
        print(f"{'Window':15} {'Yes_logit':>10} {'No_logit':>10} {'Diff':>10} {'Y_prob':>8} {'N_prob':>8} {'Recovery':>10}")
        print("-" * 85)

        window_keys = [k for k in patched_windows.keys() if k.count("-") == 1]
        window_keys = [k for k in window_keys if int(k.split("-")[1][1:]) - int(k.split("-")[0][1:]) + 1 == window_size]
        window_keys = sorted(window_keys, key=lambda x: int(x.split("-")[0][1:]))

        for patch_name in window_keys:
            data = patched_windows[patch_name]
            recovery = calc_recovery(data)
            print(
                f"{patch_name:15} {data['yes_logit']:>10.4f} {data['no_logit']:>10.4f} "
                f"{data['logit_diff']:>10.4f} {data['yes_prob']:>8.4f} {data['no_prob']:>8.4f} "
                f"{recovery:>9.1f}%"
            )

    # Residual stream patching
    print("\n" + "=" * 100)
    print("RESIDUAL STREAM PATCHING (corrupt -> patch in clean resid at final token)")
    print("=" * 100)
    print(f"\n{'Location':20} {'Yes_logit':>10} {'No_logit':>10} {'Diff':>10} {'Y_prob':>8} {'N_prob':>8} {'Recovery':>10}")
    print("-" * 90)

    patched_resid = results["patched_resid"]

    def sort_key_resid(x):
        if x == "resid_post_final":
            return (999, 0)
        parts = x.split("_")
        layer = int(parts[2][1:])
        is_mid = 1 if parts[1] == "mid" else 0
        return (layer, is_mid)

    sorted_keys = sorted(patched_resid.keys(), key=sort_key_resid)

    for patch_name in sorted_keys:
        data = patched_resid[patch_name]
        recovery = calc_recovery(data)
        print(
            f"{patch_name:20} {data['yes_logit']:>10.4f} {data['no_logit']:>10.4f} "
            f"{data['logit_diff']:>10.4f} {data['yes_prob']:>8.4f} {data['no_prob']:>8.4f} "
            f"{recovery:>9.1f}%"
        )

    # Summary: top 30 most impactful patches across all types
    print("\n" + "=" * 100)
    print("TOP 30 MOST IMPACTFUL PATCHES (by absolute recovery %):")
    print("-" * 90)

    all_patches = []
    for patch_name, data in patched_comp.items():
        recovery = calc_recovery(data)
        all_patches.append((patch_name, recovery, data, "component"))

    for patch_name, data in patched_layers.items():
        recovery = calc_recovery(data)
        all_patches.append((patch_name, recovery, data, "layer"))

    for patch_name, data in patched_windows.items():
        recovery = calc_recovery(data)
        all_patches.append((patch_name, recovery, data, "window"))

    for patch_name, data in patched_resid.items():
        recovery = calc_recovery(data)
        all_patches.append((patch_name, recovery, data, "resid"))

    sorted_by_recovery = sorted(all_patches, key=lambda x: abs(x[1]), reverse=True)[:30]

    for i, (patch_name, recovery, data, patch_type) in enumerate(sorted_by_recovery, 1):
        print(
            f"{i:2}. {patch_name:20} [{patch_type:9}] recovery={recovery:>7.1f}% | "
            f"diff={data['logit_diff']:>8.4f} | Y_prob={data['yes_prob']:.4f} N_prob={data['no_prob']:.4f}"
        )


@app.local_entrypoint()
def main():
    model = Qwen3Model()

    print(f"CLEAN prompt: {repr(CLEAN)}")
    print(f"CORRUPT prompt: {repr(CORRUPT)}")
    print()

    # Layer-level patching sweep
    results = model.activation_patching_sweep.remote(CLEAN, CORRUPT)
    print_results(results)

    # Head-level patching for all layers
    print("\n\n")
    head_results = model.head_patching_sweep.remote(CLEAN, CORRUPT)
    print_head_results(head_results)

    # Save charts to volume
    print("\n\nSaving charts to Modal volume...")
    save_patching_charts.remote(results, head_results, CLEAN, CORRUPT)
    print("Done! Charts saved to modal volume 'emoji-results' in /patching_results/")


if __name__ == "__main__":
    main()
