O script `questao_2.py` realiza os seguintes passos:

1.  **Geração de Dados**: Gera um conjunto de chaves inteiras únicas e aleatórias para serem inseridas nas estruturas.
2.  **Execução dos Testes**:
    *   **Hash Linear**: A estrutura é testada com diferentes valores para o fator de carga máximo (`alpha_max`). Para cada configuração, medimos:
        *   `insertions`: O número de chaves inseridas.
        *   `storage`: O espaço total requerido (número de slots).
        *   `avg_insertion_cost`: O custo médio de inserção, medido pelo número de acessos à página por inserção.
    *   **Hash Extensível**: A estrutura é testada para o mesmo conjunto de chaves, medindo as mesmas métricas (exceto `alpha_max`, que não se aplica).
3.  **Coleta de Resultados**: Os resultados de cada execução (diferentes `alpha_max` para hash linear e a execução para hash extensível) são compilados e salvos em `questao_2_resultados.json`.
