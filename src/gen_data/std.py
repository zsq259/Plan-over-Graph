import math, json

def topological_sort(rules: list) -> list:
    graph = {}
    in_degree = {}
    for rule in rules:
        for source in rule["source"]:
            if source not in graph:
                graph[source] = []
                in_degree[source] = 0
        for target in rule["target"]:
            if target not in graph:
                graph[target] = []
                in_degree[target] = 0
        for source in rule["source"]:
            for target in rule["target"]:
                graph[source].append(target)
                in_degree[target] += 1
    queue = [node for node in in_degree if in_degree[node] == 0]
    result = []
    exist_nodes = []
    while queue:
        node = queue.pop(0)
        exist_nodes.append(node)
        for target in graph[node]:
            in_degree[target] -= 1
            if in_degree[target] == 0:
                queue.append(target)
                for rule in rules:
                    if target in rule["target"]:
                        if all(source in exist_nodes for source in rule["source"]):
                            result.append(rule)
    return result

def convert_rules(rules: list) -> list:
    converted_rules = []
    for rule in rules:
        converted_rule = {
            "name": f"Subtask{len(converted_rules) + 1}",
            "source": rule["source"],
            "target": rule["target"],
            "dependencies": []
        }
        converted_rules.append(converted_rule)
    for rule in converted_rules:
        for src in rule["source"]:
            for dep_rule in converted_rules:
                if src in dep_rule["target"]:
                    rule["dependencies"].append(dep_rule["name"])
    return converted_rules

def min_time_cost_to_target(task_info: dict) -> int:
    rules = task_info["rules"]
    initial_source = task_info["initial_source"]
    target = task_info["target"]

    time_map = {source: 0 for source in initial_source}
    cost_map = {source: 0 for source in initial_source}
    rules_map = {source: [] for source in initial_source}
    path_count = {source: 1 for source in initial_source}
    
    second_rules_map = {source: [] for source in initial_source}
    second_time_map = {source: 0 for source in initial_source}

    def get_time(node):
        return time_map.get(node, float('inf'))
    def get_cost(node):
        return cost_map.get(node, float('inf'))
    def get_rules(node):
        return rules_map.get(node, [])
    def make_hashable(d):
        if isinstance(d, dict):
            return frozenset((k, make_hashable(v)) for k, v in d.items())
        elif isinstance(d, list):
            return tuple(make_hashable(i) for i in d)
        return d

    def get_new_rules(rule):
        new_rules = []
        for src in rule["source"]:
            new_rules.extend(get_rules(src))
        new_rules.append(rule)
        unique_rules = []
        seen = set()
        for r in new_rules:
            r_tuple = make_hashable(r)
            if r_tuple not in seen:
                seen.add(r_tuple)
                unique_rules.append(r)
        return unique_rules
    
    def get_second_new_rules(rule):
        new_rules = []
        for src in rule["source"]:
            new_rules.extend(second_rules_map.get(src, []))
        new_rules.append(rule)
        unique_rules = []
        seen = set()
        for r in new_rules:
            r_tuple = make_hashable(r)
            if r_tuple not in seen:
                seen.add(r_tuple)
                unique_rules.append(r)
        return unique_rules

    sorted_rules = topological_sort(rules)
    
    for rule in sorted_rules:
        if not all(source in time_map for source in rule["source"]):
            raise ValueError("Invalid rule")
        source_time = max(get_time(src) for src in rule["source"])
        new_time = source_time + rule["time"]
        new_rules = get_new_rules(rule)
        new_cost = sum(rule["cost"] for rule in new_rules)
        new_path_count = math.prod(path_count[src] for src in rule["source"])
        for target_node in rule["target"]:
            if new_time < get_time(target_node):
                second_time_map[target_node] = get_time(target_node)
                second_rules_map[target_node] = get_rules(target_node)

                time_map[target_node] = new_time
                rules_map[target_node] = new_rules
                cost_map[target_node] = new_cost
            elif new_time == get_time(target_node):
                if new_cost < get_cost(target_node):
                    second_time_map[target_node] = get_time(target_node)
                    second_rules_map[target_node] = get_rules(target_node)

                    cost_map[target_node] = new_cost
                    rules_map[target_node] = new_rules
                else:
                    second_time_map[target_node] = new_time
                    second_rules_map[target_node] = new_rules
            else:
                second_time_map[target_node] = new_time
                second_rules_map[target_node] = new_rules


            if target_node not in path_count:
                path_count[target_node] = new_path_count
            else:                
                path_count[target_node] += new_path_count            
    
    converted_rules = convert_rules(get_rules(target))
    second_best_converted_rules = convert_rules(second_rules_map.get(target, []))
    return time_map.get(target, float('inf')), cost_map.get(target, float('inf')), path_count.get(target, 0), converted_rules, second_best_converted_rules, second_time_map[target]

def main():
    task_info = {"rules": [{ "source": ["N1"], "target": ["N2"], "time": 3, "cost": 1 }, { "source": ["N3"], "target": ["N4"], "time": 3, "cost": 1 }, { "source": ["N2"], "target": ["N5"], "time": 4, "cost": 1 }, { "source": ["N4", "N5"], "target": ["N6"], "time": 2, "cost": 1 }, { "source": ["N2"], "target": ["N6"], "time": 8, "cost": 1 }, { "source": ["N7"], "target": ["N8"], "time": 5, "cost": 1 }, { "source": ["N4"], "target": ["N8"], "time": 1, "cost": 1 }, { "source": ["N6", "N8"], "target": ["N9"], "time": 2, "cost": 1 }, { "source": ["N1"], "target": ["N9"], "time": 15, "cost": 1 }, ], "initial_source": ["N1", "N3", "N7"], "target": "N9"}

    min_time, min_cost, path_count, plan, feasible, feasible_time = min_time_cost_to_target(task_info)
    print(plan)
    print(feasible)
    print(f"to target {task_info['target']} min time is {min_time}")
    print(f"to target {task_info['target']} min cost is {min_cost}")
    print(f"to target {task_info['target']} path count is {path_count}")

if __name__ == "__main__":
    main()