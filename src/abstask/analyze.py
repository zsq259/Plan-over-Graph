import json
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

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
        return None

    # 读取数据文件
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 初始化结果存储
    category = {"ratios": [], "cost_ratios": [], "success_count": 0, "failure_count": 0}

    # 遍历数据
    for item in data:
        task_id = item["question"]["id"]
        answer_time = item["question"]["answer"]
        min_cost = item["question"]["min_cost"]
        result = item.get("result")
        result_time = None if result is None else result[0]
        result_cost = None if result is None else result[1]

        # 统计成功或失败任务
        if result_time is not None and result_cost is not None:
            category["success_count"] += 1
            time_ratio = result_time / answer_time
            cost_ratio = result_cost / min_cost
            category["ratios"].append(time_ratio)
            category["cost_ratios"].append(cost_ratio)
        else:
            category["failure_count"] += 1

    # 分析统计数据
    results = []
    time_stats = analyze_ratios(category["ratios"])
    cost_stats = analyze_ratios(category["cost_ratios"])
    total_count = category["success_count"] + category["failure_count"]
    if total_count > 0:
        success_rate = category["success_count"] / total_count
        failure_rate = category["failure_count"] / total_count
    else:
        success_rate = None
        failure_rate = None

    if time_stats and cost_stats:
        results.append({
            "Category": os.path.basename(file_path).replace("-output.json", ""),
            "Success Count": category["success_count"],
            "Failure Count": category["failure_count"],
            "Success Rate": success_rate,
            "Failure Rate": failure_rate,
            "Min Time Ratio": time_stats["min_ratio"],
            "Max Time Ratio": time_stats["max_ratio"],
            "Avg Time Ratio": time_stats["avg_ratio"],
            "Min Cost Ratio": cost_stats["min_ratio"],
            "Max Cost Ratio": cost_stats["max_ratio"],
            "Avg Cost Ratio": cost_stats["avg_ratio"]
        })
    else:
        results.append({
            "Category": os.path.basename(file_path).replace("-output.json", ""),
            "Success Count": category["success_count"],
            "Failure Count": category["failure_count"],
            "Success Rate": success_rate,
            "Failure Rate": failure_rate,
            "Min Time Ratio": None,
            "Max Time Ratio": None,
            "Avg Time Ratio": None,
            "Min Cost Ratio": None,
            "Max Cost Ratio": None,
            "Avg Cost Ratio": None
        })
    return results

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="分析 JSON 数据文件")
    parser.add_argument("file_prefixes", type=str, nargs='+', help="JSON 数据文件的文件名前缀列表")
    parser.add_argument("--output", type=str, default="output.csv", help="输出文件的路径")
    args = parser.parse_args()

    # 基目录和文件后缀
    base_dir = "/home/zhangsq/1/test/data/abstask/result/"
    file_suffix = "-output.json"

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

    # 截断小数点后数据
    df = df.round(2)

    print(df)
    df.to_csv(args.output, index=False)
    
    # 可视化表格并保存为图片
    fig, ax = plt.subplots(figsize=(12, 8))  # 设置图片大小
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)  # 设置表格缩放比例
    plt.savefig("analysis_results.png", bbox_inches='tight')
    print("表格已保存为 analysis_results.png")

if __name__ == "__main__":
    main()