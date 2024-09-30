import multiprocessing
import time
from collections import deque

class Task:
    def __init__(self, task_id, dependencies, execution_time):
        self.task_id = task_id
        self.dependencies = dependencies
        self.execution_time = execution_time
        self.completed = multiprocessing.Value('b', False)  # 使用 multiprocessing.Value 共享状态

    def execute(self):
        print(f'Starting execution of {self.task_id} for {self.execution_time} seconds')
        time.sleep(self.execution_time)  # 使用 time.sleep 模拟任务执行
        with self.completed.get_lock():
            self.completed.value = True
        print(f'Finished execution of {self.task_id}')

class Scheduler:
    def __init__(self, tasks):
        self.tasks = {task.task_id: task for task in tasks}
        self.dependency_count = {task.task_id: len(task.dependencies) for task in tasks}

    def run(self):
        while self.tasks:
            # 找到可以执行的任务
            executable_tasks = [task for task in self.tasks.values() if self.dependency_count[task.task_id] == 0]

            if not executable_tasks:
                break

            processes = {}
            for task in executable_tasks:
                process = multiprocessing.Process(target=self.execute_task, args=(task,))
                process.start()
                processes[process] = task.task_id

            while processes:
                for process in list(processes):
                    process.join()  # 等待进程完成
                    task_id = processes.pop(process)
                    with self.tasks[task_id].completed.get_lock():
                        self.tasks[task_id].completed.value = True
                    # 更新依赖关系并立即启动依赖任务
                    for dependent_task_id, task in self.tasks.items():
                        if task_id in task.dependencies:
                            task.dependencies.remove(task_id)
                            self.dependency_count[dependent_task_id] -= 1
                            if self.dependency_count[dependent_task_id] == 0:
                                new_process = multiprocessing.Process(target=self.execute_task, args=(task,))
                                new_process.start()
                                processes[new_process] = dependent_task_id
                    del self.tasks[task_id]

    def execute_task(self, task):
        task.execute()  # 执行任务

# 示例任务和依赖关系，包括执行时间
tasks = [
    Task('task1', [], 2),  # task1 执行 2 秒
    Task('task2', ['task1'], 5),  # task2 依赖 task1，执行 5 秒
    Task('task3', [], 8),  # task3 执行 8 秒
    Task('task4', ['task2', 'task3'], 4),  # task4 依赖 task2 和 task3，执行 4 秒
    Task('task5', [], 4),  
]

if __name__ == '__main__':
    scheduler = Scheduler(tasks)
    scheduler.run()