import random
import json
import time
import math

class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [False] * size
        self.hash_params = []
        
        for _ in range(num_hashes):
            self.hash_params.append({
                'a': self._generate_random_prime(),
                'b': random.randint(0, size - 1)
            })
    
    def _generate_random_prime(self):
        primes = [31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
                  101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173]
        return random.choice(primes)
    
    def hash(self, key, i):
        params = self.hash_params[i]
        return (params['a'] * key + params['b']) % self.size
    
    def insert(self, key):
        for i in range(self.num_hashes):
            index = self.hash(key, i)
            self.bit_array[index] = True
    
    def contains(self, key):
        for i in range(self.num_hashes):
            index = self.hash(key, i)
            if not self.bit_array[index]:
                return False
        return True
    
    def get_bit_count(self):
        return sum(self.bit_array)
    
    def get_fill_ratio(self):
        return self.get_bit_count() / self.size

def generate_random_keys(count, max_val):
    return list(random.sample(range(max_val), count))

def measure_time(func):
    start = time.time()
    func()
    end = time.time()
    return (end - start) * 1000

def run_experiment():
    print("=== Estudo Experimental sobre Filtros de Bloom ===\n")
    
    num_elements = 10000
    num_tests = 10000
    filter_sizes = [1000, 5000, 10000, 20000, 50000]
    hash_counts = [1, 3, 5, 7, 10]
    
    insert_keys = generate_random_keys(num_elements, num_elements * 10)
    test_keys = generate_random_keys(num_tests, num_elements * 10)
    
    insert_set = set(insert_keys)
    negative_test_keys = [key for key in test_keys if key not in insert_set]
    
    results = {
        'experiments': [],
        'summary': {}
    }
    
    print(f"Inserindo {num_elements} elementos")
    print(f"Testando com {num_tests} consultas\n")
    
    print("Tamanho\tHashes\tTempo Ins(ms)\tTempo Cons(ms)\tFP Rate\tFill Ratio")
    print("-" * 70)
    
    for size in filter_sizes:
        for num_hashes in hash_counts:
            bloom = BloomFilter(size, num_hashes)
            
            def insert_all():
                for key in insert_keys:
                    bloom.insert(key)
            
            insert_time = measure_time(insert_all)
            
            false_positives = 0
            def query_all():
                nonlocal false_positives
                for key in negative_test_keys[:num_tests]:
                    if bloom.contains(key):
                        false_positives += 1
            
            query_time = measure_time(query_all)
            
            true_positives = 0
            for key in insert_keys:
                if bloom.contains(key):
                    true_positives += 1
            
            fp_rate = false_positives / len(negative_test_keys[:num_tests])
            fill_ratio = bloom.get_fill_ratio()
            
            result = {
                'size': size,
                'numHashes': num_hashes,
                'insertTime': insert_time,
                'queryTime': query_time,
                'fpRate': fp_rate,
                'fillRatio': fill_ratio,
                'truePositives': true_positives,
                'falsePositives': false_positives
            }
            
            results['experiments'].append(result)
            
            print(f"{size}\t{num_hashes}\t{insert_time:.2f}\t\t{query_time:.2f}\t\t{fp_rate*100:.2f}%\t{fill_ratio*100:.1f}%")
        
        print()
    
    print("\n=== ANÁLISE DOS RESULTADOS ===\n")
    
    print("1. COMPARAÇÃO COM TAXA TEÓRICA DE FALSOS POSITIVOS:")
    print("Tamanho\tHashes\tFP Observado\tFP Teórico\tDiferença")
    print("-" * 60)
    
    for exp in results['experiments']:
        k = exp['numHashes']
        m = exp['size']
        n = num_elements
        
        theoretical_fp = math.pow(1 - math.exp(-k * n / m), k)
        difference = abs(exp['fpRate'] - theoretical_fp)
        
        print(f"{m}\t{k}\t{exp['fpRate']*100:.2f}%\t\t{theoretical_fp*100:.2f}%\t\t{difference*100:.2f}%")
    
    print("\n2. NÚMERO ÓTIMO DE FUNÇÕES HASH:")
    print("Tamanho\tK Ótimo Teórico\tK Ótimo Observado\tMenor FP Rate")
    print("-" * 60)
    
    for size in filter_sizes:
        experiments_for_size = [exp for exp in results['experiments'] if exp['size'] == size]
        best_exp = min(experiments_for_size, key=lambda x: x['fpRate'])
        
        theoretical_optimal_k = round((size / num_elements) * math.log(2))
        
        print(f"{size}\t{theoretical_optimal_k}\t\t{best_exp['numHashes']}\t\t\t{best_exp['fpRate']*100:.2f}%")
    
    print("\n3. ANÁLISE DE DESEMPENHO:")
    print("- Impacto do número de hashes no tempo de inserção:")
    
    size_for_analysis = 10000
    perf_experiments = [exp for exp in results['experiments'] if exp['size'] == size_for_analysis]
    
    for exp in perf_experiments:
        avg_insert_time = exp['insertTime'] / num_elements
        print(f"  K={exp['numHashes']}: {avg_insert_time:.4f}ms por inserção")
    
    print("\n4. EFICIÊNCIA DE MEMÓRIA:")
    print("Tamanho\tBits/Elemento\tFill Ratio Médio")
    print("-" * 45)
    
    for size in filter_sizes:
        experiments_for_size = [exp for exp in results['experiments'] if exp['size'] == size]
        avg_fill_ratio = sum(exp['fillRatio'] for exp in experiments_for_size) / len(experiments_for_size)
        bits_per_element = size / num_elements
        
        print(f"{size}\t{bits_per_element:.2f}\t\t{avg_fill_ratio*100:.1f}%")
    
    with open('questao_3_resultados.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nResultados detalhados salvos em 'questao_3_resultados.json'")

if __name__ == '__main__':
    run_experiment() 
