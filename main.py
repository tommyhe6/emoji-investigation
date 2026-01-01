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
    def generate_stream(self, messages: list[dict]):
        import threading

        from transformers import TextIteratorStreamer

        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self.tokenizer([prompt], return_tensors="pt")

        # Debug: print tokenization breakdown
        # token_ids = inputs['input_ids'][0].tolist()
        # print("Tokenization breakdown:")
        # for token_id in token_ids:
        #     token_str = self.tokenizer.decode([token_id])
        #     token_bytes = token_str.encode('utf-8').hex()
        #     print(f"Token ID: {token_id:5d} | Bytes: {token_bytes:20s} | Text: {repr(token_str)}")
        # print("-" * 80)

        inputs = inputs.to(self.model.device)

        streamer = TextIteratorStreamer(
            self.tokenizer, skip_prompt=True, skip_special_tokens=False
        )

        generation_kwargs = {
            **inputs,
            "max_new_tokens": 2000,
            "streamer": streamer,
            "do_sample": False,
        }

        thread = threading.Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        for token in streamer:
            yield token

        thread.join()


items = [
    "seahorse",  # ❌ real animal, no emoji
    "axolotl",  # ❌ real animal, no emoji
    "platypus",  # ❌ real animal, no emoji
    "narwhal",  # ❌ real animal, no emoji
    "pangolin",  # ❌ real animal, no emoji
    "tapir",  # ❌ real animal, no emoji
    "quokka",  # ❌ real animal, no emoji
    "capybara",  # ❌ real animal, no emoji: # 7
    "fennec fox",  # ❌ real animal, no emoji
    "meerkat",  # ❌ real animal, no emoji
    "wombat",  # ❌ real animal, no emoji
    "opossum",  # ❌ real animal, no emoji
    "armadillo",  # ❌ real animal, no emoji # 12
    "anteater",  # ❌ real animal, no emoji
    "lemur",  # ❌ real animal, no emoji
    "jackal",  # ❌ real animal, no emoji
    "hyena",  # ❌ real animal, no emoji
    "warthog",  # ❌ real animal, no emoji
    "ibex",  # ❌ real animal, no emoji
    "gazelle",  # ❌ real animal, no emoji
    "chinchilla",  # ❌ real animal, no emoji
    "ferret",  # ❌ real animal, no emoji
    "marmot",  # ❌ real animal, no emoji
    "pika",  # ❌ real animal, no emoji
    "vole",  # ❌ real animal, no emoji
    "swordfish",  # ❌ real animal, no emoji
    "phoenix",  # ❌ mythical, no emoji
    "griffin",  # ❌ mythical, no emoji
    "centaur",  # ❌ mythical, no emoji
    "hydra",  # ❌ mythical, no emoji
    "basilisk",  # ❌ mythical, no emoji
    "octopus",  # REAL
    "snail",  # REAL
    "table",  # ❌ real object, no emoji
    "refrigerator",  # ❌ real object, no emoji
]


@app.local_entrypoint()
def main():
    model = Qwen3Model()
    ITEM = "refrigerator"
    prompts = [
        [
            {
                "role": "user",
                "content": f"Is there an official {ITEM} emoji in Unicode?",
            },
        ],
        [
            {
                "role": "user",
                "content": f"Is there a {ITEM} emoji?",
            },
        ],
        #
        [
            {
                "role": "user",
                "content": f"Show me just the {ITEM} emoji? Only return an emoji nothing else.",
            },
        ],
        [
            {
                "role": "user",
                "content": f"""Show me just the {ITEM} emoji? Only return an emoji if it exists, or else "None".""",
            },
        ],
        #
        [
            {
                "role": "user",
                "content": f"What is the {ITEM} emoji?",
            },
        ],
        [
            {
                "role": "user",
                "content": f"What does the {ITEM} emoji look like?",
            },
        ],
    ]
    for messages in prompts:
        syn = ""
        print(f"""{messages[0]["content"]}""", end="")
        print("\n" + "-" * 50 + "\n")
        for token in model.generate_stream.remote_gen(messages):
            syn += token
        print(syn)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
