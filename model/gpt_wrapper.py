import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from model.model import Model

class GPTWrapper(Model):
    def __init__(self, name=None, base_url=None, api_key=None):
        super().__init__(name=name)
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai_base_url = os.getenv("OPENAI_BASE_URL")
        self.client = OpenAI(base_url=openai_base_url, api_key=openai_api_key)
    
    def predict(self, prompt, stop=None, max_tokens = 1024):
        try:
            response = self.client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                temperature=0,
                max_tokens=max_tokens,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=stop
            )
        except OpenAIError as e:
            return "An error occurred while processing the request."
        except Exception as e:
            return "An unexpected error occurred."
        # print("-------------------------------------")
        # print("\033[93m" + prompt + "\033[0m")
        # print("response:\n")
        # print(response)
        # print("text:\n")
        # print("\033[92m" + response.choices[0].text + "\033[0m")
        # print("-------------------------------------")
        return response.choices[0].text