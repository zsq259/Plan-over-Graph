import os, copy
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from model.model import Model
from src.logger_config import logger, COLOR_CODES, RESET

class GPTWrapper(Model):
    def __init__(self, name=None):
        super().__init__(name=name)
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai_base_url = os.getenv("OPENAI_BASE_URL")
        self.openai_api_key = openai_api_key
        self.openai_base_url = openai_base_url
        
    def predict(self, prompt, stop=None, max_tokens = 1024):
        try:
            client = OpenAI(base_url=self.openai_base_url, api_key=self.openai_api_key)
            response = client.completions.create(
                model=self.name,
                prompt=prompt,
                temperature=0,
                max_tokens=max_tokens,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=stop
            )
        except OpenAIError as e:
            logger.error(f"Error: {COLOR_CODES['RED']}{e}{RESET}")
            exit(1)
        except Exception as e:
            logger.error(f"Error: {COLOR_CODES['RED']}{e}{RESET}")
            exit(1)
        with open("2.txt", "a") as f:
            f.write("\n-------------------------------------\n")
            f.write(prompt)
            f.write("\n")
            f.write(response.choices[0].text)
            f.write("\n-------------------------------------\n")
        return response.choices[0].text