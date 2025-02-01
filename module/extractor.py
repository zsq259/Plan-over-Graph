from src.utils import extract_json
from src.logger_config import logger, COLOR_CODES, RESET
from template.extract_rules import instruction, example

class Extractor:
    def __init__(self, model):
        self.model = model
    
    def extract(self, task: str, max_retry=3) -> dict:
        while max_retry > 0:
            try:
                prompt = instruction.format(example=example, task=task).replace("\'", "\"")
                print(prompt)
                response = self.model.predict(prompt)
                print(response)
                rules = extract_json(response)
                return rules
            except ValueError as e:
                logger.info(f"Error extracting rules: {COLOR_CODES['RED']}{e}{RESET}")
                max_retry -= 1
            
        logger.info(f"Failed to extract rules after {COLOR_CODES['RED']}{max_retry}{RESET} attempts.")