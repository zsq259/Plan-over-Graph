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
    parser.add_argument("--segment_size", type=int, default=10, help="边数分段的大小")
    args = parser.parse_args()

    # 基目录和文件后缀
    model_name = "gpt-4o-mini"
    base_dir = f"/home/zhangsq/1/test/data/result/{model_name}/"
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
    
    node_count = df['Node Count'][0]

    # 添加边数段列
    segment_size = args.segment_size
    df['Edge Count Segment'] = ((df['Edge Count'] - 1) // segment_size + 1) * segment_size

    # 按边数段将数据汇总，计算平均值
    aggregated_df = df.groupby('Edge Count Segment').agg({
        'Node Count': 'mean',
        'Time Ratio': 'mean',
        'Cost Ratio': 'mean',
        'Status': lambda x: x.value_counts().idxmax()
    }).reset_index()

    output_image_path = output_dir + f"aggregated_analysis_results_seg{args.segment_size}.png"

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 18))

    # 图表1: 平均 Time Ratio 随边数段的变化
    ax1.set_title(f'{node_count} - Edge Count - Time Ratio', fontsize=16)
    ax1.set_xlabel('Edge Count', fontsize=14)
    ax1.set_ylabel('mean Time Ratio', fontsize=14)
    ax1.plot(aggregated_df['Edge Count Segment'], aggregated_df['Time Ratio'], marker='o')
    ax1.grid(True)

    # 图表2: 平均 Cost Ratio 随边数段的变化
    ax2.set_title(f'{node_count} - Edge Count - Cost Ratio', fontsize=16)
    ax2.set_xlabel('Edge Count', fontsize=14)
    ax2.set_ylabel('mean Cost Ratio', fontsize=14)
    ax2.plot(aggregated_df['Edge Count Segment'], aggregated_df['Cost Ratio'], marker='x', color='orange')
    ax2.grid(True)

    # 图表3: 成功与失败任务数量随边数段的变化
    status_counts = df.groupby(['Edge Count Segment', 'Status']).size().unstack(fill_value=0).reset_index()
    status_counts.plot(x='Edge Count Segment', kind='bar', stacked=True, ax=ax3, color=['red', 'green'])
    ax3.set_title(f'{node_count} - Edge Count - Task Status', fontsize=16)
    ax3.set_xlabel('Edge Count', fontsize=14)
    ax3.set_ylabel('Count', fontsize=14)
    ax3.legend(title='Status')

    fig.tight_layout()
    plt.savefig(output_image_path, bbox_inches='tight')
    plt.close()
    print(f"图表已保存为 {output_image_path}")

if __name__ == "__main__":
    main()