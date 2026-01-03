from dataclasses import dataclass
from enum import Enum

import modal

app = modal.App("qwen3-inference")

MODEL_ID = "Qwen/Qwen3-4B-Instruct-2507"


class Category(Enum):
    ANIMAL = "animal"
    MYTHICAL = "mythical"
    OBJECT = "object"
    FOOD = "food"
    NATURE = "nature"
    SYMBOL = "symbol"


@dataclass
class BenchItem:
    name: str
    has_emoji: bool
    category: Category


BENCH_ITEMS = [
    # Animals WITHOUT emoji (27)
    BenchItem("seahorse", False, Category.ANIMAL),
    BenchItem("axolotl", False, Category.ANIMAL),
    BenchItem("platypus", False, Category.ANIMAL),
    BenchItem("narwhal", False, Category.ANIMAL),
    BenchItem("pangolin", False, Category.ANIMAL),
    BenchItem("tapir", False, Category.ANIMAL),
    BenchItem("quokka", False, Category.ANIMAL),
    BenchItem("capybara", False, Category.ANIMAL),
    BenchItem("fennec fox", False, Category.ANIMAL),
    BenchItem("meerkat", False, Category.ANIMAL),
    BenchItem("wombat", False, Category.ANIMAL),
    BenchItem("opossum", False, Category.ANIMAL),
    BenchItem("armadillo", False, Category.ANIMAL),
    BenchItem("anteater", False, Category.ANIMAL),
    BenchItem("lemur", False, Category.ANIMAL),
    BenchItem("jackal", False, Category.ANIMAL),
    BenchItem("hyena", False, Category.ANIMAL),
    BenchItem("warthog", False, Category.ANIMAL),
    BenchItem("ibex", False, Category.ANIMAL),
    BenchItem("gazelle", False, Category.ANIMAL),
    BenchItem("chinchilla", False, Category.ANIMAL),
    BenchItem("ferret", False, Category.ANIMAL),
    BenchItem("marmot", False, Category.ANIMAL),
    BenchItem("pika", False, Category.ANIMAL),
    BenchItem("vole", False, Category.ANIMAL),
    BenchItem("mongoose", False, Category.ANIMAL),
    BenchItem("iguana", False, Category.ANIMAL),
    # Animals WITH emoji (32)
    BenchItem("otter", True, Category.ANIMAL),
    BenchItem("sloth", True, Category.ANIMAL),
    BenchItem("octopus", True, Category.ANIMAL),  # 🐙
    BenchItem("snail", True, Category.ANIMAL),  # 🐌
    BenchItem("dolphin", True, Category.ANIMAL),  # 🐬
    BenchItem("whale", True, Category.ANIMAL),  # 🐋
    BenchItem("shark", True, Category.ANIMAL),  # 🦈
    BenchItem("turtle", True, Category.ANIMAL),  # 🐢
    BenchItem("crocodile", True, Category.ANIMAL),  # 🐊
    BenchItem("snake", True, Category.ANIMAL),  # 🐍
    BenchItem("lizard", True, Category.ANIMAL),  # 🦎
    BenchItem("frog", True, Category.ANIMAL),  # 🐸
    BenchItem("butterfly", True, Category.ANIMAL),  # 🦋
    BenchItem("bee", True, Category.ANIMAL),  # 🐝
    BenchItem("ladybug", True, Category.ANIMAL),  # 🐞
    BenchItem("scorpion", True, Category.ANIMAL),  # 🦂
    BenchItem("spider", True, Category.ANIMAL),  # 🕷️
    BenchItem("cat", True, Category.ANIMAL),  # 🐱
    BenchItem("dog", True, Category.ANIMAL),  # 🐕
    BenchItem("rabbit", True, Category.ANIMAL),  # 🐰
    BenchItem("mouse", True, Category.ANIMAL),  # 🐭
    BenchItem("hamster", True, Category.ANIMAL),  # 🐹
    BenchItem("elephant", True, Category.ANIMAL),  # 🐘
    BenchItem("lion", True, Category.ANIMAL),  # 🦁
    BenchItem("tiger", True, Category.ANIMAL),  # 🐯
    BenchItem("monkey", True, Category.ANIMAL),  # 🐒
    BenchItem("penguin", True, Category.ANIMAL),  # 🐧
    BenchItem("owl", True, Category.ANIMAL),  # 🦉
    BenchItem("eagle", True, Category.ANIMAL),  # 🦅
    BenchItem("parrot", True, Category.ANIMAL),  # 🦜
    BenchItem("swan", True, Category.ANIMAL),  # 🦢
    BenchItem("peacock", True, Category.ANIMAL),  # 🦚
    # Mythical WITHOUT emoji (5)
    BenchItem("phoenix", False, Category.MYTHICAL),
    BenchItem("griffin", False, Category.MYTHICAL),
    BenchItem("centaur", False, Category.MYTHICAL),
    BenchItem("hydra", False, Category.MYTHICAL),
    BenchItem("basilisk", False, Category.MYTHICAL),
    # Mythical WITH emoji (5)
    BenchItem("dragon", True, Category.MYTHICAL),  # 🐉
    BenchItem("unicorn", True, Category.MYTHICAL),  # 🦄
    BenchItem("mermaid", True, Category.MYTHICAL),  # 🧜‍♀️
    BenchItem("fairy", True, Category.MYTHICAL),  # 🧚
    BenchItem("genie", True, Category.MYTHICAL),  # 🧞
    # Objects WITHOUT emoji (5)
    BenchItem("refrigerator", False, Category.OBJECT),
    BenchItem("toaster", False, Category.OBJECT),
    BenchItem("blender", False, Category.OBJECT),
    BenchItem("dishwasher", False, Category.OBJECT),
    BenchItem("bookshelf", False, Category.OBJECT),
    # Objects WITH emoji (5)
    BenchItem("computer", True, Category.OBJECT),  # 💻
    BenchItem("telephone", True, Category.OBJECT),  # ☎️
    BenchItem("television", True, Category.OBJECT),  # 📺
    BenchItem("camera", True, Category.OBJECT),  # 📷
    BenchItem("scissors", True, Category.OBJECT),  # ✂️
    # Food WITHOUT emoji (5)
    BenchItem("quinoa", False, Category.FOOD),
    BenchItem("tofu", False, Category.FOOD),
    BenchItem("hummus", False, Category.FOOD),
    BenchItem("oatmeal", False, Category.FOOD),
    BenchItem("granola", False, Category.FOOD),
    # Food WITH emoji (5)
    BenchItem("pizza", True, Category.FOOD),  # 🍕
    BenchItem("hamburger", True, Category.FOOD),  # 🍔
    BenchItem("apple", True, Category.FOOD),  # 🍎
    BenchItem("banana", True, Category.FOOD),  # 🍌
    BenchItem("strawberry", True, Category.FOOD),  # 🍓
    # Nature WITHOUT emoji (5)
    BenchItem("pebble", False, Category.NATURE),
    BenchItem("boulder", False, Category.NATURE),
    BenchItem("meadow", False, Category.NATURE),
    BenchItem("valley", False, Category.NATURE),
    BenchItem("cliff", False, Category.NATURE),
    # Nature WITH emoji (5)
    BenchItem("sun", True, Category.NATURE),  # ☀️
    BenchItem("moon", True, Category.NATURE),  # 🌙
    BenchItem("star", True, Category.NATURE),  # ⭐
    BenchItem("rainbow", True, Category.NATURE),  # 🌈
    BenchItem("volcano", True, Category.NATURE),  # 🌋
]


