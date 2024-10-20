import json, re
from collections import deque
from module.subtask import SubTaskNode
from model.model import Model
from src.logger_config import logger, COLOR_CODES, RESET

class Planner:
    def __init__(self, model: Model, env):
        self._name = 'Planner'
        self.sub_tasks = []
        self.model = model
        self.env = env
    
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
    def __init__(self, model, env):
        super().__init__(model, env)
        self._name = 'ParallelPlanner'

    def decompose_task(self, prompt: str, node_type) -> list[SubTaskNode]:
        subtasks = []
        valid = False
        max_retry = 3
        retry_count = 0
        while not valid and retry_count < max_retry:
            subtasks = []
            valid = True
            try:
                response = self.model.predict(prompt)
                tasks = self.extract_json(response)
            except ValueError as e:
                logger.info(f"Error decomposing task: {COLOR_CODES['RED']}{e}{RESET}")
                valid = False
                if retry_count == 0:
                    prompt = "You have failed to decompose the task. Please try again." + prompt
                retry_count += 1
                continue
            
            logger.info(f"Decomposed task: {COLOR_CODES['CYAN']}{tasks}{RESET}")
            for task in tasks:
                subtask = node_type(task)
                subtasks.append(subtask)
            
            if hasattr(self.env, 'is_valid_sub_node'):
                for subtask in subtasks:
                    if not self.env.is_valid_sub_node(subtask):
                        valid = False
                        logger.info(f"Subtask {COLOR_CODES['RED']}{subtask.name}{RESET} is invalid, retrying...")            
                        if retry_count == 0:
                            prompt = "You have failed to decompose the task. Please try again." + prompt
                        retry_count += 1
                        break
        if not valid:
            raise ValueError("Failed to decompose task")
        return subtasks, tasks
    
    def plan(self, task: str, node_type) -> list[SubTaskNode]:
        subtasks, plan = self.decompose_task(task, node_type)
        return self.topological_sort(subtasks), plan
    
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
[{'name': 'Subtask1', 'source': ['N1'], 'target': 'N2', 'dependencies': []}, {'name': 'Subtask2', 'source': ['N1', 'N2'], 'target': 'N3', 'dependencies': ['Subtask1']}, {'name': 'Subtask3', 'source': ['N3'], 'target': 'N4', 'dependencies': ['Subtask2']}, {'name': 'Subtask4', 'source': ['N1'], 'target': 'N4', 'dependencies': ['Subtask3']}, {'name': 'Subtask5', 'source': ['N2'], 'target': 'N4', 'dependencies': ['Subtask4']}, {'name': 'Subtask6', 'source': ['N3'], 'target': 'N5', 'dependencies': ['Subtask3']}, {'name': 'Subtask7', 'source': ['N1'], 'target': 'N5', 'dependencies': ['Subtask6']}, {'name': 'Subtask8', 'source': ['N2'], 'target': 'N5', 'dependencies': ['Subtask7']}, {'name': 'Subtask9', 'source': ['N2', 'N1'], 'target': 'N6', 'dependencies': ['Subtask1']}, {'name': 'Subtask10', 'source': ['N4'], 'target': 'N6', 'dependencies': ['Subtask3']}, {'name': 'Subtask11', 'source': ['N1', 'N2', 'N5'], 'target': 'N7', 'dependencies': ['Subtask2', 'Subtask8']}, {'name': 'Subtask12', 'source': ['N4', 'N6', 'N3'], 'target': 'N7', 'dependencies': ['Subtask3', 'Subtask10']}, {'name': 'Subtask13', 'source': ['N3', 'N1', 'N4'], 'target': 'N8', 'dependencies': ['Subtask3', 'Subtask4']}, {'name': 'Subtask14', 'source': ['N7', 'N5'], 'target': 'N8', 'dependencies': ['Subtask6', 'Subtask11']}, {'name': 'Subtask15', 'source': ['N8', 'N2'], 'target': 'N9', 'dependencies': ['Subtask8', 'Subtask13']}, {'name': 'Subtask16', 'source': ['N7', 'N6'], 'target': 'N9', 'dependencies': ['Subtask10', 'Subtask12']}]
```
"""
    planner = ParallelPlanner(None, None)
    tasks = planner.extract_json(content)
    