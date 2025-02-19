import random
import os, json
import argparse
from cyaron import Graph
from src.gen_data.std import min_time_cost_to_target

def get_random_int(a, b):
    numbers = list(range(a, b + 1))
    weights = [x + 1 for x in numbers]
    return random.choices(numbers, weights=weights, k=1)[0]

def generate_tree(n):
    parent = [None] * n
    edges = []
    
    max_depth = 3
    depth = [None] * n
    depth[0] = 0
    
    for i in range(1, n):
        max_parent_depth = min(depth[i - 1] + 1, max_depth)
        
        valid_parents = [p for p in range(i) if depth[p] < max_parent_depth]
        
        if valid_parents:
            p = random.choice(valid_parents)
            parent[i] = p
            edges.append((i, p))
            depth[i] = depth[p] + 1
        else:
            p = 0
            parent[i] = p
            edges.append((i, p))
            depth[i] = 1
    
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
    edges, parent = generate_tree(n)
    num_ancestor_edges = random.randint(0, (m - (n - 1)) // 2)
    edges = add_ancestor_edges(edges, n, parent, num_ancestor_edges)
    num_cross_edges = m - len(edges)
    edges = add_cross_edges(edges, n, parent, num_cross_edges)
    results = []
    for e in edges:
        results.append((n - e[0], n - e[1]))    
    return results

def generate_abstract_workflow(graph_type, n_nodes, m_edges, group_size_range=(1, 1), time_range=(1, 50), cost_range=(1, 1)):
    edges = []
    if graph_type == "random":
        graph = Graph.DAG(n_nodes, m_edges, repeated_edges=False)
        edges = list(graph.iterate_edges())
        edges = [(e.start, e.end) for e in edges]
    elif graph_type == "tree":
        edges = generate_graph(n_nodes, m_edges)
        
    # for e in edges:
    #     print(e[0], e[1])
    
    node_mapping = {node: f"N{node}" for node in range(1, n_nodes + 1)}

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
            continue
        
        random.shuffle(predecessors)
        group_size = random.randint(group_size_range[0], group_size_range[1])
        if graph_type == "tree":
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
    
    source_nodes = set()
    target_nodes = set()
    for rule in workflow:
        source_nodes.update(rule["source"])
        target_nodes.add(rule["target"][0])
    tail_nodes = target_nodes - source_nodes
    new_target = random.choice(list(tail_nodes))
    
    return {
        "rules": workflow,
        "initial_source": source,
        "target": new_target
    }

def main():
    parser = argparse.ArgumentParser(description="Generate test data for the abstract workflow task.")
    parser.add_argument("--config", type=int, help="Number of test cases to generate", default=1000)
    parser.add_argument("--nodes", type=int, nargs=2, help="Number of nodes in the graph", default=(50, 50))
    parser.add_argument("--edge_config", type=int, help="Edge configuration", default=1)
    parser.add_argument("--graph_type", type=str, help="Type of graph to generate", default="tree")
    args = parser.parse_args()
    config = args.config
    nodes = args.nodes
    edge_config = args.edge_config
    if args.graph_type not in ["random", "tree"]:
        raise ValueError("Invalid graph type.")
    graph_type = "r" if args.graph_type == "random" else "t"
    
    test_file = f'data/dev/{nodes[1]}-{edge_config}-{config}-{graph_type}.json'
    if os.path.exists(test_file):
        user_input = input(f"File {test_file} already exists. Overwrite? (y/n) ")
        if user_input.lower() != 'y':
            print("Exiting...")
            exit()
    
    data = []
    count = 0
    while count < config:
        print(f"Generating {count + 1}/{config}...")
        n = random.randint(nodes[0], nodes[1])        
        m = 0
        if edge_config == 1:
            if args.graph_type == "random":
                m = random.randint(n * 2, n * 3)
            elif args.graph_type == "tree":
                m = random.randint(n, n * 3 // 2)
        elif edge_config == 2:
            m = random.randint(n * (n - 1) // 3, n * (n - 1) // 2)
        elif edge_config == 3:
            m = random.randint(n, n * (n - 1) // 2)
        abstract_workflow = generate_abstract_workflow(args.graph_type, n, m)
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
    
    with open(test_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data has been saved to {test_file}.")

    
if __name__ == "__main__":
    main()