def download_model():
    from huggingface_hub import snapshot_download

    snapshot_download(MODEL_ID)


image = (
    modal.Image.debian_slim(python_version="3.13")
    .uv_sync(".")
    .run_function(download_model)
)

volume = modal.Volume.from_name("emoji-results", create_if_missing=True)
VOLUME_PATH = "/results"


@app.cls(image=image, gpu="A100", timeout=600)
class Qwen3Model:
    @modal.enter()
    def load_model(self):
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_ID).to("cuda")

    @modal.method()
    def generate(self, prompt: str, max_tokens: int = 50) -> dict:
        import torch

        inputs = self.tokenizer([prompt], return_tensors="pt").to(self.model.device)
        generated_ids = inputs["input_ids"][0].tolist()
        output_tokens = []

        for _ in range(max_tokens):
            with torch.no_grad():
                outputs = self.model(
                    input_ids=torch.tensor([generated_ids]).to(self.model.device)
                )
                logits = outputs.logits[0, -1, :]
                next_token_id = torch.argmax(logits).item()
                generated_ids.append(next_token_id)
                output_tokens.append(self.tokenizer.decode([next_token_id]))

                if next_token_id == self.tokenizer.eos_token_id:
                    break

        return {
            "response": "".join(output_tokens),
            "yes_logit": None,
            "no_logit": None,
            "yes_prob": None,
            "no_prob": None,
            "top_token": None,
            "top_logit": None,
            "top_prob": None,
            "dla": None,
        }

    @modal.method()
    def generate_with_logits(self, prompt: str) -> dict:
        import torch

        inputs = self.tokenizer([prompt], return_tensors="pt").to(self.model.device)
        generated_ids = inputs["input_ids"][0].tolist()

        with torch.no_grad():
            outputs = self.model(
                input_ids=torch.tensor([generated_ids]).to(self.model.device)
            )
            logits = outputs.logits[0, -1, :]

            # Get Yes/No token IDs
            yes_id = self.tokenizer.encode("Yes", add_special_tokens=False)[0]
            no_id = self.tokenizer.encode("No", add_special_tokens=False)[0]

            yes_logit = logits[yes_id].item()
            no_logit = logits[no_id].item()

            # Compute probabilities
            probs = torch.softmax(logits, dim=-1)
            yes_prob = probs[yes_id].item()
            no_prob = probs[no_id].item()

            # Get top token
            top_logit, top_idx = torch.max(logits, dim=-1)
            top_token = self.tokenizer.decode([top_idx.item()])

            # Generate full response
            next_token_id = top_idx.item()
            generated_ids.append(next_token_id)
            output_tokens = [top_token]

            for _ in range(20):
                outputs = self.model(
                    input_ids=torch.tensor([generated_ids]).to(self.model.device)
                )
                logits = outputs.logits[0, -1, :]
                next_token_id = torch.argmax(logits).item()
                generated_ids.append(next_token_id)
                output_tokens.append(self.tokenizer.decode([next_token_id]))
                if next_token_id == self.tokenizer.eos_token_id:
                    break

        return {
            "response": "".join(output_tokens),
            "yes_logit": yes_logit,
            "no_logit": no_logit,
            "yes_prob": yes_prob,
            "no_prob": no_prob,
            "top_token": top_token,
            "top_logit": top_logit.item(),
            "top_prob": probs[top_idx].item(),
            "dla": None,
        }

    @modal.method()
    def generate_with_dla(self, prompt: str) -> dict:
        """
        Generate with logits AND Direct Logit Attribution for Yes vs No.
        """
        import torch

        inputs = self.tokenizer([prompt], return_tensors="pt").to(self.model.device)
        cache = {}
        hooks = []

        def cache_output(name):
            def hook(module, input, output):
                out = output[0] if isinstance(output, tuple) else output
                cache[name] = out
            return hook

        # Hook all components
        hooks.append(self.model.model.embed_tokens.register_forward_hook(cache_output("embed")))
        for i, layer in enumerate(self.model.model.layers):
            hooks.append(layer.self_attn.register_forward_hook(cache_output(f"L{i}_attn")))
            hooks.append(layer.mlp.register_forward_hook(cache_output(f"L{i}_mlp")))
        hooks.append(self.model.model.norm.register_forward_hook(cache_output("final_norm")))

        with torch.no_grad():
            outputs = self.model(input_ids=inputs["input_ids"])
            logits = outputs.logits[0, -1, :]

        for hook in hooks:
            hook.remove()

        # Get Yes/No token IDs
        yes_id = self.tokenizer.encode("Yes", add_special_tokens=False)[0]
        no_id = self.tokenizer.encode("No", add_special_tokens=False)[0]

        yes_logit = logits[yes_id].item()
        no_logit = logits[no_id].item()

        probs = torch.softmax(logits, dim=-1)
        yes_prob = probs[yes_id].item()
        no_prob = probs[no_id].item()

        top_logit_val, top_idx = torch.max(logits, dim=-1)
        top_token = self.tokenizer.decode([top_idx.item()])

        # DLA: logit diff direction
        lm_head = self.model.lm_head.weight
        logit_dir = lm_head[yes_id] - lm_head[no_id]
        logit_diff = yes_logit - no_logit

        pos = -1
        contributions = []
        total_attn = 0.0
        total_mlp = 0.0

        # Embedding
        embed = cache["embed"][0, pos, :]
        embed_contrib = torch.dot(embed, logit_dir).item()
        contributions.append(("Embed", embed_contrib))
        residual = embed.clone()

        # Each layer
        num_layers = len(self.model.model.layers)
        for i in range(num_layers):
            attn_out = cache[f"L{i}_attn"][0, pos, :]
            attn_contrib = torch.dot(attn_out, logit_dir).item()
            contributions.append((f"L{i}_attn", attn_contrib))
            total_attn += attn_contrib
            residual = residual + attn_out

            mlp_out = cache[f"L{i}_mlp"][0, pos, :]
            mlp_contrib = torch.dot(mlp_out, logit_dir).item()
            contributions.append((f"L{i}_mlp", mlp_contrib))
            total_mlp += mlp_contrib
            residual = residual + mlp_out

        # Final RMSNorm contribution
        final_normed = cache["final_norm"][0, pos, :]
        norm_delta = final_normed - residual
        norm_contrib = torch.dot(norm_delta, logit_dir).item()
        contributions.append(("RMSNorm", norm_contrib))

        # LM head bias
        bias_contrib = 0.0
        if self.model.lm_head.bias is not None:
            bias_contrib = (
                self.model.lm_head.bias[yes_id] - self.model.lm_head.bias[no_id]
            ).item()

        total = embed_contrib + total_attn + total_mlp + norm_contrib + bias_contrib

        # Generate response
        generated_ids = inputs["input_ids"][0].tolist()
        next_token_id = top_idx.item()
        generated_ids.append(next_token_id)
        output_tokens = [top_token]

        for _ in range(20):
            with torch.no_grad():
                outputs = self.model(
                    input_ids=torch.tensor([generated_ids]).to(self.model.device)
                )
                next_logits = outputs.logits[0, -1, :]
                next_token_id = torch.argmax(next_logits).item()
                generated_ids.append(next_token_id)
                output_tokens.append(self.tokenizer.decode([next_token_id]))
                if next_token_id == self.tokenizer.eos_token_id:
                    break

        return {
            "response": "".join(output_tokens),
            "yes_logit": yes_logit,
            "no_logit": no_logit,
            "yes_prob": yes_prob,
            "no_prob": no_prob,
            "top_token": top_token,
            "top_logit": top_logit_val.item(),
            "top_prob": probs[top_idx].item(),
            "dla": {
                "logit_diff": logit_diff,
                "contributions": contributions,
                "total_attn": total_attn,
                "total_mlp": total_mlp,
                "embed_contrib": embed_contrib,
                "norm_contrib": norm_contrib,
                "bias_contrib": bias_contrib,
                "total": total,
                "error": logit_diff - total,
            },
        }

    @modal.method()
    def generate_with_patch(
        self, prompt: str, clean_prompt: str, patch_config: str, max_tokens: int = 50
    ) -> dict:
        """
        Generate with activation patching from a clean prompt.

        patch_config formats:
        - resid_pre_L35: patch residual stream before layer 35
        - resid_mid_L22: patch residual mid layer 22
        - resid_post_final: patch final residual stream
        - L22: patch entire layer 22 (attn + mlp)
        - L22-L25: patch layers 22-25 (window)
        - L22H20: patch head 20 of layer 22
        - L22_attn / L22_mlp: patch component
        """
        import re

        import torch

        # Parse patch config
        config = patch_config.strip()
        patch_info = None

        if match := re.match(r"resid_pre_L(\d+)$", config):
            patch_info = {"type": "resid_pre", "layer": int(match.group(1))}
        elif match := re.match(r"resid_mid_L(\d+)$", config):
            patch_info = {"type": "resid_mid", "layer": int(match.group(1))}
        elif config == "resid_post_final":
            patch_info = {"type": "resid_post_final"}
        elif match := re.match(r"L(\d+)H(\d+)$", config):
            patch_info = {"type": "head", "layer": int(match.group(1)), "head": int(match.group(2))}
        elif match := re.match(r"L(\d+)-L(\d+)$", config):
            patch_info = {"type": "window", "start": int(match.group(1)), "end": int(match.group(2))}
        elif match := re.match(r"L(\d+)_(attn|mlp)$", config):
            patch_info = {"type": "component", "layer": int(match.group(1)), "component": match.group(2)}
        elif match := re.match(r"L(\d+)$", config):
            patch_info = {"type": "layer", "layer": int(match.group(1))}
        else:
            raise ValueError(f"Unknown patch config: {config}")

        clean_inputs = self.tokenizer([clean_prompt], return_tensors="pt").to(self.model.device)
        corrupt_inputs = self.tokenizer([prompt], return_tensors="pt").to(self.model.device)

        num_heads = self.model.config.num_attention_heads
        head_dim = self.model.config.hidden_size // num_heads

        # Cache clean activations
        clean_cache = {}
        hooks = []

        def cache_output(name):
            def hook(module, input, output):
                out = output[0] if isinstance(output, tuple) else output
                clean_cache[name] = out.detach().clone()
            return hook

        def cache_input(name):
            def hook(module, input):
                inp = input[0] if isinstance(input, tuple) else input
                clean_cache[name] = inp.detach().clone()
            return hook

        patch_type = patch_info["type"]

        if patch_type == "resid_pre":
            layer_idx = patch_info["layer"]
            hooks.append(self.model.model.layers[layer_idx].register_forward_pre_hook(cache_input(f"resid_pre_L{layer_idx}")))
        elif patch_type == "resid_mid":
            layer_idx = patch_info["layer"]
            hooks.append(self.model.model.layers[layer_idx].mlp.register_forward_pre_hook(cache_input(f"resid_mid_L{layer_idx}")))
        elif patch_type == "resid_post_final":
            hooks.append(self.model.model.norm.register_forward_pre_hook(cache_input("resid_post_final")))
        elif patch_type == "head":
            layer_idx = patch_info["layer"]
            hooks.append(self.model.model.layers[layer_idx].self_attn.register_forward_hook(cache_output(f"L{layer_idx}_attn")))
        elif patch_type == "component":
            layer_idx = patch_info["layer"]
            comp = patch_info["component"]
            if comp == "attn":
                hooks.append(self.model.model.layers[layer_idx].self_attn.register_forward_hook(cache_output(f"L{layer_idx}_attn")))
            else:
                hooks.append(self.model.model.layers[layer_idx].mlp.register_forward_hook(cache_output(f"L{layer_idx}_mlp")))
        elif patch_type == "layer":
            layer_idx = patch_info["layer"]
            hooks.append(self.model.model.layers[layer_idx].self_attn.register_forward_hook(cache_output(f"L{layer_idx}_attn")))
            hooks.append(self.model.model.layers[layer_idx].mlp.register_forward_hook(cache_output(f"L{layer_idx}_mlp")))
        elif patch_type == "window":
            for layer_idx in range(patch_info["start"], patch_info["end"] + 1):
                hooks.append(self.model.model.layers[layer_idx].self_attn.register_forward_hook(cache_output(f"L{layer_idx}_attn")))
                hooks.append(self.model.model.layers[layer_idx].mlp.register_forward_hook(cache_output(f"L{layer_idx}_mlp")))

        with torch.no_grad():
            self.model(input_ids=clean_inputs["input_ids"])

        for hook in hooks:
            hook.remove()

        # Set up patching hooks
        patch_hooks = []

        def make_resid_patch_hook(clean_act):
            def hook(module, input):
                inp = input[0] if isinstance(input, tuple) else input
                inp[:, -1, :] = clean_act[:, -1, :]
                if isinstance(input, tuple):
                    return (inp,) + input[1:]
                return (inp,)
            return hook

        def make_output_patch_hook(clean_act):
            def hook(module, input, output):
                out = output[0] if isinstance(output, tuple) else output
                out[:, -1, :] = clean_act[:, -1, :]
                if isinstance(output, tuple):
                    return (out,) + output[1:]
                return out
            return hook

        def make_head_patch_hook(clean_act, head_idx, head_dim):
            start = head_idx * head_dim
            end = (head_idx + 1) * head_dim
            def hook(module, input, output):
                out = output[0] if isinstance(output, tuple) else output
                out[:, -1, start:end] = clean_act[:, -1, start:end]
                if isinstance(output, tuple):
                    return (out,) + output[1:]
                return out
            return hook

        if patch_type == "resid_pre":
            layer_idx = patch_info["layer"]
            clean_act = clean_cache[f"resid_pre_L{layer_idx}"]
            patch_hooks.append(self.model.model.layers[layer_idx].register_forward_pre_hook(make_resid_patch_hook(clean_act)))
        elif patch_type == "resid_mid":
            layer_idx = patch_info["layer"]
            clean_act = clean_cache[f"resid_mid_L{layer_idx}"]
            patch_hooks.append(self.model.model.layers[layer_idx].mlp.register_forward_pre_hook(make_resid_patch_hook(clean_act)))
        elif patch_type == "resid_post_final":
            clean_act = clean_cache["resid_post_final"]
            patch_hooks.append(self.model.model.norm.register_forward_pre_hook(make_resid_patch_hook(clean_act)))
        elif patch_type == "head":
            layer_idx = patch_info["layer"]
            head_idx = patch_info["head"]
            clean_act = clean_cache[f"L{layer_idx}_attn"]
            patch_hooks.append(self.model.model.layers[layer_idx].self_attn.register_forward_hook(
                make_head_patch_hook(clean_act, head_idx, head_dim)
            ))
        elif patch_type == "component":
            layer_idx = patch_info["layer"]
            comp = patch_info["component"]
            if comp == "attn":
                clean_act = clean_cache[f"L{layer_idx}_attn"]
                patch_hooks.append(self.model.model.layers[layer_idx].self_attn.register_forward_hook(make_output_patch_hook(clean_act)))
            else:
                clean_act = clean_cache[f"L{layer_idx}_mlp"]
                patch_hooks.append(self.model.model.layers[layer_idx].mlp.register_forward_hook(make_output_patch_hook(clean_act)))
        elif patch_type == "layer":
            layer_idx = patch_info["layer"]
            clean_attn = clean_cache[f"L{layer_idx}_attn"]
            clean_mlp = clean_cache[f"L{layer_idx}_mlp"]
            patch_hooks.append(self.model.model.layers[layer_idx].self_attn.register_forward_hook(make_output_patch_hook(clean_attn)))
            patch_hooks.append(self.model.model.layers[layer_idx].mlp.register_forward_hook(make_output_patch_hook(clean_mlp)))
        elif patch_type == "window":
            for layer_idx in range(patch_info["start"], patch_info["end"] + 1):
                clean_attn = clean_cache[f"L{layer_idx}_attn"]
                clean_mlp = clean_cache[f"L{layer_idx}_mlp"]
                patch_hooks.append(self.model.model.layers[layer_idx].self_attn.register_forward_hook(make_output_patch_hook(clean_attn)))
                patch_hooks.append(self.model.model.layers[layer_idx].mlp.register_forward_hook(make_output_patch_hook(clean_mlp)))

        # Get Yes/No token IDs
        yes_id = self.tokenizer.encode("Yes", add_special_tokens=False)[0]
        no_id = self.tokenizer.encode("No", add_special_tokens=False)[0]

        # Generate with patching
        generated_ids = corrupt_inputs["input_ids"][0].tolist()
        output_tokens = []
        first_logits = None

        for step in range(max_tokens):
            with torch.no_grad():
                outputs = self.model(
                    input_ids=torch.tensor([generated_ids]).to(self.model.device)
                )
                logits = outputs.logits[0, -1, :]

                if step == 0:
                    first_logits = logits.clone()

                next_token_id = torch.argmax(logits).item()
                generated_ids.append(next_token_id)
                output_tokens.append(self.tokenizer.decode([next_token_id]))

                if next_token_id == self.tokenizer.eos_token_id:
                    break

        for hook in patch_hooks:
            hook.remove()

        # Extract logit info
        yes_logit = first_logits[yes_id].item()
        no_logit = first_logits[no_id].item()
        probs = torch.softmax(first_logits, dim=-1)
        yes_prob = probs[yes_id].item()
        no_prob = probs[no_id].item()
        top_logit, top_idx = torch.max(first_logits, dim=-1)
        top_token = self.tokenizer.decode([top_idx.item()])

        return {
            "response": "".join(output_tokens),
            "yes_logit": yes_logit,
            "no_logit": no_logit,
            "yes_prob": yes_prob,
            "no_prob": no_prob,
            "top_token": top_token,
            "top_logit": top_logit.item(),
            "top_prob": probs[top_idx].item(),
            "dla": None,
            "patch_config": patch_config,
        }


