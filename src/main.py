import os, sys, json
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
    parser.add_argument("--question", type=str, help="The single question to ask.", default=None)
    parser.add_argument("--test_file", type=str, help="The test file to use.", default=None)
    parser.add_argument("--output_file", type=str, help="The output file to write to.", default=None)

    args = parser.parse_args()
    task = args.task
    model = args.model
    scheduler_type = args.scheduler

    logger.info(f"Running task: {task}")
    logger.info(f"Using model: {model}")
    logger.info(f"Using scheduler: {scheduler_type}")
    
    if "llama" in model.lower():
        model = LlamaWrapper(model)
    else:
        model = "gpt-3.5-turbo-instruct"
        model = GPTWrapper(name=model)
    
    multiprocessing.set_start_method('spawn')
    planner = ParallelPlanner(model)

    try:
        if task == "hotpotqa":
            env = WikiEnv()
            executor = HotPotQAExcutor(env)
            runner = HotPotQARunner(model, executor)
            if scheduler_type == "parallel":
                scheduler = ParallelScheduler(runner)
            else:
                raise ValueError(f"Unsupported scheduler type: {scheduler_type}")
            if args.question:
                result = scheduler.run(planner.plan(args.question))
            elif args.test_file:
                with open(args.test_file, "r") as f:
                    data = json.load(f)

                if os.path.exists(args.output_file):
                    with open(args.output_file, "r") as f:
                        partial_results = json.load(f)
                else:
                    partial_results = []

                processed_questions = set(result['question']['id'] for result in partial_results)

                for question in data:
                    if question['id'] not in processed_questions:
                        result = scheduler.run(planner.plan(question))
                        partial_results.append({'question': question, 'result': result})
                        with open(args.output_file, "w") as f:
                            json.dump(partial_results, f, ensure_ascii=False, indent=4)

                with open(args.output_file, "w") as f:
                    json.dump(partial_results, f, ensure_ascii=False, indent=4)
            else:
                raise ValueError("Either --question or --test_file must be provided.")
        else:
            raise ValueError(f"Unsupported task: {task}")

    except KeyboardInterrupt:
        logger.info(f"{COLOR_CODES['YELLOW']}Program interrupted by user{RESET}")
        for process in multiprocessing.active_children():
            process.terminate()
        sys.exit(0)
    except Exception as e:
        logger.error(f"{COLOR_CODES['RED']}Error: {e}{RESET}")

if __name__ == "__main__":
    main()