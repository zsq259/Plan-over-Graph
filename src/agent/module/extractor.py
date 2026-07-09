import json
from src.utils.utils import extract_json
from src.utils.logger_config import logger, COLOR_CODES, RESET
from template.extract_rules import instruction, example
from template.validate_extraction import get_validation_prompt

class Extractor:
    def __init__(self, model, validation_iterations=0):
        self.model = model
        self.validation_iterations = validation_iterations
        self.iteration_count = 0
        self.extraction_history = []
    
    def extract(self, task: str, max_retry=3) -> dict:
        rules = self._extract_rules(task, max_retry)
        if rules and self.validation_iterations > 0:
            rules = self._validate_and_refine(task, rules)
        return rules
    
    def _extract_rules(self, task: str, max_retry: int) -> dict:
        """Initial rule extraction."""
        retry_count = 0
        while retry_count < max_retry:
            try:
                prompt = instruction.format(example=example, task=task).replace("\'", "\"")
                response = self.model.predict(prompt)
                rules = extract_json(response)
                self.iteration_count = 1
                self.extraction_history.append({"iteration": 0, "rules": rules, "type": "initial_extraction"})
                return rules
            except ValueError as e:
                logger.info(f"Error extracting rules: {COLOR_CODES['RED']}{e}{RESET}")
                retry_count += 1
        
        logger.info(f"Failed to extract rules after {COLOR_CODES['RED']}{max_retry}{RESET} attempts.")
        return None
    
    def _validate_and_refine(self, original_task: str, extracted_rules: dict) -> dict:
        """Validate extracted rules and refine through feedback loop."""
        current_rules = extracted_rules
        
        for iteration in range(self.validation_iterations):
            try:
                extracted_json_str = json.dumps(current_rules, indent=2, ensure_ascii=False)
                validation_prompt = get_validation_prompt(original_task, extracted_json_str)
                validation_prompt = validation_prompt.replace("\'", "\"")
                
                validation_response = self.model.predict(validation_prompt)
                validation_result = extract_json(validation_response)
                
                is_valid = validation_result.get("is_valid", False)
                issues = validation_result.get("issues", [])
                
                if is_valid or not issues:
                    break
                
                if validation_result.get("corrected_rules"):
                    corrected = validation_result["corrected_rules"]
                    if isinstance(corrected, str):
                        corrected = json.loads(corrected)
                    current_rules = corrected
                    self.extraction_history.append({"iteration": iteration + 1, "rules": corrected, "type": "validation_correction"})
                    self.iteration_count += 1
            except Exception as e:
                logger.info(f"Validation iteration {iteration+1} failed: {e}")
                break
        
        return current_rules