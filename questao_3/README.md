## Parâmetros do Filtro de Bloom

- **m**: número de bits do filtro
- **n**: número de funções hashing
- **k**: número de registros representados pelo filtro
- **α**: percentual esperado do universo de registros que satisfaz os critérios do filtro

Fixei o k nos valores 10 e 100 como visto nos slides das aulas para facilitar o desenvolvimento já que o mesmo não precisava ser alterado.


## Fórmulas do Filtro de Bloom

Assumindo que as funções hash distribuem uniformemente as chaves no intervalo [0, m-1]:

### Probabilidades Básicas
- **$p_1 = \frac{1}{m}$**: Probabilidade de um bit ser ligado por uma função aplicada a um registro
- **$p_0 = 1 - \frac{1}{m}$**: Probabilidade de um bit permanecer desligado

### Probabilidades Compostas
- **$p_0^n = \left(1 - \frac{1}{m}\right)^n$**: Probabilidade de um bit estar desligado após aplicar n funções a um registro
- **$p_0^{nk} = \left(1 - \frac{1}{m}\right)^{nk}$**: Probabilidade de um bit estar desligado após aplicar n funções a k registros
- **$1 - p_0^{nk} = 1 - \left(1 - \frac{1}{m}\right)^{nk}$**: Probabilidade de um bit estar ligado após todas as inserções

### Probabilidade de Falso Positivo
$$P = \left(1 - p_0^{nk}\right)^n = \left(1 - \left(1 - \frac{1}{m}\right)^{nk}\right)^n$$

### Probabilidade de Falso Positivo Considerando α
$$F = (1 - \alpha) \times P$$
Onde α é a porção de registros que se espera estar representada no filtro.

### Número Ótimo de Funções Hash
$$n_{\text{ótimo}} = \frac{m}{k} \times \ln(2)$$

## TRADE-OFFS observados:
Mais funções hash → Menor taxa de FP, mas maior tempo de operação

Filtro maior → Menor taxa de FP, mas maior uso de memória

K ótimo observado ≈ K ótimo teórico para a maioria dos casos
