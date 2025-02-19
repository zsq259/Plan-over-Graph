import os
import json
import argparse
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

def process_model_data(model, test_points):
    success_rates = []
    optimal_rates = []
    
    for point in test_points:
        file_names = [f"{point}-1-100-r-output.json", f"{point}-1-100-t-output.json"]
        total_count = 0
        success_count = 0
        optimal_count = 0
        
        for file_name in file_names:
            file_path = os.path.join("data", "result", model, file_name)
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue
                
                for item in data:
                    total_count += 1
                    model_ans = None
                    if "result" in item and isinstance(item["result"], list) and len(item["result"]) > 0:
                        model_ans = item["result"][0]
                    optimal_ans = item.get("question", {}).get("min_time", None)
                    
                    if model_ans is not None and str(model_ans).strip() != "":
                        success_count += 1
                        if str(model_ans) == str(optimal_ans):
                            optimal_count += 1
            else:
                continue
        
        if total_count > 0:
            success_rate = success_count / total_count
            optimal_rate = optimal_count / total_count
        else:
            success_rate = 0
            optimal_rate = 0
        
        success_rates.append(success_rate)
        optimal_rates.append(optimal_rate)
    
    return success_rates, optimal_rates

def main():
    plt.style.use('seaborn-v0_8-whitegrid')
    
    parser = argparse.ArgumentParser(description="Plot model performance vs. number of test points")
    parser.add_argument("--models", nargs="+", required=True, help="List of model names to evaluate")
    args = parser.parse_args()

    test_points = [10, 20, 30, 40, 50]

    model_success = {}
    model_optimal = {}
    for model in args.models:
        s_rate, o_rate = process_model_data(model, test_points)
        model_success[model] = s_rate
        model_optimal[model] = o_rate

    n_groups = len(test_points)
    n_models = len(args.models)
    index = np.arange(n_groups)
    group_width = 0.8
    bar_gap = 0.05
    bar_width = (group_width - bar_gap * (n_models - 1)) / n_models

    fig, ax = plt.subplots(figsize=(12, 7))

    hatch_patterns = ['///', '...', 'xxx', '+++','\\\\\\', '//////']

    for i, model in enumerate(args.models):
        model_hatch = hatch_patterns[i % len(hatch_patterns)]
        positions = index - group_width/2 + bar_width/2 + i * (bar_width + bar_gap)
        
        s_rates = model_success[model]
        o_rates = model_optimal[model]
        
        ax.bar(positions, o_rates, bar_width,
               color='white',
               edgecolor='black',
               linewidth=1,
               label="_nolegend_")
        ax.bar(positions, o_rates, bar_width,
               color='none',
               edgecolor='orange',
               linewidth=1,
               hatch=model_hatch,
               label="_nolegend_")
        
        remainder = [s - o for s, o in zip(s_rates, o_rates)]
        ax.bar(positions, remainder, bar_width, bottom=o_rates,
               color='white',
               edgecolor='black',
               linewidth=1,
               label="_nolegend_")
        ax.bar(positions, remainder, bar_width, bottom=o_rates,
               color='none',
               edgecolor='green',
               linewidth=1,
               hatch=model_hatch,
               label="_nolegend_")
        
        for x, s in zip(positions, s_rates):
            ax.text(x, s + 0.01, f"{s:.2f}", ha='center', va='bottom', fontsize=9)

    ax.set_xlabel("Number of Test Points", fontsize=12)
    ax.set_ylabel("Rate", fontsize=12)
    # ax.set_title("Model Performance vs. Number of Test Points", fontsize=14)
    ax.set_xticks(index)
    ax.set_xticklabels([str(tp) for tp in test_points], fontsize=12)

    optimal_legend = mpatches.Patch(facecolor='white', edgecolor='orange', hatch='///',
                                    label='Optimal Rate (lower portion)')
    success_legend = mpatches.Patch(facecolor='white', edgecolor='green', hatch='///',
                                    label='Success Rate (upper portion)')
    
    model_handles = []
    for i, model in enumerate(args.models):
        model_hatch = hatch_patterns[i % len(hatch_patterns)]
        patch = mpatches.Patch(facecolor='white', edgecolor='black', hatch=model_hatch, label=model)
        model_handles.append(patch)
    
    all_handles = model_handles + [optimal_legend, success_legend]
    all_labels = [h.get_label() for h in all_handles]
    
    legend = fig.legend(all_handles, all_labels,
                        loc='upper center',
                        bbox_to_anchor=(0.5, 1.08),
                        ncol=3,
                        frameon=True,
                        fontsize=10)
    legend.get_frame().set_edgecolor('black')
    legend.get_frame().set_linewidth(2)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    output_dir = os.path.join("data", "result")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "node_results.png")
    plt.savefig(output_file, bbox_inches='tight')
    print(f"Plot saved to: {output_file}")

if __name__ == "__main__":
    main()
