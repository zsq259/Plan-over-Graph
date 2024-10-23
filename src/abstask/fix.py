import json
from src.abstask.std import min_time_cost_to_target

def fix(input_file):
    data = json.load(open(input_file, "r"))
    for question in data:
        task_info = question["question"]
        time, cost, path_count = min_time_cost_to_target(task_info)
        if question['answer'] != time:
            print(f"id {question['id']} Answer Expected: {question['answer']}, Got: {time}")
            data[question['id'] - 1]['answer'] = time
        if question['min_cost'] != cost:
            print(f"id {question['id']} Cost Expected: {question['min_cost']}, Got: {cost}")
            data[question['id'] - 1]['min_cost'] = cost
        if question['path_count'] != path_count:
            print(f"id {question['id']} Path Count Expected: {question['path_count']}, Got: {path_count}")
            data[question['id'] - 1]['path_count'] = path_count
    json.dump(data, open(input_file, "w"), ensure_ascii=False, indent=4)
    
def main():
    input_file = "/home/zhangsq/1/test/data/abstask/dev/10-2-100.json"
    fix(input_file)

if __name__ == "__main__":
    main()