import json
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

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

def main():
    parser = argparse.ArgumentParser(description="Analyze edge results")
    parser.add_argument("--models", type=str, nargs='+', required=True,
                      help="list of model names")
    parser.add_argument("--file_args", type=str, nargs='+', required=True,
                      help="list of file arguments in the format: prefix:segment_size")
    args = parser.parse_args()

    file_params = []
    for arg in args.file_args:
        try:
            prefix, seg_size = arg.split(':')
            file_params.append((prefix.strip(), int(seg_size)))
        except:
            print(f"Invalid file argument: {arg}")
            continue

    analysis_results = []
    for model_name in args.models:
        base_dir = f"data/result/{model_name}/"
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

    num_columns = len(analysis_results)
    if num_columns == 0:
        print("No data to analyze")
        return

    plt.rcParams.update({
        'font.size': 18,
        'axes.titlesize': 18,
        'axes.labelsize': 18,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'axes.titleweight': 'bold'
    })

    fig, axs = plt.subplots(2, num_columns,
                          figsize=(7*num_columns, 10),
                          squeeze=False,
                          gridspec_kw={'hspace': 0.2, 'wspace': 0.1})

    colors = {'Failure': '#d62728', 'Feasible': '#2ca02c', 'Optimal': '#ffbb78'}

    for idx, result in enumerate(analysis_results):
        ax1 = axs[0][idx]
        result["agg_data"].plot(x="Edge Segment", y=["Time Ratio", "Cost Ratio"],
                              ax=ax1, marker='o', linestyle='--', linewidth=1)
        title_model_name = result["model_name"]
        if title_model_name == "claude-3-5-sonnet-20241022":
            title_model_name = "Claude 3.5 Sonnet"
        elif title_model_name == "Llama-3.1-8B-Instruct-DPO":
            title_model_name = "Llama-3.1-8b-Instruct-Trained"
        ax1.set_title(f'{title_model_name}'
                     f'\n{result["node_count"]} Nodes')
        ax1.set_xlabel("Edge Count")
        ax1.grid(True, alpha=0.3)
        ax1.legend().set_visible(False)

        ax2 = axs[1][idx]
        status_cols = [col for col in colors if col in result["status_data"].columns]

        result["status_data"].plot(x="Edge Segment", y=status_cols,
                                kind="bar", stacked=True,
                                ax=ax2, color=[colors[col] for col in status_cols],
                                width=0.8)

        ax2.set_xlabel("Edge Count")
        ax2.get_legend().remove()
        ax2.grid(True, axis='y', alpha=0.3)

        if idx == 0:
            ax1.set_ylabel("Ratio")
            ax2.set_ylabel("Count")

    handles, labels = axs[0][0].get_legend_handles_labels()
    fig.legend(handles, ["Time Ratio", "Cost Ratio"], loc='upper left',
             bbox_to_anchor=(0.122, 0.88), ncol=1)
    
    status_handles = [plt.Rectangle((0,0),1,1, color=colors[k]) 
                    for k in colors if k in status_cols]
    fig.legend(status_handles, colors.keys(),
             loc='lower left', bbox_to_anchor=(0.122, 0.32),
             ncol=1)

    combined_output_dir = "data/result/figures/"
    os.makedirs(combined_output_dir, exist_ok=True)
    output_path = os.path.join(combined_output_dir, "edge_results.png")
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    print(f"Saved figure to {output_path}")
    output_path = os.path.join(combined_output_dir, "edge_results.pdf")
    plt.savefig(output_path, bbox_inches='tight')

if __name__ == "__main__":
    main()