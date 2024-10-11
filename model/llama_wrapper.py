import os
from dotenv import load_dotenv
import torch
from transformers import pipeline
from huggingface_hub import login
from model.model import Model
from src.logger_config import logger, COLOR_CODES, RESET


# load_dotenv()
# huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
# login(token=huggingface_token)

class LlamaWrapper(Model):
    def __init__(self, model_id = "meta-llama/Llama-3.2-1B-Instruct"):
        super().__init__(name="LlamaWrapper")
        self.model_id = model_id

    def predict(self, prompt, max_new_tokens=1024, stop=None):
        pipe = pipeline(
            "text-generation",
            model=self.model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        messages = [
            # {"role": "system", "content": "You are a Nekomusume chatbot who always responds in Nekomusume speak!"},
            {"role": "user", "content": prompt},
        ]
        try:
            outputs = pipe(
                messages,
                max_new_tokens=max_new_tokens,
                pad_token_id=pipe.tokenizer.eos_token_id,
                stop=stop,
            )
            response_text = outputs[0]["generated_text"][-1]['content']
        except Exception as e:
            # print(e)
            logger.error(f"Error: {COLOR_CODES['RED']}{e}{RESET}")
            
            exit(1)

        # with open("2.txt", "a") as f:
        #     f.write("\n-------------------------------------\n")
        #     f.write(prompt)
        #     f.write("\n")
        #     f.write(response_text)
        #     f.write("\n-------------------------------------\n")
        # print(prompt)
        # print(response_text)
        return response_text

def main():
    llama_wrapper = LlamaWrapper()
    prompt = "My name is Julien and I like to"
    response = llama_wrapper.predict(prompt)
    # print(response)

if __name__ == "__main__":
    main()