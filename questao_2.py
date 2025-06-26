import random
import json
import time

class Page:
    def __init__(self, capacity):
        self.capacity = capacity
        self.records = []
        self.overflow_page = None
    
    def is_full(self):
        return len(self.records) >= self.capacity
    
    def insert(self, record):
        if not self.is_full():
            self.records.append(record)
            return True
        return False
    
    def __repr__(self):
        return f"Page(records={self.records})"

class ExtensibleHashing:
    def __init__(self, page_capacity):
        self.page_capacity = page_capacity
        self.global_depth = 1
        self.pages = [Page(page_capacity), Page(page_capacity)]
        self.directory = {
            '0': {'page_index': 0, 'local_depth': 1},
            '1': {'page_index': 1, 'local_depth': 1}
        }
        self.io_cost = 0
    
    def hash(self, key):
        # Knuth's multiplicative hash
        h = (key * 2654435761) & 0xFFFFFFFF
        return format(h, '032b')
    
    def get_dir_key(self, key_hash):
        return key_hash[-self.global_depth:]
    
    def insert(self, key):
        key_hash = self.hash(key)
        
        while True:
            dir_key = self.get_dir_key(key_hash)
            entry = self.directory[dir_key]
            page_index = entry['page_index']
            page = self.pages[page_index]
            self.io_cost += 1
            
            if not page.is_full():
                page.insert(key)
                self.io_cost += 1
                return
            
            # Página cheia, precisa dividir
            self.io_cost += 1
            
            local_depth = entry['local_depth']
            
            if local_depth == self.global_depth:
                self._double_directory()
            
            # Criar nova página
            new_page = Page(self.page_capacity)
            self.pages.append(new_page)
            new_page_index = len(self.pages) - 1
            self.io_cost += 1
            
            new_local_depth = local_depth + 1
            
            # Coletar registros para redistribuir
            records_to_redistribute = page.records[:]
            page.records = []
            
            # Atualizar entradas do diretório
            affected_entries = []
            for d_key, d_entry in self.directory.items():
                if d_entry['page_index'] == page_index:
                    d_entry['local_depth'] = new_local_depth
                    affected_entries.append(d_key)
            
            # Determinar quais entradas apontam para a nova página
            discriminator_bit = 32 - new_local_depth
            for d_key in affected_entries:
                extended_key = d_key.zfill(32)
                if extended_key[discriminator_bit] == '1':
                    self.directory[d_key]['page_index'] = new_page_index
            
            # Redistribuir todas as chaves antigas
            for record in records_to_redistribute:
                h = self.hash(record)
                dk = self.get_dir_key(h)
                p_idx = self.directory[dk]['page_index']
                self.pages[p_idx].insert(record)
    
    def _double_directory(self):
        self.global_depth += 1
        if self.global_depth > 20:
            raise Exception("Profundidade global excessiva")
        
        new_directory = {}
        for key, value in self.directory.items():
            new_directory['0' + key] = value.copy()
            new_directory['1' + key] = value.copy()
        self.directory = new_directory
    
    def get_space_usage(self):
        return len(self.directory) + len(self.pages)

class LinearHashing:
    def __init__(self, page_capacity, alpha_max=0.75):
        self.page_capacity = page_capacity
        self.alpha_max = alpha_max
        self.level = 0
        self.split_pointer = 0
        self.num_records = 0
        self.pages = [Page(page_capacity)]
        self.num_initial_pages = 1
        self.io_cost = 0
    
    def hash(self, key, level):
        return key % (self.num_initial_pages * (2 ** level))
    
    def get_page_index(self, key):
        h = self.hash(key, self.level)
        if h < self.split_pointer:
            h = self.hash(key, self.level + 1)
        return h
    
    def _find_page_and_insert(self, key):
        page_index = self.get_page_index(key)
        
        while page_index >= len(self.pages):
            self.pages.append(Page(self.page_capacity))
        
        page = self.pages[page_index]
        self.io_cost += 1
        
        # Inserção com tratamento de overflow
        current_page = page
        while current_page.is_full():
            if current_page.overflow_page is None:
                current_page.overflow_page = Page(self.page_capacity)
                self.io_cost += 1
            self.io_cost += 1
            current_page = current_page.overflow_page
        
        current_page.insert(key)
        self.io_cost += 1
    
    def insert(self, key):
        self._find_page_and_insert(key)
        self.num_records += 1
        
        if self.get_load_factor() > self.alpha_max:
            self._split()
    
    def _split(self):
        self.pages.append(Page(self.page_capacity))
        self.io_cost += 1
        
        page_to_split = self.pages[self.split_pointer]
        self.io_cost += 1
        
        # Coletar todos os registros
        all_records = []
        current_page = page_to_split
        while current_page:
            all_records.extend(current_page.records)
            current_page = current_page.overflow_page
        
        # Limpar a página original
        page_to_split.records = []
        page_to_split.overflow_page = None
        self.io_cost += 1
        
        # Atualizar ponteiro de split
        self.split_pointer += 1
        
        # Redistribuir registros
        for record in all_records:
            self._find_page_and_insert(record)
        
        # Checar se um novo nível começou
        if self.split_pointer == self.num_initial_pages * (2 ** self.level):
            self.level += 1
            self.split_pointer = 0
    
    def get_load_factor(self):
        num_slots = len(self.pages) * self.page_capacity
        return self.num_records / num_slots if num_slots > 0 else 0
    
    def get_space_usage(self):
        space = len(self.pages)
        for page in self.pages:
            current = page.overflow_page
            while current:
                space += 1
                current = current.overflow_page
        return space

