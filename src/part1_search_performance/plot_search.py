import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/results_unified_search.csv')
OUT_DIR = os.path.join(os.path.dirname(__file__), '../../analysis/search_performance')

# Cores definidas:
COLORS = {
    'Standard': '#f03a53',
    'Optimized': '#0bafee'
}

ORDER = ['Standard', 'Optimized']  # ordem fixa


def load_data():
    if not os.path.exists(DATA_PATH):
        print("Erro: CSV não encontrado.")
        return None
    
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    return pd.read_csv(DATA_PATH)


# ============================================================
# 1) LATÊNCIA
# ============================================================
def plot_latency():
    df = load_data()
    if df is None:
        return

    sns.set_theme(style="white")
    plt.figure(figsize=(7, 5))

    # barras sem desvio (erro = None) e ordem fixa
    ax = sns.barplot(
        data=df,
        x='Method',
        y='Avg_Search_Time_ns',
        hue='Method',
        palette=COLORS,
        order=ORDER,
        hue_order=ORDER,
        legend=False,
        width=0.45,
        errorbar=None  # remove indicativo de desvio
    )

    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f ns', padding=3, fontweight='bold')

    plt.ylabel("Search Time (ns)", fontsize=12)

    sns.despine(top=True, right=True)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'search_latency.png'), dpi=600)
    print("Gráfico salvo: search_latency.png")


# ============================================================
# 2) PROFUNDIDADE
# ============================================================
def plot_depth():
    df = load_data()
    if df is None:
        return

    sns.set_theme(style="white")
    plt.figure(figsize=(7, 5))

    means = df.groupby('Method')['Avg_Depth'].mean().reset_index()

    ax = sns.barplot(
        data=means,
        x='Method',
        y='Avg_Depth',
        hue='Method',
        palette=COLORS,
        order=ORDER,
        hue_order=ORDER,
        legend=False,
        width=0.45,
        errorbar=None  # remove indicativo de desvio
    )

    for container in ax.containers:
        ax.bar_label(container, fmt='%.3f', padding=3, fontweight='bold')

    plt.ylabel("Average Depth", fontsize=12)

    sns.despine(top=True, right=True)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'avg_depth.png'), dpi=600)
    print("Gráfico salvo: avg_depth.png")


# ============================================================
# Execução
# ============================================================
if __name__ == '__main__':
    plot_latency()
    plot_depth()
