import json
from model.llama_wrapper import LlamaWrapper
from module.planner import Planner
from template.extract_rules import instruction, example

def normalize_rule(rule):
    """增强的标准化函数，解决列表不可哈希问题"""
    return {
        # 将列表转换为元组确保可哈希
        "sources": tuple(sorted(rule["source"])),
        "targets": tuple(sorted(rule["target"])),
        "time": float(rule["time"]),
        "cost": float(rule["cost"])
    }

def compare_rule_sets(extracted, existing):
    """修复后的对比函数"""
    # 前置验证（新增）
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

    # 初始节点对比
    if sorted(extracted["initial_source"]) != sorted(existing["initial_source"]):
        return False
    
    # 最终节点对比
    if extracted["target"] != existing["target"]:
        return False
    
    # 规则数量对比
    if len(extracted["rules"]) != len(existing["rules"]):
        return False
    
    # 创建可哈希规则表示（修复关键错误点）
    def create_rule_signature(rules):
        return {
            (tuple(sorted(r["source"])), tuple(sorted(r["target"])), float(r["time"]), float(r["cost"]))
            for r in rules
        }
    
    extracted_signatures = create_rule_signature(extracted["rules"])
    existing_signatures = create_rule_signature(existing["rules"])
    
    return extracted_signatures == existing_signatures

def main():
    model = "/data/share/data/llama-factory/LLaMA-Factory/Meta-Llama-3.1-8B-Instruct"
    model = LlamaWrapper(model)

    file_path = "/data/share/data/llama-factory/test/data/dev/10-1-100-s-filtered.json"
    data = json.load(open(file_path, "r"))

    planner = Planner()

    for d in data:
        task = d['story']
        prompt = instruction.format(example=example, task=task).replace("\'", "\"")
        # print(prompt)
        # response = model.predict(prompt)
        response = """
        
        {
            "rules": [
                {
                    "id": 0,
                    "source": [
                        "N1"
                    ],
                    "target": [
                        "N2"
                    ],
                    "time": 12,
                    "cost": 1
                },
                {
                    "id": 1,
                    "source": [
                        "N1",
                        "N2"
                    ],
                    "target": [
                        "N3"
                    ],
                    "time": 28,
                    "cost": 1
                },
                {
                    "id": 2,
                    "source": [
                        "N2",
                        "N1"
                    ],
                    "target": [
                        "N4"
                    ],
                    "time": 3,
                    "cost": 1
                },
                {
                    "id": 3,
                    "source": [
                        "N3"
                    ],
                    "target": [
                        "N4"
                    ],
                    "time": 14,
                    "cost": 1
                },
                {
                    "id": 4,
                    "source": [
                        "N1",
                        "N4"
                    ],
                    "target": [
                        "N5"
                    ],
                    "time": 12,
                    "cost": 1
                },
                {
                    "id": 5,
                    "source": [
                        "N2",
                        "N5",
                        "N3"
                    ],
                    "target": [
                        "N6"
                    ],
                    "time": 18,
                    "cost": 1
                },
                {
                    "id": 6,
                    "source": [
                        "N3",
                        "N6"
                    ],
                    "target": [
                        "N7"
                    ],
                    "time": 49,
                    "cost": 1
                },
                {
                    "id": 7,
                    "source": [
                        "N2",
                        "N5"
                    ],
                    "target": [
                        "N7"
                    ],
                    "time": 39,
                    "cost": 1
                },
                {
                    "id": 8,
                    "source": [
                        "N7"
                    ],
                    "target": [
                        "N8"
                    ],
                    "time": 49,
                    "cost": 1
                },
                {
                    "id": 9,
                    "source": [
                        "N5"
                    ],
                    "target": [
                        "N8"
                    ],
                    "time": 34,
                    "cost": 1
                },
                {
                    "id": 10,
                    "source": [
                        "N1"
                    ],
                    "target": [
                        "N8"
                    ],
                    "time": 42,
                    "cost": 1
                },
                {
                    "id": 11,
                    "source": [
                        "N2"
                    ],
                    "target": [
                        "N8"
                    ],
                    "time": 20,
                    "cost": 1
                },
                {
                    "id": 12,
                    "source": [
                        "N1",
                        "N7"
                    ],
                    "target": [
                        "N9"
                    ],
                    "time": 34,
                    "cost": 1
                },
                {
                    "id": 13,
                    "source": [
                        "N4",
                        "N3"
                    ],
                    "target": [
                        "N9"
                    ],
                    "time": 24,
                    "cost": 1
                }
            ],
            "initial_source": [
                "N1"
            ],
            "target": "N8"
        }
        """
        # print(response)
        rules = planner.extract_json(response)
        print(rules)
        print(compare_rule_sets(rules, d['question']))
        break

if __name__ == "__main__":
    main()