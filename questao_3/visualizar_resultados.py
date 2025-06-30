import json
import matplotlib.pyplot as plt
import numpy as np

def plot_main_analysis():
    with open('questao_3_resultados.json', 'r') as f:
        data = json.load(f)

    theory = data.get('theory', [])

    plt.style.use('seaborn-v0_8-whitegrid')
    
    plt.figure(figsize=(12, 8))
    
    # primeramente testando o comportamento igualzinho ao que está nos slides para validar o código.
    m_selected = 1000
    k_values_to_plot = [10, 100]
    colors = ['blue', 'red']
    
    for i, k in enumerate(k_values_to_plot):
        theory_data = [item for item in theory if item['m'] == m_selected and item['k'] == k]
        theory_data.sort(key=lambda x: x['n'])
        
        if theory_data:
            n_theory = [0] + [item['n'] for item in theory_data]
            P_theory = [0.0] + [item['P'] for item in theory_data]
            
            plt.plot(n_theory, P_theory, 
                    color=colors[i], linewidth=2.5,
                    label=f'k = {k}')
            
            n_optimal = round((m_selected / k) * np.log(2))
            P_optimal = next((item['P'] for item in theory_data if item['n'] == n_optimal), None)
            
            if P_optimal is not None:
                plt.plot(n_optimal, P_optimal, 'o', color=colors[i], markersize=8, 
                        markeredgecolor='black', markeredgewidth=1.5)
                plt.annotate(f'ótimo n = {n_optimal}', 
                            xy=(n_optimal, P_optimal),
                            xytext=(n_optimal + 50, P_optimal + 0.02),
                            color=colors[i],
                            fontsize=11,
                            arrowprops=dict(arrowstyle='->', color=colors[i], lw=1))
    
    plt.xlim(0, 600)
    plt.ylim(0, 0.30)
    
    plt.xlabel('Filtro com n func. hashing', fontsize=12)
    plt.ylabel('Probabilidade de positivo', fontsize=12)
    
    plt.grid(True, alpha=0.3)
    
    plt.text(0.5, 1.05, 'Comportamento em função do número n de funções hashing',
             ha='center', transform=plt.gca().transAxes, fontsize=14, color='blue')
    plt.text(0.5, 1.02, f'Considerando: m = {m_selected} bits, k ∈ {{{k_values_to_plot[0]}, {k_values_to_plot[1]}}}:',
             ha='center', transform=plt.gca().transAxes, fontsize=12)
    
    plt.tight_layout()
    plt.savefig('bloom_m1000_comparacao.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    plt.figure(figsize=(14, 10))
    
    k_selected = 100
    m_values = sorted(list(set(item['m'] for item in theory)))
    colors = plt.cm.viridis(np.linspace(0, 1, len(m_values)))
    
    for i, m in enumerate(m_values):
        theory_data = [item for item in theory if item['m'] == m and item['k'] == k_selected]
        theory_data.sort(key=lambda x: x['n'])
        
        if theory_data:
            n_theory = [0] + [item['n'] for item in theory_data]
            P_theory = [0.0] + [item['P'] for item in theory_data]
            
            plt.plot(n_theory, P_theory, 
                    linestyle='-', linewidth=2.5,
                    label=f'm = {m:,} bits', color=colors[i])
            
            n_optimal = round((m / k_selected) * np.log(2))
            P_optimal = next((item['P'] for item in theory_data if item['n'] == n_optimal), None)
            
            if P_optimal is not None and n_optimal <= 600:
                plt.plot(n_optimal, P_optimal, 'o', markersize=8, color=colors[i], 
                        markeredgecolor='black', markeredgewidth=1.5)
    
    plt.xlim(0, 600)
    plt.ylim(0, 1.05)
    
    plt.xlabel('Número de Funções Hash (n)', fontsize=14)
    plt.ylabel('Probabilidade de Falso Positivo', fontsize=14)
    plt.title(f'Probabilidade de Falso Positivo vs Número de Funções Hash\nk = {k_selected} registros', fontsize=16)
    
    plt.legend(title='Tamanho do Filtro', fontsize=11, title_fontsize=12, loc='center right')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('bloom_todos_m_k100.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    plot_main_analysis() 
