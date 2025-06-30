import random
import json
import time
import math

class BloomFilter:
    def __init__(self, m, n):
        """
        m: número de bits do filtro
        n: número de funções hashing
        """
        self.m = m
        self.n = n
        self.bit_array = [False] * m
        self.hash_params = []
        
        for _ in range(n):
            self.hash_params.append({
                'a': self._generate_random_prime(),
                'b': random.randint(0, m - 1)
            })
    
    def _generate_random_prime(self):
        primes = [31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
                  101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173]
        return random.choice(primes)
    
    def hash(self, key, i):
        params = self.hash_params[i]
        return (params['a'] * key + params['b']) % self.m
    
    def insert(self, key):
        for i in range(self.n):
            index = self.hash(key, i)
            self.bit_array[index] = True
    
    def contains(self, key):
        for i in range(self.n):
            index = self.hash(key, i)
            if not self.bit_array[index]:
                return False
        return True
    
    def get_bit_count(self):
        return sum(self.bit_array)
    
    def get_fill_ratio(self):
        return self.get_bit_count() / self.m

def generate_random_keys(count, max_val):
    return list(random.sample(range(max_val), count))

def measure_time(func):
    start = time.time()
    func()
    end = time.time()
    return (end - start) * 1000

def calculate_P_probability(m, n, k):
    """
    Calcula a probabilidade P de falso positivo (fórmula exata)
    P = (1 - (1 - 1/m)^(nk))^n
    
    m: número de bits do filtro
    n: número de funções hashing
    k: número de registros inseridos
    """
    if n == 0:
        return 0.0
    p0_nk = math.pow(1 - 1/m, n*k)
    P = math.pow(1 - p0_nk, n)
    return P

def calculate_F_probability(P, alpha):
    """
    Calcula a probabilidade F de falso positivo considerando α
    F = (1 - α) * P
    
    P: probabilidade de falso positivo
    α: porção esperada de registros representados
    """
    return (1 - alpha) * P

def calculate_optimal_n(m, k):
    """
    Calcula o número ótimo de funções hash
    n_ótimo = (m/k) * ln(2)
    """
    return round((m / k) * math.log(2))

def run_experiment():
    k_values = [10, 100]
    m_values = [1000, 10000, 50000, 100000]
    
    # Criar ranges de n
    n_values = list(range(1, 51, 2))  # Para experimentos práticos
    n_values_theory = list(range(1, 601, 5))  # Para cálculos teóricos
    
    results = {
        'parameters': {
            'k_values': k_values,
            'm_values': m_values,
            'n_values_exp': n_values,
            'n_values_theory': n_values_theory
        },
        'experiments': [],
        'theory': [],
        'analysis': {}
    }
    
    print(f"Valores de k: {k_values}")
    print(f"Valores de m: {m_values}")
    print(f"Valores de n para teoria: 1 a 600 (passo 5)\n")
    
    print("Calculando valores teóricos...")
    for k in k_values:
        for m in m_values:
            for n in n_values_theory:
                P = calculate_P_probability(m, n, k)
                alpha = k / (k * 10)
                F = calculate_F_probability(P, alpha)
                
                results['theory'].append({
                    'm': m,
                    'n': n,
                    'k': k,
                    'alpha': alpha,
                    'P': P,
                    'F': F
                })
    
    print("\nRealizando experimentos práticos para validação...")
    print("m\tk\tn\tP\t\tFP Obs.\t\tFill Ratio")
    print("-" * 70)
    
    selected_cases = [
        (1000, 10),    # Filtro pequeno, poucos registros
        (1000, 100),   # Filtro pequeno, muitos registros
        (10000, 100),  # Filtro médio, registros médios
        (10000, 1000), # Filtro médio, muitos registros
    ]
    
    for m, k in selected_cases:
        print(f"\n--- m = {m}, k = {k} ---")
        
        num_tests = min(1000, k * 10)
        universe_size = k * 10
        insert_keys = generate_random_keys(k, universe_size)
        
        for n in [1, 5, 10, 20, 50]:
            bloom = BloomFilter(m, n)
            
            for key in insert_keys:
                bloom.insert(key)
            
            false_positives = 0
            test_keys = generate_random_keys(num_tests, universe_size)
            insert_set = set(insert_keys)
            negative_test_keys = [key for key in test_keys if key not in insert_set]
            
            for key in negative_test_keys[:num_tests]:
                if bloom.contains(key):
                    false_positives += 1
            
            fp_rate_observed = false_positives / len(negative_test_keys[:num_tests]) if negative_test_keys else 0
            P = calculate_P_probability(m, n, k)
            fill_ratio = bloom.get_fill_ratio()
            
            result = {
                'm': m,
                'n': n,
                'k': k,
                'P': P,
                'fpRateObserved': fp_rate_observed,
                'fillRatio': fill_ratio
            }
            
            results['experiments'].append(result)
            
            print(f"{m}\t{k}\t{n}\t{P:.4f}\t\t{fp_rate_observed:.4f}\t\t{fill_ratio:.3f}")
    
    print("VALORES ÓTIMOS DE n:")
    print("m\tk\tn_ótimo\t\tP_mínimo")
    print("-" * 50)
    
    for m in [1000, 10000, 50000]:
        for k in [10, 100, 1000, 10000]:
            if k <= m:
                n_optimal = calculate_optimal_n(m, k)
                P_optimal = calculate_P_probability(m, n_optimal, k)
                print(f"{m}\t{k}\t{n_optimal}\t\t{P_optimal:.6f}")
    
    with open('questao_3_resultados.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nResultados salvos em 'questao_3_resultados.json'")

if __name__ == '__main__':
    run_experiment() 
