import json
import os

# 设置文件路径
file_path = "/home/maxb/hst/test/data/abstask/output.json"

# 检查文件是否存在
if not os.path.exists(file_path):
    print(f"文件路径 {file_path} 不存在。请检查路径是否正确。")
    exit(1)

# 读取数据文件
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 初始化分类统计变量
config = [50, 30, 20]  # 各分类的任务数量
category_ranges = [
    (1, config[0]),  # 第一类
    (config[0] + 1, config[0] + config[1]),  # 第二类
    (config[0] + config[1] + 1, sum(config))  # 第三类
]

# 初始化结果存储
categories = {
    "Category 1": {"ratios": [], "success_count": 0, "failure_count": 0},
    "Category 2": {"ratios": [], "success_count": 0, "failure_count": 0},
    "Category 3": {"ratios": [], "success_count": 0, "failure_count": 0}
}

# 遍历数据
for item in data:
    task_id = item["question"]["id"]
    answer_time = item["question"]["answer"]
    result_time = item.get("result")

    # 根据任务编号归类
    if category_ranges[0][0] <= task_id <= category_ranges[0][1]:
        category_key = "Category 1"
    elif category_ranges[1][0] <= task_id <= category_ranges[1][1]:
        category_key = "Category 2"
    else:
        category_key = "Category 3"

    # 统计成功或失败任务
    if result_time is not None:
        categories[category_key]["success_count"] += 1
        ratio = result_time / answer_time
        categories[category_key]["ratios"].append(ratio)
    else:
        categories[category_key]["failure_count"] += 1

# 定义一个函数来统计结果
def analyze_ratios(ratios):
    if len(ratios) == 0:
        return None
    return {
        "min_ratio": min(ratios),
        "max_ratio": max(ratios),
        "avg_ratio": sum(ratios) / len(ratios)
    }

# 分析每个类别的统计数据
for category, data in categories.items():
    stats = analyze_ratios(data["ratios"])
    if stats:
        print(f"{category} 统计结果：")
        print(f"成功任务数: {data['success_count']}")
        print(f"失败任务数: {data['failure_count']}")
        print(f"成功率: {data['success_count'] / (data['success_count'] + data['failure_count']):.2%}")
        print(f"失败率: {data['failure_count'] / (data['success_count'] + data['failure_count']):.2%}")
        print(f"最小比例: {stats['min_ratio']:.2f}")
        print(f"最大比例: {stats['max_ratio']:.2f}")
        print(f"平均比例: {stats['avg_ratio']:.2f}\n")
    else:
        print(f"{category} 没有成功完成的任务。\n")
