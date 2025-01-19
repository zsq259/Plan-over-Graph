import os, time
# from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from model.model import Model
from src.logger_config import logger, COLOR_CODES, RESET

class GPTWrapper(Model):
    def __init__(self, name=None):
        super().__init__(name=name)
        # load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai_base_url = os.getenv("OPENAI_BASE_URL")
        self.openai_api_key = openai_api_key
        self.openai_base_url = openai_base_url
        self.is_chat_model = False
        
    def chat_create(self, client, prompt, stop=None, max_tokens = 1024):
        response = client.chat.completions.create(
                    model=self.name,
                    # prompt=prompt,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=max_tokens,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    stop=stop
                )
        return response.choices[0].message.content
    
    def create(self, client, prompt, stop=None, max_tokens = 1024):
        response = client.completions.create(
                    model=self.name,
                    prompt=prompt,
                    temperature=0.2,
                    max_tokens=max_tokens,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    stop=stop
                )
        return response.choices[0].text
    
    def predict(self, prompt, stop=None, max_tokens = 1024, retries=3, delay=2):
        attempt = 0
        while attempt < retries:
            try:
                client = OpenAI(base_url=self.openai_base_url, api_key=self.openai_api_key)
                if self.is_chat_model:
                    response = self.chat_create(client, prompt, stop=stop, max_tokens=max_tokens)
                    break
                else :
                    response = self.create(client, prompt, stop=stop, max_tokens=max_tokens)
                    break
            except OpenAIError as e:
                logger.error(f"Error: {COLOR_CODES['RED']}{e}{RESET}")
                attempt += 1
                if attempt < retries:
                    logger.info(f"Retrying in {delay} seconds.")
                    time.sleep(delay)
                else:
                    logger.error(f"All {retries} attempts failed.")
                    exit(1)
            except Exception as e:
                logger.error(f"Unexpected error: {COLOR_CODES['RED']}{e}{RESET}")
                exit(1)
        with open("2.txt", "a") as f:
            f.write("\n-------------------------------------\n")
            f.write(prompt)
            f.write("\n")
            f.write(response)
            f.write("\n-------------------------------------\n")
        return response