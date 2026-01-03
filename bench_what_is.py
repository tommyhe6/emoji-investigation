from dataclasses import dataclass
from enum import Enum

import modal

app = modal.App("emoji-what-is")

MODEL_ID = "Qwen/Qwen3-4B-Instruct-2507"


class Category(Enum):
    ANIMAL = "animal"
    MYTHICAL = "mythical"
    OBJECT = "object"
    FOOD = "food"
    NATURE = "nature"
    SYMBOL = "symbol"
    PERSON = "person"
    TRANSPORT = "transport"
    PLACE = "place"


@dataclass
class EmojiItem:
    emoji: str
    expected_answers: list[str]
    category: Category
    correct_token: str | None = None  # token for correct answer (from logits)
    wrong_token_space: str | None = None  # wrong token with space prompt
    wrong_token_nospace: str | None = None  # wrong token without space prompt


# 100 emojis with expected one-word answers
# correct_token: the token prefix for correct answer (from no-space logits)
# wrong_token_space: wrong token with space prompt (None if correct)
# wrong_token_nospace: wrong token without space prompt (None if correct)
EMOJI_ITEMS = [
    # Animals (40)
    EmojiItem("🐙", ["octopus"], Category.ANIMAL, "Oct", "Sn", None),
    EmojiItem("🐌", ["snail"], Category.ANIMAL, "Sn", "Snake", None),
    EmojiItem("🐬", ["dolphin"], Category.ANIMAL, "D", "B", None),
    EmojiItem("🐋", ["whale"], Category.ANIMAL, "Wh", "Sea", None),
    EmojiItem("🦈", ["shark"], Category.ANIMAL, "Sh", None, None),
    EmojiItem("🐢", ["turtle"], Category.ANIMAL, "T", None, None),
    EmojiItem("🐊", ["crocodile", "alligator"], Category.ANIMAL, "Cro", "Snake", None),
    EmojiItem("🐍", ["snake"], Category.ANIMAL, "Snake", None, None),
    EmojiItem("🦎", ["lizard"], Category.ANIMAL, "L", "T", None),
    EmojiItem("🐸", ["frog"], Category.ANIMAL, "F", "S", None),
    EmojiItem("🦋", ["butterfly"], Category.ANIMAL, "But", None, None),
    EmojiItem("🐝", ["bee"], Category.ANIMAL, "B", None, None),
    EmojiItem("🐞", ["ladybug", "bug"], Category.ANIMAL, "Bug", None, "Ground"),
    EmojiItem("🦂", ["scorpion"], Category.ANIMAL, "S", "P", "T"),
    EmojiItem("🕷️", ["spider"], Category.ANIMAL, "Spider", None, None),
    EmojiItem("🐱", ["cat"], Category.ANIMAL, "Cat", None, None),
    EmojiItem("🐕", ["dog"], Category.ANIMAL, "Dog", None, None),
    EmojiItem("🐰", ["rabbit", "bunny"], Category.ANIMAL, "R", None, None),
    EmojiItem("🐭", ["mouse"], Category.ANIMAL, "Mouse", None, None),
    EmojiItem("🐹", ["hamster"], Category.ANIMAL, "H", "P", "H"),
    EmojiItem("🐘", ["elephant"], Category.ANIMAL, "Ele", "P", None),
    EmojiItem("🦁", ["lion"], Category.ANIMAL, "L", "Wolf", None),
    EmojiItem("🐯", ["tiger"], Category.ANIMAL, "T", None, None),
    EmojiItem("🐒", ["monkey"], Category.ANIMAL, "Monkey", None, None),
    EmojiItem("🐧", ["penguin"], Category.ANIMAL, "P", "Se", None),
    EmojiItem("🦉", ["owl"], Category.ANIMAL, "O", "C", "E"),
    EmojiItem("🦅", ["eagle"], Category.ANIMAL, "E", "Crow", None),
    EmojiItem("🦜", ["parrot"], Category.ANIMAL, "Par", "Monkey", "D"),
    EmojiItem("🦢", ["swan"], Category.ANIMAL, "S", "T", "O"),
    EmojiItem("🦚", ["peacock"], Category.ANIMAL, "Pe", "Fox", None),
    EmojiItem("🦦", ["otter"], Category.ANIMAL, "O", "G", "D"),
    EmojiItem("🦥", ["sloth"], Category.ANIMAL, "Sl", "T", "P"),
    EmojiItem("🐻", ["bear"], Category.ANIMAL, "Bear", None, None),
    EmojiItem("🐼", ["panda"], Category.ANIMAL, "P", None, None),
    EmojiItem("🦊", ["fox"], Category.ANIMAL, "Fox", None, None),
    EmojiItem("🐺", ["wolf"], Category.ANIMAL, "Wolf", None, None),
    EmojiItem("🦝", ["raccoon"], Category.ANIMAL, "R", "Crow", "T"),
    EmojiItem("🐮", ["cow"], Category.ANIMAL, "Cow", "B", None),
    EmojiItem("🐷", ["pig"], Category.ANIMAL, "P", "P", None),  # P is ambiguous
    EmojiItem(
        "🐔", ["chicken", "chickens"], Category.ANIMAL, "Ch", "Ch", None
    ),  # chick vs chicken
    # Mythical (5)
    EmojiItem("🐉", ["dragon"], Category.ANIMAL, "Dragon", None, None),
    EmojiItem(
        "🦄", ["unicorn", "unicorns"], Category.MYTHICAL, "Un", "Un", None
    ),  # unicore vs unicorn
    EmojiItem("🧜‍♀️", ["mermaid"], Category.MYTHICAL, "Mer", "W", None),
    EmojiItem("🧚", ["fairy"], Category.MYTHICAL, "F", "G", "G"),
    EmojiItem("🧞", ["genie"], Category.MYTHICAL, "G", "W", "Wizard"),
    # Objects (20)
    EmojiItem("💻", ["computer", "laptop"], Category.OBJECT, "L", None, None),
    EmojiItem("☎️", ["telephone", "phone"], Category.OBJECT, "Phone", None, None),
    EmojiItem("📺", ["television", "tv"], Category.OBJECT, "TV", None, None),
    EmojiItem("📷", ["camera"], Category.OBJECT, "Camera", None, None),
    EmojiItem("✂️", ["scissors"], Category.OBJECT, "Sc", None, None),
    EmojiItem("🔑", ["key"], Category.OBJECT, "Key", "Lock", "Lock"),
    EmojiItem("🔒", ["lock", "padlock"], Category.OBJECT, "Lock", None, None),
    EmojiItem("💡", ["lightbulb", "bulb"], Category.OBJECT, "Light", None, None),
    EmojiItem("🔨", ["hammer"], Category.OBJECT, "Ham", "S", None),
    EmojiItem("🪓", ["axe"], Category.OBJECT, "A", "S", "S"),
    EmojiItem("🔧", ["wrench"], Category.OBJECT, "W", None, None),
    EmojiItem("⚙️", ["gear", "cog"], Category.OBJECT, "Gear", None, None),
    EmojiItem("🧲", ["magnet"], Category.OBJECT, "M", "Rock", None),
    EmojiItem("🪞", ["mirror"], Category.OBJECT, "Mirror", None, None),
    EmojiItem("🧳", ["suitcase", "luggage"], Category.OBJECT, "Suit", None, None),
    EmojiItem("🎸", ["guitar"], Category.OBJECT, "G", None, None),
    EmojiItem("🎹", ["piano", "keyboard"], Category.OBJECT, "P", "G", None),
    EmojiItem("🎺", ["trumpet"], Category.OBJECT, "Trump", "U", None),
    EmojiItem("🥁", ["drum"], Category.OBJECT, "Dr", "Av", None),
    EmojiItem(
        "🎯", ["target", "dart", "dartboard"], Category.OBJECT, "Target", None, None
    ),
    # Food (15)
    EmojiItem("🍕", ["pizza"], Category.FOOD, "Pizza", None, None),
    EmojiItem("🍔", ["hamburger", "burger"], Category.FOOD, "H", None, None),
    EmojiItem("🍎", ["apple"], Category.FOOD, "Apple", None, None),
    EmojiItem("🍌", ["banana"], Category.FOOD, "Ban", None, None),
    EmojiItem("🍓", ["strawberry"], Category.FOOD, "Str", None, None),
    EmojiItem("🍇", ["grapes"], Category.FOOD, "Gr", "Gr", None),  # grape vs grapes
    EmojiItem("🍊", ["orange", "tangerine"], Category.FOOD, "Orange", None, None),
    EmojiItem("🍋", ["lemon"], Category.FOOD, "L", None, None),
    EmojiItem("🍉", ["watermelon"], Category.FOOD, "Water", None, None),
    EmojiItem("🍒", ["cherry", "cherries"], Category.FOOD, "Ch", "Rose", "Ber"),
    EmojiItem("🥕", ["carrot"], Category.FOOD, "Car", "E", None),
    EmojiItem("🥦", ["broccoli"], Category.FOOD, "Bro", "L", None),
    EmojiItem("🌽", ["corn"], Category.FOOD, "Corn", None, None),
    EmojiItem("🧀", ["cheese"], Category.FOOD, "Che", None, None),
    EmojiItem("🥚", ["egg"], Category.FOOD, "E", None, None),
    # Nature (10)
    EmojiItem("☀️", ["sun"], Category.NATURE, "Sun", None, None),
    EmojiItem("🌙", ["moon"], Category.NATURE, "Moon", None, None),
    EmojiItem("⭐", ["star"], Category.NATURE, "Star", None, None),
    EmojiItem("🌈", ["rainbow"], Category.NATURE, "Rain", None, None),
    EmojiItem("🌋", ["volcano"], Category.NATURE, "Vol", "Fire", None),
    EmojiItem("🌊", ["wave", "ocean"], Category.NATURE, "Ocean", None, None),
    EmojiItem("❄️", ["snowflake", "snow"], Category.NATURE, "Snow", None, None),
    EmojiItem("🔥", ["fire", "flame"], Category.NATURE, "Fire", None, None),
    EmojiItem("🌲", ["tree", "pine"], Category.NATURE, "Tree", None, None),
    EmojiItem("🌵", ["cactus"], Category.NATURE, "C", "D", None),
    # Symbols/Misc (10)
    EmojiItem("❤️", ["heart"], Category.SYMBOL, "Heart", None, None),
    EmojiItem("💀", ["skull", "dead"], Category.SYMBOL, "Dead", "Death", None),
    EmojiItem("👁️", ["eye"], Category.SYMBOL, "Eye", None, None),
    EmojiItem("👂", ["ear"], Category.SYMBOL, "Ear", "E", None),
    EmojiItem("👃", ["nose"], Category.SYMBOL, "N", "Face", None),
    EmojiItem("👄", ["mouth", "lips"], Category.SYMBOL, "M", "Face", None),
    EmojiItem(
        "✋", ["hand"], Category.SYMBOL, "Hand", "Hand", None
    ),  # handshake vs hand
    EmojiItem(
        "👣",
        ["footprints", "feet", "footsteps"],
        Category.SYMBOL,
        "Foot",
        "Walking",
        None,
    ),
    EmojiItem("💎", ["diamond", "gem"], Category.SYMBOL, "Diamond", None, None),
    EmojiItem("👑", ["crown"], Category.SYMBOL, "C", None, None),
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
        }

    @modal.method()
    def generate_with_logits(self, prompt: str, max_tokens: int = 20) -> dict:
        import torch

        inputs = self.tokenizer([prompt], return_tensors="pt").to(self.model.device)
        generated_ids = inputs["input_ids"][0].tolist()

        with torch.no_grad():
            outputs = self.model(
                input_ids=torch.tensor([generated_ids]).to(self.model.device)
            )
            logits = outputs.logits[0, -1, :]

            probs = torch.softmax(logits, dim=-1)
            top_logit, top_idx = torch.max(logits, dim=-1)
            top_token = self.tokenizer.decode([top_idx.item()])

            # Get top 10 tokens
            top_k = 10
            top_logits, top_indices = torch.topk(logits, top_k)
            top_tokens = [
                (
                    self.tokenizer.decode([idx.item()]),
                    logits[idx].item(),
                    probs[idx].item(),
                )
                for idx in top_indices
            ]

            # Generate full response
            next_token_id = top_idx.item()
            generated_ids.append(next_token_id)
            output_tokens = [top_token]

            for _ in range(max_tokens):
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
            "top_token": top_token,
            "top_logit": top_logit.item(),
            "top_prob": probs[top_idx].item(),
            "top_10": top_tokens,
        }

    @modal.method()
    def generate_with_dla(self, prompt: str, token_a: str, token_b: str) -> dict:
        """
        Generate with Direct Logit Attribution for token_a vs token_b.
        Returns contributions from each component to the logit difference.
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

        hooks.append(
            self.model.model.embed_tokens.register_forward_hook(cache_output("embed"))
        )
        for i, layer in enumerate(self.model.model.layers):
            hooks.append(
                layer.self_attn.register_forward_hook(cache_output(f"L{i}_attn"))
            )
            hooks.append(layer.mlp.register_forward_hook(cache_output(f"L{i}_mlp")))
        hooks.append(
            self.model.model.norm.register_forward_hook(cache_output("final_norm"))
        )

        with torch.no_grad():
            outputs = self.model(input_ids=inputs["input_ids"])
            logits = outputs.logits[0, -1, :]

        for hook in hooks:
            hook.remove()

        token_a_id = self.tokenizer.encode(token_a, add_special_tokens=False)[0]
        token_b_id = self.tokenizer.encode(token_b, add_special_tokens=False)[0]

        token_a_logit = logits[token_a_id].item()
        token_b_logit = logits[token_b_id].item()

        probs = torch.softmax(logits, dim=-1)
        token_a_prob = probs[token_a_id].item()
        token_b_prob = probs[token_b_id].item()

        top_logit_val, top_idx = torch.max(logits, dim=-1)
        top_token = self.tokenizer.decode([top_idx.item()])

        # Get top 10 tokens
        top_k = 10
        top_logits, top_indices = torch.topk(logits, top_k)
        top_tokens = [
            (self.tokenizer.decode([idx.item()]), logits[idx].item(), probs[idx].item())
            for idx in top_indices
        ]

        # DLA: logit diff direction (token_a - token_b)
        lm_head = self.model.lm_head.weight
        logit_dir = lm_head[token_a_id] - lm_head[token_b_id]
        logit_diff = token_a_logit - token_b_logit

        pos = -1
        contributions = []
        total_attn = 0.0
        total_mlp = 0.0

        embed = cache["embed"][0, pos, :]
        embed_contrib = torch.dot(embed, logit_dir).item()
        contributions.append(("Embed", embed_contrib))
        residual = embed.clone()

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

        final_normed = cache["final_norm"][0, pos, :]
        norm_delta = final_normed - residual
        norm_contrib = torch.dot(norm_delta, logit_dir).item()
        contributions.append(("RMSNorm", norm_contrib))

        bias_contrib = 0.0
        if self.model.lm_head.bias is not None:
            bias_contrib = (
                self.model.lm_head.bias[token_a_id]
                - self.model.lm_head.bias[token_b_id]
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
            "token_a": token_a,
            "token_b": token_b,
            "token_a_logit": token_a_logit,
            "token_b_logit": token_b_logit,
            "token_a_prob": token_a_prob,
            "token_b_prob": token_b_prob,
            "top_token": top_token,
            "top_logit": top_logit_val.item(),
            "top_prob": probs[top_idx].item(),
            "top_10": top_tokens,
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
        """Generate with activation patching from a clean prompt."""
        import re

        import torch

        config = patch_config.strip()
        patch_info = None

        if match := re.match(r"resid_pre_L(\d+)$", config):
            patch_info = {"type": "resid_pre", "layer": int(match.group(1))}
        elif match := re.match(r"resid_mid_L(\d+)$", config):
            patch_info = {"type": "resid_mid", "layer": int(match.group(1))}
        elif config == "resid_post_final":
            patch_info = {"type": "resid_post_final"}
        elif match := re.match(r"L(\d+)H(\d+)$", config):
            patch_info = {
                "type": "head",
                "layer": int(match.group(1)),
                "head": int(match.group(2)),
            }
        elif match := re.match(r"L(\d+)-L(\d+)$", config):
            patch_info = {
                "type": "window",
                "start": int(match.group(1)),
                "end": int(match.group(2)),
            }
        elif match := re.match(r"L(\d+)_(attn|mlp)$", config):
            patch_info = {
                "type": "component",
                "layer": int(match.group(1)),
                "component": match.group(2),
            }
        elif match := re.match(r"L(\d+)$", config):
            patch_info = {"type": "layer", "layer": int(match.group(1))}
        else:
            raise ValueError(f"Unknown patch config: {config}")

        clean_inputs = self.tokenizer([clean_prompt], return_tensors="pt").to(
            self.model.device
        )
        corrupt_inputs = self.tokenizer([prompt], return_tensors="pt").to(
            self.model.device
        )

        num_heads = self.model.config.num_attention_heads
        head_dim = self.model.config.hidden_size // num_heads

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
            hooks.append(
                self.model.model.layers[layer_idx].register_forward_pre_hook(
                    cache_input(f"resid_pre_L{layer_idx}")
                )
            )
        elif patch_type == "resid_mid":
            layer_idx = patch_info["layer"]
            hooks.append(
                self.model.model.layers[layer_idx].mlp.register_forward_pre_hook(
                    cache_input(f"resid_mid_L{layer_idx}")
                )
            )
        elif patch_type == "resid_post_final":
            hooks.append(
                self.model.model.norm.register_forward_pre_hook(
                    cache_input("resid_post_final")
                )
            )
        elif patch_type == "head":
            layer_idx = patch_info["layer"]
            hooks.append(
                self.model.model.layers[layer_idx].self_attn.register_forward_hook(
                    cache_output(f"L{layer_idx}_attn")
                )
            )
        elif patch_type == "component":
            layer_idx = patch_info["layer"]
            comp = patch_info["component"]
            if comp == "attn":
                hooks.append(
                    self.model.model.layers[layer_idx].self_attn.register_forward_hook(
                        cache_output(f"L{layer_idx}_attn")
                    )
                )
            else:
                hooks.append(
                    self.model.model.layers[layer_idx].mlp.register_forward_hook(
                        cache_output(f"L{layer_idx}_mlp")
                    )
                )
        elif patch_type == "layer":
            layer_idx = patch_info["layer"]
            hooks.append(
                self.model.model.layers[layer_idx].self_attn.register_forward_hook(
                    cache_output(f"L{layer_idx}_attn")
                )
            )
            hooks.append(
                self.model.model.layers[layer_idx].mlp.register_forward_hook(
                    cache_output(f"L{layer_idx}_mlp")
                )
            )
        elif patch_type == "window":
            for layer_idx in range(patch_info["start"], patch_info["end"] + 1):
                hooks.append(
                    self.model.model.layers[layer_idx].self_attn.register_forward_hook(
                        cache_output(f"L{layer_idx}_attn")
                    )
                )
                hooks.append(
                    self.model.model.layers[layer_idx].mlp.register_forward_hook(
                        cache_output(f"L{layer_idx}_mlp")
                    )
                )

        with torch.no_grad():
            self.model(input_ids=clean_inputs["input_ids"])

        for hook in hooks:
            hook.remove()

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
            patch_hooks.append(
                self.model.model.layers[layer_idx].register_forward_pre_hook(
                    make_resid_patch_hook(clean_act)
                )
            )
        elif patch_type == "resid_mid":
            layer_idx = patch_info["layer"]
            clean_act = clean_cache[f"resid_mid_L{layer_idx}"]
            patch_hooks.append(
                self.model.model.layers[layer_idx].mlp.register_forward_pre_hook(
                    make_resid_patch_hook(clean_act)
                )
            )
        elif patch_type == "resid_post_final":
            clean_act = clean_cache["resid_post_final"]
            patch_hooks.append(
                self.model.model.norm.register_forward_pre_hook(
                    make_resid_patch_hook(clean_act)
                )
            )
        elif patch_type == "head":
            layer_idx = patch_info["layer"]
            head_idx = patch_info["head"]
            clean_act = clean_cache[f"L{layer_idx}_attn"]
            patch_hooks.append(
                self.model.model.layers[layer_idx].self_attn.register_forward_hook(
                    make_head_patch_hook(clean_act, head_idx, head_dim)
                )
            )
        elif patch_type == "component":
            layer_idx = patch_info["layer"]
            comp = patch_info["component"]
            if comp == "attn":
                clean_act = clean_cache[f"L{layer_idx}_attn"]
                patch_hooks.append(
                    self.model.model.layers[layer_idx].self_attn.register_forward_hook(
                        make_output_patch_hook(clean_act)
                    )
                )
            else:
                clean_act = clean_cache[f"L{layer_idx}_mlp"]
                patch_hooks.append(
                    self.model.model.layers[layer_idx].mlp.register_forward_hook(
                        make_output_patch_hook(clean_act)
                    )
                )
        elif patch_type == "layer":
            layer_idx = patch_info["layer"]
            clean_attn = clean_cache[f"L{layer_idx}_attn"]
            clean_mlp = clean_cache[f"L{layer_idx}_mlp"]
            patch_hooks.append(
                self.model.model.layers[layer_idx].self_attn.register_forward_hook(
                    make_output_patch_hook(clean_attn)
                )
            )
            patch_hooks.append(
                self.model.model.layers[layer_idx].mlp.register_forward_hook(
                    make_output_patch_hook(clean_mlp)
                )
            )
        elif patch_type == "window":
            for layer_idx in range(patch_info["start"], patch_info["end"] + 1):
                clean_attn = clean_cache[f"L{layer_idx}_attn"]
                clean_mlp = clean_cache[f"L{layer_idx}_mlp"]
                patch_hooks.append(
                    self.model.model.layers[layer_idx].self_attn.register_forward_hook(
                        make_output_patch_hook(clean_attn)
                    )
                )
                patch_hooks.append(
                    self.model.model.layers[layer_idx].mlp.register_forward_hook(
                        make_output_patch_hook(clean_mlp)
                    )
                )

        generated_ids = corrupt_inputs["input_ids"][0].tolist()
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

        for hook in patch_hooks:
            hook.remove()

        return {
            "response": "".join(output_tokens),
            "patch_config": patch_config,
        }


# BASE
def mp_space_base(emoji: str) -> str:
    return f"""What emoji is: {emoji}? Answer in 1 word."""


def mp_no_space_base(emoji: str) -> str:
    return f"""What emoji is:{emoji}? Answer in 1 word."""

# INSTRUCT
def mp_space_instruct(emoji: str) -> str:
    return f"""<|im_start|>user