# =============================================================================
# CONFIGURATION - modify these to change behavior
# =============================================================================

# Patch config: set to None to disable patching, or a string like:
#   "L22", "L22-L25", "L22H20", "resid_pre_L35", "L22_attn", "L22_mlp"
PATCH_CONFIG = None

# Clean prompt for patching experiments (used when PATCH_CONFIG is set)
CLEAN_PROMPT = """<|im_start|>user
Is there an official bee emoji in Unicode? Only reply Yes or No.<|im_end|>
<|im_start|>assistant
"""

# =============================================================================


@dataclass
class DLAInfo:
    logit_diff: float
    contributions: list[tuple[str, float]]
    total_attn: float
    total_mlp: float
    embed_contrib: float
    norm_contrib: float
    bias_contrib: float
    total: float
    error: float


@dataclass
class LogitInfo:
    yes_logit: float
    no_logit: float
    yes_prob: float
    no_prob: float
    top_token: str
    top_logit: float
    top_prob: float


@dataclass
class BenchResult:
    item: BenchItem
    prompt_variant: str
    model_answer: str
    model_said_yes: bool
    correct: bool
    logit_info: LogitInfo | None = None
    dla_info: DLAInfo | None = None


def mp_official_unicode(item_name: str) -> str:
    return f"""<|im_start|>user
Is there an official {item_name} emoji in Unicode? Only reply Yes or No.<|im_end|>
<|im_start|>assistant
"""

