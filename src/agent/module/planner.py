import json, re
from collections import deque
from src.agent.module.subtask import SubTaskNode
from src.agent.model.model import Model
from src.utils.logger_config import logger, COLOR_CODES, RESET
from src.utils.utils import extract_json

class Planner:
    def __init__(self, model: Model=None, env=None):
        self._name = 'Planner'
        self.sub_tasks = []
        self.model = model
        self.env = env
    
    def decompose_task(self, task: str) -> list[SubTaskNode]:
        raise NotImplementedError
    
    def plan(self, task: str) -> list[SubTaskNode]:
        raise NotImplementedError
        
class ParallelPlanner(Planner):
    def __init__(self, model, env):
        super().__init__(model, env)
        self._name = 'ParallelPlanner'

    def decompose_task(self, prompt: str, node_type, max_retry) -> list[SubTaskNode]:
        subtasks = []
        valid = False
        retry_count = 0
        failed_plans = []
        while not valid and retry_count < max_retry:
            subtasks = []
            valid = True
            try:
                prompt = prompt.replace("'", '"')
                response = self.model.predict(prompt)
                tasks = extract_json(response)
                if isinstance(tasks, dict):
                    tasks = tasks['plan']
                # plans = tasks['plan']
                plans = tasks
            except ValueError as e:
                logger.info(f"Error decomposing task: {COLOR_CODES['RED']}{e}{RESET}")
                valid = False
                plans = response
                failed_plans.append(plans)
                if retry_count == 0:
                    # prompt = "You have failed to decompose the task. Please try again." + prompt
                    prompt = "Failed to decompose the task. Please ensure the json format is correct and wrapped in triple backticks." + prompt
                retry_count += 1
                continue
            
            logger.info(f"Decomposed task: {COLOR_CODES['CYAN']}{tasks}{RESET}")
            for task in plans:
                subtask = node_type(task)
                subtasks.append(subtask)
            
            if hasattr(self.env, 'is_valid_sub_node'):
                for subtask in subtasks:
                    if not self.env.is_valid_sub_node(subtask):
                        valid = False
                        failed_plans.append(plans)
                        logger.info(f"Subtask {COLOR_CODES['RED']}{subtask.name}{RESET} is invalid, retrying...")            
                        if retry_count == 0:
                            prompt = "You have failed to decompose the task. Please try again." + prompt
                        retry_count += 1
                        break
        if not valid:
            # raise ValueError("Failed to decompose task")
            logger.warning(f"Failed to decompose task: {COLOR_CODES['RED']}retry count: {retry_count}{RESET}")
        #     return subtasks, tasks, False
        return subtasks, plans, valid, failed_plans
    
    def plan(self, task: str, node_type, max_retry) -> list[SubTaskNode]:        
        subtasks, plan, valid, failed_plans = self.decompose_task(task, node_type, max_retry)
        subtasks = self.topological_sort(subtasks)
        if not subtasks:
            valid = False
        return subtasks, plan, valid, failed_plans
    
    def topological_sort(self, tasks: list[SubTaskNode]) -> list[SubTaskNode]:
        in_degree = {task.name: 0 for task in tasks}
        graph = {task.name: [] for task in tasks}
        for task in tasks:
            for dependency in task.dependencies:
                in_degree[task.name] += 1
                if dependency in graph:
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
            return None
        
        return sorted_tasks
    
if __name__ == "__main__":
    content = ""
    planner = ParallelPlanner(None, None)
    tasks = extract_json(content)
    print(json.dumps(tasks, indent=4))
    