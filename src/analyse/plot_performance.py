import os
import json
import argparse
import matplotlib.pyplot as plt
import numpy as np

def process_model_data(model, test_points):
    """Process model data and calculate metrics including time/cost ratios."""
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
                
                # Parse model result
                if "result" in item and isinstance(item["result"], list) and len(item["result"]) >= 2:
                    model_ans = item["result"][0]
                    model_time = item["result"][0]
                    model_cost = item["result"][1]
                
                # Get optimal values
                optimal_ans = item["question"]["min_time"]
                optimal_cost_val = item["question"]["min_cost"]
                
                # Calculate ratios
                if model_ans is not None and str(model_ans).strip() != "":
                    success_count += 1
                    time_ratio = model_time / optimal_ans if optimal_ans != 0 else 4
                    cost_ratio = model_cost / optimal_cost_val if optimal_cost_val != 0 else 4
                    
                    # Check optimal
                    if str(model_ans) == str(optimal_ans) and (model_cost == optimal_cost_val):
                        optimal_count += 1
                else:
                    time_ratio = 4.0
                    cost_ratio = 4.0
                
                time_ratio_sum += time_ratio
                cost_ratio_sum += cost_ratio
        
        # Calculate averages
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

def setup_plt_style():
    """Set plotting style for reuse by other functions."""
    plt.style.use('seaborn-v0_8-whitegrid')
    
    plt.rcParams.update({
        'font.size': 18,
        'axes.titlesize': 18,
        'axes.labelsize': 18,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'axes.titleweight': 'bold'
    })

def create_performance_plot(models, test_points=None):
    """
    Create the performance comparison figure and return the plt object.
    
    Args:
        models: List of model names to evaluate.
        test_points: List of test points, default is [10, 20, 30, 40, 50].
        
    Returns:
        tuple: (plt, fig) Matplotlib pyplot object and figure object.
    """
    setup_plt_style()
    
    if test_points is None:
        test_points = [10, 20, 30, 40, 50]

    # Initialize data containers
    metrics = {
        'success': {},
        'optimal': {},
        'time_ratio': {},
        'cost_ratio': {}
    }

    model_names = {
        "gpt-4o": "GPT-4o",
        "Llama-3.1-8B-Instruct": "Llama",
        "Llama-3.1-8B-Instruct-DPO": "Llama-Trained",
        "claude-3-5-sonnet-20241022": "Claude",
    }
    
    # Process data for all models
    for model in models:
        s, o, t, c = process_model_data(model, test_points)
        model_display = model_names.get(model, model)  # Use mapped name or original name
        metrics['success'][model_display] = s
        metrics['optimal'][model_display] = o
        metrics['time_ratio'][model_display] = t
        metrics['cost_ratio'][model_display] = c

    # Create figure with two subplots
    fig = plt.figure(figsize=(28, 7.5))

    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1], wspace=0.15)
    ax_top = fig.add_subplot(gs[0])
    ax_bottom = fig.add_subplot(gs[1])
    
    # Styling configuration
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    style_config = {
        'top': {
            'time_ratio': {'ls': '-', 'marker': 'o'},
            'cost_ratio': {'ls': '--', 'marker': 's'}
        },
        'bottom': {
            'success': {'ls': '-', 'marker': 'o'},
            'optimal': {'ls': '--', 'marker': 's'}
        }
    }

    # Plot top axes (ratios)
    for idx, model in enumerate(models):
        model_display = model_names.get(model, model)
        color = colors[idx % len(colors)]
        
        # Plot time ratio
        ax_top.plot(
            test_points, metrics['time_ratio'][model_display],
            color=color,
            linestyle=style_config['top']['time_ratio']['ls'],
            marker=style_config['top']['time_ratio']['marker'],
            linewidth=1,
            markersize=6,
            label=f'{model_display} Time or Success'
        )
        
        # Plot cost ratio
        ax_top.plot(
            test_points, metrics['cost_ratio'][model_display],
            color=color,
            linestyle=style_config['top']['cost_ratio']['ls'],
            marker=style_config['top']['cost_ratio']['marker'],
            linewidth=1,
            markersize=6,
            label=f'{model_display} Cost or Optimal'
        )

    # Configure top axes
    ax_top.set_title('Time & Cost Ratios', pad=8, weight='bold')
    ax_top.set_xlabel('Number of Test Points')
    ax_top.set_ylabel('Ratio')
    ax_top.set_ylim(0, 5.5)
    ax_top.grid(True, linestyle='--', alpha=0.7)
    ax_top.axhline(4, color='gray', linestyle=':', alpha=0.7)  # Threshold line

    # Plot bottom axes (success rates)
    for idx, model in enumerate(models):
        model_display = model_names.get(model, model)
        color = colors[idx % len(colors)]
        
        # Plot success rate
        ax_bottom.plot(
            test_points, metrics['success'][model_display],
            color=color,
            linestyle=style_config['bottom']['success']['ls'],
            marker=style_config['bottom']['success']['marker'],
            linewidth=1,
            markersize=6,
            label=f'{model_display} Success'
        )
        
        # Plot optimal rate
        ax_bottom.plot(
            test_points, metrics['optimal'][model_display],
            color=color,
            linestyle=style_config['bottom']['optimal']['ls'],
            marker=style_config['bottom']['optimal']['marker'],
            linewidth=1,
            markersize=6,
            label=f'{model_display} Optimal'
        )

    # Configure bottom axes
    ax_bottom.set_title('Success & Optimal Rates', pad=7)
    ax_bottom.set_xlabel('Number of Test Points')
    ax_bottom.set_ylabel('Rate')
    ax_bottom.set_ylim(0, 1.05)
    ax_bottom.set_xticks(test_points)
    ax_bottom.grid(True, linestyle='--', alpha=0.7)

    # Create unified legend
    handles_top, labels_top = ax_top.get_legend_handles_labels()
    handles_bottom, labels_bottom = ax_bottom.get_legend_handles_labels()
    
    top_legend = ax_top.legend(
        loc='upper center',
        bbox_to_anchor=(1.05, 1.25), 
        ncol=4,
        # fontsize=10,
        frameon=True,
    )
    top_legend.get_title().set_position((-40, -15))
    
    return plt, fig

def save_plot(plt, fig, output_dir="data/result/figures", filename_base="node_results_line"):
    """Save plots to the specified location."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save PNG format
    output_file = os.path.join(output_dir, f"{filename_base}.png")
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    print(f"Plot saved to: {output_file}")
    
    # Save PDF format
    output_file = os.path.join(output_dir, f"{filename_base}.pdf")
    plt.savefig(output_file, bbox_inches='tight')
    print(f"Plot saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Plot model performance vs. number of test points")
    parser.add_argument("--models", nargs="+", required=True, help="List of model names to evaluate")
    args = parser.parse_args()

    # Create plot
    plt_obj, fig = create_performance_plot(args.models)
    
    # Save plot
    save_plot(plt_obj, fig)

if __name__ == "__main__":
    main()