def mp_official(item_name: str) -> str:
    return f"""<|im_start|>user
Is there an official {item_name} emoji? Only reply Yes or No.<|im_end|>
<|im_start|>assistant
"""


def mp_casual(item_name: str) -> str:
    return f"""<|im_start|>user
Is there {item_name} emoji? Only reply Yes or No.<|im_end|>
<|im_start|>assistant
"""


PROMPT_VARIANTS = [
    ("official_unicode", mp_official_unicode),
    ("official", mp_official),
    ("casual", mp_casual),
]


def parse_answer(response: str) -> bool:
    response_lower = response.strip().lower()
    return response_lower.startswith("yes")


def print_dla_chart(dla: DLAInfo, item_name: str):
    """Print full DLA chart like dla.py."""
    print("    " + "=" * 76)
    print(f"    DIRECT LOGIT ATTRIBUTION: Yes vs No for '{item_name}'")
    print("    " + "=" * 76)
    print(f"    Logit diff (Yes - No): {dla.logit_diff:.4f}")
    print()
    print(f"    {'Component':15s} {'Contrib':>10s} {'Cumul':>10s}")
    print("    " + "-" * 40)

    cumul = 0.0
    for name, contrib in dla.contributions:
        cumul += contrib
        print(f"    {name:15s} {contrib:10.4f} {cumul:10.4f}")

    print("    " + "-" * 40)
    print(f"    {'Total Attn':15s} {dla.total_attn:10.4f}")
    print(f"    {'Total MLP':15s} {dla.total_mlp:10.4f}")
    print(f"    {'Bias':15s} {dla.bias_contrib:10.4f}")
    print("    " + "-" * 40)
    print(f"    {'Sum':15s} {dla.total:10.4f}")
    print(f"    {'Actual':15s} {dla.logit_diff:10.4f}")
    print(f"    {'Error':15s} {dla.error:10.4f}")
    print("    " + "=" * 76)


