import subprocess
import concurrent.futures

from env.exec_env import ExecEnv
from env.wiki_env import WikiEnv

class ParallelEnv(ExecEnv):
    def __init__(self, env):
        if not hasattr(env, 'step'):
            raise TypeError("The provided environment does not have a 'step' method.")
        self.env = env

    def run_action(self, action):
        try:
            result = self.env.step(action)
            return result
        except Exception as e:
            return str(e)

    def run_actions(self, actions):
        # print(actions)
        results = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            future_to_action = {executor.submit(self.run_action, action.lower()): action for action in actions}
            for future in concurrent.futures.as_completed(future_to_action):
                action = future_to_action[future]
                try:
                    result = future.result()
                    results.append((action, result))
                except Exception as exc:
                    results.append(str(exc))
        # print(results)
        return self.env.combine(results)
    
    def step(self, actions):
        return self.run_actions(actions)

# 示例执行环境函数
def exec_env(action):
    result = subprocess.run(action, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8')

if __name__ == "__main__":
    env = ParallelEnv(WikiEnv())
    # actions = ["echo 'Action 1'", "echo 'Action 2'", "echo 'Action 3'"]
    actions = ["Search[Der Rosenkavalier]", "Search[I Capuleti e i Montecchi]"]
    results = env.run_actions(actions)

    print(results)