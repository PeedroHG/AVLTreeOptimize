import sys
import os
import time
import csv
import random
import statistics

SIZES = [10000] 

REPETITIONS = 5

SCENARIOS = ['Random', 'Sorted', 'SteadyState']
METHODS = ['Standard', 'Optimized']

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from avl_tree import AVLTree
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from avl_tree import AVLTree

def run_comprehensive_benchmark():
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

            master_pool = list(range(n * 2))
            
            for scenario in SCENARIOS:
                print(f"  > Cenário: {scenario}")
                
                for method in METHODS:
                    run_times = []
                    
                    for r in range(1, REPETITIONS + 1):
                        current_pool = master_pool[:]
                        
                        avl = AVLTree(method.lower())
                        
                        if scenario == 'Sorted':
                            warmup_data = list(range(n))
                            for x in warmup_data:
                                avl.insert(x)
                            
                            keys_to_delete = warmup_data[:]
                            random.shuffle(keys_to_delete)
                            keys_to_delete = keys_to_delete[:n//2] 
                            
                        elif scenario == 'Random' or scenario == 'SteadyState':
                            warmup_data = list(range(n))
                            random.shuffle(warmup_data)
                            for x in warmup_data:
                                avl.insert(x)
                            
                            if scenario == 'Random':
                    
                                keys_to_delete = warmup_data[:n//2]
                            else:
                                keys_to_delete = [] 
                        elapsed = 0.0
                        
                        if scenario in ['Random', 'Sorted']:
                            start = time.perf_counter()
                            for k in keys_to_delete:
                                avl.delete(k)
                            end = time.perf_counter()
                            elapsed = end - start
                            
                        elif scenario == 'SteadyState':
                            ops_count = n // 2
                            pool_idx = n 
                            t_accum = 0.0
                            
                            current_nodes = list(range(n)) if scenario == 'Sorted' else warmup_data
                            random.shuffle(current_nodes)
                            
                            for i in range(ops_count):
                                val_rem = current_nodes.pop() 
                                val_add = current_pool[pool_idx] 
                                pool_idx += 1
                                
                                t0 = time.perf_counter()
                                avl.delete(val_rem)
                                t1 = time.perf_counter()
                                t_accum += (t1 - t0)
                                
                                avl.insert(val_add)
                                current_nodes.append(val_add) 
                                
                            elapsed = t_accum

                        time_ms = elapsed * 1000
                        run_times.append(time_ms)
                        writer.writerow([n, scenario, method, r, time_ms])
                        
                        del avl
                    
                    avg_time = statistics.mean(run_times)
                    print(f"    [{method}] Média (5 runs): {avg_time:.4f} ms")

    print(f"\nBenchmark Concluído. Dados salvos em: {csv_path}")

if __name__ == '__main__':
    run_comprehensive_benchmark()