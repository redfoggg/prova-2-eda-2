import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

def load_data():
    """Carrega os dados do arquivo JSON"""
    with open('questao_3_resultados.json', 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data['experiments'])

def plot_fp_rate_vs_hashes(df):
    """Gráfico da taxa de falsos positivos vs número de hashes"""
    plt.figure(figsize=(12, 8))
    
    # Agrupar por tamanho do filtro
    sizes = df['size'].unique()
    colors = plt.cm.viridis(np.linspace(0, 1, len(sizes)))
    
    for i, size in enumerate(sizes):
        data_size = df[df['size'] == size]
        plt.plot(data_size['numHashes'], data_size['fpRate'] * 100, 
                marker='o', linewidth=2, markersize=8, 
                label=f'Tamanho = {size:,}', color=colors[i])
    
    plt.xlabel('Número de Funções Hash (k)')
    plt.ylabel('Taxa de Falsos Positivos (%)')
    plt.title('Taxa de Falsos Positivos vs Número de Funções Hash\npara Diferentes Tamanhos de Filtro')
    plt.legend(title='Tamanho do Filtro', loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('bloom_fp_rate_vs_hashes.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_performance_metrics(df):
    """Gráfico de métricas de desempenho (tempo de inserção e consulta)"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    sizes = df['size'].unique()
    colors = plt.cm.plasma(np.linspace(0, 1, len(sizes)))
    
    # Tempo de inserção
    for i, size in enumerate(sizes):
        data_size = df[df['size'] == size]
        ax1.plot(data_size['numHashes'], data_size['insertTime'], 
                marker='s', linewidth=2, markersize=8, 
                label=f'Tamanho = {size:,}', color=colors[i])
    
    ax1.set_xlabel('Número de Funções Hash (k)')
    ax1.set_ylabel('Tempo de Inserção (ms)')
    ax1.set_title('Tempo de Inserção vs Número de Funções Hash')
    ax1.legend(title='Tamanho do Filtro', loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Tempo de consulta
    for i, size in enumerate(sizes):
        data_size = df[df['size'] == size]
        ax2.plot(data_size['numHashes'], data_size['queryTime'], 
                marker='o', linewidth=2, markersize=8, 
                label=f'Tamanho = {size:,}', color=colors[i])
    
    ax2.set_xlabel('Número de Funções Hash (k)')
    ax2.set_ylabel('Tempo de Consulta (ms)')
    ax2.set_title('Tempo de Consulta vs Número de Funções Hash')
    ax2.legend(title='Tamanho do Filtro', loc='best')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('bloom_performance_metrics.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_fill_ratio(df):
    """Gráfico da taxa de preenchimento do filtro"""
    plt.figure(figsize=(12, 8))
    
    sizes = df['size'].unique()
    colors = plt.cm.coolwarm(np.linspace(0, 1, len(sizes)))
    
    for i, size in enumerate(sizes):
        data_size = df[df['size'] == size]
        plt.plot(data_size['numHashes'], data_size['fillRatio'] * 100, 
                marker='D', linewidth=2, markersize=8, 
                label=f'Tamanho = {size:,}', color=colors[i])
    
    plt.xlabel('Número de Funções Hash (k)')
    plt.ylabel('Taxa de Preenchimento (%)')
    plt.title('Taxa de Preenchimento do Filtro vs Número de Funções Hash')
    plt.legend(title='Tamanho do Filtro', loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('bloom_fill_ratio.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_theoretical_vs_observed(df, num_elements=10000):
    """Compara taxa de FP teórica vs observada"""
    plt.figure(figsize=(14, 8))
    
    # Calcular taxa teórica para cada experimento
    theoretical_fp = []
    for _, row in df.iterrows():
        k = row['numHashes']
        m = row['size']
        n = num_elements
        # Taxa teórica: (1 - e^(-kn/m))^k
        fp_theory = (1 - np.exp(-k * n / m)) ** k
        theoretical_fp.append(fp_theory * 100)
    
    # Scatter plot
    plt.scatter(theoretical_fp, df['fpRate'] * 100, 
               c=df['size'], cmap='viridis', s=100, alpha=0.7, edgecolors='black')
    
    # Linha de referência (y=x)
    max_val = max(max(theoretical_fp), df['fpRate'].max() * 100)
    plt.plot([0, max_val], [0, max_val], 'r--', linewidth=2, label='Perfeita Concordância')
    
    plt.xlabel('Taxa de FP Teórica (%)')
    plt.ylabel('Taxa de FP Observada (%)')
    plt.title('Comparação entre Taxa de Falsos Positivos Teórica e Observada')
    plt.colorbar(label='Tamanho do Filtro')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('bloom_theoretical_vs_observed.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_optimal_k_analysis(df, num_elements=10000):
    """Análise do número ótimo de funções hash"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    sizes = df['size'].unique()
    
    # Para cada tamanho, encontrar o k com menor FP rate
    optimal_k_observed = []
    optimal_k_theoretical = []
    min_fp_rates = []
    
    for size in sizes:
        data_size = df[df['size'] == size]
        best_row = data_size.loc[data_size['fpRate'].idxmin()]
        optimal_k_observed.append(best_row['numHashes'])
        min_fp_rates.append(best_row['fpRate'] * 100)
        
        # k ótimo teórico = (m/n) * ln(2)
        k_theory = (size / num_elements) * np.log(2)
        optimal_k_theoretical.append(k_theory)
    
    # Gráfico 1: K ótimo teórico vs observado
    x = range(len(sizes))
    width = 0.35
    
    ax1.bar([i - width/2 for i in x], optimal_k_theoretical, width, 
            label='K Ótimo Teórico', color='skyblue', edgecolor='black')
    ax1.bar([i + width/2 for i in x], optimal_k_observed, width, 
            label='K Ótimo Observado', color='lightcoral', edgecolor='black')
    
    ax1.set_xlabel('Tamanho do Filtro')
    ax1.set_ylabel('Número Ótimo de Funções Hash')
    ax1.set_title('Comparação entre K Ótimo Teórico e Observado')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'{s:,}' for s in sizes], rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Gráfico 2: Taxa de FP mínima para cada tamanho
    ax2.plot(sizes, min_fp_rates, marker='o', linewidth=2, markersize=10, color='darkgreen')
    ax2.set_xlabel('Tamanho do Filtro')
    ax2.set_ylabel('Taxa de FP Mínima (%)')
    ax2.set_title('Taxa de Falsos Positivos Mínima por Tamanho de Filtro')
    ax2.set_xscale('log')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('bloom_optimal_k_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_memory_efficiency(df, num_elements=10000):
    """Análise de eficiência de memória"""
    plt.figure(figsize=(12, 8))
    
    sizes = df['size'].unique()
    
    # Calcular bits por elemento e taxa de FP média para cada tamanho
    bits_per_element = []
    avg_fp_rates = []
    
    for size in sizes:
        bits_per_element.append(size / num_elements)
        data_size = df[df['size'] == size]
        avg_fp_rates.append(data_size['fpRate'].mean() * 100)
    
    # Criar gráfico com dois eixos Y
    _, ax1 = plt.subplots(figsize=(12, 8))
    
    color = 'tab:blue'
    ax1.set_xlabel('Bits por Elemento')
    ax1.set_ylabel('Taxa de FP Média (%)', color=color)
    ax1.plot(bits_per_element, avg_fp_rates, marker='o', linewidth=3, 
            markersize=10, color=color, label='Taxa de FP Média')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)
    
    # Adicionar linha de tendência
    z = np.polyfit(bits_per_element, avg_fp_rates, 2)
    p = np.poly1d(z)
    x_smooth = np.linspace(min(bits_per_element), max(bits_per_element), 100)
    ax1.plot(x_smooth, p(x_smooth), '--', color='darkblue', alpha=0.7, linewidth=2)
    
    # Anotar pontos com tamanhos
    for _, (bits, fp, size) in enumerate(zip(bits_per_element, avg_fp_rates, sizes)):
        ax1.annotate(f'{size:,}', (bits, fp), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=10)
    
    plt.title('Eficiência de Memória: Taxa de FP vs Bits por Elemento')
    plt.tight_layout()
    plt.savefig('bloom_memory_efficiency.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_summary_dashboard(df):
    """Cria um dashboard com resumo dos principais resultados"""
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Taxa de FP por tamanho e k
    ax1 = fig.add_subplot(gs[0, :2])
    pivot_fp = df.pivot(index='numHashes', columns='size', values='fpRate')
    im = ax1.imshow(pivot_fp.values * 100, cmap='RdYlGn_r', aspect='auto')
    ax1.set_xticks(range(len(pivot_fp.columns)))
    ax1.set_xticklabels([f'{s:,}' for s in pivot_fp.columns])
    ax1.set_yticks(range(len(pivot_fp.index)))
    ax1.set_yticklabels(pivot_fp.index)
    ax1.set_xlabel('Tamanho do Filtro')
    ax1.set_ylabel('Número de Hashes')
    ax1.set_title('Taxa de Falsos Positivos (%)')
    plt.colorbar(im, ax=ax1)
    
    # Adicionar valores no heatmap
    for i in range(len(pivot_fp.index)):
        for j in range(len(pivot_fp.columns)):
            text = ax1.text(j, i, f'{pivot_fp.values[i, j]*100:.1f}', 
                           ha="center", va="center", color="black", fontsize=9)
    
    # 2. Tempo médio de operação
    ax2 = fig.add_subplot(gs[0, 2])
    avg_times = df.groupby('numHashes')[['insertTime', 'queryTime']].mean()
    avg_times.plot(kind='bar', ax=ax2, color=['steelblue', 'orange'])
    ax2.set_xlabel('Número de Hashes')
    ax2.set_ylabel('Tempo (ms)')
    ax2.set_title('Tempo Médio de Operação')
    ax2.legend(['Inserção', 'Consulta'])
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Taxa de preenchimento média
    ax3 = fig.add_subplot(gs[1, :])
    for size in df['size'].unique():
        data_size = df[df['size'] == size]
        ax3.plot(data_size['numHashes'], data_size['fillRatio'] * 100, 
                marker='o', linewidth=2, label=f'{size:,}')
    ax3.set_xlabel('Número de Hashes')
    ax3.set_ylabel('Taxa de Preenchimento (%)')
    ax3.set_title('Taxa de Preenchimento por Configuração')
    ax3.legend(title='Tamanho', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax3.grid(True, alpha=0.3)
    
    # 4. Estatísticas resumidas
    ax4 = fig.add_subplot(gs[2, :])
    ax4.axis('off')
    
    # Calcular estatísticas
    best_config = df.loc[df['fpRate'].idxmin()]
    worst_config = df.loc[df['fpRate'].idxmax()]
    fastest_insert = df.loc[df['insertTime'].idxmin()]
    
    summary_text = f"""
    📊 RESUMO DOS EXPERIMENTOS COM BLOOM FILTER
    
    ✅ Melhor Configuração (Menor Taxa de FP):
       • Tamanho: {best_config['size']:,} | Hashes: {best_config['numHashes']} | Taxa FP: {best_config['fpRate']*100:.2f}%
    
    ❌ Pior Configuração (Maior Taxa de FP):
       • Tamanho: {worst_config['size']:,} | Hashes: {worst_config['numHashes']} | Taxa FP: {worst_config['fpRate']*100:.2f}%
    
    ⚡ Inserção Mais Rápida:
       • Tamanho: {fastest_insert['size']:,} | Hashes: {fastest_insert['numHashes']} | Tempo: {fastest_insert['insertTime']:.2f}ms
    
    📈 Insights:
       • Aumentar o número de hashes reduz a taxa de FP, mas aumenta o tempo de operação
       • Filtros maiores têm menor taxa de FP, mas usam mais memória
       • A taxa de preenchimento aumenta com mais hashes e elementos
    """
    
    ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes, 
            fontsize=12, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))
    
    plt.suptitle('Dashboard de Análise - Experimentos com Bloom Filter', fontsize=16)
    plt.tight_layout()
    plt.savefig('bloom_summary_dashboard.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Função principal para gerar todos os gráficos"""
    print("Carregando dados...")
    df = load_data()
    
    print("\nGerando gráficos...")
    
    print("1. Taxa de falsos positivos vs número de hashes...")
    plot_fp_rate_vs_hashes(df)
    
    print("2. Métricas de desempenho...")
    plot_performance_metrics(df)
    
    print("3. Taxa de preenchimento...")
    plot_fill_ratio(df)
    
    print("4. Comparação teórico vs observado...")
    plot_theoretical_vs_observed(df)
    
    print("5. Análise do K ótimo...")
    plot_optimal_k_analysis(df)
    
    print("6. Eficiência de memória...")
    plot_memory_efficiency(df)
    
    print("7. Dashboard resumido...")
    create_summary_dashboard(df)
    
    print("\n✅ Todos os gráficos foram gerados com sucesso!")
    print("📁 Arquivos salvos:")
    print("   - bloom_fp_rate_vs_hashes.png")
    print("   - bloom_performance_metrics.png")
    print("   - bloom_fill_ratio.png")
    print("   - bloom_theoretical_vs_observed.png")
    print("   - bloom_optimal_k_analysis.png")
    print("   - bloom_memory_efficiency.png")
    print("   - bloom_summary_dashboard.png")

if __name__ == '__main__':
    main() 
