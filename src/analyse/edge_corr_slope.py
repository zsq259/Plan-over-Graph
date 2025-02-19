import json, os
import argparse

def analyze_file(file_path):
    if not os.path.exists(file_path):
        print(f"file not found: {file_path}")
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []
    for item in data:
        task_id = item["question"]["id"]
        node_count = item["question"]["node_count"]
        edge_count = item["question"]["edge_count"]
        answer_time = item["question"]["min_time"]
        min_cost = item["question"]["min_cost"]
        result = item.get("result")
        result_time = None if result is None else result[0]
        result_cost = None if result is None else result[1]

        time_ratio = None if result_time is None else result_time / answer_time
        cost_ratio = None if result_cost is None else result_cost / min_cost
        status = "Failure"
        if result_time and result_cost:
            status = "Optimal" if (result_time == answer_time and result_cost == min_cost) else "Feasible"
        
        results.append({
            "Node Count": node_count,
            "Edge Count": edge_count,
            "Time Ratio": time_ratio,
            "Cost Ratio": cost_ratio,
            "Status": status
        })

    return results

def get_model_results(model_name):
    # test_points = [10, 20, 30, 40, 50]
    test_points = [10, 30]
    file_dir = f"data/result/{model_name}/"
    print(f"Model {model_name}: ")
    
    for point in test_points:
    
        file_path = f"{file_dir}{point}-3-1000-r-output.json"
        results = analyze_file(file_path)
        print("Node Count: ", point)
        segment = 1 if point == 10 else 10
        max_edge_count = max([r["Edge Count"] for r in results])
        min_edge_count = min([r["Edge Count"] for r in results])
        seg_sum = max_edge_count // segment + 1
        min_seg_idx = min_edge_count // segment
        success_rates = [0] * seg_sum
        optimal_rates = [0] * seg_sum
        time_ratios = [0] * seg_sum
        cost_ratios = [0] * seg_sum
        seg_counts = [0] * seg_sum
        for r in results:
            seg_idx = r["Edge Count"] // segment
            seg_counts[seg_idx] += 1
            success_rates[seg_idx] += 1 if r["Status"] == "Feasible" or r["Status"] == "Optimal" else 0
            optimal_rates[seg_idx] += 1 if r["Status"] == "Optimal" else 0
            time_ratios[seg_idx] += r["Time Ratio"] if r["Time Ratio"] else 4
            cost_ratios[seg_idx] += r["Cost Ratio"] if r["Cost Ratio"] else 4

        for i in range(seg_sum):
            if seg_counts[i] == 0:
                continue
            
            # time_ratios[i] /= success_rates[i]
            # cost_ratios[i] /= success_rates[i]
            time_ratios[i] /= seg_counts[i]
            cost_ratios[i] /= seg_counts[i]
            success_rates[i] /= seg_counts[i]
            optimal_rates[i] /= seg_counts[i]
            
        
        edge_segments = [i * segment for i in range(seg_sum)]

        edge_segments = edge_segments[min_seg_idx:]
        success_rates = success_rates[min_seg_idx:]
        optimal_rates = optimal_rates[min_seg_idx:]
        time_ratios = time_ratios[min_seg_idx:]
        cost_ratios = cost_ratios[min_seg_idx:]
        # Normalization
        def normalize(data):
            # import numpy as np
            # data = np.array(data)
            # mean = np.mean(data)
            # std = np.std(data)
            # return ((data - mean) / std).tolist()
            max_data = max(data)
            min_data = min(data)
            return [(d - min_data) / (max_data - min_data) for d in data]
        
        edge_segments = normalize(edge_segments)
        success_rates = normalize(success_rates)
        optimal_rates = normalize(optimal_rates)
        time_ratios = normalize(time_ratios)
        cost_ratios = normalize(cost_ratios)
            

        # compute the Pearson Correlation Coefficient
        from scipy.stats import pearsonr
        # print(edge_segments)
        # print(success_rates)
        success_corr, _ = pearsonr(edge_segments, success_rates)
        print("Success Rate Correlation: ", round(success_corr, 2))
        optimal_corr, _ = pearsonr(edge_segments, optimal_rates)
        print("Optimal Rate Correlation: ", round(optimal_corr, 2))
        time_corr, _ = pearsonr(edge_segments, time_ratios)
        print("Time Ratio Correlation: ", round(time_corr, 2))
        cost_corr, _ = pearsonr(edge_segments, cost_ratios)
        print("Cost Ratio Correlation: ", round(cost_corr, 2))

        # compute the gradient
        # print(edge_segments)
        # print(time_ratios)

        import numpy as np
        success_grad = np.polyfit(edge_segments, success_rates, 1)[0]
        print("Success Rate Slope: ", round(success_grad, 2))
        optimal_grad = np.polyfit(edge_segments, optimal_rates, 1)[0]
        print("Optimal Rate Slope: ", round(optimal_grad, 2))
        time_grad = np.polyfit(edge_segments, time_ratios, 1)[0]
        print("Time Ratio Slope: ", round(time_grad, 2))
        cost_grad = np.polyfit(edge_segments, cost_ratios, 1)[0]
        print("Cost Ratio Slope: ", round(cost_grad, 2)) 
        print("\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=str, nargs='+', required=True, help="List of model names")
    args = parser.parse_args()

    for model in args.models:
        get_model_results(model)

if __name__ == "__main__":
    main()