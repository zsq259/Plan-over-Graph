import json
import os
import argparse

parser = argparse.ArgumentParser(description="Data statistics")
parser.add_argument("--file_name", type=str, default=None, help="The file name to analyze")
args = parser.parse_args()

def collect_data(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    average_time_ratio = 0
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
        average_time_ratio += time_ratio
        
    average_time_ratio /= len(data)
    average_edge_num /= len(data)
    average_rule_num /= len(data)
    
    return average_time_ratio, average_edge_num, average_rule_num


file_dir = "data/dev/test"
file_names = []
if args.file_name:
    file_names.append(args.file_name)
else:
    for file_name in os.listdir(file_dir):
        if file_name.endswith(".json"):
            file_names.append(file_name.removesuffix(".json"))            
    
# save statistic in a table
data_statistics = []
for file_name in file_names:
    file_path = f"data/dev/test/{file_name}.json"
    average_time_ratio, average_edge_num, average_rule_num = collect_data(file_path)
    data_statistics.append([file_name, average_time_ratio])
    
data_statistics.sort(key=lambda x: x[0])
print("File Name\tAverage Time Ratio")
for d in data_statistics:
    print(f"{d[0]}\t{d[1]:.2f}")