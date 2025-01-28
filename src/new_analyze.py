import json
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def analyze_ratios(ratios):
    if len(ratios) == 0:
        return None
    return {
        "min_ratio": min(ratios),
        "max_ratio": max(ratios),
        "avg_ratio": sum(ratios) / len(ratios)
    }

def analyze_file(file_path):
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"文件路径 {file_path} 不存在。请检查路径是否正确。")
        return None, None

    # 读取数据文件
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 初始化结果存储
    results = []
    failed_results = []
    time_ratios = []
    cost_ratios = []

    feasible_count = 0  # 可行解计数器
    optimal_count = 0   # 最优解计数器
    
    # 遍历数据
    for item in data:
        task_id = item["question"]["id"]
        answer_time = item["question"]["min_time"]
        min_cost = item["question"]["min_cost"]
        result = item.get("result")
        result_time = None if result is None else result[0]
        result_cost = None if result is None else result[1]

        # 获取节点数和边数
        nodes = item["question"].get("node_count", 0)
        edges = item["question"].get("edge_count", 0)

        # 统计成功或失败任务
        if result_time is not None and result_cost is not None:
            time_ratio = result_time / answer_time
            cost_ratio = result_cost / min_cost
            time_ratios.append(time_ratio)
            cost_ratios.append(cost_ratio)
            results.append({
                "Category": os.path.basename(file_path).replace("-output.json", ""),
                "Node Count": nodes,
                "Edge Count": edges,
                "Time Ratio": time_ratio,
                "Cost Ratio": cost_ratio
            })
            if result_time == answer_time and result_cost == min_cost:
                optimal_count += 1
            else:
                feasible_count += 1
        else:
            # 记录失败的任务
            failed_results.append({
                "Category": os.path.basename(file_path).replace("-output.json", ""),
                "Node Count": nodes,
                "Edge Count": edges,
            })
    in_all_results = []
    time_stats = analyze_ratios(time_ratios)
    cost_stats = analyze_ratios(cost_ratios)
    total_count = len(results) + len(failed_results)
    if total_count > 0:
        success_rate = len(results) / total_count
        failure_rate = len(failed_results) / total_count
        feasible_accuracy = feasible_count / total_count
        optimal_accuracy = optimal_count / total_count
    else:
        success_rate = None
        failure_rate = None
        feasible_accuracy = None
        optimal_accuracy = None

    if time_stats and cost_stats:
        in_all_results.append({
            "Category": os.path.basename(file_path).replace("-output.json", ""),
            "Success Rate": success_rate,
            "Failure Rate": failure_rate,
            "Feasible Accuracy": feasible_accuracy,
            "Optimal Accuracy": optimal_accuracy,
            "Min Time Ratio": time_stats["min_ratio"],
            "Max Time Ratio": time_stats["max_ratio"],
            "Avg Time Ratio": time_stats["avg_ratio"],
            "Min Cost Ratio": cost_stats["min_ratio"],
            "Max Cost Ratio": cost_stats["max_ratio"],
            "Avg Cost Ratio": cost_stats["avg_ratio"]
        })
    else:
        in_all_results.append({
            "Category": os.path.basename(file_path).replace("-output.json", ""),
            "Success Rate": success_rate,
            "Failure Rate": failure_rate,
            "Feasible Accuracy": feasible_accuracy,
            "Optimal Accuracy": optimal_accuracy,
            "Min Time Ratio": None,
            "Max Time Ratio": None,
            "Avg Time Ratio": None,
            "Min Cost Ratio": None,
            "Max Cost Ratio": None,
            "Avg Cost Ratio": None
        })
    return results, failed_results, in_all_results[0]

def visualize_failed_data(failed_df, output_dir):
    plt.figure(figsize=(8, 6))

    # 绘制失败数据的散点图
    plt.scatter(failed_df['Node Count'], failed_df['Edge Count'], 
                s=100, c='red', alpha=0.7, edgecolors='w')
    
    plt.title('Failed Tasks Distribution')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Number of Edges')
    plt.grid()
    plt.tight_layout()
    plt.savefig(output_dir + "failed_tasks_distribution.png", bbox_inches='tight')
    plt.show()

