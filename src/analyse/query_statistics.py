import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from collections import Counter
import seaborn as sns
import json

def main():
    all_data = []
    file_paths = [
        "data/dev/test/10-1-100-s.json",
        "data/dev/test/30-1-100-s.json"
    ]
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_data.extend(data)
    
    print(len(all_data))

    fig = plt.figure(figsize=(6, 15))
    plt.rcParams.update({
        'font.size': 18,
        'axes.titlesize': 18,
        'axes.labelsize': 18,
        'xtick.labelsize': 15,
        'ytick.labelsize': 15,
        'axes.titleweight': 'bold'
    })

    gs = GridSpec(2, 1, height_ratios=[2, 3])
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    token_counts = [d['tokens'] for d in all_data]
    sns.histplot(
        token_counts,
        kde=True,
        bins=min(20, len(set(token_counts))),
        color='blue',
        edgecolor='black',
        ax=ax1
    )
    ax1.set_xlabel('Token Count')
    ax1.set_ylabel('Frequency')
    
    
    keywords = [d['keyword'] for d in all_data]
    category_counts = Counter(keywords)
    
    # combine categories with less than 1% of the data into
    # a single category called "Other"
    min_threshold = 0.01 * sum(category_counts.values()) 
    labels = []
    sizes = []
    other_size = 0
    for k, v in category_counts.items():
        if v >= min_threshold:
            labels.append(k)
            sizes.append(v)
        else:
            other_size += v
    if other_size > 0:
        labels.append("Other")
        sizes.append(other_size)

    wedges, texts, autotexts = ax2.pie(
        sizes,
        labels=labels,
        autopct=lambda p: f'{p:.1f}%' if p >= 5 else '',
        startangle=140,
        colors=plt.cm.Paired.colors,
        textprops={ 'fontsize': 18},
        pctdistance=0.8
    )
    
    img_path = "data/result/figures/specific_task_statistics"
    plt.savefig(f"{img_path}.png", bbox_inches='tight')
    plt.close()
    print(f"File saved in {img_path}.png")

if __name__ == "__main__":
    main()