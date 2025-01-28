import os, time
from openai import OpenAI, OpenAIError
from model.model import Model
from src.logger_config import logger, COLOR_CODES, RESET

class GPTWrapper(Model):
    def __init__(self, name=None):
        super().__init__(name=name)
        if "deepseek" in name.lower():
            self.openai_api_key = os.environ.get("DEEPSEEK_API_KEY")
            self.openai_base_url = os.environ.get("DEEPSEEK_BASE_URL")
            self.is_chat_model = True
        elif "claude" in name.lower():
            self.openai_api_key = os.environ.get("CLAUDE_API_KEY")
            self.openai_base_url = os.environ.get("CLAUDE_BASE_URL")
            self.is_chat_model = True
        else:
            self.openai_api_key = os.environ.get("OPENAI_API_KEY")
            self.openai_base_url = os.environ.get("OPENAI_BASE_URL")
            self.is_chat_model = True
        
    def chat_create(self, client, prompt, stop=None, max_tokens = 1024):
        response = client.chat.completions.create(
                    model=self.name,                    
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
    
def main():
    from template.specific_task import instruction, example_task
    task = """{'rules': [{'id': 0, 'source': ['N1'], 'target': ['N2'], 'time': 41, 'cost': 1}, {'id': 1, 'source': ['N2'], 'target': ['N3'], 'time': 25, 'cost': 1}, {'id': 2, 'source': ['N3', 'N1'], 'target': ['N4'], 'time': 13, 'cost': 1}, {'id': 3, 'source': ['N2'], 'target': ['N4'], 'time': 22, 'cost': 1}, {'id': 4, 'source': ['N4', 'N1', 'N2'], 'target': ['N5'], 'time': 19, 'cost': 1}, {'id': 5, 'source': ['N1'], 'target': ['N6'], 'time': 13, 'cost': 1}, {'id': 6, 'source': ['N4'], 'target': ['N6'], 'time': 16, 'cost': 1}, {'id': 7, 'source': ['N5'], 'target': ['N6'], 'time': 9, 'cost': 1}, {'id': 8, 'source': ['N3', 'N5'], 'target': ['N7'], 'time': 10, 'cost': 1}, {'id': 9, 'source': ['N1'], 'target': ['N7'], 'time': 5, 'cost': 1}, {'id': 10, 'source': ['N6', 'N3'], 'target': ['N8'], 'time': 10, 'cost': 1}, {'id': 11, 'source': ['N6'], 'target': ['N9'], 'time': 29, 'cost': 1}, {'id': 12, 'source': ['N3'], 'target': ['N9'], 'time': 10, 'cost': 1}, {'id': 13, 'source': ['N5'], 'target': ['N9'], 'time': 48, 'cost': 1}, {'id': 14, 'source': ['N8'], 'target': ['N9'], 'time': 17, 'cost': 1}, {'id': 15, 'source': ['N2', 'N3', 'N5'], 'target': ['N10'], 'time': 8, 'cost': 1}, {'id': 16, 'source': ['N6', 'N4', 'N9'], 'target': ['N10'], 'time': 24, 'cost': 1}], 'initial_source': ['N1'], 'target': 'N10'}"""
    model = GPTWrapper(name="claude-3-5-sonnet-20241022")
    prompt = instruction.format(task=task, example_task=example_task)
    response = model.predict(prompt)
    print(response)

if __name__ == "__main__":
    main()