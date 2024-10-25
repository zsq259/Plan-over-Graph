import json
from template.planner.abstask_cost_plan import instruction, example

def convert_task_form(task):
    prompt = instruction.format(example=example, task=task['question'])
    output = str(task['answer'])
    new_task = {"instruction": prompt, "output": output}
    return new_task

def convert_data(input_file, output_file):
    data = json.load(open(input_file, "r"))
    new_data = []
    for task in data:
        new_task = convert_task_form(task)
        new_data.append(new_task)
    return new_data
    # json.dump(new_data, open(output_file, "w"), ensure_ascii=False, indent=4)
        
def main():
    file_list = [
        "10-1-100",
        "10-2-100",
        "30-1-100",
        "50-1-100",
    ]
    input_dir = "/home/zhangsq/1/test/data/abstask/dev/"
    file_suffix = ".json"
    output_file = "/home/zhangsq/1/test/data/abstask/dev/alpaca_form/abstask.json"
    new_data = []
    for file in file_list:
        input_file = input_dir + file + file_suffix
        new_data.extend(convert_data(input_file, output_file))
    
    json.dump(new_data, open(output_file, "w"), ensure_ascii=False, indent=4)
    
if __name__ == "__main__":
    main()