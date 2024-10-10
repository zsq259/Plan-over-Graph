import multiprocessing
import time
from module.subtask import SubTaskNode
from src.logger_config import logger, COLOR_CODES, RESET

class scheduler:
    def __init__(self, runner):
        self.name = 'scheduler'
        self.runner = runner
    
    def run(self, task: list) -> str:
        raise NotImplementedError
    
class ParallelScheduler(scheduler):
    def __init__(self, runner):
        super().__init__(runner)
        self.name = 'ParallelScheduler'
        
    def execute_task(self, task, queue):
        result = self.runner.run(task)
        queue.put((task.question, result))
    
    def run(self, tasks: list[SubTaskNode]) -> str:
        self.tasks = {task.name: task for task in tasks}
        self.dependency_count = {task.name: len(task.dependencies) for task in tasks}
        self.task_completed = {task.name: multiprocessing.Value('b', False) for task in tasks}

        queue = multiprocessing.Queue()
        final_result = None

        while self.tasks:
            executable_tasks = [task for task in self.tasks.values() if self.dependency_count[task.name] == 0]
            if not executable_tasks:
                break

            processes = {}
            for task in executable_tasks:
                process = multiprocessing.Process(target=self.execute_task, args=(task, queue))
                process.start()
                processes[process] = task.name

            while processes:
                for process in list(processes):
                    process.join()
                    task_name = processes.pop(process)
                    
                    completed_task, result = queue.get()
                    # print(f"Task \033[92m{completed_task}\033[0m completed with result: \033[92m{result}\033[0m")
                    logger.info(f"Task {COLOR_CODES['GREEN']}{completed_task}{RESET} completed with result: {COLOR_CODES['GREEN']}{result}{RESET}")
                    final_result = result
                    
                    with self.task_completed[task_name].get_lock():
                        self.task_completed[task_name].value = True
                    
                    for dependent_task_name, task in self.tasks.items():
                        if task_name in task.dependencies:
                            task.dependencies.remove(task_name)
                            task.infos.append((completed_task, result))
                            self.dependency_count[dependent_task_name] -= 1
                            if self.dependency_count[dependent_task_name] == 0:
                                new_process = multiprocessing.Process(target=self.execute_task, args=(task, queue))
                                new_process.start()
                                processes[new_process] = dependent_task_name
                    del self.tasks[task_name]

        return final_result

if __name__ == "__main__":
    # print("Running scheduler")
    logger.info("Running scheduler")
    from module.runner import SimpleSimRunner
    runner = SimpleSimRunner(None, None)
    scheduler = ParallelScheduler(runner)
    tasks = [
        SubTaskNode({"name": "task1", "question": "dtask1", "dependencies": []}),
        SubTaskNode({"name": "task2", "question": "dtask2", "dependencies": ["task1"]}),
        SubTaskNode({"name": "task3", "question": "dtask3", "dependencies": []}),
        SubTaskNode({"name": "task4", "question": "dtask4", "dependencies": ["task2", "task3"]}),
        SubTaskNode({"name": "task5", "question": "dtask5", "dependencies": []})
    ]
    scheduler.run(tasks)
    # print("All tasks completed")
    logger.info("All tasks completed")