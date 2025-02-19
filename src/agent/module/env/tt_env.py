import json
from typing import List, Dict, Set
from src.agent.module.subtask import SubTTNode

class TTEnv:
    def __init__(self, config: dict | str | None):
        if config is None:
            config = {}
        if isinstance(config, str):
            config = json.loads(config)
        self.rules = config.get("rules", [])
        self.initial_sources = config.get("initial_source", [])
        self.available_materials: Set[str] = set(self.initial_sources)
        self.synthesized_materials: Set[str] = set()
        self.target = config.get("target", "")
        self.material_earliest_time: Dict[str, int] = {material: 0 for material in self.initial_sources}
        self.total_cost = 0
        self.log = ""
    
    def reset(self):
        self.available_materials = set(self.initial_sources)
        self.synthesized_materials = set()
        self.material_earliest_time = {material: 0 for material in self.initial_sources}
        self.total_cost = 0
        self.log = ""
    
    def is_valid_sub_node(self, sub_node: SubTTNode) -> bool:
        if sub_node.perform_rule_indx is not None:
            sub_node.time = self.rules[sub_node.perform_rule_indx].get("time", 0)
            sub_node.cost = self.rules[sub_node.perform_rule_indx].get("cost", 0)
            return True
        for rule in self.rules:
            if sorted(rule["target"]) == sorted(sub_node.target):
                if sorted(rule["source"]) == sorted(sub_node.source):
                    sub_node.time = rule.get("time", 0)
                    sub_node.cost = rule.get("cost", 0)
                    return True
        return False
    
    def commit(self, sub_node: SubTTNode):
        if sub_node.source is None or sub_node.target is None:
            sub_node.source = self.rules[sub_node.perform_rule_indx]["source"]
            sub_node.target = self.rules[sub_node.perform_rule_indx]["target"]
            
        if not self.is_valid_sub_node(sub_node):            
            raise ValueError(f"Reaction {sub_node.name} does not match any rule.")
        
        for material in sub_node.source:
            if material not in self.available_materials:                
                raise ValueError(f"Running {sub_node.name}: Source material {material} is not available.")
        
        self.available_materials.update(sub_node.target)
        self.synthesized_materials.update(sub_node.target)
        
        current_time = 0
        for source in sub_node.source:
            current_time = max(current_time, self.material_earliest_time[source])
        current_time += sub_node.time
        
        for target in sub_node.target:
            if target not in self.material_earliest_time:
                self.material_earliest_time[target] = current_time
            else:
                self.material_earliest_time[target] = min(self.material_earliest_time[target], current_time)
        
        self.total_cost += sub_node.cost
        
        self.log += f"{sub_node.name} successfully committed. Time: {sub_node.time}, Current time: {current_time}\n"
        print(f"{sub_node.name} successfully committed. Time: {sub_node.time}, Current time: {current_time}")        
        return current_time
    
    def get_available_materials(self) -> Set[str]:
        return self.available_materials.copy()

    def get_final_result(self) -> int:
        return self.material_earliest_time.get(self.target, None), self.total_cost

if __name__ == "__main__":
    config_json = '''
    {
        "rules": [
            {
                "source": [
                    "N1"
                ],
                "target": [
                    "N2"
                ],
                "time": 4
            },
            {
                "source": [
                    "N1"
                ],
                "target": [
                    "N3"
                ],
                "time": 2
            },
            {
                "source": [
                    "N2"
                ],
                "target": [
                    "N3"
                ],
                "time": 4
            },
            {
                "source": [
                    "N1"
                ],
                "target": [
                    "N4"
                ],
                "time": 3
            },
            {
                "source": [
                    "N2"
                ],
                "target": [
                    "N4"
                ],
                "time": 2
            },
            {
                "source": [
                    "N3"
                ],
                "target": [
                    "N4"
                ],
                "time": 4
            },
            {
                "source": [
                    "N4"
                ],
                "target": [
                    "N5"
                ],
                "time": 2
            },
            {
                "source": [
                    "N3"
                ],
                "target": [
                    "N5"
                ],
                "time": 4
            },
            {
                "source": [
                    "N1"
                ],
                "target": [
                    "N6"
                ],
                "time": 1
            },
            {
                "source": [
                    "N4"
                ],
                "target": [
                    "N6"
                ],
                "time": 5
            },
            {
                "source": [
                    "N3"
                ],
                "target": [
                    "N6"
                ],
                "time": 2
            },
            {
                "source": [
                    "N2",
                    "N3",
                    "N5"
                ],
                "target": [
                    "N7"
                ],
                "time": 5
            },
            {
                "source": [
                    "N4"
                ],
                "target": [
                    "N7"
                ],
                "time": 2
            },
            {
                "source": [
                    "N3"
                ],
                "target": [
                    "N8"
                ],
                "time": 4
            },
            {
                "source": [
                    "N2"
                ],
                "target": [
                    "N8"
                ],
                "time": 2
            },
            {
                "source": [
                    "N7"
                ],
                "target": [
                    "N8"
                ],
                "time": 4
            },
            {
                "source": [
                    "N1"
                ],
                "target": [
                    "N8"
                ],
                "time": 4
            },
            {
                "source": [
                    "N6"
                ],
                "target": [
                    "N8"
                ],
                "time": 1
            },
            {
                "source": [
                    "N5"
                ],
                "target": [
                    "N8"
                ],
                "time": 5
            },
            {
                "source": [
                    "N4"
                ],
                "target": [
                    "N8"
                ],
                "time": 5
            },
            {
                "source": [
                    "N4",
                    "N7"
                ],
                "target": [
                    "N9"
                ],
                "time": 4
            },
            {
                "source": [
                    "N5",
                    "N3"
                ],
                "target": [
                    "N9"
                ],
                "time": 2
            },
            {
                "source": [
                    "N1"
                ],
                "target": [
                    "N10"
                ],
                "time": 3
            },
            {
                "source": [
                    "N3"
                ],
                "target": [
                    "N10"
                ],
                "time": 1
            },
            {
                "source": [
                    "N2"
                ],
                "target": [
                    "N10"
                ],
                "time": 1
            },
            {
                "source": [
                    "N8"
                ],
                "target": [
                    "N10"
                ],
                "time": 3
            }
        ],
        "initial_source": [
            "N1"
        ],
        "target": "N10"
    }
    '''
        
    env = TTEnv(config_json)
    
    print("initial_sources:", env.initial_sources)    
    
    tasks = """
    [{"name": "Subtask1", "source": ["N1"], "target": "N2", "dependencies": []}]
    """
 
    subtasks = json.loads(tasks)
    for task in subtasks:
        subtask = SubTTNode(task)
        print(f"Subtask {subtask.name} is valid: {env.is_valid_sub_node(subtask)}")
    