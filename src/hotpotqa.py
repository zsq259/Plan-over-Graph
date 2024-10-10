import sys
import multiprocessing
from model.gpt_wrapper import GPTWrapper
from model.llama_wrapper import LlamaWrapper
from module.env.wiki_env import WikiEnv
from module.excutor import HotPotQAExcutor
from module.runner import HotPotQARunner
from module.scheduler import ParallelScheduler
from module.planner import ParallelPlanner
from src.logger_config import logger, COLOR_CODES, RESET

def main():
    try:
        # question = "Are Giuseppe Verdi and Ambroise Thomas both Opera composers ?"
        question = "Which is longer, the Yangtze River or the Yellow River?"

        model = LlamaWrapper()
        env = WikiEnv()
        executor = HotPotQAExcutor(env)
        runner = HotPotQARunner(model, executor)
        scheduler = ParallelScheduler(runner)
        planner = ParallelPlanner(model)

        result = scheduler.run(planner.plan(question))
        # print(result)
    except KeyboardInterrupt:
        # print("program interrupted by user")
        logger.info(f"{COLOR_CODES['YELLOW']}Program interrupted by user{RESET}")
        for process in multiprocessing.active_children():
            process.terminate()
        sys.exit(0)
    except Exception as e:
        # print(e)
        logger.error(f"{COLOR_CODES['RED']}Error: {e}{RESET}")
        

if __name__ == "__main__":
    main()