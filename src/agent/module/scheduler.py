import multiprocessing
import time, copy
from src.agent.module.subtask import SubTaskNode
from src.utils.logger_config import logger, COLOR_CODES, RESET

def execute_task(runner, task, queue):
    result = runner.run(task)
    if hasattr(task, 'question'):
        queue.put((task.question, result))
    else:
        queue.put((task.name, result))
    
class scheduler:
    def __init__(self, runner, env):
        self.name = 'scheduler'
        self.runner = runner
        self.env = env
    
    def run(self, task: list) -> str:
        raise NotImplementedError
    
class ParallelScheduler(scheduler):
    def __init__(self, runner, env):
        super().__init__(runner, env)
        self.name = 'ParallelScheduler'
        
    def copy_runner(self):
        return copy.deepcopy(self.runner)
    
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
                new_runner = self.copy_runner()
                process = multiprocessing.Process(target=execute_task, args=(new_runner, task, queue))
                process.start()
                processes[process] = task.name

            while processes:
                for process in list(processes):
                    process.join()
                    task_name = processes.pop(process)
                    
                    completed_task, result = queue.get()
                    logger.info(f"Task {COLOR_CODES['GREEN']}{completed_task}{RESET} completed with result: {COLOR_CODES['GREEN']}{result}{RESET}")
                    if hasattr(self.env, 'commit'):
                        result = self.env.commit(self.tasks[task_name])
                    self.tasks[task_name].answer = result
                    final_result = result
                    
                    with self.task_completed[task_name].get_lock():
                        self.task_completed[task_name].value = True
                    
                    for dependent_task_name, task in self.tasks.items():
                        if task_name in task.dependencies:
                            task.dependencies.remove(task_name)
                            if hasattr(self.env, 'update'):
                                self.env.update(task, self.tasks[task_name])
                            self.dependency_count[dependent_task_name] -= 1
                            if self.dependency_count[dependent_task_name] == 0:
                                new_runner = self.copy_runner()
                                new_process = multiprocessing.Process(target=execute_task, args=(new_runner, task, queue))
                                new_process.start()
                                processes[new_process] = dependent_task_name
                    del self.tasks[task_name]

        if hasattr(self.env, 'get_final_result'):
            return self.env.get_final_result()
        return final_result

if __name__ == "__main__":
    logger.info("Running scheduler")
    from src.agent.module.runner import SimpleSimRunner
    from src.agent.model.gpt_wrapper import GPTWrapper
    from src.agent.model.llama_wrapper import LlamaWrapper
    # model = GPTWrapper(name="gpt-3.5-turbo-instruct")
    model = LlamaWrapper()
    # excutor = HotPotQAExcutor(WikiEnv())
    # runner = SimpleSimRunner(model, excutor)
    # multiprocessing.set_start_method('spawn')
    # scheduler = ParallelScheduler(runner)
    # tasks = [
    #     SubTaskNode({"name": "task1", "question": "dtask1", "dependencies": []}),
    #     SubTaskNode({"name": "task2", "question": "dtask2", "dependencies": ["task1"]}),
    #     SubTaskNode({"name": "task3", "question": "dtask3", "dependencies": []}),
    #     SubTaskNode({"name": "task4", "question": "dtask4", "dependencies": ["task2", "task3"]}),
    #     SubTaskNode({"name": "task5", "question": "dtask5", "dependencies": []})
    # ]
    # scheduler.run(tasks)
    # logger.info("All tasks completed")