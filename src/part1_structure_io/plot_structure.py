import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Configurações e Constantes ---
CSV_REL_PATH = '../../data/results_structure.csv'
OUT_DIR_REL_PATH = '../../analysis/structure_io'

def configurar_ambiente():
    """Define caminhos e cria diretórios de saída se necessário."""
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, CSV_REL_PATH)
    out_dir = os.path.join(base_dir, OUT_DIR_REL_PATH)
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    return data_path, out_dir

def carregar_dados(data_path):
    """Lê o CSV e retorna o DataFrame. Retorna None em caso de erro."""
    print(f"Loading data from: {data_path}")
    try:
        return pd.read_csv(data_path)
    except FileNotFoundError:
        print("Error: CSV file not found. Run the benchmark first.")
        return None

def definir_estilo():
    """Aplica o tema visual global."""
    sns.set_theme(style="white")

def plotar_escalabilidade(df, out_dir):
    """Gera o gráfico de linha com legenda limpa (sem títulos de grupo)."""
    print("Generating Scalability Plot...")
    
    df_scaling = df[df['Scenario'].isin(['Random', 'Sorted'])]
    
    cores_personalizadas = {
        "Standard": "#f03a53",
        "Optimized": "#0bafee"
    }
    
    plt.figure(figsize=(10, 6))
    
    ax = sns.lineplot(
        data=df_scaling, 
        x='Size', 
        y='Total_Rotations', 
        hue='Method', 
        style='Scenario', 
        markers=True, 
        dashes=False,
        err_style='band',
        palette=cores_personalizadas,
        linewidth=2.5
    )
    
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('Total Rotations', fontsize=12, labelpad=10)
    plt.xlabel('Tree Size N', fontsize=12, labelpad=10)
    
    handles, labels = ax.get_legend_handles_labels()
    
    limpo_handles = []
    limpo_labels = []
    
    for h, l in zip(handles, labels):
        if l not in ['Method', 'Scenario']:
            limpo_handles.append(h)
            limpo_labels.append(l)
            
    ax.legend(limpo_handles, limpo_labels, frameon=False)
    
    sns.despine()
    
    save_path = os.path.join(out_dir, 'rotations_scaling.png')
    plt.savefig(save_path, dpi=600, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()

def _calcular_reducao_percentual(df):
    """Processa os dados para calcular a redução percentual usando SEMPRE tamanho N = 100k."""
    
    # Média por grupo
    df_mean = df.groupby(['Scenario', 'Method', 'Size'], as_index=False)['Total_Rotations'].mean()
    
    # Volume fixo comum a todos os cenários
    target_size = 100000
    
    # RANDOM + SORTED para N = 100k
    df_static = df_mean[
        (df_mean['Scenario'].isin(['Random', 'Sorted'])) &
        (df_mean['Size'] == target_size)
    ].copy()
    
    # LONG RUNNING (já é 100k)
    df_long = df_mean[df_mean['Scenario'] == 'Long_Running'].copy()
    
    # Junta os três cenários
    df_final = pd.concat([df_static, df_long], ignore_index=True)
    
    # Tabela pivot
    pivot = df_final.pivot(index='Scenario', columns='Method', values='Total_Rotations')
    
    # Cálculo
    pivot['Reduction_Pct'] = ((pivot['Standard'] - pivot['Optimized']) / pivot['Standard']) * 100
    
    # Renomeia cenário para estética
    pivot = pivot.rename(index={'Long_Running': 'Long Running'})
    
    # Ordem correta de exibição
    pivot = pivot.reindex(['Random', 'Sorted', 'Long Running'])
    
    return pivot.reset_index()

def plotar_eficiencia(df, out_dir):
    """Gera o gráfico de barras (Write Amplification Reduction %)."""
    print("Generating Efficiency Bar Chart...")
    
    plot_data = _calcular_reducao_percentual(df)
    custom_palette = ["#0bafee", "#f03a53", "#ffb91b"]

    plt.figure(figsize=(8, 6))
    
    ax = sns.barplot(
        data=plot_data,
        x='Scenario', 
        y='Reduction_Pct', 
        hue='Scenario',
        palette=custom_palette,
        edgecolor=None, 
        dodge=False,
        width=0.5
    )
    
    # Labels nas barras
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', padding=5, weight='bold', fontsize=12, color='#333333')
        
    plt.ylim(0, 25)
    plt.ylabel('Reduction in Rotations (%)', fontsize=12, labelpad=10)
    plt.xlabel('') 
    plt.xticks(fontsize=12, weight='medium')
    
    sns.despine(left=True, top=True, right=True)
    plt.tick_params(axis='y', length=0)
    
    save_path = os.path.join(out_dir, 'reduction_efficiency.png')
    plt.savefig(save_path, dpi=600, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()

def main():
    # 1. Configuração
    data_path, out_dir = configurar_ambiente()
    
    # 2. Carregamento
    df = carregar_dados(data_path)
    if df is None:
        return

    # 3. Estilo
    definir_estilo()
    
    # 4. Geração dos Gráficos
    plotar_escalabilidade(df, out_dir)
    plotar_eficiencia(df, out_dir)
    
    print("\nAll plots generated successfully.")

if __name__ == '__main__':
    main()
