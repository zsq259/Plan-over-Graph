from transformers import AutoModelForCausalLM, AutoTokenizer
from model.model import Model
from src.logger_config import logger, COLOR_CODES, RESET

class QwenWrapper(Model):
    def __init__(self, model_id="Qwen/Qwen2.5-7B-Instruct", system_message=None):
        super().__init__(name="QwenWrapper")
        self.model_id = model_id
        self.system_message = system_message or "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            torch_dtype="auto",
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)

    def predict(self, prompt, max_new_tokens=8192, temperature=0.2, top_p=0.9, stop=None):
        messages = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": prompt}
        ]
        
        try:
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                pad_token_id=self.tokenizer.eos_token_id
            )
            generated_ids = generated_ids[:, model_inputs.input_ids.shape[1]:]
            response = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            self._log_interaction(prompt, response)
            return response
        
        except Exception as e:
            error_msg = f"{COLOR_CODES['RED']}生成错误: {str(e)}{RESET}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def _log_interaction(self, prompt, response):
        with open("5.txt", "a", encoding="utf-8") as f:
            f.write("\nstart:-------------------------------------\n")
            f.write(f"Input:\n{prompt}\n")
            f.write(f"Response:\n{response}\n")
            f.write("end:-------------------------------------\n")

def main():
    qwen = QwenWrapper()
    prompt = "Explain quantum computing in simple terms"
    response = qwen.predict(
        prompt,
        max_new_tokens=1024,
        temperature=0.7,
        top_p=0.95
    )
    print("用户输入:", prompt)
    print("模型响应:", response)

if __name__ == "__main__":
    main()