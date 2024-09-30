from model.model import Model
from env.exec_env import ExecEnv

class TaskRunner:
    def __init__(self, model: Model, env: ExecEnv):
        self.model = model
        self.env = env
    
    def run(self, question):
        raise NotImplementedError
    
class HotpotQARunner(TaskRunner):
    def __init__(self, model: Model, env: ExecEnv):
        super().__init__(model, env)
    
    def step(self, prompt, i, print_info=True):
        thought, action = self.model.step(prompt + f"Thought {i}:", stop=[f"\nObservation {i}:"])
        obs, r, done, info = self.env.step(action)
        obs = obs.replace('\\n', '')
        step_str = f"Thought {i}: {thought}\nAction {i}: {action}\nObservation {i}: {obs}\n"
        prompt += step_str
        if print_info:
            print(step_str)
        return prompt, r, done, info

    def run(self, question, print_info=True):
        from template.webthink import instruction, webthink_example
        prompt = instruction.format(examples=webthink_example, question=question)
        if print_info:
            print("Question:", question)
        for i in range(1, 11):
            prompt, r, done, info = self.step(prompt, i, print_info)
            if done:
                break
        if not done:
            obs, r, done, info = self.env.step("finish[]")
        print(info, '\n')
        return info["answer"]
            