def plot_dla_single(dla: DLAInfo, item_name: str, correct: bool, output_dir: str):
    """Plot DLA bar chart for a single item."""
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    os.makedirs(output_dir, exist_ok=True)

    contributions = dla.contributions
    names = [c[0] for c in contributions]
    values = [c[1] for c in contributions]

    fig, ax = plt.subplots(figsize=(16, 5))

    colors = []
    for name in names:
        if name == "Embed":
            colors.append("pink")
        elif name == "RMSNorm":
            colors.append("pink")
        elif "attn" in name:
            colors.append("olive")
        else:
            colors.append("steelblue")

    bars = ax.bar(range(len(values)), values, color=colors, edgecolor="black", linewidth=0.5)

    ax.axhline(y=0, color="gray", linestyle="-", linewidth=0.5)
    ax.set_ylabel("Contribution to Yes-No logit diff")
    ax.set_title(f"DLA: '{item_name}' ({'✓' if correct else '✗'})")

    # X-axis labels
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=90, fontsize=6)

    plt.tight_layout()
    safe_name = item_name.replace(" ", "_").replace("/", "_")
    plt.savefig(f"{output_dir}/dla_{safe_name}.png", dpi=150)
    plt.close()


def plot_dla_aggregate(results: list, output_dir: str):
    """Plot aggregate DLA with quartiles across all prompts."""
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Collect all contributions
    all_contribs = {}
    for r in results:
        if r.dla_info is None:
            continue
        for name, val in r.dla_info.contributions:
            if name not in all_contribs:
                all_contribs[name] = []
            all_contribs[name].append(val)

    # Get ordered names from first result
    names = [c[0] for c in results[0].dla_info.contributions]

    medians = []
    q1s = []
    q3s = []
    mins = []
    maxs = []

    for name in names:
        vals = np.array(all_contribs[name])
        medians.append(np.median(vals))
        q1s.append(np.percentile(vals, 25))
        q3s.append(np.percentile(vals, 75))
        mins.append(np.min(vals))
        maxs.append(np.max(vals))

    medians = np.array(medians)
    q1s = np.array(q1s)
    q3s = np.array(q3s)
    mins = np.array(mins)
    maxs = np.array(maxs)

    fig, ax = plt.subplots(figsize=(16, 6))

    x = np.arange(len(names))

    colors = []
    for name in names:
        if name == "Embed":
            colors.append("pink")
        elif name == "RMSNorm":
            colors.append("pink")
        elif "attn" in name:
            colors.append("olive")
        else:
            colors.append("steelblue")

    # Plot IQR as bars
    bar_bottoms = q1s
    bar_heights = q3s - q1s
    for i, (bottom, height, color) in enumerate(zip(bar_bottoms, bar_heights, colors)):
        ax.bar(i, height, bottom=bottom, color=color, edgecolor="black", linewidth=0.5, width=0.8)

    # Plot min-max as lines
    for i in range(len(names)):
        ax.plot([i, i], [mins[i], maxs[i]], color="black", linewidth=1.5)

    ax.axhline(y=0, color="lightcoral", linestyle="--", linewidth=1)
    ax.set_ylabel("Contribution to Yes-No logit diff")
    ax.set_title(f"DLA Aggregate (n={len(results)}): Bars=IQR, Lines=Min-Max")

    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=90, fontsize=6)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/dla_aggregate.png", dpi=150)
    plt.close()


