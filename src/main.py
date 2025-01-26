import os, sys, json
import argparse
import importlib
import multiprocessing
from module.env.tt_env import TTEnv
from module.runner import TTRunner
from module.scheduler import ParallelScheduler
from module.planner import ParallelPlanner
from module.subtask import SubTTNode
from src.logger_config import logger, COLOR_CODES, RESET

def preprocess_question(args):
    questions = []
    partial_results = []
    if args.question:
        if isinstance(args.question, str):
            questions.append(json.loads(args.question))
        else:
            questions.append(args.question)
    elif args.test_file:
        with open(args.test_file, "r") as f:
            data = json.load(f)

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
    else:
        raise ValueError("Either --question or --test_file must be provided.")
    
    prompts = []
    if args.task == "abstask":
        for question in questions:            
            template_module = importlib.import_module(f'template.{args.template}')
            instruction = template_module.instruction
            example = template_module.example
            prompt = instruction.format(example=example, task=question['question'])
            prompts.append((question, prompt))
    elif args.task == "specific_task":
        for question in questions:
            template_module = importlib.import_module(f'template.{args.template}')
            instruction = template_module.instruction
            example = template_module.example
            prompt = instruction.format(example=example, task=question['story'])
            prompts.append((question, prompt))
    
    return partial_results, prompts
            
def main():
    parser = argparse.ArgumentParser(description="Run the specified task with the given model and scheduler.")
    parser.add_argument("--task", type=str, required=True, help="The task to run.")
    parser.add_argument('--template', type=str, required=True, help='The template to use.')
    parser.add_argument("--model", type=str, required=True, help="The model to use.")
    parser.add_argument("--scheduler", type=str, required=True, help="The scheduler to use.")
    parser.add_argument("--question", type=str, help="The single question to ask.", default=None)
    parser.add_argument("--test_file", type=str, help="The test file to use.", default=None)
    parser.add_argument("--output_file", type=str, help="The output file to write to.", default=None)

    args = parser.parse_args()
    task = args.task
    model = args.model
    scheduler_type = args.scheduler
    
    if args.output_file:
        output_dir = os.path.dirname(args.output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    logger.info(f"Running task: {task}")
    logger.info(f"Using model: {model}")
    logger.info(f"Using scheduler: {scheduler_type}")
    
    if "llama" in model.lower():
        from model.llama_wrapper import LlamaWrapper
        model = LlamaWrapper(model)
    else:
        from model.gpt_wrapper import GPTWrapper
        model = GPTWrapper(name=model)
    
    multiprocessing.set_start_method('spawn')

    try:
        def save_results(partial_results, output_file):
            with open(output_file, "w") as f:
                json.dump(partial_results, f, ensure_ascii=False, indent=4)
        
        partial_results, prompts = preprocess_question(args)
        for question, prompt in prompts:
            if task == "abstask" or task == "specific_task":
                env = TTEnv(question['question'])
                runner = TTRunner(None, None)
                node_type = SubTTNode    
            else:
                raise ValueError(f"Unsupported task: {task}")
            planner = ParallelPlanner(model, env)
            scheduler = ParallelScheduler(runner, env)
            
            max_retry = 1
            retry_count = 0
            plan = None
            base_prompt = prompt
            all_failed_plans = []
            while retry_count < max_retry:
                subtasks, plan, valid, failed_plans = planner.plan(prompt, node_type)
                if valid:
                    try:
                        result = scheduler.run(subtasks)
                        break
                    except Exception as e:
                        for process in multiprocessing.active_children():
                            process.terminate()
                        logger.error(f"Error1: {COLOR_CODES['RED']}{e}{RESET}")
                        retry_count += 1
                        result = None
                        env.reset()
                else:
                    retry_count += 1
                    result = None
                    env.reset()
                    all_failed_plans.extend(failed_plans)
                    
            partial_results.append({'question': question, 'failed_plans': all_failed_plans, 'plan': plan, 'result': result})
            if args.output_file:
                save_results(partial_results, args.output_file)
        if args.output_file:
           save_results(partial_results, args.output_file) 
        else:
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