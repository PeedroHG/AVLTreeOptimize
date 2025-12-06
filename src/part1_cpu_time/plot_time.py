import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_10k_analysis():
    # Caminho relativo para a pasta data
    data_path = os.path.join(os.path.dirname(__file__), '../../data/results_deletion_time_comprehensive.csv')
    out_dir = os.path.join(os.path.dirname(__file__), '../../analysis/cpu_time')
    
    # Criar diretório se não existir
    if not os.path.exists(out_dir): os.makedirs(out_dir)

    print(f"Lendo dados de: {data_path}")
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print("Erro: Arquivo CSV não encontrado. Verifique se o benchmark foi executado e o arquivo salvo.")
        return

    # Filtrar apenas dados de N = 10.000
    df_10k = df[df['Size'] == 10000].copy()

    if df_10k.empty:
        print("Aviso: Não foram encontrados dados para Size=10000 no CSV.")
        return

    # Calcular a média das repetições para o gráfico
    # (O Seaborn faz isso automático, mas calculamos para garantir os labels corretos)
    df_avg = df_10k.groupby(['Scenario', 'Method'], as_index=False)['Deletion_Time_ms'].mean()

    # --- CONFIGURAÇÃO ESTÉTICA ---
    sns.set_theme(style="white")
    plt.rcParams['font.family'] = 'sans-serif'
    
    cores_personalizadas = {
        "Standard": "#f03a53",
        "Optimized": "#0bafee"
    }

    plt.figure(figsize=(8, 6))
    
    # Plotar Gráfico de Barras
    ax = sns.barplot(
        data=df_avg,
        x='Scenario',
        y='Deletion_Time_ms',
        hue='Method',
        palette=cores_personalizadas,
        edgecolor=".2",
        linewidth=0,   # Sem bordas
        width=0.6      # Barras mais finas
    )
    ax.set_ylim(top=df_avg['Deletion_Time_ms'].max() * 1.25)
    # Títulos e Labels
    plt.ylabel('Deletion Time (ms)', fontsize=11)
    plt.xlabel('')
    plt.legend(
    title=None,
    loc='upper left',
    bbox_to_anchor=(0.02, 0.98),
    frameon=False
)
    
    # Remover "caixa" do gráfico (spines)
    sns.despine()

    # Adicionar os valores exatos em cima das barras
    for container in ax.containers:
        # Pega a altura da barra e escreve o valor
        ax.bar_label(container, fmt='%.1f ms', padding=3, fontsize=10, fontweight='bold')

    plt.tight_layout()
    # Salvar
    save_path = os.path.join(out_dir, 'cpu_tradeoff_10k.png')
    plt.savefig(save_path, dpi=600)
    print(f"Gráfico salvo com sucesso em: {save_path}")

if __name__ == '__main__':
    plot_10k_analysis()