def plot_dla_by_group(results: list, output_dir: str):
    """Plot separate aggregate DLA for TP, TN, FP, FN."""
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Split by confusion matrix categories
    # TP: has_emoji=True, model_said_yes=True (correct Yes)
    # TN: has_emoji=False, model_said_yes=False (correct No)
    # FP: has_emoji=False, model_said_yes=True (wrong Yes)
    # FN: has_emoji=True, model_said_yes=False (wrong No)
    tp_results = [r for r in results if r.item.has_emoji and r.model_said_yes and r.dla_info]
    tn_results = [r for r in results if not r.item.has_emoji and not r.model_said_yes and r.dla_info]
    fp_results = [r for r in results if not r.item.has_emoji and r.model_said_yes and r.dla_info]
    fn_results = [r for r in results if r.item.has_emoji and not r.model_said_yes and r.dla_info]

    groups = [
        ("true_positive", tp_results, "TP: Has emoji, said Yes (correct)"),
        ("true_negative", tn_results, "TN: No emoji, said No (correct)"),
        ("false_positive", fp_results, "FP: No emoji, said Yes (wrong)"),
        ("false_negative", fn_results, "FN: Has emoji, said No (wrong)"),
    ]

    for group_name, group_results, title in groups:
        if not group_results:
            print(f"  Skipping {group_name}: no results")
            continue

        all_contribs = {}
        for r in group_results:
            for name, val in r.dla_info.contributions:
                if name not in all_contribs:
                    all_contribs[name] = []
                all_contribs[name].append(val)

        names = [c[0] for c in group_results[0].dla_info.contributions]

        medians = []
        q1s = []
        q3s = []
        mins = []
        maxs = []

        for name in names:
            vals = np.array(all_contribs[name])
            medians.append(np.median(vals))
            q1s.append(np.percentile(vals, 25))
            q3s.append(np.percentile(vals, 75))
            mins.append(np.min(vals))
            maxs.append(np.max(vals))

        medians = np.array(medians)
        q1s = np.array(q1s)
        q3s = np.array(q3s)
        mins = np.array(mins)
        maxs = np.array(maxs)

        fig, ax = plt.subplots(figsize=(16, 6))

        x = np.arange(len(names))

        colors = []
        for name in names:
            if name == "Embed":
                colors.append("pink")
            elif name == "RMSNorm":
                colors.append("pink")
            elif "attn" in name:
                colors.append("olive")
            else:
                colors.append("steelblue")

        bar_bottoms = q1s
        bar_heights = q3s - q1s
        for i, (bottom, height, color) in enumerate(zip(bar_bottoms, bar_heights, colors)):
            ax.bar(i, height, bottom=bottom, color=color, edgecolor="black", linewidth=0.5, width=0.8)

        for i in range(len(names)):
            ax.plot([i, i], [mins[i], maxs[i]], color="black", linewidth=1.5)

        ax.axhline(y=0, color="lightcoral", linestyle="--", linewidth=1)
        ax.set_ylabel("Contribution to Yes-No logit diff")
        ax.set_title(f"DLA Aggregate - {title} (n={len(group_results)})")

        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=90, fontsize=6)

        plt.tight_layout()
        plt.savefig(f"{output_dir}/dla_aggregate_{group_name}.png", dpi=150)
        plt.close()
        print(f"  Saved {group_name} (n={len(group_results)})")


