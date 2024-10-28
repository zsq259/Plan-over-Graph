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
            results.append({
                "Category": os.path.basename(file_path).replace("-output.json", ""),
                "Node Count": nodes,
                "Edge Count": edges,
                "Time Ratio": time_ratio,
                "Cost Ratio": cost_ratio
            })
        else:
            # 记录失败的任务
            failed_results.append({
                "Category": os.path.basename(file_path).replace("-output.json", ""),
                "Node Count": nodes,
                "Edge Count": edges,
            })

    return results, failed_results

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



def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="分析 JSON 数据文件")
    parser.add_argument("file_prefixes", type=str, nargs='+', help="JSON 数据文件的文件名前缀列表")
    args = parser.parse_args()

    # 基目录和文件后缀
    model_name = "llama-31-8b-instruct"
    base_dir = f"/home/zhangsq/1/test/data/abstask/result/{model_name}/"
    file_suffix = "-output.json"

    # 获取文件路径列表
    file_paths = [os.path.join(base_dir, file_prefix + file_suffix) for file_prefix in args.file_prefixes]

    # 初始化结果存储
    all_results = []
    all_failed_results = []

    # 分析每个文件
    for file_path in file_paths:
        file_results, file_failed_results = analyze_file(file_path)
        if file_results:
            all_results.extend(file_results)
        if file_failed_results:
            all_failed_results.extend(file_failed_results)

    # 将结果转换为 DataFrame 并输出
    df = pd.DataFrame(all_results)
    failed_df = pd.DataFrame(all_failed_results)

    # 截断小数点后数据
    df = df.round(2)

    # 对 DataFrame 按节点数进行排序
    df = df.sort_values(by='Node Count')

    print(df)
    output_dir = base_dir + "analysis/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    df.to_csv(output_dir + "result.csv", index=False)
    
    # 可视化表格并保存为图片
    fig, ax = plt.subplots(figsize=(12, 8))  # 设置图片大小
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)  # 设置表格缩放比例
    plt.savefig(output_dir + "analysis_results.png", bbox_inches='tight')
    print("表格已保存为 analysis_results.png")

    # 可视化成功数据
    visualize_data(df, output_dir)

    # 可视化失败数据
    visualize_failed_data(failed_df, output_dir)

if __name__ == "__main__":
    main()