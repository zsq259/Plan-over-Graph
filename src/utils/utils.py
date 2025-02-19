import re
import json

def get_model(model_name):
    if "llama" in model_name.lower():
        from src.agent.model.llama_wrapper import LlamaWrapper
        return LlamaWrapper(model_name)
    elif "qwen" in model_name.lower():
        from src.agent.model.qwen_wrapper import QwenWrapper
        return QwenWrapper(model_name)
    else:
        from src.agent.model.gpt_wrapper import GPTWrapper
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

from collections import Counter

def compare_rule_sets(extracted, existing):
    def validate_structure(obj):
        if not isinstance(obj, dict):
            raise ValueError("input must be a dictionary")
        for key in ["initial_source", "target", "rules"]:
            if key not in obj:
                raise KeyError(f"missing key: {key}")
        if not all(isinstance(r, dict) for r in obj["rules"]):
            raise TypeError("rules must be a list of dictionaries")
    
    validate_structure(extracted)
    validate_structure(existing)

    # calculate similarity
    def list_similarity(a, b):
        """calculate Jaccard similarity between two lists"""
        counter_a = Counter(a)
        counter_b = Counter(b)
        common = counter_a & counter_b
        sum_common = sum(common.values())
        sum_total = sum((counter_a | counter_b).values())
        return sum_common / sum_total if sum_total != 0 else 1.0

    initial_source_sim = list_similarity(extracted["initial_source"], existing["initial_source"])

    target_sim = 1.0 if extracted["target"] == existing["target"] else 0.0

    def create_rule_signature(rules):
        for r in rules:
            if r["time"] == None:
                r["time"] = float("inf")
            if r["cost"] == None:
                r["cost"] = float("inf")
        return {
            (tuple(sorted(r["source"])), tuple(sorted(r["target"])), float(r["time"]), float(r["cost"]))
            for r in rules
        }
    
    extracted_signatures = create_rule_signature(extracted["rules"])
    existing_signatures = create_rule_signature(existing["rules"])

    common_rules = extracted_signatures & existing_signatures
    rules_common_count = len(common_rules)
    rules_total = len(extracted_signatures) + len(existing_signatures)
    rules_sim = (2 * rules_common_count) / rules_total if rules_total != 0 else 1.0

    # overall similarity score (average of the three)
    similarity_score = (initial_source_sim + target_sim + rules_sim) / 3

    is_identical = (
        sorted(extracted["initial_source"]) == sorted(existing["initial_source"]) 
        and extracted["target"] == existing["target"] 
        and len(extracted["rules"]) == len(existing["rules"]) 
        and extracted_signatures == existing_signatures
    )

    return (is_identical, similarity_score)