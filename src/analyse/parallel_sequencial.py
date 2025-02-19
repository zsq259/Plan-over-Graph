import json
import argparse

def get_excution_ratio(data):
    results = []
    invalid_subtask_count = 0
    invalid_dependency_count = 0
    success_count = 0
    optimal_count = 0
    time_ratios = []
    cost_ratios = []
    for d in data:
        rules = d['question']['question']["rules"]
        plan = d["plan"]
        if not d['result'] or not d['result'][0]:
            flag = False
            time_ratios.append(4)
            cost_ratios.append(4)
            if not plan or not isinstance(plan, list):
                invalid_subtask_count += 1
                continue
            for p in plan:
                flag1 = False
                for r in rules:
                    if sorted(p['source']) == sorted(r['source']) and sorted(p['target']) == sorted(r['target']):
                        flag1 = True
                        break
                if not flag1:
                    flag = True
                    break
            if flag:
                invalid_subtask_count += 1
            else:
                invalid_dependency_count += 1
            continue
        parallel_time = d["result"][0]
        success_count += 1
        if parallel_time == d['question']['min_time']:
            optimal_count += 1
        sequential_time = 0
        for p in plan:
            for r in rules:
                if sorted(p['source']) == sorted(r['source']) and sorted(p['target']) == sorted(r['target']):
                    sequential_time += r['time']
                    break
        ratio = parallel_time / sequential_time
        results.append(ratio)

        time_ratio = d['result'][0] / d['question']['min_time']
        cost_ratio = d['result'][1] / d['question']['min_cost']
        time_ratios.append(time_ratio)
        cost_ratios.append(cost_ratio)

    ave_time_ratio = sum(time_ratios) / len(time_ratios)
    ave_cost_ratio = sum(cost_ratios) / len(cost_ratios)

    # return average ratio
    return sum(results) / len(results), (invalid_subtask_count, invalid_dependency_count), (success_count, optimal_count), (ave_time_ratio, ave_cost_ratio)

def get_model_results(model_name):
    test_points = [10, 20, 30, 40, 50]
    # test_points = [10, 30]
    test_cates = ["r", "t"]
    file_dir = f"data/result/{model_name}/"
    results = {}
    invalid_subtask_count = 0
    invalid_dependency_count = 0
    success_counts = []
    optimal_counts = []
    ave_time_ratios = []
    ave_cost_ratios = []
    for point in test_points:
        success_count = 0
        optimal_count = 0
        time_ratio = 0
        cost_ratio = 0
        for cate in test_cates:
            file_path = f"{file_dir}{point}-1-100-{cate}-output.json"
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            ratio, wrong_case_rate, success_optimal_count, ave_time_cost_ratio = get_excution_ratio(data)
            invalid_subtask_count += wrong_case_rate[0]
            invalid_dependency_count += wrong_case_rate[1]
            success_count += success_optimal_count[0]
            optimal_count += success_optimal_count[1]
            time_ratio += ave_time_cost_ratio[0]
            cost_ratio += ave_time_cost_ratio[1]
            # store 2 decimal places
            ratio = round(ratio, 2)
            results[f"{point}-{cate}"] = ratio
        success_counts.append(success_count)
        optimal_counts.append(optimal_count)
        ave_time_ratios.append(time_ratio / 2)
        ave_cost_ratios.append(cost_ratio / 2)
    
    print(f"Model {model_name}")
    # print(f"Invalid subtask count: {invalid_subtask_count}")
    # print(f"Invalid dependency count: {invalid_dependency_count}")

    def normalize(data):
        max_data = max(data)
        min_data = min(data)
        return [(d - min_data) / (max_data - min_data) for d in data]
    test_points = normalize(test_points)
    success_counts = normalize(success_counts)
    optimal_counts = normalize(optimal_counts)
    ave_time_ratios = normalize(ave_time_ratios)
    ave_cost_ratios = normalize(ave_cost_ratios)

    # compute the Pearson Correlation Coefficient for success and optimal counts with node count

    from scipy.stats import pearsonr
    # store 2 decimal places
    corr, _ = pearsonr(test_points, success_counts)
    print(f"Pearson correlation coefficient for success counts and node counts: {round(corr, 2)}")
    corr, _ = pearsonr(test_points, optimal_counts)
    print(f"Pearson correlation coefficient for optimal counts and node counts: {round(corr, 2)}")
    corr, _ = pearsonr(test_points, ave_time_ratios)
    print(f"Pearson correlation coefficient for average time ratios and node counts: {round(corr, 2)}")
    corr, _ = pearsonr(test_points, ave_cost_ratios)
    print(f"Pearson correlation coefficient for average cost ratios and node counts: {round(corr, 2)}")

    # compute the gradient of the line of best fit for success and optimal counts with node count
    import numpy as np
    success_counts = np.array(success_counts)
    optimal_counts = np.array(optimal_counts)
    m, c = np.polyfit(test_points, success_counts, 1)
    print(f"Slopes of the line of best fit for success counts and node counts: {round(m, 2)}")
    m, c = np.polyfit(test_points, optimal_counts, 1)
    print(f"Slopes of the line of best fit for optimal counts and node counts: {round(m, 2)}")
    m, c = np.polyfit(test_points, ave_time_ratios, 1)
    print(f"Slopes of the line of best fit for average time ratios and node counts: {round(m, 2)}")
    m, c = np.polyfit(test_points, ave_cost_ratios, 1)
    print(f"Slopes of the line of best fit for average cost ratios and node counts: {round(m, 2)}")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=str, nargs='+', required=True, help="List of model names")
    args = parser.parse_args()

    for model in args.models:
        get_model_results(model)

if __name__ == "__main__":
    main()