import sys
import os
import time
import csv
import random
import statistics

# --- CONFIGURAÇÃO ---
# Tamanhos para teste de escalabilidade
SIZES = [10000] 
# Número de repetições para garantir consistência estatística
REPETITIONS = 5
# Cenários a testar
SCENARIOS = ['Random', 'Sorted', 'SteadyState']
METHODS = ['Standard', 'Optimized']

# Setup path para importar a classe AVL
# Assume que o script está em: experiments/benchmarks/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from avl_tree import AVLTree
except ImportError:
    # Fallback caso a estrutura de pastas seja diferente
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from avl_tree import AVLTree

def run_comprehensive_benchmark():
    # Prepara diretório de dados
    data_dir = os.path.join(os.path.dirname(__file__), '../../data')
    if not os.path.exists(data_dir): os.makedirs(data_dir)
    
    csv_path = os.path.join(data_dir, 'results_deletion_time_comprehensive.csv')
    
    print(f"--- INICIANDO BENCHMARK COMPLETO DE REMOÇÃO ---")
    print(f"Sizes: {SIZES}")
    print(f"Scenarios: {SCENARIOS}")
    print(f"Repetitions: {REPETITIONS}\n")
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Size', 'Scenario', 'Method', 'Repetition', 'Deletion_Time_ms'])
        
        for n in SIZES:
            print(f"--> Processando Tamanho N = {n}")
            
            # Gera pool de dados base (0 até 2N para ter margem)
            # Usamos um pool fixo por tamanho para ser justo entre os métodos
            master_pool = list(range(n * 2))
            
            for scenario in SCENARIOS:
                print(f"  > Cenário: {scenario}")
                
                for method in METHODS:
                    run_times = []
                    
                    for r in range(1, REPETITIONS + 1):
                        # Garante independência estatística entre repetições
                        # mas usa o mesmo seed para Standard e Optimized se quisesse pareamento perfeito
                        # aqui usaremos shuffle novo a cada repetição
                        current_pool = master_pool[:]
                        
                        # --- PREPARAÇÃO DA ÁRVORE (WARMUP) ---
                        avl = AVLTree(method.lower())
                        
                        if scenario == 'Sorted':
                            # Inserção Sequencial (0, 1, 2... N)
                            # Pior caso de balanceamento na inserção
                            warmup_data = list(range(n))
                            for x in warmup_data:
                                avl.insert(x)
                            
                            # Para remover, embaralharmos para ser remoção aleatória
                            keys_to_delete = warmup_data[:]
                            random.shuffle(keys_to_delete)
                            keys_to_delete = keys_to_delete[:n//2] # Remover 50%
                            
                        elif scenario == 'Random' or scenario == 'SteadyState':
                            # Inserção Aleatória
                            warmup_data = list(range(n))
                            random.shuffle(warmup_data)
                            for x in warmup_data:
                                avl.insert(x)
                            
                            if scenario == 'Random':
                                # Define 50% para remover
                                keys_to_delete = warmup_data[:n//2]
                            else:
                                # SteadyState não tem lista pré-definida de delete, é dinâmica
                                keys_to_delete = [] # Não usado
                        
                        # --- MEDIÇÃO (BENCHMARK) ---
                        elapsed = 0.0
                        
                        if scenario in ['Random', 'Sorted']:
                            # Caso Simples: Medir o loop de remoção inteiro
                            start = time.perf_counter()
                            for k in keys_to_delete:
                                avl.delete(k)
                            end = time.perf_counter()
                            elapsed = end - start
                            
                        elif scenario == 'SteadyState':
                            # Caso Complexo: Tira e Põe (Manutenção)
                            # Vamos executar N/2 operações de troca
                            ops_count = n // 2
                            pool_idx = n # Começa pegando do pool de reserva
                            
                            # Aqui precisamos medir APENAS o delete, o que é custoso em Python puro
                            # devido ao overhead do timer. 
                            # Abordagem: Acumular o tempo de delete
                            
                            t_accum = 0.0
                            
                            # Lista de nós presentes para remover (embaralhada)
                            current_nodes = list(range(n)) if scenario == 'Sorted' else warmup_data
                            random.shuffle(current_nodes)
                            
                            for i in range(ops_count):
                                val_rem = current_nodes.pop() # Pega um para remover
                                val_add = current_pool[pool_idx] # Pega um novo
                                pool_idx += 1
                                
                                # CRÍTICO: Medir só o delete
                                t0 = time.perf_counter()
                                avl.delete(val_rem)
                                t1 = time.perf_counter()
                                t_accum += (t1 - t0)
                                
                                # Insert fora do relógio
                                avl.insert(val_add)
                                current_nodes.append(val_add) # Mantém registro
                                
                            elapsed = t_accum

                        # Registra
                        time_ms = elapsed * 1000
                        run_times.append(time_ms)
                        writer.writerow([n, scenario, method, r, time_ms])
                        
                        # Limpeza
                        del avl
                    
                    # --- ESTATÍSTICAS DA RODADA ---
                    avg_time = statistics.mean(run_times)
                    print(f"    [{method}] Média (5 runs): {avg_time:.4f} ms")

    print(f"\nBenchmark Concluído. Dados salvos em: {csv_path}")

if __name__ == '__main__':
    run_comprehensive_benchmark()