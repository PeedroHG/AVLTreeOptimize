import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot():
    data_path = os.path.join(os.path.dirname(__file__), '../../data/results_search.csv')
    out_dir = os.path.join(os.path.dirname(__file__), '../../analysis/search_performance')
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    
    print("Generating Search Performance Plots...")
    df = pd.read_csv(data_path)
    sns.set_theme(style="whitegrid")
    
    # Plot 1: Search Latency Comparison
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(data=df, x='Method', y='Avg_Search_Time_ns', palette=['#4c72b0', '#dd8452'])
    
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f ns', padding=3, fontsize=12)
        
    plt.title('Average Search Latency (Read Performance)', fontsize=14)
    plt.ylabel('Time per Search (nanoseconds)', fontsize=12)
    plt.ylim(0, df['Avg_Search_Time_ns'].max() * 1.2)
    
    # Add text annotation about height
    h_std = df[df['Method']=='Standard']['Final_Height'].values[0]
    h_opt = df[df['Method']=='Optimized']['Final_Height'].values[0]
    
    plt.text(0, df['Avg_Search_Time_ns'].min() * 0.5, f"Height: {h_std}", 
             ha='center', color='white', fontweight='bold')
    plt.text(1, df['Avg_Search_Time_ns'].min() * 0.5, f"Height: {h_opt}", 
             ha='center', color='white', fontweight='bold')

    plt.savefig(os.path.join(out_dir, 'search_latency.png'), dpi=300)
    print("Plot generated: search_latency.png")

if __name__ == '__main__':
    plot()