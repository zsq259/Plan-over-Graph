from module.subtask import SubTaskNode

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
    
    def run(self, task: list) -> str:
        return task