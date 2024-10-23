import random
import json
import os
from cyaron import *
from src.abstask.std import min_time_cost_to_target

def generate_abstract_workflow(n_nodes, m_edges, group_size_range=(1, 3), time_range=(1, 50), cost_range=(1, 1)):
    """
    生成一个抽象的工作体系。
    
    :param n_nodes: 节点数量
    :param m_edges: 边数量
    :param group_size_range: 前驱节点分组的大小范围
    :param time_range: 转换所需时间的范围
    :return: 转换方式列表
    """
    # 使用 cyaron 生成 DAG
    graph = Graph.DAG(n_nodes, m_edges, repeated_edges=False)
    edges = list(graph.iterate_edges())
    
    # 为每个节点分配抽象名称，如 N1, N2, ...
    node_mapping = {node: f"N{node}" for node in range(1, n_nodes + 1)}
    
    # 构建前驱节点字典
    predecessors_dict = {f"N{node}": [] for node in range(1, n_nodes + 1)}
    for edge in edges:
        source = node_mapping[edge.start]
        target = node_mapping[edge.end]
        predecessors_dict[target].append(source)
    
    workflow = []
    source = []
    
    for target, predecessors in predecessors_dict.items():
        if not predecessors:
            source.append(target)
            continue  # 没有前驱节点，可能是起始节点
        
        # 随机分组前驱节点
        random.shuffle(predecessors)
        group_size = random.randint(group_size_range[0], group_size_range[1])
        groups = [predecessors[i:i + group_size] for i in range(0, len(predecessors), group_size)]
        
        for group in groups:
            transformation = {
                "source": group,
                "target": [target],
                "time": random.randint(time_range[0], time_range[1]),
                "cost": random.randint(cost_range[0], cost_range[1])
            }
            workflow.append(transformation)
    
    # 找到所有的 source 和 target 节点
    source_nodes = set()
    target_nodes = set()

    for rule in workflow:
        source_nodes.update(rule["source"])
        target_nodes.add(rule["target"][0])

    # 找到尾部节点（没有作为 source 出现的 target 节点）
    tail_nodes = target_nodes - source_nodes

    # 随机选择一个尾部节点作为目标
    new_target = random.choice(list(tail_nodes))

    return {
        "rules": workflow,
        "initial_source": source,
        "target": new_target
    }

def main():
    test_file = 'data/abstask/dev/50-1-100.json'
    if os.path.exists(test_file):
        user_input = input(f"文件 {test_file} 已存在。是否继续？(y/n): ")
        if user_input.lower() != 'y':
            print("操作已取消。")
            exit()
    # config = [50, 30, 20]
    # nodes = [(8, 10), (25, 30), (45, 50)]
    config = [100]
    nodes = [(45, 50)]

    data = []
    count = 0
    for i in range(len(config)):
        for _ in range(config[i]):
            count += 1
            n = random.randint(nodes[i][0], nodes[i][1])
            # m = random.randint(n * (n - 1) // 3, n * (n - 1) // 2)
            m = random.randint(n * 2, n * 3)
            abstract_workflow = generate_abstract_workflow(n, m)
            min_time, min_cost, path_count = min_time_cost_to_target(abstract_workflow)
            item = {
                "id": count,
                "node_count": n,
                "edge_count": m,
                "question": abstract_workflow,
                "answer": min_time,
                "min_cost": min_cost,
                "path_count": path_count
            }
            data.append(item)
    
    with open(test_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # print(json.dumps(abstract_workflow, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()