import sys
import os
import csv
import random

# Ajustar path para importar a classe
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from avl_tree import AVLTree

# --- CONFIGURAÇÃO ---
TREE_SIZE = 100000 
LONG_RUN_OPS = 500000 
REPETITIONS = 5
OUTPUT_FILE = 'results_topology_complete.csv'

def run_topology_benchmark():
    # Setup de diretórios
    data_dir = os.path.join(os.path.dirname(__file__), '../../data')
    if not os.path.exists(data_dir): os.makedirs(data_dir)
    csv_path = os.path.join(data_dir, OUTPUT_FILE)

    print(f"--- BENCHMARK DE TOPOLOGIA (N={TREE_SIZE}) ---")
    print(f"Métricas: Altura Final (Pior Caso) vs Profundidade Média (Caso Médio)")
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Scenario', 'Repetition', 'Method', 'Avg_Depth', 'Final_Height'])

        # Loop de Repetições para estatística
        for r in range(1, REPETITIONS + 1):
            print(f"\n>>> Rodada {r}/{REPETITIONS}")

            # --- 1. CENÁRIO RANDOM ---
            print("   [1/3] Random: Inserção Aleatória -> Remoção Aleatória")
            data = list(range(TREE_SIZE))
            random.shuffle(data)
            to_delete = data[:TREE_SIZE // 2] # Remover 50%
            
            # Standard
            avl = AVLTree('standard')
            for x in data: avl.insert(x)
            for x in to_delete: avl.delete(x)
            writer.writerow(['Random', r, 'Standard', avl.get_average_depth(), avl.get_height(avl.root)])
            
            # Optimized
            avl = AVLTree('optimized')
            for x in data: avl.insert(x)
            for x in to_delete: avl.delete(x)
            writer.writerow(['Random', r, 'Optimized', avl.get_average_depth(), avl.get_height(avl.root)])

            # --- 2. CENÁRIO SORTED (PIOR CASO) ---
            print("   [2/3] Sorted: Inserção Ordenada -> Remoção Aleatória")
            # Inserir 0..N (Ordenado)
            # Deletar aleatório
            
            # Standard
            avl = AVLTree('standard')
            for x in range(TREE_SIZE): avl.insert(x)
            for x in to_delete: avl.delete(x) # Reusa a lista embaralhada para deletar
            writer.writerow(['Sorted', r, 'Standard', avl.get_average_depth(), avl.get_height(avl.root)])
            
            # Optimized
            avl = AVLTree('optimized')
            for x in range(TREE_SIZE): avl.insert(x)
            for x in to_delete: avl.delete(x)
            writer.writerow(['Sorted', r, 'Optimized', avl.get_average_depth(), avl.get_height(avl.root)])

            # --- 3. CENÁRIO LONG RUNNING ---
            print("   [3/3] Long Running: Estado Estacionário (Demorado...)")
            pool = list(range(TREE_SIZE * 2))
            random.shuffle(pool)
            
            # Standard
            avl = AVLTree('standard')
            for i in range(TREE_SIZE): avl.insert(pool[i])
            for k in range(LONG_RUN_OPS):
                rem = pool[k % TREE_SIZE]
                add = pool[(k + TREE_SIZE) % len(pool)]
                avl.delete(rem)
                avl.insert(add)
                pool[k % TREE_SIZE] = add
            writer.writerow(['Long_Running', r, 'Standard', avl.get_average_depth(), avl.get_height(avl.root)])
            
            # Optimized
            # Reset pool logic
            random.shuffle(pool)
            avl = AVLTree('optimized')
            for i in range(TREE_SIZE): avl.insert(pool[i])
            for k in range(LONG_RUN_OPS):
                rem = pool[k % TREE_SIZE]
                add = pool[(k + TREE_SIZE) % len(pool)]
                avl.delete(rem)
                avl.insert(add)
                pool[k % TREE_SIZE] = add
            writer.writerow(['Long_Running', r, 'Optimized', avl.get_average_depth(), avl.get_height(avl.root)])

    print(f"\nBenchmark Finalizado! Dados salvos em: {csv_path}")

if __name__ == '__main__':
    run_topology_benchmark()