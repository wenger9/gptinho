import torch
from instruct_pipeline import InstructionTextGenerationPipeline
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("databricks/dolly-v2-3b", padding_side="left")
model = AutoModelForCausalLM.from_pretrained("databricks/dolly-v2-3b", device_map="auto", torch_dtype=torch.bfloat16)
print("model and token loaded")
generate_text = InstructionTextGenerationPipeline(model=model, tokenizer=tokenizer)
print("model initialized")

res = generate_text("Explain to me the difference between nuclear fission and fusion.")
print(res[0]["generated_text"])
