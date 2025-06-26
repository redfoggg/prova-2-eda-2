import json
import matplotlib.pyplot as plt

# Carregar dados
with open('questao_3_resultados.json', 'r') as f:
    data = json.load(f)

experiments = data['experiments']

# Organizar dados por tamanho
data_by_size = {}
for exp in experiments:
    size = exp['size']
    if size not in data_by_size:
        data_by_size[size] = {'numHashes': [], 'fpRate': [], 'insertTime': [], 'fillRatio': []}
    
    data_by_size[size]['numHashes'].append(exp['numHashes'])
    data_by_size[size]['fpRate'].append(exp['fpRate'] * 100)
    data_by_size[size]['insertTime'].append(exp['insertTime'])
    data_by_size[size]['fillRatio'].append(exp['fillRatio'] * 100)

# Criar gráficos básicos
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# 1. Taxa de Falsos Positivos
colors = ['blue', 'green', 'red', 'purple', 'orange']
for i, (size, data) in enumerate(data_by_size.items()):
    ax1.plot(data['numHashes'], data['fpRate'], 
             marker='o', label=f'Size={size}', color=colors[i])
ax1.set_xlabel('Número de Hashes')
ax1.set_ylabel('Taxa de Falsos Positivos (%)')
ax1.set_title('Taxa de FP vs Número de Hashes')
ax1.legend()
ax1.grid(True)

# 2. Tempo de Inserção
for i, (size, data) in enumerate(data_by_size.items()):
    ax2.plot(data['numHashes'], data['insertTime'], 
             marker='s', label=f'Size={size}', color=colors[i])
ax2.set_xlabel('Número de Hashes')
ax2.set_ylabel('Tempo de Inserção (ms)')
ax2.set_title('Tempo de Inserção vs Número de Hashes')
ax2.legend()
ax2.grid(True)

# 3. Taxa de Preenchimento
for i, (size, data) in enumerate(data_by_size.items()):
    ax3.plot(data['numHashes'], data['fillRatio'], 
             marker='^', label=f'Size={size}', color=colors[i])
ax3.set_xlabel('Número de Hashes')
ax3.set_ylabel('Taxa de Preenchimento (%)')
ax3.set_title('Taxa de Preenchimento vs Número de Hashes')
ax3.legend()
ax3.grid(True)

# 4. Resumo textual
ax4.axis('off')
summary_text = "RESUMO DOS EXPERIMENTOS\n\n"

# Encontrar melhor configuração
best = min(experiments, key=lambda x: x['fpRate'])
worst = max(experiments, key=lambda x: x['fpRate'])

summary_text += f"Melhor config (menor FP):\n"
summary_text += f"  Size={best['size']}, K={best['numHashes']}\n"
summary_text += f"  FP Rate={best['fpRate']*100:.2f}%\n\n"

summary_text += f"Pior config (maior FP):\n"
summary_text += f"  Size={worst['size']}, K={worst['numHashes']}\n"
summary_text += f"  FP Rate={worst['fpRate']*100:.2f}%\n\n"

summary_text += "Insights:\n"
summary_text += "- Mais hashes = Menor FP\n"
summary_text += "- Filtro maior = Menor FP\n"
summary_text += "- Trade-off: Memória vs Precisão"

ax4.text(0.1, 0.5, summary_text, fontsize=12, verticalalignment='center')

plt.suptitle('Análise dos Experimentos com Bloom Filter', fontsize=16)
plt.tight_layout()
plt.savefig('bloom_analysis_simple.png', dpi=300)
plt.show()

print("Gráfico salvo como 'bloom_analysis_simple.png'")
print("\nPara visualizações mais detalhadas, instale pandas e numpy.") 