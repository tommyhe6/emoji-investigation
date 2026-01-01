from tokenizers import Tokenizer
from tokenizers.models import BPE


MODEL_ID = "Qwen/Qwen3-4B-Instruct-2507"

tokenizer = Tokenizer.from_pretrained(MODEL_ID)
model = tokenizer.model
a = model.id_to_token(11162)
print(a.encode())
