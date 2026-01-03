import modal

app = modal.App("qwen3-inference")

MODEL_ID = "Qwen/Qwen3-4B-Base"


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
    def generate_stream(self, messages: str):
        import torch

        prompt = messages
        inputs = self.tokenizer([prompt], return_tensors="pt").to(self.model.device)

        # Print input tokenization
        input_token_ids = inputs["input_ids"][0].tolist()
        print("=" * 80)
        print("INPUT TOKENIZATION:")
        print("=" * 80)
        for token_id in input_token_ids:
            token_str = self.tokenizer.decode([token_id])
            token_bytes = token_str.encode("utf-8").hex()
            print(
                f"Token ID: {token_id:5d} | Bytes: {token_bytes:30s} | Text: {repr(token_str)}"
            )
        print("-" * 80)

        # Generate tokens one by one to access logits
        generated_ids = inputs["input_ids"][0].tolist()
        output_tokens = []

        print("\n" + "=" * 80)
        print("OUTPUT TOKENIZATION WITH LOGIT DISTRIBUTIONS:")
        print("=" * 80)

        for step in range(2000):
            with torch.no_grad():
                outputs = self.model(
                    input_ids=torch.tensor([generated_ids]).to(self.model.device)
                )
                logits = outputs.logits[0, -1, :]  # Last position logits

                # Get top 10 predictions by logit value
                top_logits, top_indices = torch.topk(logits, k=10)

                # Compute probabilities
                probs = torch.softmax(logits, dim=-1)
                top_probs = probs[top_indices]

                # Greedy selection
                next_token_id = top_indices[0].item()
                next_token = self.tokenizer.decode([next_token_id])
                next_token_bytes = next_token.encode("utf-8").hex()

                print(
                    f"\nToken ID: {next_token_id:5d} | Bytes: {next_token_bytes:30s} | Text: {repr(next_token)}"
                )
                print(f"  Top 10 alternatives:")
                for logit, prob, idx in zip(
                    top_logits.tolist(), top_probs.tolist(), top_indices.tolist()
                ):
                    token_str = self.tokenizer.decode([idx])
                    print(
                        f"    {idx:5d} ({repr(token_str):20s}): logit={logit:8.4f}  prob={prob:.4f}"
                    )

                generated_ids.append(next_token_id)
                output_tokens.append(next_token)
                yield next_token

                # Check for end of generation
                if next_token_id == self.tokenizer.eos_token_id:
                    break

        print("-" * 80)


@app.local_entrypoint()
def main():
    model = Qwen3Model()
    prompts = [
f"""Is there an official octopus emoji in Unicode?""",
    ]
    for prompt in prompts:
        syn = ""
        print(f"""{prompt}""", end="")
        print("\n" + "-" * 50 + "\n")
        for token in model.generate_stream.remote_gen(prompt):
            print(token)
            syn += token
        print(syn)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
