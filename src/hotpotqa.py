from model.gpt_wrapper import GPTWrapper
from env.parallel_env import ParallelEnv
from env.wiki_env import WikiEnv
from src.runner import HotpotQARunner

question = "Are Giuseppe Verdi and Ambroise Thomas both Opera composers ?"

wiki = WikiEnv()
model = GPTWrapper()
env = ParallelEnv(wiki)

runner = HotpotQARunner(model, env)
runner.run(question)