def generate_random_keys(count):
    return random.sample(range(count * 10), count)

def run_experiment():
    print("=== Estudo Comparativo: Hash Extensível vs Hash Linear ===\n")
    
    page_capacity = 10
    n_values = [1000, 2000, 5000, 10000, 20000]
    alpha_max_values = [0.6, 0.75, 0.9]
    
    # Gerar chaves aleatórias
    max_n = max(n_values)
    keys = generate_random_keys(max_n)
    
    results = {
        'extensible': {'space': [], 'effort': []},
        'linear': {}
    }
    
    for alpha in alpha_max_values:
        results['linear'][alpha] = {'space': [], 'effort': []}
    
    # Teste do Hash Extensível
    print("Executando Hash Extensível...")
    print("n\tEspaço\tEsforço(I/O)")
    print("-" * 30)
    
    for n in n_values:
        eh = ExtensibleHashing(page_capacity)
        for i in range(n):
            eh.insert(keys[i])
        results['extensible']['space'].append(eh.get_space_usage())
        results['extensible']['effort'].append(eh.io_cost)
        print(f"{n}\t{eh.get_space_usage()}\t{eh.io_cost}")
    
    # Teste do Hash Linear
    for alpha in alpha_max_values:
        print(f"\nExecutando Hash Linear (alpha_max={alpha})...")
        print("n\tEspaço\tEsforço(I/O)")
        print("-" * 30)
        
        for n in n_values:
            lh = LinearHashing(page_capacity, alpha_max=alpha)
            for i in range(n):
                lh.insert(keys[i])
            results['linear'][alpha]['space'].append(lh.get_space_usage())
            results['linear'][alpha]['effort'].append(lh.io_cost)
            print(f"{n}\t{lh.get_space_usage()}\t{lh.io_cost}")
    
    # Análise comparativa
    print("\n=== ANÁLISE COMPARATIVA ===\n")
    
    print("1. ESPAÇO REQUERIDO:")
    print("n\tExt.\tLin(0.6)\tLin(0.75)\tLin(0.9)")
    print("-" * 50)
    for i in range(len(n_values)):
        row = [
            n_values[i],
            results['extensible']['space'][i],
            results['linear'][0.6]['space'][i],
            results['linear'][0.75]['space'][i],
            results['linear'][0.9]['space'][i]
        ]
        print('\t'.join(map(str, row)))
    
    print("\n2. ESFORÇO DE INCLUSÃO (I/O):")
    print("n\tExt.\tLin(0.6)\tLin(0.75)\tLin(0.9)")
    print("-" * 50)
    for i in range(len(n_values)):
        row = [
            n_values[i],
            results['extensible']['effort'][i],
            results['linear'][0.6]['effort'][i],
            results['linear'][0.75]['effort'][i],
            results['linear'][0.9]['effort'][i]
        ]
        print('\t'.join(map(str, row)))
    
    # Análise de tendências
    print("\n=== ANÁLISE DE TENDÊNCIAS ===\n")
    
    print("Taxa de crescimento do espaço (relativo a n=1000):")
    base_idx = 0
    for i in range(1, len(n_values)):
        ext_growth = results['extensible']['space'][i] / results['extensible']['space'][base_idx]
        lin75_growth = results['linear'][0.75]['space'][i] / results['linear'][0.75]['space'][base_idx]
        print(f"n={n_values[i]}: Extensível={ext_growth:.2f}x, Linear(0.75)={lin75_growth:.2f}x")
    
    print("\nEfeito do parâmetro alpha_max no Hash Linear:")
    for i in range(len(n_values)):
        space60 = results['linear'][0.6]['space'][i]
        space75 = results['linear'][0.75]['space'][i]
        space90 = results['linear'][0.9]['space'][i]
        ratio6075 = space60 / space75
        ratio7590 = space75 / space90
        print(f"n={n_values[i]}: α(0.6)/α(0.75)={ratio6075:.2f}, α(0.75)/α(0.9)={ratio7590:.2f}")
    
    # Salvar resultados
    with open('questao_2_resultados.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nResultados exportados para 'questao_2_resultados.json'")

if __name__ == '__main__':
    run_experiment() 