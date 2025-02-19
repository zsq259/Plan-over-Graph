import json, re, time
from src.agent.module.subtask import SubTaskNode, SubQANode, SubTTNode
from src.utils.logger_config import logger, COLOR_CODES, RESET

class Runner:
    def __init__(self, model, executor):
        self._name = 'Runner'
        self.model = model
        self.executor = executor
    
    def run(self, subtask: SubTaskNode) -> str:
        raise NotImplementedError
    
class SimpleSimRunner(Runner):
    def __init__(self, model, executor):
        super().__init__(model, executor)
        self._name = 'SimpleSimRunner'
    
    def run(self, subtask: SubTaskNode) -> str:
        import random, time
        t_ = random.randint(1, 10)
        logger.info(f'Starting {subtask.name} for {t_} seconds')
        time.sleep(t_)
        logger.info(f'Finished {subtask.name}')
        return subtask.name
    
class TTRunner(Runner):
    def __init__(self, model, executor):
        super().__init__(model, executor)
        self._name = 'TTRunner'
    
    def run(self, subtask: SubTTNode) -> str:
        # time.sleep(subtask.time)
        return subtask.name
    
if __name__ == "__main__":
    pass