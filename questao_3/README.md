O script `questao_3.py` foi projetado para analisar o comportamento do Filtro de Bloom sob diferentes configurações. O processo é o seguinte:

1.  **Definição dos Parâmetros**: O experimento é executado para um conjunto de `tamanhos de filtro` (m) e `número de funções hash` (k).
2.  **Geração de Chaves**: São gerados dois conjuntos de chaves inteiras distintas e aleatórias:
    *   `insert_keys`: Chaves que serão efetivamente inseridas no filtro.
    *   `negative_test_keys`: Chaves que garantidamente **não** estão no filtro, usadas para medir a taxa de falsos positivos.
3.  **Execução e Medição**: Para cada combinação de `tamanho` e `num_hashes`:
    *   Um novo Filtro de Bloom é criado.
    *   As `insert_keys` são inseridas, e o tempo de inserção (`insertTime`) é medido.
    *   O filtro é consultado com as `negative_test_keys`. O tempo de consulta (`queryTime`) e o número de **falsos positivos** são registrados.
4.  **Cálculo de Métricas**: As seguintes métricas são calculadas:
    *   `fpRate`: A taxa de falsos positivos (falsos positivos / total de chaves de teste negativas). Esta é a métrica de precisão mais importante.
    *   `fillRatio`: A proporção de bits '1' no array de bits do filtro, indicando sua densidade.
    *   `theoretical_fp`: A taxa de falsos positivos teórica, calculada pela fórmula `(1 - e^(-kn/m))^k`, para comparação.
5.  **Armazenamento**: Todos os resultados e métricas são salvos no arquivo `questao_3_resultados.json`.
