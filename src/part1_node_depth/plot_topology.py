import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot():
    # Caminhos
    data_path = os.path.join(os.path.dirname(__file__), '../../data/results_topology_complete.csv')
    out_dir = os.path.join(os.path.dirname(__file__), '../../analysis/node_depth')
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    
    print("Gerando gráficos de Topologia...")
    df = pd.read_csv(data_path)
    sns.set_theme(style="whitegrid")
    
    # --- GRÁFICO: Profundidade Média (Compacidade) ---
    plt.figure(figsize=(10, 6))
    
    # Barplot com intervalo de confiança (ci) para mostrar robustez
    ax = sns.barplot(
        data=df, 
        x='Scenario', 
        y='Avg_Depth', 
        hue='Method', 
        palette='muted',
        gap=0.1
    )
    
    # Zoom no eixo Y para ver a diferença (A árvore tem ~16.6 de profundidade, a diferença é sutil)
    min_val = df['Avg_Depth'].min()
    max_val = df['Avg_Depth'].max()
    # Foca a câmera na "crista da onda"
    plt.ylim(min_val * 0.98, max_val * 1.01)
    
    # Labels precisos (3 casas decimais)
    for container in ax.containers:
        ax.bar_label(container, fmt='%.3f', padding=3, fontsize=10)
        
    plt.title('Análise de Compacidade: Profundidade Média dos Nós', fontsize=14)
    plt.ylabel('Profundidade Média (Menor é Melhor)', fontsize=12)
    plt.xlabel('Cenário de Teste', fontsize=12)
    # plt.legend(title='Método', loc='upper right')
    
    save_path = os.path.join(out_dir, 'avg_depth_comparison.png')
    plt.savefig(save_path, dpi=300)
    print(f"Gráfico salvo: {save_path}")

if __name__ == '__main__':
    plot()