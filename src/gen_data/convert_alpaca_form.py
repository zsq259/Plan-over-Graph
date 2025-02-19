import json
import re
import argparse
from template.abstask_plan import instruction, example

def convert_task_form(task, dpo):
    example_ = re.sub(' +', ' ', example.replace("\n", ""))
    prompt = instruction.format(example=example_, task=task['question'])
    ins = prompt.split("Task:\n")[0] + "Task:\n"
    input = prompt.split("Task:\n")[1]
    if dpo:
        chosen = str(task['answer'])
        rejected = str(task['feasible'])
        new_task = {"instruction": ins, "input": input, "chosen": chosen, "rejected": rejected}
    else:
        # output = str(task['answer'])
        if 'feasible' not in task:
            print(task)
        if not task['feasible'] or len(task['feasible']) == 0:
            return None
        output = str(task['feasible'])
        new_task = {"instruction": ins, "input": input, "output": output}
    return new_task

def convert_data(input_file, dpo):
    data = json.load(open(input_file, "r"))
    new_data = []
    for task in data:
        new_task = convert_task_form(task, dpo)
        if new_task:
            new_data.append(new_task)
    return new_data
        
def main():
    parser = argparse.ArgumentParser(description="Convert data to ALPaCA format")
    parser.add_argument("--file_list", type=str, nargs='+', help="json file list")
    parser.add_argument("--output_name", type=str)
    parser.add_argument("--dpo", help="whether to convert to DPO format", type=bool, default=False)
    args = parser.parse_args()
    
    # file_list = [
    #     "30-3-100"
    #     "10-1-1000-t",
    #     "30-1-1000-t",
    #     "50-1-1000-t",
    # ]
    input_dir = "data/dev/"
    file_suffix = ".json"
    output_file = f"data/dev/alpaca_form/{args.output_name}.json"
    new_data = []
    for file in args.file_list:
        input_file = input_dir + file + file_suffix
        new_data.extend(convert_data(input_file, args.dpo))
    
    json.dump(new_data, open(output_file, "w"), ensure_ascii=False, indent=4)
    
if __name__ == "__main__":
    main()