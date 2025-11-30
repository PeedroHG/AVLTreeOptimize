import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot():
    data_path = os.path.join(os.path.dirname(__file__), '../../data/results_structure.csv')
    out_dir = os.path.join(os.path.dirname(__file__), '../../analysis/structure_io')
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    
    print("Generating Phase 2 Plots...")
    df = pd.read_csv(data_path)
    sns.set_theme(style="whitegrid")
    
    # --- PLOT 1: Rotations vs Size (Log Scale) ---
    # Filters only scaling scenarios
    df_scaling = df[df['Scenario'].isin(['Random', 'Sorted'])]
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_scaling, x='Size', y='Total_Rotations', hue='Method', style='Scenario', markers=True, dashes=False)
    plt.xscale('log')
    plt.yscale('log') # Rotations grow fast, log scale helps visualization
    plt.title('Scalability: Rotations vs Tree Size', fontsize=14)
    plt.ylabel('Total Rotations (Log Scale)', fontsize=12)
    plt.xlabel('Tree Size N (Log Scale)', fontsize=12)
    plt.savefig(os.path.join(out_dir, 'rotations_scaling.png'), dpi=300)
    
    # --- PLOT 2: Write Amplification Reduction % (Bar Chart) ---
    # Aggregate means to calculate %
    df_mean = df.groupby(['Scenario', 'Method', 'Size'], as_index=False)['Total_Rotations'].mean()
    
    # We create a specific view for the largest size (1M) to show the impact
    df_1m = df_mean[df_mean['Size'] == 1000000].copy()
    # Add Long Running (which is 100k but represents large volume)
    df_long = df_mean[df_mean['Scenario'] == 'Long_Running'].copy()
    
    df_final = pd.concat([df_1m, df_long])
    
    # Calculation logic
    pivot = df_final.pivot(index='Scenario', columns='Method', values='Total_Rotations')
    pivot['Reduction_Pct'] = ((pivot['Standard'] - pivot['Optimized']) / pivot['Standard']) * 100
    
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x=pivot.index, y=pivot['Reduction_Pct'], color='cornflowerblue')
    for container in ax.containers: ax.bar_label(container, fmt='%.1f%%', padding=3, weight='bold')
    
    plt.title('Write Reduction Efficiency (High Volume)', fontsize=14)
    plt.ylabel('Reduction in Rotations (%)', fontsize=12)
    plt.xlabel('Scenario', fontsize=12)
    plt.ylim(0, 25)
    plt.savefig(os.path.join(out_dir, 'reduction_efficiency.png'), dpi=300)
    
    print("Plots Phase 2 generated.")

if __name__ == '__main__':
    plot()