def plot_prompt_variant_results(all_results: dict[str, list[BenchResult]], output_dir: str):
    """Plot confusion matrix breakdown across prompt variants."""
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    os.makedirs(output_dir, exist_ok=True)

    variants = list(all_results.keys())

    # Calculate TP, TN, FP, FN for each variant
    metrics = {}
    for variant, results in all_results.items():
        tp = sum(1 for r in results if r.item.has_emoji and r.model_said_yes)
        tn = sum(1 for r in results if not r.item.has_emoji and not r.model_said_yes)
        fp = sum(1 for r in results if not r.item.has_emoji and r.model_said_yes)
        fn = sum(1 for r in results if r.item.has_emoji and not r.model_said_yes)
        metrics[variant] = {"TP": tp, "TN": tn, "FP": fp, "FN": fn}

    # Plot 1: Stacked bar chart by prompt variant
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: Items WITH emoji (TP vs FN)
    ax = axes[0]
    x = np.arange(len(variants))
    width = 0.6
    tp_vals = [metrics[v]["TP"] for v in variants]
    fn_vals = [metrics[v]["FN"] for v in variants]

    ax.bar(x, tp_vals, width, label="TP (correctly said Yes)", color="forestgreen")
    ax.bar(x, fn_vals, width, bottom=tp_vals, label="FN (wrongly said No)", color="salmon")

    ax.set_ylabel("Count")
    ax.set_title("Items WITH Emoji (should say Yes)")
    ax.set_xticks(x)
    ax.set_xticklabels([v.replace("_", "\n") for v in variants])
    ax.legend()

    # Add totals
    for i, v in enumerate(variants):
        total = tp_vals[i] + fn_vals[i]
        ax.annotate(f"{tp_vals[i]}/{total}", xy=(i, tp_vals[i] / 2), ha="center", va="center", fontweight="bold", color="white")
        if fn_vals[i] > 0:
            ax.annotate(f"{fn_vals[i]}", xy=(i, tp_vals[i] + fn_vals[i] / 2), ha="center", va="center", fontweight="bold")

    # Right: Items WITHOUT emoji (TN vs FP)
    ax = axes[1]
    tn_vals = [metrics[v]["TN"] for v in variants]
    fp_vals = [metrics[v]["FP"] for v in variants]

    ax.bar(x, tn_vals, width, label="TN (correctly said No)", color="forestgreen")
    ax.bar(x, fp_vals, width, bottom=tn_vals, label="FP (wrongly said Yes)", color="salmon")

    ax.set_ylabel("Count")
    ax.set_title("Items WITHOUT Emoji (should say No)")
    ax.set_xticks(x)
    ax.set_xticklabels([v.replace("_", "\n") for v in variants])
    ax.legend()

    for i, v in enumerate(variants):
        total = tn_vals[i] + fp_vals[i]
        ax.annotate(f"{tn_vals[i]}/{total}", xy=(i, tn_vals[i] / 2), ha="center", va="center", fontweight="bold", color="white")
        if fp_vals[i] > 0:
            ax.annotate(f"{fp_vals[i]}", xy=(i, tn_vals[i] + fp_vals[i] / 2), ha="center", va="center", fontweight="bold")

    plt.tight_layout()
    plt.savefig(f"{output_dir}/prompt_variants_by_ground_truth.png", dpi=150)
    plt.close()

    # Plot 2: Full confusion matrix heatmap per variant
    fig, axes = plt.subplots(1, len(variants), figsize=(5 * len(variants), 4))
    if len(variants) == 1:
        axes = [axes]

    for ax, variant in zip(axes, variants):
        m = metrics[variant]
        matrix = np.array([[m["TP"], m["FN"]], [m["FP"], m["TN"]]])

        im = ax.imshow(matrix, cmap="RdYlGn", vmin=0, vmax=max(m["TP"] + m["FN"], m["FP"] + m["TN"]))

        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(["Said Yes", "Said No"])
        ax.set_yticklabels(["Has Emoji", "No Emoji"])
        ax.set_title(f"{variant.replace('_', ' ').title()}")

        # Add text annotations
        labels = [["TP", "FN"], ["FP", "TN"]]
        for i in range(2):
            for j in range(2):
                val = matrix[i, j]
                color = "white" if val > matrix.max() / 2 else "black"
                ax.text(j, i, f"{labels[i][j]}\n{val}", ha="center", va="center", color=color, fontweight="bold")

    plt.tight_layout()
    plt.savefig(f"{output_dir}/prompt_variants_confusion_matrices.png", dpi=150)
    plt.close()

    # Plot 3: Accuracy comparison
    fig, ax = plt.subplots(figsize=(10, 5))

    x = np.arange(len(variants))
    width = 0.25

    accuracy = [(metrics[v]["TP"] + metrics[v]["TN"]) / sum(metrics[v].values()) * 100 for v in variants]
    recall = [metrics[v]["TP"] / (metrics[v]["TP"] + metrics[v]["FN"]) * 100 if (metrics[v]["TP"] + metrics[v]["FN"]) > 0 else 0 for v in variants]
    specificity = [metrics[v]["TN"] / (metrics[v]["TN"] + metrics[v]["FP"]) * 100 if (metrics[v]["TN"] + metrics[v]["FP"]) > 0 else 0 for v in variants]

    bars1 = ax.bar(x - width, accuracy, width, label="Accuracy", color="steelblue")
    bars2 = ax.bar(x, recall, width, label="Recall (TP Rate)", color="forestgreen")
    bars3 = ax.bar(x + width, specificity, width, label="Specificity (TN Rate)", color="darkorange")

    ax.set_ylabel("Percentage")
    ax.set_title("Performance Metrics by Prompt Variant")
    ax.set_xticks(x)
    ax.set_xticklabels([v.replace("_", " ").title() for v in variants])
    ax.legend()
    ax.set_ylim(0, 105)

    # Add value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"{height:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/prompt_variants_metrics.png", dpi=150)
    plt.close()

    print(f"Saved prompt variant charts to {output_dir}")
    return metrics


@app.function(image=image, volumes={VOLUME_PATH: volume}, timeout=600)
def save_variant_charts(all_results_data: dict[str, list[dict]]):
    """Save prompt variant comparison charts to volume."""
    output_dir = f"{VOLUME_PATH}/existence_variants"

    # Reconstruct BenchResult objects
    all_results = {}
    for variant, results_data in all_results_data.items():
        results = []
        for rd in results_data:
            item = BenchItem(
                name=rd["item_name"],
                has_emoji=rd["has_emoji"],
                category=Category(rd["category"]),
            )
            result = BenchResult(
                item=item,
                prompt_variant=variant,
                model_answer=rd["model_answer"],
                model_said_yes=rd["model_said_yes"],
                correct=rd["correct"],
            )
            results.append(result)
        all_results[variant] = results

    metrics = plot_prompt_variant_results(all_results, output_dir)
    volume.commit()
    return metrics


@app.function(image=image, volumes={VOLUME_PATH: volume}, timeout=600)
def save_plots(results_data: list[dict]):
    """Save all DLA plots to the volume."""
    import os

    output_dir = f"{VOLUME_PATH}/dla_charts_casual"
    os.makedirs(output_dir, exist_ok=True)

    # Reconstruct results
    results = []
    for rd in results_data:
        item = BenchItem(
            name=rd["item_name"],
            has_emoji=rd["has_emoji"],
            category=Category(rd["category"]),
        )
        logit_info = LogitInfo(**rd["logit_info"])
        dla_info = DLAInfo(
            logit_diff=rd["dla"]["logit_diff"],
            contributions=rd["dla"]["contributions"],
            total_attn=rd["dla"]["total_attn"],
            total_mlp=rd["dla"]["total_mlp"],
            embed_contrib=rd["dla"]["embed_contrib"],
            norm_contrib=rd["dla"]["norm_contrib"],
            bias_contrib=rd["dla"]["bias_contrib"],
            total=rd["dla"]["total"],
            error=rd["dla"]["error"],
        )
        result = BenchResult(
            item=item,
            model_answer=rd["model_answer"],
            model_said_yes=rd["model_said_yes"],
            correct=rd["correct"],
            logit_info=logit_info,
            dla_info=dla_info,
        )
        results.append(result)

        # Plot individual
        plot_dla_single(dla_info, item.name, rd["correct"], output_dir)

    # Plot aggregates
    plot_dla_aggregate(results, output_dir)
    plot_dla_by_group(results, output_dir)

    volume.commit()
    print(f"Saved {len(results)} individual plots + aggregates to {output_dir}")


