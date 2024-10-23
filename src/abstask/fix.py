import json
from src.abstask.std import min_time_cost_to_target

def fix(input_file):
    data = json.load(open(input_file, "r"))
    new_data = []
    for question in data:
        task_info = question["question"]
        time, cost, path_count, plan = min_time_cost_to_target(task_info)
        question["min_time"] = time
        question["answer"] = plan
        new_data.append(question)    
    json.dump(new_data, open(input_file, "w"), ensure_ascii=False, indent=4)
    
def main():
    input_file = "/home/zhangsq/1/test/data/abstask/dev/50-1-100.json"
    fix(input_file)

if __name__ == "__main__":
    main()