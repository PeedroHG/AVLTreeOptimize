import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot():
    # Caminhos relativos baseados na estrutura de pastas
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, '../../data/results_structure.csv')
    out_dir = os.path.join(base_dir, '../../analysis/structure_io')
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    print(f"Loading data from: {data_path}")
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print("Error: CSV file not found. Run the benchmark first.")
        return

    sns.set_theme(style="whitegrid")
    
    # --- PLOT 1: Rotations vs Size (Scalability) ---
    print("Generating Scalability Plot...")
    
    # Filters only scaling scenarios (Random and Sorted)
    df_scaling = df[df['Scenario'].isin(['Random', 'Sorted'])]
    
    plt.figure(figsize=(10, 6))
    
    # OBS: O Seaborn automaticamente calcula a média e o intervalo de confiança (sombra)
    # para as 5 repetições. Não é necessário agrupar manualmente aqui.
    sns.lineplot(
        data=df_scaling, 
        x='Size', 
        y='Total_Rotations', 
        hue='Method', 
        style='Scenario', 
        markers=True, 
        dashes=False,
        err_style='band' # Desenha a sombra de variação entre os testes
    )
    
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Scalability: Rotations vs Tree Size (Lower is Better)', fontsize=14)
    plt.ylabel('Total Rotations (Log Scale)', fontsize=12)
    plt.xlabel('Tree Size N (Log Scale)', fontsize=12)
    plt.grid(True, which="both", ls="-", alpha=0.5)
    
    plot1_path = os.path.join(out_dir, 'rotations_scaling.png')
    plt.savefig(plot1_path, dpi=300)
    print(f"Saved: {plot1_path}")
    
    # --- PLOT 2: Write Amplification Reduction % (Bar Chart) ---
    print("Generating Efficiency Bar Chart...")
    
    # 1. Agrupar por Cenário/Método/Tamanho e tirar a MÉDIA das 5 repetições
    # Isso é crucial agora que temos múltiplas execuções para todos os cenários.
    df_mean = df.groupby(['Scenario', 'Method', 'Size'], as_index=False)['Total_Rotations'].mean()
    
    # 2. Selecionar os dados para comparação
    # Para Random e Sorted, pegamos o MAIOR tamanho testado (ex: 1.000.000)
    max_size = df[df['Scenario'] != 'Long_Running']['Size'].max()
    df_high_volume = df_mean[
        (df_mean['Size'] == max_size) & 
        (df_mean['Scenario'].isin(['Random', 'Sorted']))
    ].copy()
    
    # Para Long_Running, pegamos ele independente do tamanho (pois ele representa 1M ops)
    df_long = df_mean[df_mean['Scenario'] == 'Long_Running'].copy()
    
    # 3. Combinar os dados
    df_final = pd.concat([df_high_volume, df_long])
    
    # 4. Calcular a redução percentual usando Pivot Table
    pivot = df_final.pivot(index='Scenario', columns='Method', values='Total_Rotations')
    
    # Fórmula: (Standard - Optimized) / Standard
    pivot['Reduction_Pct'] = ((pivot['Standard'] - pivot['Optimized']) / pivot['Standard']) * 100
    
    # Ordenar para exibição consistente
    # Vamos reindexar para garantir uma ordem lógica no gráfico
    desired_order = ['Random', 'Sorted', 'Long_Running']
    pivot = pivot.reindex(desired_order)
    
    # Debug: Mostrar os valores calculados no console
    print("\nCalculated Reductions:")
    print(pivot['Reduction_Pct'])
    
    # Plotagem
    plt.figure(figsize=(8, 6))
    
    # Reset index para usar no barplot
    plot_data = pivot.reset_index()
    
    ax = sns.barplot(
        data=plot_data,
        x='Scenario', 
        y='Reduction_Pct', 
        color='cornflowerblue',
        edgecolor='black'
    )
    
    # Adicionar os rótulos de porcentagem
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', padding=3, weight='bold', fontsize=11)
    
    plt.title('Write Reduction Efficiency (High Volume)', fontsize=14)
    plt.ylabel('Reduction in Rotations (%)', fontsize=12)
    plt.xlabel('Scenario', fontsize=12)
    plt.ylim(0, max(pivot['Reduction_Pct']) * 1.2) # Dá 20% de respiro no topo
    
    plot2_path = os.path.join(out_dir, 'reduction_efficiency.png')
    plt.savefig(plot2_path, dpi=300)
    print(f"Saved: {plot2_path}")
    
    print("\nAll plots generated successfully.")

if __name__ == '__main__':
    plot()