@app.local_entrypoint()
def main():
    model = Qwen3Model()

    # Run all prompt variants
    all_results: dict[str, list[BenchResult]] = {}
    all_results_data: dict[str, list[dict]] = {}

    print(f"Running benchmark on {len(BENCH_ITEMS)} items across {len(PROMPT_VARIANTS)} prompt variants...")
    print(f"Total runs: {len(BENCH_ITEMS) * len(PROMPT_VARIANTS)}")
    print("=" * 100)

    for variant_name, prompt_fn in PROMPT_VARIANTS:
        print(f"\n{'='*40} {variant_name.upper()} {'='*40}")
        results: list[BenchResult] = []
        results_data: list[dict] = []

        for item in BENCH_ITEMS:
            prompt = prompt_fn(item.name)

            if PATCH_CONFIG:
                output = model.generate_with_patch.remote(prompt, CLEAN_PROMPT, PATCH_CONFIG)
            else:
                output = model.generate.remote(prompt)

            response = output["response"]

            logit_info = None
            if output["yes_logit"] is not None:
                logit_info = LogitInfo(
                    yes_logit=output["yes_logit"],
                    no_logit=output["no_logit"],
                    yes_prob=output["yes_prob"],
                    no_prob=output["no_prob"],
                    top_token=output["top_token"],
                    top_logit=output["top_logit"],
                    top_prob=output["top_prob"],
                )

            dla_data = output["dla"]
            dla_info = None
            if dla_data is not None:
                dla_info = DLAInfo(
                    logit_diff=dla_data["logit_diff"],
                    contributions=dla_data["contributions"],
                    total_attn=dla_data["total_attn"],
                    total_mlp=dla_data["total_mlp"],
                    embed_contrib=dla_data["embed_contrib"],
                    norm_contrib=dla_data["norm_contrib"],
                    bias_contrib=dla_data["bias_contrib"],
                    total=dla_data["total"],
                    error=dla_data["error"],
                )

            model_said_yes = parse_answer(response)
            correct = model_said_yes == item.has_emoji

            result = BenchResult(
                item=item,
                prompt_variant=variant_name,
                model_answer=response.strip(),
                model_said_yes=model_said_yes,
                correct=correct,
                logit_info=logit_info,
                dla_info=dla_info,
            )
            results.append(result)

            results_data.append({
                "item_name": item.name,
                "has_emoji": item.has_emoji,
                "category": item.category.value,
                "model_answer": response.strip(),
                "model_said_yes": model_said_yes,
                "correct": correct,
                "logit_info": {
                    "yes_logit": logit_info.yes_logit if logit_info else None,
                    "no_logit": logit_info.no_logit if logit_info else None,
                    "yes_prob": logit_info.yes_prob if logit_info else None,
                    "no_prob": logit_info.no_prob if logit_info else None,
                    "top_token": logit_info.top_token if logit_info else None,
                    "top_logit": logit_info.top_logit if logit_info else None,
                    "top_prob": logit_info.top_prob if logit_info else None,
                } if logit_info else None,
                "dla": dla_data,
            })

            status = "✓" if correct else "✗"
            expected = "Yes" if item.has_emoji else "No"
            got = "Yes" if model_said_yes else "No"

            if logit_info:
                logit_diff = logit_info.yes_logit - logit_info.no_logit
                print(
                    f"{status} {item.name:20} | exp={expected:3} got={got:3} | "
                    f"Y_logit={logit_info.yes_logit:+7.2f} N_logit={logit_info.no_logit:+7.2f} diff={logit_diff:+.2f} | "
                    f"Y_prob={logit_info.yes_prob:.3f} N_prob={logit_info.no_prob:.3f}"
                )
            else:
                print(f"{status} {item.name:20} | exp={expected:3} got={got:3} | {response.strip()[:30]}")

        all_results[variant_name] = results
        all_results_data[variant_name] = results_data

        # Print summary for this variant
        correct_count = sum(1 for r in results if r.correct)
        tp = sum(1 for r in results if r.item.has_emoji and r.model_said_yes)
        tn = sum(1 for r in results if not r.item.has_emoji and not r.model_said_yes)
        fp = sum(1 for r in results if not r.item.has_emoji and r.model_said_yes)
        fn = sum(1 for r in results if r.item.has_emoji and not r.model_said_yes)

        print(f"\n{variant_name}: {correct_count}/{len(results)} ({100 * correct_count / len(results):.1f}%)")
        print(f"  TP={tp} TN={tn} FP={fp} FN={fn}")

    # Save comparison charts
    print("\n" + "=" * 100)
    print("Saving prompt variant comparison charts...")
    metrics = save_variant_charts.remote(all_results_data)

    # Print final summary table
    print("\n" + "=" * 100)
    print("FINAL SUMMARY - All Prompt Variants")
    print("=" * 100)
    print(f"{'Variant':<20} {'Accuracy':>10} {'TP':>6} {'TN':>6} {'FP':>6} {'FN':>6} {'Recall':>10} {'Specificity':>12}")
    print("-" * 90)

    for variant_name, results in all_results.items():
        tp = sum(1 for r in results if r.item.has_emoji and r.model_said_yes)
        tn = sum(1 for r in results if not r.item.has_emoji and not r.model_said_yes)
        fp = sum(1 for r in results if not r.item.has_emoji and r.model_said_yes)
        fn = sum(1 for r in results if r.item.has_emoji and not r.model_said_yes)

        accuracy = (tp + tn) / len(results) * 100
        recall = tp / (tp + fn) * 100 if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) * 100 if (tn + fp) > 0 else 0

        print(f"{variant_name:<20} {accuracy:>9.1f}% {tp:>6} {tn:>6} {fp:>6} {fn:>6} {recall:>9.1f}% {specificity:>11.1f}%")

    print("\nCharts saved to modal volume 'emoji-results' in /existence_variants/")


if __name__ == "__main__":
    main()
