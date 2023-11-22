from transformers import AutoTokenizer
import os

tokenizer = AutoTokenizer.from_pretrained("./tokenizer", trust_remote_code=True, use_fast=False)

path_name = "./pure_text_data"

all_tokens = 0
for file_name in os.listdir(path_name):
    full_name = os.path.join(path_name,file_name)
    with open(full_name,"r",encoding="utf-8") as f:
        s = "".join(f.readlines())
    token_num = len(tokenizer.encode(s))
    print(f"{file_name}:{token_num}")
    all_tokens+=token_num

print(f"all_tokens:{all_tokens}")