def visualize_data(df, output_dir):
    plt.figure(figsize=(14, 6))

    # 自定义颜色映射，使得最小值也能显示较深的颜色
    blues_cmap = mcolors.LinearSegmentedColormap.from_list("custom_blues", ["#ADD8E6", "#0000FF"])
    reds_cmap = mcolors.LinearSegmentedColormap.from_list("custom_reds", ["#FFC0CB", "#FF0000"])

    # 设置颜色映射的范围
    norm_blues = mcolors.Normalize(vmin=df['Edge Count'].min(), vmax=df['Edge Count'].max())
    norm_reds = mcolors.Normalize(vmin=df['Edge Count'].min(), vmax=df['Edge Count'].max())

    # 绘制时间比率与节点数的关系
    plt.subplot(1, 2, 1)
    scatter = plt.scatter(df['Node Count'], df['Time Ratio'], 
                          s=100, c=df['Edge Count'], cmap=blues_cmap, 
                          alpha=0.8, edgecolors='w', norm=norm_blues)
    plt.title('Time Ratio vs Node Count')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Time Ratio')
    plt.grid()
    plt.colorbar(scatter, label='Edge Count')  # 显示边数的颜色条

    # 绘制消耗比率与节点数的关系
    plt.subplot(1, 2, 2)
    scatter = plt.scatter(df['Node Count'], df['Cost Ratio'], 
                          s=100, c=df['Edge Count'], cmap=reds_cmap, 
                          alpha=0.8, edgecolors='w', norm=norm_reds)
    plt.title('Cost Ratio vs Node Count')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Cost Ratio')
    plt.grid()
    plt.colorbar(scatter, label='Edge Count')  # 显示边数的颜色条

    plt.tight_layout()
    plt.savefig(output_dir + "ratios_visualization.png", bbox_inches='tight')
    plt.show()

def generate_combined_table_image(model_name, results, output_image_path):
    # 创建一个 DataFrame 来存储所有结果
    df = pd.DataFrame(results)
    
    # 添加汇总行
    if not df.empty:
        # 初始化汇总字典
        summary = {"Category": "Overall"}
        
        # 需要计算平均值的列
        avg_columns = ["Success Rate", "Failure Rate", "Feasible Accuracy", "Optimal Accuracy",
                      "Avg Time Ratio", "Avg Cost Ratio"]
        
        # 需要取极值的列
        minmax_columns = ["Min Time Ratio", "Max Time Ratio", "Min Cost Ratio", "Max Cost Ratio"]
        
        # 计算平均值
        for col in avg_columns:
            valid_values = df[col].dropna()
            summary[col] = valid_values.mean() if not valid_values.empty else None
        
        # 计算全局最小值和最大值
        for col in ["Min Time Ratio", "Min Cost Ratio"]:
            valid_values = df[col].dropna()
            summary[col] = valid_values.min() if not valid_values.empty else None
        
        for col in ["Max Time Ratio", "Max Cost Ratio"]:
            valid_values = df[col].dropna()
            summary[col] = valid_values.max() if not valid_values.empty else None
        
        # 创建包含汇总行的新DataFrame
        summary_df = pd.DataFrame([summary])
        combined_df = pd.concat([df, summary_df], ignore_index=True)
    else:
        combined_df = df
    
    # 保留两位小数
    combined_df = combined_df.round(2)
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(12, (len(results)+1)*0.5 + 1))  # 增加高度适应汇总行
    ax.set_title(f"{model_name} Analysis Results", fontsize=16)
    ax.axis('off')
    
    # 创建表格并设置样式
    table = ax.table(cellText=combined_df.values, 
                    colLabels=combined_df.columns, 
                    cellLoc='center', 
                    loc='center',
                    colColours=['#f5f5f5']*len(combined_df.columns))
    
    # 设置汇总行样式
    if not df.empty:
        # 计算表格中的实际行号（数据行号 + 列标题行）
        last_data_row = len(combined_df)  # 因为列标题占用了第0行
        for j in range(len(combined_df.columns)):
            table[(last_data_row, j)].set_facecolor('#e6e6e6')  # 修改这里
    
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)
    
    # 保存图片
    plt.tight_layout()
    plt.savefig(output_image_path, bbox_inches='tight')
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="分析 JSON 数据文件")
    parser.add_argument("--file_prefixes", type=str, nargs='+', help="JSON 数据文件的文件名前缀列表")
    parser.add_argument("--model_name", type=str, help="模型名称")
    args = parser.parse_args()

    base_dir = f"data/result/{args.model_name}/"
    file_suffix = "-output.json"
    output_dir = base_dir + "analysis/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not args.file_prefixes or len(args.file_prefixes) == 0:
        file_paths = [os.path.join(base_dir, file_name) for file_name in os.listdir(base_dir) if file_name.endswith(file_suffix)]
        file_paths.sort()
    else:
        file_paths = [os.path.join(base_dir, file_prefix + file_suffix) for file_prefix in args.file_prefixes]

    all_results = []
    all_failed_results = []
    all_in_all_results = []

    for file_path in file_paths:
        file_results, file_failed_results, file_in_all_results = analyze_file(file_path)
        if file_results:
            all_results.extend(file_results)
        if file_failed_results:
            all_failed_results.extend(file_failed_results)
        all_in_all_results.append(file_in_all_results)

    generate_combined_table_image(args.model_name, all_in_all_results, output_dir + "output_image.png")
    
    print(type(all_results))
    df = pd.DataFrame(all_results)
    failed_df = pd.DataFrame(all_failed_results)

    df = df.round(2)

    df = df.sort_values(by='Node Count')

    print(df)
    df.to_csv(output_dir + "result.csv", index=False)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    plt.savefig(output_dir + "analysis_results.png", bbox_inches='tight')
    print("表格已保存为 analysis_results.png")

    
    visualize_data(df, output_dir)
    visualize_failed_data(failed_df, output_dir)

if __name__ == "__main__":
    main()