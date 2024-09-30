from module.subtask import SubTaskNode

class Runner:
    def __init__(self, model, executor):
        self._name = 'Runner'
        self.model = model
        self.executor = executor
    
    def run(self, SubTaskNode) -> str:
        raise NotImplementedError
    