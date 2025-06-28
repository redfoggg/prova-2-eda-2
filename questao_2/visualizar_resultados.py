import json
import matplotlib.pyplot as plt

def plot_results():
    with open('questao_2_resultados.json', 'r') as f:
        data = json.load(f)

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    n_values = list(range(1000, 1000 + len(data['extensible']['space']) * 1000, 1000))

    ax1.set_title('Espaço Requerido vs. Número de Registros', fontsize=14)
    ax1.set_xlabel('Número de Registros (n)')
    ax1.set_ylabel('Espaço Total (Slots)')

    ax1.plot(n_values, data['extensible']['space'],
             marker='o', linestyle='--', label='Hash Extensível', color='red', linewidth=2)

    colors = ['blue', 'green', 'orange']
    markers = ['s', '^', 'D']
    
    for i, (alpha, values) in enumerate(data['linear'].items()):
        ax1.plot(n_values, values['space'],
                 marker=markers[i], linestyle='-', label=f'Hash Linear (α_max={alpha})', 
                 color=colors[i], linewidth=2)

    ax1.legend()
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    ax2.set_title('Esforço Total de Inserção vs. Número de Registros', fontsize=14)
    ax2.set_xlabel('Número de Registros (n)')
    ax2.set_ylabel('Esforço Total (Acessos à Página)')

    ax2.plot(n_values, data['extensible']['effort'],
             marker='o', linestyle='--', label='Hash Extensível', color='red', linewidth=2)

    for i, (alpha, values) in enumerate(data['linear'].items()):
        ax2.plot(n_values, values['effort'],
                 marker=markers[i], linestyle='-', label=f'Hash Linear (α_max={alpha})', 
                 color=colors[i], linewidth=2)

    ax2.legend()
    ax2.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.savefig('comparativo_hash.png', dpi=300)
    plt.show()

    print("\n=== ANÁLISE DOS RESULTADOS ===\n")
    
    print("ESPAÇO REQUERIDO:")
    print("- Hash Extensível usa mais espaço para valores pequenos de n")
    print("- Hash Linear com α_max maior usa menos espaço (mais denso)")
    
    print("\nESFORÇO DE INSERÇÃO:")
    print("- Hash Extensível tem menor esforço de inserção")
    print("- Hash Linear com α_max maior tem maior esforço (mais colisões)")
    
    print("\nGráficos salvos em 'comparativo_hash.png'")

if __name__ == '__main__':
    plot_results() 