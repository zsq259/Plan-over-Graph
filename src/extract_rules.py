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
        # task = d['story']
        task = """
        In a large-scale space exploration initiative, multiple agencies collaborate to establish the "Mars Colony(N10)" efficiently. The project begins with four key missions: "Launch Pad Construction(N1)," "Satellite Deployment(N2)," "Lunar Base Setup(N6)," and "Orbital Station Assembly(N7)." The "Launch Pad(N1)" requires 34 days and costs 1 to develop the "Rocket System(N3)," which then takes 15 days and costs 1 to enable the "Communication Network(N4)." Meanwhile, the "Satellite Deployment(N2)" can establish the "Communication Network(N4)" in 6 days at a cost of 1, or deploy a "Deep Space Probe(N5)" in 17 days at a cost of 1. The "Orbital Station(N7)" prepares astronauts for the "Crew Training Program(N8)" in 31 days and at a cost of 1, while the "Lunar Base(N6)" contributes data to the same program in 44 days and at a cost of 1. Once trained, the "Crew Program(N8)" launches the "Mars Expedition(N9)" in 39 days and at a cost of 1. The "Deep Space Probe(N5)" bypasses crew requirements and directly initiates the "Mars Expedition(N9)" in 16 days at a cost of 1. The expedition then establishes the "Mars Colony(N10)" in 14 days and at a cost of 1. Alternatively, the fully operational "Communication Network(N4)" skips interplanetary missions and directly finalizes the colony in 15 days at a cost of 1. Teams prioritize pathways based on timelines and resource availability to achieve the goal.
        """
        prompt = instruction.format(example=example, task=task).replace("\'", "\"")
        print(prompt)
        response = model.predict(prompt)
        print(response)
        break
        rules = planner.extract_json(response)
        print(rules)
        print(compare_rule_sets(rules, d['question']))
        break

if __name__ == "__main__":
    main()