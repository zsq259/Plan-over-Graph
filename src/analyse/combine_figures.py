import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# ========================
# Part 1: Node performance analysis
# ========================

def process_model_data(model, test_points):
    """Process model data and compute metrics (from the first script)."""
    success_rates = []
    optimal_rates = []
    time_ratios = []
    cost_ratios = []
    
    for point in test_points:
        file_names = [f"{point}-1-100-r-output.json", f"{point}-1-100-t-output.json"]
        total_count = 0
        success_count = 0
        optimal_count = 0
        time_ratio_sum = 0.0
        cost_ratio_sum = 0.0
        
        for file_name in file_names:
            file_path = os.path.join("data", "result", model, file_name)
            if not os.path.exists(file_path):
                continue
                
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue
            
            for item in data:
                total_count += 1
                model_ans = None
                model_time = None
                model_cost = None
                
                # Parse model outputs
                if "result" in item and isinstance(item["result"], list) and len(item["result"]) >= 2:
                    model_ans = item["result"][0]
                    model_time = item["result"][0]
                    model_cost = item["result"][1]
                
                # Get optimal values
                optimal_ans = item["question"]["min_time"]
                optimal_cost_val = item["question"]["min_cost"]
                
                # Compute ratios
                if model_ans is not None and str(model_ans).strip() != "":
                    success_count += 1
                    time_ratio = model_time / optimal_ans if optimal_ans != 0 else 4
                    cost_ratio = model_cost / optimal_cost_val if optimal_cost_val != 0 else 4
                    
                    # Check whether the output is optimal
                    if str(model_ans) == str(optimal_ans) and (model_cost == optimal_cost_val):
                        optimal_count += 1
                else:
                    time_ratio = 4.0
                    cost_ratio = 4.0
                
                time_ratio_sum += time_ratio
                cost_ratio_sum += cost_ratio
        
        # Compute averages
        if total_count > 0:
            success_rate = success_count / total_count
            optimal_rate = optimal_count / total_count
            time_avg = time_ratio_sum / total_count
            cost_avg = cost_ratio_sum / total_count
        else:
            success_rate = optimal_rate = time_avg = cost_avg = 0
        
        success_rates.append(success_rate)
        optimal_rates.append(optimal_rate)
        time_ratios.append(time_avg)
        cost_ratios.append(cost_avg)
    
    return success_rates, optimal_rates, time_ratios, cost_ratios

# ========================
# Part 2: Edge performance analysis
# ========================

def analyze_file(file_path):
    """Analyze one file (from the second script)."""
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

