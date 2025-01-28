import json, os
from model.gpt_wrapper import GPTWrapper
from model.llama_wrapper import LlamaWrapper
from module.extractor import Extractor
from src.utils import compare_rule_sets

def main():
    # model = GPTWrapper("deepseek-reasoner")
    model = LlamaWrapper("/data/share/data/llama-factory/LLaMA-Factory/saves/llama3-8b/lora/merged_model/sft_abstask_12000")
    extractor = Extractor(model)

    file_path = "data/dev/10-1-100-s_2.json"
    output_path = "data/result/llama-31-8b-instruct-sft23/10-1-100-s_2.json"
    data = json.load(open(file_path, "r"))

    results = []
    if os.path.exists(output_path):
        with open(output_path, "r") as f:
            results = json.load(f)
    
    exist_ids = set([r['id'] for r in results])
    
    for d in data:
        if d['id'] in exist_ids:
            continue
        task = d['story']
        try:
            rules = extractor.extract(task)
            d['model_rules'] = rules
            valid = compare_rule_sets(rules, d['question'])
            d['valid'] = valid
            results.append(d)
            with open(output_path, "w") as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error extracting rules for id {d['id']}: {e}")
            continue
            
if __name__ == "__main__":
    main()