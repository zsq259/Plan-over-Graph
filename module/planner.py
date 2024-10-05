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
        json_regex = r'```json\n\s*\[\n\s*[\s\S]*?\]\n\s*```?'
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
    planner = ParallelPlanner('model')
    response = planner.extract_json(instruction.format(example=example, task='Create a new project'))
    subtasks = []
    for task in response:
        subtask = SubTaskNode(task)
        # print(subtask.name, subtask.dependencies, subtask.infos, subtask.answer)
        subtasks.append(subtask)
    import random
    random.shuffle(subtasks)
    for task in subtasks:
        print(task.name, task.dependencies, task.infos, task.answer)
    sorted_tasks = planner.topological_sort(subtasks)
    # print(sorted_tasks)
    for task in sorted_tasks:
        print(task.name, task.dependencies, task.infos, task.answer)