What emoji is: {emoji}? Answer in 1 word.<|im_end|>
<|im_start|>assistant
"""


def prompt_no_space_instruct(emoji: str) -> str:
    return f"""<|im_start|>user
What emoji is:{emoji}? Answer in 1 word.<|im_end|>
<|im_start|>assistant
"""


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
class BenchResult:
    item: EmojiItem
    prompt_type: str  # "with_space" or "no_space"
    model_answer: str
    first_word: str
    correct: bool
    top_10: list[tuple[str, float, float]] | None = None
    dla_info: DLAInfo | None = None
    token_a: str | None = None
    token_b: str | None = None


def print_dla_chart(dla: DLAInfo, label: str, token_a: str, token_b: str):
    """Print full DLA chart."""
    print("    " + "=" * 76)
    print(f"    DIRECT LOGIT ATTRIBUTION: {token_a} vs {token_b} for '{label}'")
    print("    " + "=" * 76)
    print(f"    Logit diff ({token_a} - {token_b}): {dla.logit_diff:.4f}")
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


def extract_first_word(response: str) -> str:
    """Extract the first word from a response."""
    response = response.strip()
    # Remove thinking tags if present
    if "<think>" in response:
        response = response.split("</think>")[-1].strip()
    # Get first word
    words = response.split()
    if words:
        return words[0].lower().strip(".,!?;:'\"")
    return ""


def check_answer(response: str, expected_answers: list[str]) -> bool:
    """Check if the response (stripped and lowered) is in the expected answers."""
    cleaned = (
        response.replace("<|im_end|>", "").replace("<|endoftext|>", "").strip().lower()
    )
    return cleaned in [e.lower() for e in expected_answers]


# Set to True to run DLA on all items with wrong tokens
RUN_DLA_WRONG = False


def run_dla_on_wrong_items(model):
    """Run DLA on all items that have wrong tokens, comparing correct vs wrong."""
    print("Running DLA on items with wrong tokens...")
    print("=" * 100)

    for idx, item in enumerate(EMOJI_ITEMS):
        # Check space prompt
        if item.wrong_token_space and item.correct_token:
            prompt = mp_space_base(item.emoji)
            print(
                f"\n[{idx}] {item.emoji} [S] correct={item.correct_token} wrong={item.wrong_token_space}"
            )

            output = model.generate_with_dla.remote(
                prompt, item.correct_token, item.wrong_token_space
            )

            response = output["response"]
            first_word = extract_first_word(response)
            top_10 = output.get("top_10", [])
            top_10_str = " ".join(
                f"{tok}({prob:.2f})" for tok, logit, prob in top_10[:5]
            )
            print(f"  got={first_word:15} | {top_10_str}")

            dla_data = output.get("dla")
            if dla_data:
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
                print_dla_chart(
                    dla_info,
                    f"{item.emoji} [S]",
                    item.correct_token,
                    item.wrong_token_space,
                )

        # Check no-space prompt
        if item.wrong_token_nospace and item.correct_token:
            prompt = mp_no_space_base(item.emoji)
            print(
                f"\n[{idx}] {item.emoji} [N] correct={item.correct_token} wrong={item.wrong_token_nospace}"
            )

            output = model.generate_with_dla.remote(
                prompt, item.correct_token, item.wrong_token_nospace
            )

            response = output["response"]
            first_word = extract_first_word(response)
            top_10 = output.get("top_10", [])
            top_10_str = " ".join(
                f"{tok}({prob:.2f})" for tok, logit, prob in top_10[:5]
            )
            print(f"  got={first_word:15} | {top_10_str}")

            dla_data = output.get("dla")
            if dla_data:
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
                print_dla_chart(
                    dla_info,
                    f"{item.emoji} [N]",
                    item.correct_token,
                    item.wrong_token_nospace,
                )


@app.local_entrypoint()
def main():
    model = Qwen3Model()

    if RUN_DLA_WRONG:
        run_dla_on_wrong_items(model)
        return

    # Determine model name and prompt functions from MODEL_ID
    if "Instruct" in MODEL_ID:
        model_name = "Instruct"
        mp_space = mp_space_instruct
        mp_no_space = prompt_no_space_instruct
    else:
        model_name = "Base"
        mp_space = mp_space_base
        mp_no_space = mp_no_space_base

    # Full benchmark mode
    results: list[BenchResult] = []
    results_data: list[dict] = []

    print(f"Running 'What is' benchmark on {len(EMOJI_ITEMS)} emojis ({model_name})...")
    print("=" * 100)

    for item in EMOJI_ITEMS:
        for prompt_type, prompt_fn in [
            ("with_space", mp_space),
            ("no_space", mp_no_space),
        ]:
            prompt = prompt_fn(item.emoji)
            output = model.generate_with_logits.remote(prompt)

            response = output["response"]
            first_word = extract_first_word(response)
            correct = check_answer(response, item.expected_answers)

            result = BenchResult(
                item=item,
                prompt_type=prompt_type,
                model_answer=response.strip(),
                first_word=first_word,
                correct=correct,
                top_10=output.get("top_10"),
            )
            results.append(result)

            # Collect data for saving
            results_data.append({
                "emoji": item.emoji,
                "expected_answers": item.expected_answers,
                "category": item.category.value,
                "prompt_type": prompt_type,
                "model_answer": response.strip(),
                "first_word": first_word,
                "correct": correct,
                "top_10": output.get("top_10"),
            })

            status = "✓" if correct else "✗"
            space_marker = "S" if prompt_type == "with_space" else "N"
            top_10 = output.get("top_10", [])
            top_10_str = " ".join(
                f"{tok}({prob:.2f})" for tok, logit, prob in top_10[:5]
            )
            print(
                f"{status} [{space_marker}] {item.emoji} | exp={'/'.join(item.expected_answers):15} got={first_word:15} | {top_10_str}"
            )

    print("=" * 100)

    # Summary
    with_space_results = [r for r in results if r.prompt_type == "with_space"]
    no_space_results = [r for r in results if r.prompt_type == "no_space"]

    with_correct = sum(1 for r in with_space_results if r.correct)
    no_correct = sum(1 for r in no_space_results if r.correct)

    print(
        f"\nWith space:    {with_correct}/{len(with_space_results)} ({100 * with_correct / len(with_space_results):.1f}%)"
    )
    print(
        f"No space:      {no_correct}/{len(no_space_results)} ({100 * no_correct / len(no_space_results):.1f}%)"
    )

    # Find discrepancies
    print("\n" + "-" * 80)
    print("DISCREPANCIES (different answers between space/no-space):")
    print("-" * 80)

    for item in EMOJI_ITEMS:
        with_space = next(
            r for r in results if r.item == item and r.prompt_type == "with_space"
        )
        no_space = next(
            r for r in results if r.item == item and r.prompt_type == "no_space"
        )

        if with_space.first_word != no_space.first_word:
            print(f"{item.emoji} ({'/'.join(item.expected_answers)})")
            print(
                f"  With space: {with_space.first_word:15} {'✓' if with_space.correct else '✗'}"
            )
            print(
                f"  No space:   {no_space.first_word:15} {'✓' if no_space.correct else '✗'}"
            )

    # Breakdown by category
    print("\n" + "-" * 80)
    print("BREAKDOWN BY CATEGORY:")
    print("-" * 80)

    for category in Category:
        cat_items = [item for item in EMOJI_ITEMS if item.category == category]
        if not cat_items:
            continue

        cat_with = [r for r in with_space_results if r.item.category == category]
        cat_no = [r for r in no_space_results if r.item.category == category]

        cat_with_correct = sum(1 for r in cat_with if r.correct)
        cat_no_correct = sum(1 for r in cat_no if r.correct)

        print(f"\n{category.value.upper()} ({len(cat_items)} items):")
        print(
            f"  With space: {cat_with_correct}/{len(cat_with)} ({100 * cat_with_correct / len(cat_with):.1f}%)"
        )
        print(
            f"  No space:   {cat_no_correct}/{len(cat_no)} ({100 * cat_no_correct / len(cat_no):.1f}%)"
        )

    # All wrong answers
    wrong_with_space = [r for r in with_space_results if not r.correct]
    wrong_no_space = [r for r in no_space_results if not r.correct]

    print("\n" + "-" * 80)
    print(f"WRONG ANSWERS - WITH SPACE ({len(wrong_with_space)}):")
    print("-" * 80)
    for r in wrong_with_space:
        print(
            f"  {r.item.emoji} | exp={'/'.join(r.item.expected_answers):15} got={r.first_word:15} | {r.model_answer[:50]}"
        )

    print("\n" + "-" * 80)
    print(f"WRONG ANSWERS - NO SPACE ({len(wrong_no_space)}):")
    print("-" * 80)
    for r in wrong_no_space:
        print(
            f"  {r.item.emoji} | exp={'/'.join(r.item.expected_answers):15} got={r.first_word:15} | {r.model_answer[:50]}"
        )

    # Save results and generate plots to volume
    print("\n" + "-" * 80)
    print("Saving results and generating plots to volume...")
    print("-" * 80)
    save_results_and_plots.remote(results_data, model_name)
    print(f"Done! Results saved to modal volume 'emoji-results' under 'what_is_{model_name.lower()}'")


def plot_results_by_category(results: list[BenchResult], model_name: str, output_dir: str):
    """Plot bar chart of accuracy by category for a single model."""
    import os

    import matplotlib.pyplot as plt
    import numpy as np

    os.makedirs(output_dir, exist_ok=True)

    categories = [cat for cat in Category if any(
        item.category == cat for item in EMOJI_ITEMS
    )]
    cat_names = [cat.value for cat in categories]

    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.35
    positions = np.arange(len(categories))

    with_space_results = [r for r in results if r.prompt_type == "with_space"]
    no_space_results = [r for r in results if r.prompt_type == "no_space"]

    with_space_acc = []
    no_space_acc = []

    for cat in categories:
        cat_with = [r for r in with_space_results if r.item.category == cat]
        cat_no = [r for r in no_space_results if r.item.category == cat]

        if cat_with:
            with_space_acc.append(100 * sum(1 for r in cat_with if r.correct) / len(cat_with))
        else:
            with_space_acc.append(0)

        if cat_no:
            no_space_acc.append(100 * sum(1 for r in cat_no if r.correct) / len(cat_no))
        else:
            no_space_acc.append(0)

    ax.bar(positions - bar_width / 2, with_space_acc, bar_width, label="With Space", color="tab:blue")
    ax.bar(positions + bar_width / 2, no_space_acc, bar_width, label="No Space", color="tab:orange")

    ax.set_xlabel("Category")
    ax.set_ylabel("Accuracy (%)")
    ax.set_title(f"{model_name}: Accuracy by Category")
    ax.set_xticks(positions)
    ax.set_xticklabels(cat_names, rotation=45, ha="right")
    ax.legend()
    ax.set_ylim(0, 105)

    for i, (ws, ns) in enumerate(zip(with_space_acc, no_space_acc)):
        ax.text(i - bar_width / 2, ws + 1, f"{ws:.0f}", ha="center", fontsize=8)
        ax.text(i + bar_width / 2, ns + 1, f"{ns:.0f}", ha="center", fontsize=8)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/accuracy_by_category.png", dpi=150)
    plt.close()


def plot_results_summary(results: list[BenchResult], model_name: str, output_dir: str):
    """Plot overall accuracy summary bar chart."""
    import os

    import matplotlib.pyplot as plt
    import numpy as np

    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 5))

    with_space_results = [r for r in results if r.prompt_type == "with_space"]
    no_space_results = [r for r in results if r.prompt_type == "no_space"]

    ws_correct = sum(1 for r in with_space_results if r.correct)
    ns_correct = sum(1 for r in no_space_results if r.correct)
    total = len(with_space_results)

    ws_acc = 100 * ws_correct / total
    ns_acc = 100 * ns_correct / total

    positions = np.arange(2)
    bar_width = 0.6

    bars = ax.bar(positions, [ws_acc, ns_acc], bar_width, color=["tab:blue", "tab:orange"])

    ax.set_ylabel("Accuracy (%)")
    ax.set_title(f"{model_name}: Emoji Identification Accuracy")
    ax.set_xticks(positions)
    ax.set_xticklabels(["With Space", "No Space"])
    ax.set_ylim(0, 105)

    for i, (acc, correct) in enumerate(zip([ws_acc, ns_acc], [ws_correct, ns_correct])):
        ax.text(i, acc + 1, f"{correct}/{total}\n({acc:.0f}%)", ha="center", fontsize=10)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/accuracy_summary.png", dpi=150)
    plt.close()


def generate_markdown_summary(results: list[BenchResult], model_name: str, output_dir: str):
    """Generate markdown tables summarizing results."""
    import os

    os.makedirs(output_dir, exist_ok=True)

    lines = []
    lines.append(f"# Emoji 'What Is' Benchmark Results - {model_name}\n")

    with_space_results = [r for r in results if r.prompt_type == "with_space"]
    no_space_results = [r for r in results if r.prompt_type == "no_space"]

    ws_correct = sum(1 for r in with_space_results if r.correct)
    ns_correct = sum(1 for r in no_space_results if r.correct)
    total = len(with_space_results)

    ws_pct = 100 * ws_correct / total
    ns_pct = 100 * ns_correct / total
    diff = ws_pct - ns_pct

    # Overall summary
    lines.append("## Overall Accuracy\n")
    lines.append("| Prompt Type | Correct | Accuracy |")
    lines.append("|-------------|---------|----------|")
    lines.append(f"| With Space | {ws_correct}/{total} | {ws_pct:.1f}% |")
    lines.append(f"| No Space | {ns_correct}/{total} | {ns_pct:.1f}% |")
    lines.append(f"| **Difference** | | **{diff:+.1f}%** |")
    lines.append("")

    # By category
    lines.append("## Accuracy by Category\n")
    lines.append("| Category | Count | With Space | No Space |")
    lines.append("|----------|-------|------------|----------|")

    for cat in Category:
        cat_items = [item for item in EMOJI_ITEMS if item.category == cat]
        if not cat_items:
            continue

        cat_with = [r for r in with_space_results if r.item.category == cat]
        cat_no = [r for r in no_space_results if r.item.category == cat]

        cat_ws_correct = sum(1 for r in cat_with if r.correct)
        cat_ns_correct = sum(1 for r in cat_no if r.correct)
        count = len(cat_items)

        cat_ws_pct = 100 * cat_ws_correct / count
        cat_ns_pct = 100 * cat_ns_correct / count

        lines.append(f"| {cat.value} | {count} | {cat_ws_correct}/{count} ({cat_ws_pct:.0f}%) | {cat_ns_correct}/{count} ({cat_ns_pct:.0f}%) |")

    lines.append("")

    # Wrong answers
    wrong_with = [r for r in with_space_results if not r.correct]
    wrong_no = [r for r in no_space_results if not r.correct]

    lines.append(f"## Wrong Answers - With Space ({len(wrong_with)} errors)\n")
    if wrong_with:
        lines.append("| Emoji | Expected | Got |")
        lines.append("|-------|----------|-----|")
        for r in wrong_with:
            lines.append(f"| {r.item.emoji} | {'/'.join(r.item.expected_answers)} | {r.first_word} |")
    lines.append("")

    lines.append(f"## Wrong Answers - No Space ({len(wrong_no)} errors)\n")
    if wrong_no:
        lines.append("| Emoji | Expected | Got |")
        lines.append("|-------|----------|-----|")
        for r in wrong_no:
            lines.append(f"| {r.item.emoji} | {'/'.join(r.item.expected_answers)} | {r.first_word} |")
    lines.append("")

    markdown = "\n".join(lines)
    with open(f"{output_dir}/results.md", "w") as f:
        f.write(markdown)

    return markdown


@app.function(image=image, volumes={VOLUME_PATH: volume}, timeout=600)
def save_results_and_plots(results_data: list[dict], model_name: str):
    """Save results, plots, and markdown summary to the volume."""
    import json
    import os

    output_dir = f"{VOLUME_PATH}/what_is_{model_name.lower()}"
    os.makedirs(output_dir, exist_ok=True)

    # Save raw results as JSON
    with open(f"{output_dir}/results.json", "w") as f:
        json.dump(results_data, f, indent=2)

    # Reconstruct BenchResult objects
    emoji_to_item = {item.emoji: item for item in EMOJI_ITEMS}
    results = []

    for rd in results_data:
        item = emoji_to_item.get(rd["emoji"])
        if not item:
            continue

        result = BenchResult(
            item=item,
            prompt_type=rd["prompt_type"],
            model_answer=rd["model_answer"],
            first_word=rd["first_word"],
            correct=rd["correct"],
            top_10=rd.get("top_10"),
        )
        results.append(result)

    # Generate plots
    plot_results_by_category(results, model_name, output_dir)
    plot_results_summary(results, model_name, output_dir)

    # Generate markdown
    markdown = generate_markdown_summary(results, model_name, output_dir)

    volume.commit()
    print(f"Saved results and plots to {output_dir}")
    print(markdown)


if __name__ == "__main__":
    main()
