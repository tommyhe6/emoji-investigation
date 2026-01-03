import modal

app = modal.App("qwen3-inference")

MODEL_ID = "Qwen/Qwen3-4B-Instruct-2507"


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
    def direct_logit_attribution(self, prompt: str, str_a: str, str_b: str):
        """
        Direct Logit Attribution (DLA) for Yes/No token prediction.

        Decomposes the logit difference into additive contributions from each component:
        - Embedding
        - Attention output (per layer)
        - MLP output (per layer)
        - Final RMSNorm

        Note on RMSNorm: The final norm is applied before the LM head, so strictly speaking
        the contributions don't perfectly decompose (norm is nonlinear). However, RMSNorm
        only scales by 1/||x|| without mean-centering, so it's less problematic than LayerNorm:
        - RMSNorm preserves directions (just rescales)
        - The "Final RMSNorm" contribution captures the scaling effect
        - Residual should be small in practice
        """
        import torch

        token_a_id = self.tokenizer.encode(str_a, add_special_tokens=False)[0]
        token_b_id = self.tokenizer.encode(str_b, add_special_tokens=False)[0]

        inputs = self.tokenizer([prompt], return_tensors="pt").to(self.model.device)
        cache = {}
        hooks = []

        def cache_output(name):
            def hook(module, input, output):
                out = output[0] if isinstance(output, tuple) else output
                cache[name] = out
            return hook

        # Hook all components
        hooks.append(self.model.model.embed_tokens.register_forward_hook(cache_output('embed')))
        for i, layer in enumerate(self.model.model.layers):
            hooks.append(layer.self_attn.register_forward_hook(cache_output(f'L{i}_attn')))
            hooks.append(layer.mlp.register_forward_hook(cache_output(f'L{i}_mlp')))
        hooks.append(self.model.model.norm.register_forward_hook(cache_output('final_norm')))

        with torch.no_grad():
            outputs = self.model(input_ids=inputs['input_ids'])
            logits = outputs.logits[0, -1, :]

        for hook in hooks:
            hook.remove()

        # Logit diff direction: W_yes - W_no
        lm_head = self.model.lm_head.weight
        logit_dir = lm_head[token_a_id] - lm_head[token_b_id]

        logit_a = logits[token_a_id].item()
        logit_b = logits[token_b_id].item()
        logit_diff = logit_a - logit_b

        # Compute contributions
        pos = -1
        contributions = []
        total_attn = 0.0
        total_mlp = 0.0

        # Embedding
        embed = cache['embed'][0, pos, :]
        embed_contrib = torch.dot(embed, logit_dir).item()
        contributions.append(('Embed', embed_contrib))
        residual = embed.clone()

        # Each layer
        num_layers = len(self.model.model.layers)
        for i in range(num_layers):
            attn_out = cache[f'L{i}_attn'][0, pos, :]
            attn_contrib = torch.dot(attn_out, logit_dir).item()
            contributions.append((f'L{i}_attn', attn_contrib))
            total_attn += attn_contrib
            residual = residual + attn_out

            mlp_out = cache[f'L{i}_mlp'][0, pos, :]
            mlp_contrib = torch.dot(mlp_out, logit_dir).item()
            contributions.append((f'L{i}_mlp', mlp_contrib))
            total_mlp += mlp_contrib
            residual = residual + mlp_out

        # Final RMSNorm contribution (captures scaling effect)
        final_normed = cache['final_norm'][0, pos, :]
        norm_delta = final_normed - residual
        norm_contrib = torch.dot(norm_delta, logit_dir).item()
        contributions.append(('RMSNorm', norm_contrib))

        # LM head bias (if any)
        bias_contrib = 0.0
        if self.model.lm_head.bias is not None:
            bias_contrib = (self.model.lm_head.bias[token_a_id] -
                           self.model.lm_head.bias[token_b_id]).item()

        total = embed_contrib + total_attn + total_mlp + norm_contrib + bias_contrib

        # Print results
        print("=" * 80)
        print("DIRECT LOGIT ATTRIBUTION: Yes vs No")
        print("=" * 80)
        print(f"Token A ('{self.tokenizer.decode([token_a_id])}'): {logit_a:.4f}")
        print(f"Token B ('{self.tokenizer.decode([token_b_id])}'): {logit_b:.4f}")
        print(f"Logit diff (A - B): {logit_diff:.4f}")
        print()
        print(f"{'Component':15s} {'Contrib':>10s} {'Cumul':>10s}")
        print("-" * 40)

        cumul = 0.0
        for name, contrib in contributions:
            cumul += contrib
            print(f"{name:15s} {contrib:10.4f} {cumul:10.4f}")

        print("-" * 40)
        print(f"{'Total Attn':15s} {total_attn:10.4f}")
        print(f"{'Total MLP':15s} {total_mlp:10.4f}")
        print(f"{'Bias':15s} {bias_contrib:10.4f}")
        print("-" * 40)
        print(f"{'Sum':15s} {total:10.4f}")
        print(f"{'Actual':15s} {logit_diff:10.4f}")
        print(f"{'Error':15s} {logit_diff - total:10.4f}")
        print("=" * 80)

        return {
            'logit_diff': logit_diff,
            'contributions': contributions,
            'total_attn': total_attn,
            'total_mlp': total_mlp,
            'error': logit_diff - total,
        }


@app.local_entrypoint()
def main():
    model = Qwen3Model()
    EMOJI = "octopus"
    PROMPT = f"""<|im_start|>user
What emoji is:{EMOJI}? Answer in 1 word.<|im_end|>
<|im_start|>assistant
"""

    # TOKEN_A = 9454 # "Yes"
    # TOKEN_B = 2753 # "No"

    TOKEN_A = "Oct"
    TOKEN_B = "Sn"

    result = model.direct_logit_attribution.remote(PROMPT, TOKEN_A, TOKEN_B)


if __name__ == "__main__":
    main()
