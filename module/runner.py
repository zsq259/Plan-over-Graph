import json, re
from retry import retry
from module.subtask import SubTaskNode
from src.logger_config import logger, COLOR_CODES, RESET

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
    
class HotPotQARunner(Runner):
    def __init__(self, model, executor):
        super().__init__(model, executor)
        self._name = 'ParallelRunner'
    
    def get_thought_actions(self, content=None):
        match = re.search(r'^(.*)\nActions? \d+:\s*(.*)', content, re.DOTALL)
        if match:
            thought = match.group(1).strip()
            actions = match.group(2).strip()
            actions = actions.replace("'", '"')
            return thought, actions
        else:
            raise ValueError("Thought Actions No match: {}".format(content))
    
    def find_actions(self, actions: str) -> list | str:
        actions = actions.lower()
        if actions.startswith('['):
            return json.loads(actions)
        return actions
    
    @retry(tries=3, delay=1)
    def get_actions(self, prompt, i):
        result = self.model.predict(prompt + f"Thought {i}:", stop=[f"\nObservation {i}:"])
        thought, actions = self.get_thought_actions(result)
        actions = self.find_actions(actions)
        return thought, actions
            
    def step(self, prompt, i, print_info=True):
        thought, actions = self.get_actions(prompt, i)
        if isinstance(actions, list):
            actions = actions[0]
        obs, r, done, info = self.executor.run(actions)
        obs = obs.replace('\\n', '')
        step_str = f"Thought {i}: {thought}\nAction {i}: {actions}\nObservation {i}: {obs}\n----------\n"
        prompt += step_str
        if print_info:
            logger.info(step_str)
        return prompt, r, done, info

    def run(self, subtask: SubTaskNode, print_info=True) -> str:
        from template.webthink0 import instruction, webthink_example
        informations = ""
        if len(subtask.infos) > 0:
            informations = "\nFor the current question, before you start search, you have some initial informations:\n"
        for info in subtask.infos:
            informations += f"{info[0]}: {info[1]}\n"
        prompt = instruction.format(examples=webthink_example, question=subtask.question, informations=informations)
        if print_info:
            logger.info(f"Question: {subtask.question}")
            logger.info(f"Initial informations: {informations}")
        for i in range(1, 11):
            prompt, r, done, info = self.step(prompt, i, print_info)
            if done:
                break
        if not done:
            obs, r, done, info = self.executor.run("finish[]")
        subtask.answer = info["answer"]
        return info["answer"]
    
if __name__ == "__main__":
    content = """I need to search for a data source or API about Giuseppe Verdi, and fetch relevant information about him.
Actions 1: ["Search[data source/API for Giuseppe Verdi]"]
    """
    runner = HotPotQARunner(None, None)
    thought, actions = runner.get_thought_actions(content)
    logger.info(thought)
    logger.info(actions)
    logger.info(runner.find_actions(actions))
        