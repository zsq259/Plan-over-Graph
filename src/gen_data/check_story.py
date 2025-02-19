import json
file_path = "data/dev/10-1-100-s.json"

with open(file_path, "r") as f:
    data = json.load(f)

results = []

for d in data:
    rule_num = len(d["question"]["rules"])
    
    day_count = d["story"].count("day")
    cost_count = d["story"].count("cost")
    if rule_num != day_count and rule_num != cost_count:
        print(f"id: {d["id"]}, Rule num: {rule_num}, day count: {day_count}, cost count: {cost_count}")
        
    if abs(rule_num - day_count) < 3 or abs(rule_num - cost_count) < 3:
        results.append(d)
        
print(f"Total: {len(data)}, Filtered: {len(results)}")
output_file = "data/dev/10-1-100-s-filtered.json"
with open(output_file, "w") as f:
    json.dump(results, f, indent=4)       