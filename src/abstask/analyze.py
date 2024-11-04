import json
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def analyze_file(file_path):
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"文件路径 {file_path} 不存在。请检查路径是否正确。")
        return None

    # 读取数据文件
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 初始化结果存储
    results = []

    # 遍历数据
    for item in data:
        task_id = item["question"]["id"]
        node_count = item["question"]["node_count"]
        edge_count = item["question"]["edge_count"]
        answer_time = item["question"]["min_time"]
        min_cost = item["question"]["min_cost"]
        result = item.get("result")
        result_time = None if result is None else result[0]
        result_cost = None if result is None else result[1]

        # 统计任务
        time_ratio = None if result_time is None else result_time / answer_time
        cost_ratio = None if result_cost is None else result_cost / min_cost
        results.append({
            "Node Count": node_count,
            "Edge Count": edge_count,
            "Time Ratio": time_ratio,
            "Cost Ratio": cost_ratio,
            "Status": "Success" if result_time is not None and result_cost is not None else "Failure"
        })

    return results

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="分析 JSON 数据文件")
    parser.add_argument("file_prefixes", type=str, nargs='+', help="JSON 数据文件的文件名前缀列表")
    args = parser.parse_args()

    # 基目录和文件后缀
    model_name = "llama-31-8b-instruct"
    base_dir = f"/home/zhangsq/1/test/data/abstask/result/{model_name}/"
    file_suffix = "-output.json"
    output_dir = base_dir + "analysis/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取文件路径列表
    file_paths = [os.path.join(base_dir, file_prefix + file_suffix) for file_prefix in args.file_prefixes]

    # 初始化结果存储
    all_results = []

    # 分析每个文件
    for file_path in file_paths:
        file_results = analyze_file(file_path)
        if file_results:
            all_results.extend(file_results)

    # 将结果转换为 DataFrame 并输出
    df = pd.DataFrame(all_results)

    # 按点数分组并分析边数变化对性能的影响
    grouped = df.groupby("Node Count")
    for node_count, group in grouped:
        group = group.sort_values(by="Edge Count").reset_index(drop=True)
        output_image_path = output_dir + f"analysis_results_node_count_{node_count}.png"
        
        # 可视化 time_ratio 和 cost_ratio 随 edge_count 的变化
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 18))
        
        # 图表1: Time Ratio
        success_group = group[group['Status'] == 'Success']
        ax1.set_title(f'Node Count: {node_count} - Time Ratio', fontsize=16)
        ax1.set_xlabel('Edge Count', fontsize=14)
        ax1.set_ylabel('Time Ratio', fontsize=14, color='tab:blue')
        ax1.plot(success_group['Edge Count'], success_group['Time Ratio'], marker='o', color='tab:blue', label='Time Ratio')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        
        # 图表2: Cost Ratio
        ax2.set_title(f'Node Count: {node_count} - Cost Ratio', fontsize=16)
        ax2.set_xlabel('Edge Count', fontsize=14)
        ax2.set_ylabel('Cost Ratio', fontsize=14, color='tab:orange')
        ax2.plot(success_group['Edge Count'], success_group['Cost Ratio'], marker='x', color='tab:orange', label='Cost Ratio')
        ax2.tick_params(axis='y', labelcolor='tab:orange')
        
        # 图表3: 成功和失败任务数量随边数变化
        status_counts = group.groupby(['Edge Count', 'Status']).size().unstack(fill_value=0)
        status_counts.plot(kind='bar', stacked=True, ax=ax3, color=['tab:red', 'tab:green'])
        ax3.set_title(f'Node Count: {node_count} - Task Status by Edge Count', fontsize=16)
        ax3.set_xlabel('Edge Count', fontsize=14)
        ax3.set_ylabel('Count', fontsize=14)
        
        fig.tight_layout()
        plt.savefig(output_image_path, bbox_inches='tight')
        plt.close()
        print(f"图表已保存为 {output_image_path}")

if __name__ == "__main__":
    main()