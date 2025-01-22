import random
import os, json
import argparse
from cyaron import Graph
from src.std import min_time_cost_to_target

def get_random_int(a, b):
    numbers = list(range(a, b + 1))
    weights = [x + 1 for x in numbers]
    return random.choices(numbers, weights=weights, k=1)[0]

# def generate_tree(n):
#     parent = [None] * n
#     edges = []
#     for i in range(1, n):
#         p = get_random_int(max(i - n // 3, 0), i - 1)
#         parent[i] = p
#         edges.append((i, p))
#     return edges, parent

def generate_tree(n):
    parent = [None] * n
    edges = []
    
    # 平衡分叉的父节点选择策略
    # 设定一个最大深度阈值，避免树过深
    max_depth = 3  # 可以根据需要调整
    depth = [None] * n  # 存储每个节点的深度
    depth[0] = 0
    
    for i in range(1, n):
        # 计算当前节点的深度，限制深度范围
        max_parent_depth = min(depth[i - 1] + 1, max_depth)  # 最大父节点深度限制
        
        # 选择父节点时，确保父节点深度不超过一定阈值
        # 选择父节点范围：根据节点的深度动态调整
        valid_parents = [p for p in range(i) if depth[p] < max_parent_depth]
        
        if valid_parents:
            p = random.choice(valid_parents)  # 从有效父节点中随机选择
            parent[i] = p
            edges.append((i, p))
            depth[i] = depth[p] + 1  # 当前节点深度 = 父节点深度 + 1
        else:
            p = 0  # 如果没有合适的父节点，回到根节点
            parent[i] = p
            edges.append((i, p))
            depth[i] = 1  # 根节点的深度为 1
    
    return edges, parent

def add_ancestor_edges(edges, n, parent, num_ancestor_edges):
    num = 0
    while num < num_ancestor_edges:
        u = get_random_int(1, n - 1)
        p = parent[u]
        count = 0
        while p is not None:
            count += 1
            p = parent[p]
        if count == 0:
            continue
        t = count - 1 - get_random_int(0, count - 1)
        p = parent[u]
        while t > 0:
            p = parent[p]
            t -= 1
        if (u, p) not in edges:
            edges.append((u, p))
            num += 1
        
    return edges

def is_cross_nodes(edges, n, u, v, parent):
    if u < v:
        u, v = v, u
    if (u, v) in edges:
        return False
    while u is not None and u != v:
        u = parent[u]
    return u is None

def add_cross_edges(edges, n, parent, num_cross_edges):
    nodes = list(range(n))
    for _ in range(num_cross_edges):
        u = get_random_int(0, n - 1)
        v = get_random_int(0, n - 1)
        while not is_cross_nodes(edges, n, u, v, parent):
            u = get_random_int(0, n - 1)
            v = get_random_int(0, n - 1)
        if u < v:
            u, v = v, u
        edges.append((u, v))
    return edges

def generate_graph(n, m):
    # print("n", n, "m", m)
    edges, parent = generate_tree(n)

    num_ancestor_edges = random.randint(0, (m - (n - 1)) // 2)  # 至少有 n-1 条边是树的边
    # num_ancestor_edges //= 2
    # print("num_ancestor_edges", num_ancestor_edges)
    edges = add_ancestor_edges(edges, n, parent, num_ancestor_edges)

    num_cross_edges = m - len(edges)
    # print("num_cross_edges", num_cross_edges)
    edges = add_cross_edges(edges, n, parent, num_cross_edges)

    results = []
    for e in edges:
        results.append((n - e[0], n - e[1]))    
    return results

def generate_abstract_workflow(n_nodes, m_edges, group_size_range=(1, 1), time_range=(1, 50), cost_range=(1, 1)):
    """
    生成一个抽象的工作体系。
    
    :param n_nodes: 节点数量
    :param m_edges: 边数量
    :param group_size_range: 前驱节点分组的大小范围
    :param time_range: 转换所需时间的范围
    :return: 转换方式列表
    """
    # 使用 cyaron 生成 DAG
    # graph = Graph.DAG(n_nodes, m_edges, repeated_edges=False)
    # edges = list(graph.iterate_edges())
    # edges = [(e.start, e.end) for e in edges]
    edges = generate_graph(n_nodes, m_edges)
    # for e in edges:
    #     print(e[0], e[1])
    
    # print("fuck")
    # 为每个节点分配唯一的名称
    # node_mapping = {node: f"Node_{uuid.uuid4().hex}" for node in range(1, n_nodes + 1)}
    node_mapping = {node: f"N{node}" for node in range(1, n_nodes + 1)}

    # 构建前驱节点字典
    predecessors_dict = {node_mapping[node]: [] for node in range(1, n_nodes + 1)}
    for edge in edges:
        source = node_mapping[edge[0]]
        target = node_mapping[edge[1]]
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
        group_size = max(len(predecessors) * 2 // 3, 1)
        groups = [predecessors[i:i + group_size] for i in range(0, len(predecessors), group_size)]
        
        for group in groups:
            transformation = {
                "id": len(workflow),
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
    parser = argparse.ArgumentParser(description="生成测试数据")
    parser.add_argument("--config", type=int, help="生成的数据量", default=100)
    parser.add_argument("--nodes", type=int, nargs=2, help="节点数量范围", default=(50, 50))
    parser.add_argument("--edge_config", type=int, help="边的配置", default=1)
    args = parser.parse_args()
    config = args.config
    nodes = args.nodes
    edge_config = args.edge_config
    # config = 1000
    # nodes = (50, 50)
    # edge_config = 1
    test_file = f'data/dev/{nodes[1]}-{edge_config}-{config}-t.json'
    # test_file = "1"
    if os.path.exists(test_file):
        user_input = input(f"文件 {test_file} 已存在。是否继续？(y/n): ")
        if user_input.lower() != 'y':
            print("操作已取消。")
            exit()
    # config = [50, 30, 20]
    # nodes = [(8, 10), (25, 30), (45, 50)]
    
    data = []
    count = 0
    while count < config:
        print(f"Generating {count + 1}/{config}...")
        n = random.randint(nodes[0], nodes[1])        
        m = 0
        if edge_config == 1:
            m = random.randint(n, n * 3 // 2)
        elif edge_config == 2:
            m = random.randint(n * (n - 1) // 3, n * (n - 1) // 2)
        elif edge_config == 3:
            m = random.randint(n, n * (n - 1) // 2)
        abstract_workflow = generate_abstract_workflow(n, m)
        min_time, min_cost, path_count, plan, feasible, feasible_time = min_time_cost_to_target(abstract_workflow)
        if path_count <= 1 or len(feasible) == 0:
            continue
        count += 1
        item = {
            "id": count,
            "node_count": n,
            "edge_count": m,
            "question": abstract_workflow,
            "answer": plan,
            "feasible": feasible,
            "min_time": min_time,
            "feasible_time": feasible_time,
            "min_cost": min_cost,
            "path_count": path_count
        }
        data.append(item)
    
    # for k, v in data[0].items():
    #     print(k, v)
    #     print()
    with open(test_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data has been saved to {test_file}.")

    # print(data[0]["question"])

if __name__ == "__main__":
    main()