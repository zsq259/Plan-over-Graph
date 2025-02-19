import os
import json
import pandas as pd
import matplotlib.pyplot as plt

def load_test_results(results_dir):
    models = [d for d in os.listdir(results_dir) if os.path.isdir(os.path.join(results_dir, d))]
    models.remove("figures")
    print(models)
    test_files = set()
    model_data_counts = {}

    for model in models:
        model_path = os.path.join(results_dir, model)
        model_data_counts[model] = {}

        for filename in os.listdir(model_path):
            if filename.endswith(".json"):
                test_name = filename.replace("-output.json", "")
                test_files.add(test_name)

                file_path = os.path.join(model_path, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        model_data_counts[model][test_name] = len(data)
                    except json.JSONDecodeError:
                        model_data_counts[model][test_name] = "Error"

    return model_data_counts, sorted(test_files)


def save_table_as_image(df, output_path):
    fig, ax = plt.subplots(figsize=(len(df.columns) * 0.8 + 3, len(df) * 0.5 + 2))
    ax.axis("tight")
    ax.axis("off")

    table = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     rowLabels=df.index,
                     cellLoc="center",
                     loc="center")

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df.columns))))

    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()


if __name__ == "__main__":
    RESULTS_DIR = "data/result/"
    OUTPUT_IMG = RESULTS_DIR + "figures/model_test_summary.png"

    model_data_counts, test_files = load_test_results(RESULTS_DIR)
    df = pd.DataFrame.from_dict(model_data_counts, orient="index", columns=test_files).fillna(0)
    df = df.sort_index(axis=1).sort_index(axis=0)
    save_table_as_image(df, OUTPUT_IMG)

    print("Table saved as image:", OUTPUT_IMG)