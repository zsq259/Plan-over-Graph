import json
from typing import List, Dict, Set
from module.subtask import SubTTNode

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
    
    def is_valid_sub_node(self, sub_node: SubTTNode) -> bool:
        for rule in self.rules:
            if sorted(rule["target"]) == sorted(sub_node.target):
                if sorted(rule["source"]) == sorted(sub_node.source):
                    sub_node.time = rule.get("time", 0)
                    sub_node.cost = rule.get("cost", 0)
                    return True
        return False
    
    def commit(self, sub_node: SubTTNode):
        """
        提交一个反应，检查其合法性并更新环境。

        :param sub_node: 一个 SubTTNode 对象，表示一次反应。
        :raises ValueError: 如果反应不合法。
        """
        
        if not self.is_valid_sub_node(sub_node):
            raise ValueError(f"反应 {sub_node.name} 不符合任何规则。")
        
        for material in sub_node.source:
            if material not in self.available_materials:
                raise ValueError(f"源物质 {material} 不可用。")
        
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
        
        print(f"反应 {sub_node.name} 成功提交，所需时间: {sub_node.time}，当前时间: {current_time}")
        return current_time
    
    def get_available_materials(self) -> Set[str]:
        return self.available_materials.copy()

    def get_final_result(self) -> int:
        return self.material_earliest_time.get(self.target, None), self.total_cost
# 示例用法
if __name__ == "__main__":
    # 示例 JSON 配置
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
    
    # 初始化环境
    env = TTEnv(config_json)
    
    # 打印初始可用物质
    print("初始可用物质:", env.get_available_materials())
    tasks = """
    [{"name": "Subtask1", "source": ["N1"], "target": "N2", "dependencies": []}]
    """
 
    subtasks = json.loads(tasks)
    for task in subtasks:
        subtask = SubTTNode(task)
        print(f"Subtask {subtask.name} is valid: {env.is_valid_sub_node(subtask)}")
    # # 创建并提交一个合法的反应
    # subtask1 = SubTTNode({
    #     "name": "Task1",
    #     "source": ["N1"],
    #     "target": ["N2"],
    #     "dependencies": [],
    #     "time": 4
    # })
    # print(env.is_valid_sub_node(subtask1))
    # env.commit(subtask1)
    # print("提交后可用物质:", env.get_available_materials())

    # # 创建并提交另一个合法的反应
    # subtask2 = SubTTNode({
    #     "name": "N3",
    #     "source": ["N2"],
    #     "target": ["N3"],
    #     "dependencies": [],
    #     "time": 5
    # })
    # env.commit(subtask2)
    # print("提交后可用物质:", env.get_available_materials())

    # # 创建并提交一个使用初始物质的反应
    # subtask3 = SubTTNode({
    #     "name": "N3",
    #     "source": ["N1"],
    #     "target": ["N3"],
    #     "dependencies": [],
    #     "time": 2
    # })
    # env.commit(subtask3)
    # print("提交后可用物质:", env.get_available_materials())

    # # 创建并提交一个合法的多源反应
    # subtask4 = SubTTNode({
    #     "name": "N4",
    #     "source": ["N1", "N2"],
    #     "target": ["N4"],
    #     "dependencies": [],
    #     "time": 1
    # })
    # env.commit(subtask4)
    # print("提交后可用物质:", env.get_available_materials())

    # # 尝试提交一个不合法的反应
    # try:
    #     subtask_invalid = SubTTNode({
    #         "name": "N6",
    #         "source": ["N1", "N3"],
    #         "target": ["N6"],
    #         "dependencies": [],
    #         "time": 3
    #     })
    #     env.commit(subtask_invalid)
    # except ValueError as e:
    #     print("错误:", e)
