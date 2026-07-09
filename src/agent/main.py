import os, sys, json
import argparse
import importlib
import multiprocessing
from src.agent.module.env.tt_env import TTEnv
from src.agent.module.runner import TTRunner
from src.agent.module.scheduler import ParallelScheduler
from src.agent.module.planner import ParallelPlanner
from src.agent.module.extractor import Extractor
from src.agent.module.subtask import SubTTNode
from src.utils.utils import get_model
from src.utils.logger_config import logger, COLOR_CODES, RESET

def preprocess_question(args):
    questions = []
    partial_results = []
    with open(args.test_file, "r") as f:
        data = json.load(f)
    if not isinstance(data, list):
        data = [data]

    if os.path.exists(args.output_file):
        with open(args.output_file, "r") as f:
            partial_results = json.load(f)
    else:
        partial_results = []
    partial_results = [result for result in partial_results if result['plan'] is not None]
    processed_questions = set(result['question']['id'] for result in partial_results)
    for question in data:
        if question['id'] not in processed_questions:
            questions.append(question)
            
    return partial_results, questions
            
def main():
    parser = argparse.ArgumentParser(description="Run the specified task with the given model and scheduler.")
    parser.add_argument("--task", type=str, required=True, help="The task to run.")
    parser.add_argument('--template', type=str, required=True, help='The template to use.')
    parser.add_argument("--model", type=str, required=True, help="The model to use.")
    parser.add_argument("--scheduler", type=str, required=True, help="The scheduler to use.")
    parser.add_argument("--extractor", type=bool or str, help="Whether to use the extractor and the model to extract rules.", default=False)
    parser.add_argument("--validation_iterations", type=int, help="Number of validation refinement iterations (0 to disable).", default=0)
    parser.add_argument("--max_retry", type=int, help="The maximum number of retries.", default=3)
    parser.add_argument("--test_case", type=str, help="The test case to use.", default=None)
    parser.add_argument("--output_dir", type=str, help="The output file to write to.", default=None)

    args = parser.parse_args()
    args.test_file = f"data/dev/test/{args.test_case}.json"
    args.output_file = args.output_dir + "/" if args.output_dir and not args.output_dir.endswith("/") else args.output_dir
    args.output_file = args.output_file + args.test_case if args.output_dir else None
    args.output_file = args.output_file + "-e" if args.extractor else args.output_file
    args.output_file = args.output_file + "-output.json" if args.output_file else None
    
    if args.output_file:
        output_dir = os.path.dirname(args.output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    logger.info(f"Running task: {args.task}")
    logger.info(f"Using model: {args.model}")
    logger.info(f"Using scheduler: {args.scheduler}")
    logger.info(f"Using extractor: {args.extractor}")
    logger.info(f"Output file: {args.output_file}")
    
    model = get_model(args.model)
    
    multiprocessing.set_start_method('spawn')
    
    try:
        def save_results(partial_results, output_file):
            with open(output_file, "w") as f:
                json.dump(partial_results, f, ensure_ascii=False, indent=4)
        
        partial_results, questions = preprocess_question(args)
        for question in questions:
            retry_count = 0
            plan = None
            all_failed_plans = []
            extractor = None
            extraction_iterations = 0
            
            if isinstance(args.extractor, str):
                if args.extractor == args.model:
                    extractor = Extractor(model, validation_iterations=args.validation_iterations)
                else:
                    extractor = Extractor(get_model(args.extractor), validation_iterations=args.validation_iterations)
            else:
                extractor = Extractor(model, validation_iterations=args.validation_iterations)       
            
            while retry_count < args.max_retry:
                try:
                    prompt = ""
                    template_module = importlib.import_module(f'template.{args.template}')
                    instruction = template_module.instruction
                    example = template_module.example
                    
                    if args.task == "abstask":    
                        prompt = instruction.format(example=example, task=question['question'])
                    elif args.task == "specific_task":
                        task = question['story']
                        if args.extractor:
                            task = extractor.extract(task, args.max_retry)
                            extraction_iterations = extractor.iteration_count
                        prompt = instruction.format(example=example, task=task)
                    else:
                        raise ValueError(f"Unsupported task: {args.task}")

                    if "question" in question:
                        env = TTEnv(question['question'])
                    else:
                        env = TTEnv(task)

                    prompt = prompt.replace("\'", "\"")

                    runner = TTRunner(None, None)
                    node_type = SubTTNode
                    planner = ParallelPlanner(model, env)
                    scheduler = ParallelScheduler(runner, env)

                    subtasks, plan, valid, failed_plans = planner.plan(prompt, node_type, args.max_retry)
                    if valid:
                        result = scheduler.run(subtasks)
                        break
                    else:
                        retry_count += 1
                        result = None
                        env.reset()
                        all_failed_plans.extend(failed_plans)
                        all_failed_plans.append(plan)
                except Exception as e:
                    for process in multiprocessing.active_children():
                        process.terminate()
                    logger.error(f"Error1: {COLOR_CODES['RED']}{e}{RESET}")
                    retry_count += 1
                    result = None
                    env.reset()
                    
            partial_results.append({'question': question, 'failed_plans': all_failed_plans, 'plan': plan, 'result': result})
            if args.extractor:
                partial_results[-1]['model_rules'] = task
                if args.validation_iterations > 0:
                    partial_results[-1]['extraction_iterations'] = extraction_iterations
                    partial_results[-1]['extraction_history'] = extractor.extraction_history
            if args.output_file:
                save_results(partial_results, args.output_file)
        if not args.output_file:
            logger.info(f"Results: {COLOR_CODES['CYAN']}{partial_results}{RESET}")
    

    except KeyboardInterrupt:
        logger.info(f"{COLOR_CODES['YELLOW']}Program interrupted by user{RESET}")
        for process in multiprocessing.active_children():
            process.terminate()
        sys.exit(0)
    except Exception as e:
        logger.error(f"{COLOR_CODES['RED']}Error2: {e}{RESET}")

if __name__ == "__main__":
    main()