def process_edge_data(models, file_args, base_result_dir="data/result/"):
    """Process edge data (from the second script)."""
    file_params = []
    for arg in file_args:
        try:
            prefix, seg_size = arg.split(':')
            file_params.append((prefix.strip(), int(seg_size)))
        except:
            print(f"Invalid file argument: {arg}")
            continue

    analysis_results = []
    for model_name in models:
        base_dir = os.path.join(base_result_dir, model_name)
        file_suffix = "-output.json"

        for file_prefix, seg_size in file_params:
            file_path = os.path.join(base_dir, f"{file_prefix}{file_suffix}")
            file_data = analyze_file(file_path)
            if not file_data:
                continue
            
            df = pd.DataFrame(file_data)
            if df.empty:
                continue

            max_edge = df["Edge Count"].max()
            actual_seg = 1 if max_edge < 100 else seg_size
           
            df["Edge Segment"] = ((df["Edge Count"] - 1) // actual_seg) * actual_seg + actual_seg

            agg_df = df.groupby("Edge Segment").agg({
                "Time Ratio": "mean",
                "Cost Ratio": "mean",
                "Node Count": "first"
            }).reset_index()

            status_df = df.groupby(["Edge Segment", "Status"]).size().unstack(fill_value=0).reset_index()

            analysis_results.append({
                "model_name": model_name,
                "agg_data": agg_df,
                "status_data": status_df,
                "node_count": df["Node Count"].iloc[0],
                "seg_size": actual_seg,
                "file_prefix": file_prefix
            })
            
    return analysis_results

# ========================
# Plotting functions
# ========================

def setup_plt_style():
    """Restore the original plotting style settings."""
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({
        'font.size': 16,
        'axes.titlesize': 16,
        'axes.labelsize': 16,
        'xtick.labelsize': 14,
        'ytick.labelsize': 14,
        'axes.titleweight': 'bold',
        'legend.fontsize': 14
    })

def plot_node_performance(ax1, ax2):
    """Plot node performance charts."""
    # Hard-coded configuration
    models = ["Llama-3.1-8B-Instruct", "Llama-3.1-8B-Instruct-DPO", 
             "gpt-4o", "claude-3-5-sonnet-20241022"]
    test_points = [10, 20, 30, 40, 50]
    
    model_names = {
        "gpt-4o": "GPT-4o",
        "Llama-3.1-8B-Instruct": "Llama",
        "Llama-3.1-8B-Instruct-DPO": "Llama-Trained",
        "claude-3-5-sonnet-20241022": "Claude",
    }
    
    # Process data
    metrics = {'success': {}, 'optimal': {}, 'time_ratio': {}, 'cost_ratio': {}}
    for model in models:
        s, o, t, c = process_model_data(model, test_points)
        display_name = model_names.get(model, model)
        metrics['success'][display_name] = s
        metrics['optimal'][display_name] = o
        metrics['time_ratio'][display_name] = t
        metrics['cost_ratio'][display_name] = c

    # Plot time/cost ratios
    colors = plt.cm.tab10.colors
    for idx, model in enumerate(models):
        display_name = model_names.get(model, model)
        ax1.plot(test_points, metrics['time_ratio'][display_name],
                color=colors[idx], linestyle='-', marker='o', markersize=6, label=f'{display_name} Time or Success')
        ax1.plot(test_points, metrics['cost_ratio'][display_name],
                color=colors[idx], linestyle='--', marker='s', markersize=6, label=f'{display_name} Cost or Optimal')

    ax1.set_title('Time & Cost Ratios', pad=10)
    ax1.set_xlabel('Node Count')
    ax1.set_ylabel('Ratio')
    ax1.set_ylim(0, 5.5)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.axhline(4, color='gray', linestyle=':', alpha=0.7)

    # Plot success/optimal rates
    for idx, model in enumerate(models):
        display_name = model_names.get(model, model)
        ax2.plot(test_points, metrics['success'][display_name],
                color=colors[idx], linestyle='-', marker='o', markersize=6)
        ax2.plot(test_points, metrics['optimal'][display_name],
                color=colors[idx], linestyle='--', marker='s', markersize=6)

    ax2.set_title('Success & Optimal Rates', pad=10)
    ax2.set_xlabel('Node Count')
    ax2.set_ylabel('Rate')
    ax2.set_ylim(0, 1.05)
    ax2.grid(True, linestyle='--', alpha=0.7)

def plot_edge_performance(axes):
    """Plot edge performance charts."""
    # Hard-coded configuration
    models = ["claude-3-5-sonnet-20241022", "Llama-3.1-8B-Instruct-DPO"]
    file_args = ["10-3-1000-r:1", "30-3-1000-r:10"]
    analysis_results = process_edge_data(models, file_args)

    colors = {'Time Ratio': '#1f77b4', 'Cost Ratio': '#ff7f0e'}
    
    for idx, result in enumerate(analysis_results):
        ax = axes[idx]
        df = result["agg_data"]
        df.plot(x="Edge Segment", y=["Time Ratio", "Cost Ratio"], ax=ax,
               marker='o', linestyle='--', linewidth=1, color=[colors['Time Ratio'], colors['Cost Ratio']])
        
        # Set title
        model_name = "Claude" if "claude" in result["model_name"].lower() else "Llama-Trained"
        ax.set_title(f'{model_name}\n{result["node_count"]} Nodes')
        ax.set_xlabel("Edge Count")
        ax.grid(True, alpha=0.3)
        if idx == 0:
            ax.set_ylabel("Ratio")

# ========================
# Main program
# ========================

def main():
    # Create canvas and grid layout
    setup_plt_style()
    fig = plt.figure(figsize=(20, 10))
    gs = GridSpec(2, 1, height_ratios=[3, 2], hspace=0.3)

    # First row: node performance charts
    top_gs = gs[0].subgridspec(1, 2, wspace=0.15)
    ax1 = fig.add_subplot(top_gs[0])
    ax2 = fig.add_subplot(top_gs[1])
    plot_node_performance(ax1, ax2)

    # Second row: edge performance charts
    edge_results = process_edge_data(
        models=["claude-3-5-sonnet-20241022", "Llama-3.1-8B-Instruct-DPO"],
        file_args=["10-3-1000-r:1", "30-3-1000-r:10"]
    )
    bottom_gs = gs[1].subgridspec(1, len(edge_results), wspace=0.15)
    edge_axes = [fig.add_subplot(bottom_gs[i]) for i in range(len(edge_results))]
    plot_edge_performance(edge_axes)

    # Add unified legend
    handles_1, labels_1 = ax1.get_legend_handles_labels()
    handles_2, labels_2 = ax2.get_legend_handles_labels()
    
    top_legend = ax1.legend(
        handles=handles_1 + handles_2,
        labels=labels_1 + labels_2,
        loc='upper center',
        bbox_to_anchor=(1.09, 1.27), 
        ncol=4,
        frameon=True,
    )
    top_legend.get_title().set_position((-40, -15))

    # Adjust margins
    plt.subplots_adjust(left=0.06, right=0.98, top=0.9, bottom=0.1)

    # Save output
    os.makedirs("data/result/figures", exist_ok=True)
    plt.savefig("data/result/figures/combined_results.png", bbox_inches='tight', dpi=300)
    plt.savefig("data/result/figures/combined_results.pdf", bbox_inches='tight')
    print("Combined plots saved data/result/figures/combined_results.png")

if __name__ == "__main__":
    main()