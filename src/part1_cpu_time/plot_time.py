import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot():
    data_path = os.path.join(os.path.dirname(__file__), '../../data/results_time.csv')
    out_dir = os.path.join(os.path.dirname(__file__), '../../analysis/cpu_time')
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    
    print("Generating Phase 1 Plots...")
    df = pd.read_csv(data_path)
    
    sns.set_theme(style="whitegrid")
    
    plt.figure(figsize=(10, 6))
    # Seaborn automaticamente calcula a média das 5 repetições e desenha o intervalo de confiança
    sns.lineplot(data=df, x='Size', y='Execution_Time_ms', hue='Method', style='Method', markers=True, dashes=False)
    
    plt.title('CPU Execution Time Analysis (RAM)', fontsize=14)
    plt.ylabel('Time (ms)', fontsize=12)
    plt.xlabel('Input Size (N)', fontsize=12)
    plt.xscale('log') # Log scale fica melhor para visualizar 1k -> 1M
    
    save_path = os.path.join(out_dir, 'time_scaling.png')
    plt.savefig(save_path, dpi=300)
    print(f"Saved: {save_path}")

if __name__ == '__main__':
    plot()