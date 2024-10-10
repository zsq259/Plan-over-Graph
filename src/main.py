import sys
import argparse
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
    parser = argparse.ArgumentParser(description="Run the specified task with the given model and scheduler.")
    parser.add_argument("--task", type=str, required=True, help="The task to run.")
    parser.add_argument("--model", type=str, required=True, help="The model to use.")
    parser.add_argument("--scheduler", type=str, required=True, help="The scheduler to use.")

    args = parser.parse_args()
    task = args.task
    model = args.model
    scheduler_type = args.scheduler

    # print(f"Running task: {task}")
    # print(f"Using model: {model}")
    # print(f"Using scheduler: {scheduler_type}")
    logger.info(f"Running task: {task}")
    logger.info(f"Using model: {model}")
    logger.info(f"Using scheduler: {scheduler_type}")
    
    if "llama" in model.lower():
        model = LlamaWrapper(model)
    else:
        model = "gpt-3.5-turbo-instruct"
        model = GPTWrapper(name=model)
    planner = ParallelPlanner(model)

    try:
        if task == "hotpotqa":
            question = "Which is longer, the Yangtze River or the Yellow River?"
            env = WikiEnv()
            executor = HotPotQAExcutor(env)
            runner = HotPotQARunner(model, executor)
            if scheduler_type == "parallel":
                scheduler = ParallelScheduler(runner)
            else:
                raise ValueError(f"Unsupported scheduler type: {scheduler_type}")            
            result = scheduler.run(planner.plan(question))
            # print(result)
        else:
            raise ValueError(f"Unsupported task: {task}")

    except KeyboardInterrupt:
        # print("Program interrupted by user")
        logger.info(f"{COLOR_CODES['YELLOW']}Program interrupted by user{RESET}")
        for process in multiprocessing.active_children():
            process.terminate()
        sys.exit(0)
    except Exception as e:
        # print(e)
        logger.error(f"{COLOR_CODES['RED']}Error: {e}{RESET}")

if __name__ == "__main__":
    main()