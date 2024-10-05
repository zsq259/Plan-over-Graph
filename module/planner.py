import json, re
from collections import deque
from module.subtask import SubTaskNode
from template.decompose_plan import instruction, example 
from model.model import Model

class Planner:
    def __init__(self, model: Model):
        self._name = 'Planner'
        self.sub_tasks = []
        self.model = model
    
    def extract_json(self, text: str) -> dict:
        json_regex = r'```json\s*\[\s*[\s\S]*?\s*\]\s*(?:```|\Z)'
        matches = re.findall(json_regex, text)
        if matches:
            json_data = matches[0].replace('```json', '').replace('```', '').strip()
            try:
                parsed_json = json.loads(json_data)
                return parsed_json
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON data: {e}")
        else:
            raise ValueError(f"No JSON data found in the string: \033[38;5;214m{text}\033[0m")
    
    def decompose_task(self, task: str) -> list[SubTaskNode]:
        raise NotImplementedError
    
    def plan(self, task: str) -> list[SubTaskNode]:
        raise NotImplementedError
        
class ParallelPlanner(Planner):
    def __init__(self, model):
        super().__init__(model)
        self._name = 'ParallelPlanner'
    
    def decompose_task(self, task: str) -> list[SubTaskNode]:
        subtasks = []
        prompt = instruction.format(example=example, task=task)
        try:
            response = self.model.predict(prompt)
            tasks = self.extract_json(response)
        except ValueError as e:
            raise ValueError(f"Error decomposing task: {e}")
        
        print(f"\033[94mDecomposed task: {tasks}\033[0m")
        for task in tasks:
            subtask = SubTaskNode(task)
            subtasks.append(subtask)
        return subtasks
    
    def plan(self, task: str) -> list[SubTaskNode]:
        tasks = self.decompose_task(task)
        return self.topological_sort(tasks)
    
    def topological_sort(self, tasks: list[SubTaskNode]) -> list[SubTaskNode]:
        in_degree = {task.name: 0 for task in tasks}
        graph = {task.name: [] for task in tasks}
        for task in tasks:
            for dependency in task.dependencies:
                in_degree[task.name] += 1
                graph[dependency].append(task)
                
        queue = deque([task for task in tasks if in_degree[task.name] == 0])
        sorted_tasks = []
        while queue:
            current = queue.popleft()
            sorted_tasks.append(current)
            for neighbor in graph[current.name]:
                in_degree[neighbor.name] -= 1
                if in_degree[neighbor.name] == 0:
                    queue.append(neighbor)

        if len(sorted_tasks) != len(tasks):
            raise ValueError("Graph has at least one cycle")
        
        return sorted_tasks
    
if __name__ == "__main__":
    content = """
```json
[
    {
        "name": "retrieve_yangtze_length",
        "question": "How long is the Yangtze River?",
        "description": "Retrieve the length of the Yangtze River. This requires using the 'length of river' API and specifying the name 'Yangtze River'.",
        "dependencies": []
    },
    {
        "name": "retrieve_yellow_length",
        "question": "How long is the Yellow River?",
        "description": "Retrieve the length of the Yellow River. This requires using the 'length of river' API and specifying the name 'Yellow River'.",
        "dependencies": []
    },
    {
        "name": "compare_river_lengths",
        "question": "Which is longer, the Yangtze River or the Yellow River?",
        "description": "Compare the lengths of the Yangtze River and the Yellow River to determine which one is longer. This requires using the 'compare values' API and specifying the lengths obtained from the previous two subtasks as inputs.",
        "dependencies": [
            "retrieve_yangtze_length",
            "retrieve_yellow_length"
        ]
    }
]
```
    """
    planner = ParallelPlanner(None)
    tasks = planner.extract_json(content)
    print(tasks)