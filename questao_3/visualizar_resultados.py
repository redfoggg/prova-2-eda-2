import json
import matplotlib.pyplot as plt

def plot_simple_results():
    with open('questao_3_resultados.json', 'r') as f:
        data = json.load(f)

    experiments = data['experiments']

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    sizes = sorted(list(set(exp['size'] for exp in experiments)))
    
    ax1.set_title('Taxa de Falsos Positivos vs. Número de Hashes', fontsize=14)
    ax1.set_xlabel('Número de Funções Hash (k)')
    ax1.set_ylabel('Taxa de Falsos Positivos (%)')

    colors = ['blue', 'green', 'red', 'purple', 'orange']
    markers = ['o', 's', '^', 'D', 'v']

    for i, size in enumerate(sizes):
        size_exps = [exp for exp in experiments if exp['size'] == size]
        size_exps.sort(key=lambda x: x['numHashes'])
        
        num_hashes = [exp['numHashes'] for exp in size_exps]
        fp_rates = [exp['fpRate'] * 100 for exp in size_exps]
        
        ax1.plot(num_hashes, fp_rates,
                 marker=markers[i], linestyle='-', label=f'Tamanho = {size:,}',
                 color=colors[i], linewidth=2, markersize=8)

    ax1.legend(title='Tamanho do Filtro')
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    ax2.set_title('Desempenho vs. Número de Hashes', fontsize=14)
    ax2.set_xlabel('Número de Funções Hash (k)')
    ax2.set_ylabel('Tempo de Operação (ms)')

    representative_size = sizes[len(sizes) // 2]
    size_exps = [exp for exp in experiments if exp['size'] == representative_size]
    size_exps.sort(key=lambda x: x['numHashes'])
    
    num_hashes = [exp['numHashes'] for exp in size_exps]
    insert_times = [exp['insertTime'] for exp in size_exps]
    query_times = [exp['queryTime'] for exp in size_exps]

    ax2.plot(num_hashes, insert_times,
             marker='s', linestyle='--', color='blue', 
             label=f'Inserção (Tamanho={representative_size:,})', linewidth=2, markersize=8)
    ax2.plot(num_hashes, query_times,
             marker='^', linestyle=':', color='green', 
             label=f'Consulta (Tamanho={representative_size:,})', linewidth=2, markersize=8)

    ax2.legend()
    ax2.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.savefig('analise_bloom_filter.png', dpi=300)
    plt.show()

    print("\n=== ANÁLISE DOS RESULTADOS ===\n")
    
    print("TAXA DE FALSOS POSITIVOS:")
    print("- Filtros maiores têm menor taxa de falsos positivos")
    print("- Existe um número ótimo de hashes para cada tamanho")
    print("- Muitos hashes podem piorar a taxa (filtro muito denso)")
    
    print("\nDESEMPENHO:")
    print("- O tempo aumenta linearmente com o número de hashes")
    print("- Inserção e consulta têm tempos similares")
    
    print(f"\nGráficos salvos em 'analise_bloom_filter.png'")

if __name__ == '__main__':
    plot_simple_results() 