import math

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
    # result = [rule for rule in rules if all(in_degree[source] == 0 for source in rule["source"])]
    result = []
    exist_nodes = []
    # print(queue)
    while queue:
        node = queue.pop(0)
        exist_nodes.append(node)
        # print(f"node = {node}")
        # for rule in rules:
        #     if node in rule["source"]:
        #         if all(source in exist_nodes for source in rule["source"]):
        #             print(f"rule = {rule}")
        #             result.append(rule)
        
        for target in graph[node]:
            in_degree[target] -= 1
            if in_degree[target] == 0:
                queue.append(target)
                for rule in rules:
                    if target in rule["target"]:
                        if all(source in exist_nodes for source in rule["source"]):
                            # print(f"rule = {rule}")
                            result.append(rule)
    # print("------------------------")
                
    return result

def min_time_cost_to_target(task_info: dict) -> int:
    rules = task_info["rules"]
    initial_source = task_info["initial_source"]
    target = task_info["target"]

    time_map = {source: 0 for source in initial_source}
    cost_map = {source: 0 for source in initial_source}
    rules_map = {source: [] for source in initial_source}
    path_count = {source: 1 for source in initial_source}
    
    def get_time(node):
        return time_map.get(node, float('inf'))
    def get_cost(node):
        return cost_map.get(node, float('inf'))
    def get_rules(node):
        return rules_map.get(node, [])
    def make_hashable(d):
        """递归地将字典中的列表转换为元组，以便进行哈希操作"""
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
            r_tuple = make_hashable(r)  # 将字典转换为可哈希的对象
            if r_tuple not in seen:
                seen.add(r_tuple)
                unique_rules.append(r)

        return unique_rules


    
    # rules = sort_rules_by_topology(task_info)
    sorted_rules = topological_sort(rules)
    
    # print(len(rules))
    for rule in sorted_rules:
        if not all(source in time_map for source in rule["source"]):
            # print(sorted_rules)
            # print(rule)
            raise ValueError("Invalid rule")
        source_time = max(get_time(src) for src in rule["source"])
        new_time = source_time + rule["time"]
        # new_rules = list(set().union(*(get_rules(src) for src in rule["source"])))
        # new_rules.append(rule)
        # new_rules = list(set(new_rules))
        new_rules = get_new_rules(rule)
        new_cost = sum(rule["cost"] for rule in new_rules)
        new_path_count = math.prod(path_count[src] for src in rule["source"])
        for target_node in rule["target"]:
            if new_time < get_time(target_node):
                time_map[target_node] = new_time
                rules_map[target_node] = new_rules
                cost_map[target_node] = new_cost
            elif new_time == get_time(target_node):
                if new_cost < get_cost(target_node):
                    cost_map[target_node] = new_cost
                    rules_map[target_node] = new_rules
            if target_node not in path_count:
                path_count[target_node] = new_path_count
            else:
                path_count[target_node] += new_path_count
            # print(f"cost_map[{target_node}] = {cost_map[target_node]}")
            # print(f"path_count[{target_node}] = {path_count[target_node]}")

    return time_map.get(target, float('inf')), cost_map.get(target, float('inf')), path_count.get(target, 0)

def main():
    # 输入的任务信息
    task_info = {
                "rules": [
                    {
                        "source": [
                            "N1"
                        ],
                        "target": [
                            "N2"
                        ],
                        "time": 32,
                        "cost": 1
                    },
                    {
                        "source": [
                            "N1",
                            "N2"
                        ],
                        "target": [
                            "N3"
                        ],
                        "time": 16,
                        "cost": 1
                    },
                    {
                        "source": [
                            "N1",
                            "N3"
                        ],
                        "target": [
                            "N4"
                        ],
                        "time": 31,
                        "cost": 1
                    },
                    {
                        "source": [
                            "N3",
                            "N2",
                            "N1"
                        ],
                        "target": [
                            "N5"
                        ],
                        "time": 38,
                        "cost": 1
                    },
                    {
                        "source": [
                            "N4"
                        ],
                        "target": [
                            "N5"
                        ],
                        "time": 23,
                        "cost": 1
                    },
                    {
                        "source": [
                            "N2",
                            "N1",
                            "N3"
                        ],
                        "target": [
                            "N6"
                        ],
                        "time": 3,
                        "cost": 1
                    },
                    {
                        "source": [
                            "N5"
                        ],
                        "target": [
                            "N6"
                        ],
                        "time": 46,
                        "cost": 1
                    },
                    {
                        "source": [
                            "N6",
                            "N3",
                            "N4"
                        ],
                        "target": [
                            "N7"
                        ],
                        "time": 13,
                        "cost": 1
                    },
                    {
                        "source": [
                            "N5",
                            "N2"
                        ],
                        "target": [
                            "N7"
                        ],
                        "time": 36,
                        "cost": 1
                    },
                    {
                        "source": [
                            "N3",
                            "N7",
                            "N4"
                        ],
                        "target": [
                            "N8"
                        ],
                        "time": 16,
                        "cost": 1
                    }
                ],
                "initial_source": [
                    "N1"
                ],
                "target": "N8"
            }

    # 计算最短时间
    min_time, min_cost, path_count = min_time_cost_to_target(task_info)
    print(f"到达目标 {task_info['target']} 的最短时间是 {min_time}")
    print(f"到达目标 {task_info['target']} 的最小成本是 {min_cost}")
    print(f"到达目标 {task_info['target']} 的路径数量是 {path_count}")

if __name__ == "__main__":
    main()