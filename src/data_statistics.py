import json
import argparse

parser = argparse.ArgumentParser(description="Data statistics")
parser.add_argument("--file_name", type=str, required=True, default="50-1-100", help="The file name to analyze")
args = parser.parse_args()

file_path = f"data/dev/{args.file_name}.json"

with open(file_path, "r") as f:
    data = json.load(f)

average_time = 0
average_edge_num = 0
average_rule_num = 0

for d in data:
    time_sum = 0
    average_edge_num += d["edge_count"]
    average_rule_num += len(d["question"]["rules"])
    for node in d["answer"]:
        source = node["source"]
        target = node["target"]
        for rule in d["question"]["rules"]:
            if rule["source"] == source and rule["target"] == target:
                time_sum += rule["time"]
                break
    time_ratio = d["min_time"] / time_sum
    print(f"Time ratio: {time_ratio:.2f}")
    average_time += time_ratio
    
average_time /= len(data)
average_edge_num /= len(data)
average_rule_num /= len(data)
print(f"Average time ratio: {average_time:.2f}")
print(f"Average edge number: {average_edge_num:.2f}")
print(f"Average rule number: {average_rule_num:.2f}")