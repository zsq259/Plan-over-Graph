import re
import json

def get_model(model_name):
    if "llama" in model_name.lower():
        from model.llama_wrapper import LlamaWrapper
        return LlamaWrapper(model_name)
    elif "qwen" in model_name.lower():
        from model.qwen_wrapper import QwenWrapper
        return QwenWrapper(model_name)
    else:
        from model.gpt_wrapper import GPTWrapper
        return GPTWrapper(name=model_name)

def extract_json(text: str) -> dict:
    # json_regex = r'```json\s*\[\s*[\s\S]*?\s*\]\s*(?:```|\Z)'
    # json_regex = r'```json\s*[\{\[]\s*[\s\S]*?\s*[\}\]]\s*(?:```|\Z)'
    # json_regex = r'```json\s*(\{.*?\})\s*```'
    json_regex = f'```json\s*([\s\S]*?)\s*```'
    matches = re.findall(json_regex, text)
    # matches = re.findall(json_regex, text, re.DOTALL)
    # print(matches)
    if matches and len(matches) > 0:
        json_data = matches[0].replace('```json', '').replace('```', '').strip().replace('\'', '\"')
        try:
            parsed_json = json.loads(json_data)
            return parsed_json
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON data: {e}")
    else:
        text = text.replace("'", '"')
        try:
            parsed_json = json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON data: {e}")
        # print(parsed_json)
        if isinstance(parsed_json, list) or isinstance(parsed_json, dict):
            return parsed_json
        else:
            raise ValueError(f"No JSON data found in the string: \033[38;5;214m{text}\033[0m")
            
def normalize_rule(rule):
    return {
        "sources": tuple(sorted(rule["source"])),
        "targets": tuple(sorted(rule["target"])),
        "time": float(rule["time"]),
        "cost": float(rule["cost"])
    }

def compare_rule_sets(extracted, existing):
    def validate_structure(obj):
        if not isinstance(obj, dict):
            raise ValueError("输入必须是字典类型")
        for key in ["initial_source", "target", "rules"]:
            if key not in obj:
                raise KeyError(f"缺失必要字段: {key}")
        if not all(isinstance(r, dict) for r in obj["rules"]):
            raise TypeError("rules 必须由字典组成")
    
    validate_structure(extracted)
    validate_structure(existing)

    if sorted(extracted["initial_source"]) != sorted(existing["initial_source"]):
        return False
    
    if extracted["target"] != existing["target"]:
        return False
    
    if len(extracted["rules"]) != len(existing["rules"]):
        return False
    
    def create_rule_signature(rules):
        return {
            (tuple(sorted(r["source"])), tuple(sorted(r["target"])), float(r["time"]), float(r["cost"]))
            for r in rules
        }
    
    extracted_signatures = create_rule_signature(extracted["rules"])
    existing_signatures = create_rule_signature(existing["rules"])
    
    return extracted_signatures == existing_signatures