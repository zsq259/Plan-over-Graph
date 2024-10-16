def min_time_to_target(task_info):
    rules = task_info["rules"]
    initial_source = task_info["initial_source"]
    target = task_info["target"]

    time_map = {source: 0 for source in initial_source}
    
    def get_time(node):
        return time_map.get(node, float('inf'))
    
    updated = True
    while updated:
        updated = False
        for rule in rules:
            source_time = max(get_time(src) for src in rule["source"])
            new_time = source_time + rule["time"]
            for target_node in rule["target"]:
                if new_time < get_time(target_node):
                    time_map[target_node] = new_time
                    updated = True

    return time_map.get(target, float('inf'))

def main():
    # 输入的任务信息
    task_info = {
        "rules": [
            {
                "source": ["N1"],
                "target": ["N2"],
                "time": 3
            },
            {
                "source": ["N6"],
                "target": ["N3"],
                "time": 4
            },
            {
                "source": ["N2", "N3"],
                "target": ["N4"],
                "time": 2
            },
            {
                "source": ["N4"],
                "target": ["N5"],
                "time": 1
            },
            {
                "source": ["N2"],
                "target": ["N5"],
                "time": 5
            }
        ],
        "initial_source": ["N1", "N6"],
        "target": "N5"
    }

    # 计算最短时间
    min_time = min_time_to_target(task_info)
    print(f"到达目标 {task_info['target']} 的最短时间是 {min_time}")

if __name__ == "__main__":
    main()