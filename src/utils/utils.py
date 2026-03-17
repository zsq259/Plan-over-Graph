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
    json_regex = f'```json\s*([\s\S]*?)\s*```'
    matches = re.findall(json_regex, text)
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

    # Initial condition F1
    ext_src = Counter(extracted["initial_source"])
    exist_src = Counter(existing["initial_source"])
    tp_src = sum((ext_src & exist_src).values())
    fp_src = sum((ext_src - exist_src).values())
    fn_src = sum((exist_src - ext_src).values())

    precision_src = tp_src / (tp_src + fp_src) if (tp_src + fp_src) > 0 else 1.0
    recall_src    = tp_src / (tp_src + fn_src) if (tp_src + fn_src) > 0 else 1.0
    f1_src        = (2 * precision_src * recall_src / (precision_src + recall_src)
                     if (precision_src + recall_src) > 0 else 0.0)

    # Target accuracy
    accuracy_tgt = 1.0 if extracted["target"] == existing["target"] else 0.0

    # Rule signature generation
    def create_rule_signatures(rules):
        sigs = []
        for r in rules:
            t = float("inf") if r.get("time") is None else float(r["time"])
            c = float("inf") if r.get("cost") is None else float(r["cost"])
            src_tup = tuple(sorted(r["source"]))
            tgt_tup = tuple(sorted(r["target"]))
            sigs.append((src_tup, tgt_tup, t, c))
        return set(sigs)

    ext_rules = create_rule_signatures(extracted["rules"])
    exist_rules = create_rule_signatures(existing["rules"])
    tp_rule = len(ext_rules & exist_rules)
    fp_rule = len(ext_rules - exist_rules)
    fn_rule = len(exist_rules - ext_rules)

    precision_rule = tp_rule / (tp_rule + fp_rule) if (tp_rule + fp_rule) > 0 else 1.0
    recall_rule    = tp_rule / (tp_rule + fn_rule) if (tp_rule + fn_rule) > 0 else 1.0
    f1_rule        = (2 * precision_rule * recall_rule / (precision_rule + recall_rule)
                      if (precision_rule + recall_rule) > 0 else 0.0)

    # Overall similarity and exact-match check
    similarity_score = (f1_src + accuracy_tgt + f1_rule) / 3
    is_identical = (f1_src == 1.0 and accuracy_tgt == 1.0 and f1_rule == 1.0)

    return is_identical, similarity_score
