import os
from dotenv import load_dotenv
from openai import OpenAI
from model.model import Model

class GPTWrapper(Model):
    def __init__(self, name=None, base_url=None, api_key=None):
        super().__init__(name=name)
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai_base_url = os.getenv("OPENAI_BASE_URL")
        self.client = OpenAI(base_url=openai_base_url, api_key=openai_api_key)
    
    def predict(self, prompt, stop=["\n"]):
        response = self.client.completions.create(model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=stop)
        # print(prompt)
        return response.choices[0].text
    
    def step(self, prompt, stop=["\n"]):
        result = self.predict(prompt, stop)
        thought, actions = self.get_actions(result)
        actions = self.find_actions(actions)
        return thought, actions