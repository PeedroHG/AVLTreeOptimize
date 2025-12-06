import sys
import os
import time
import csv
import random

# Setup path para importar a classe AVL
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from avl_tree import AVLTree

# --- CONFIGURAÇÃO ---
TREE_SIZE = 100000 
LONG_RUN_OPS = 500000 # Fase de Estresse
SEARCH_OPS = 1000000  # Fase de Teste de Leitura
REPETITIONS = 5       # Repetições para média estatística

def run_unified_benchmark():
    # Cria diretório de dados
    data_dir = os.path.join(os.path.dirname(__file__), '../../data')
    if not os.path.exists(data_dir): os.makedirs(data_dir)
    csv_path = os.path.join(data_dir, 'results_unified_search.csv')

    print(f"--- BENCHMARK UNIFICADO: LONG RUNNING + BUSCA + TOPOLOGIA ---")
    print(f"Config: N={TREE_SIZE}, Stress={LONG_RUN_OPS}, Search={SEARCH_OPS}")
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        # Cabeçalho completo com todas as métricas conectadas
        writer.writerow([
            'Method', 'Repetition', 
            'Final_Height', 'Avg_Depth', 
            'Total_Search_Time_ms', 'Avg_Search_Time_ns'
        ])

        # --- LOOP DE REPETIÇÕES ---
        for r in range(1, REPETITIONS + 1):
            print(f"\n>>> Rodada {r}/{REPETITIONS}")
            
            # Preparar o Pool de Dados (Comum para ambos para ser justo)
            pool = list(range(TREE_SIZE * 2))
            random.shuffle(pool)
            
            # ==========================================
            # 1. MÉTODO PADRÃO (STANDARD)
            # ==========================================
            print("   [Standard] 1. Construindo e Estressando...", end='\r')
            avl_std = AVLTree('standard')
            
            # A) Warm-up (Encher a árvore)
            for i in range(TREE_SIZE): avl_std.insert(pool[i])
            
            # B) Long Running (Estresse)
            for k in range(LONG_RUN_OPS):
                rem = pool[k % TREE_SIZE]
                add = pool[(k + TREE_SIZE) % len(pool)]
                avl_std.delete(rem)
                avl_std.insert(add)
                pool[k % TREE_SIZE] = add # Atualiza pool virtual
            
            # C) Coleta de Métricas Estruturais (Na árvore estressada)
            h_std = avl_std.get_height(avl_std.root)
            depth_std = avl_std.get_average_depth()
            
            # D) Benchmark de Busca (Na mesma árvore)
            print(f"   [Standard] 2. Buscando {SEARCH_OPS} chaves...      ", end='\r')
            search_keys = pool[:TREE_SIZE] # Chaves que sabemos que estão lá
            
            start = time.perf_counter()
            for _ in range(SEARCH_OPS // TREE_SIZE):
                for k in search_keys:
                    avl_std.search(k)
            end = time.perf_counter()
            
            time_std_ms = (end - start) * 1000
            time_std_ns = (time_std_ms * 1e6) / SEARCH_OPS
            
            writer.writerow(['Standard', r, h_std, depth_std, time_std_ms, time_std_ns])
            print(f"   [Standard] Concluído: H={h_std}, Depth={depth_std:.3f}, Time={time_std_ns:.1f}ns")
            
            del avl_std # Limpar memória

            # ==========================================
            # 2. MÉTODO OTIMIZADO (OPTIMIZED)
            # ==========================================
            # Re-embaralhar pool para garantir independência estatística
            random.shuffle(pool)
            
            print("   [Optimized] 1. Construindo e Estressando...", end='\r')
            avl_opt = AVLTree('optimized')
            
            # A) Warm-up
            for i in range(TREE_SIZE): avl_opt.insert(pool[i])
            
            # B) Long Running
            for k in range(LONG_RUN_OPS):
                rem = pool[k % TREE_SIZE]
                add = pool[(k + TREE_SIZE) % len(pool)]
                avl_opt.delete(rem)
                avl_opt.insert(add)
                pool[k % TREE_SIZE] = add
            
            # C) Métricas Estruturais
            h_opt = avl_opt.get_height(avl_opt.root)
            depth_opt = avl_opt.get_average_depth()
            
            # D) Benchmark de Busca
            print(f"   [Optimized] 2. Buscando {SEARCH_OPS} chaves...      ", end='\r')
            search_keys = pool[:TREE_SIZE]
            
            start = time.perf_counter()
            for _ in range(SEARCH_OPS // TREE_SIZE):
                for k in search_keys:
                    avl_opt.search(k)
            end = time.perf_counter()
            
            time_opt_ms = (end - start) * 1000
            time_opt_ns = (time_opt_ms * 1e6) / SEARCH_OPS
            
            writer.writerow(['Optimized', r, h_opt, depth_opt, time_opt_ms, time_opt_ns])
            print(f"   [Optimized] Concluído: H={h_opt}, Depth={depth_opt:.3f}, Time={time_opt_ns:.1f}ns")
            
            del avl_opt

    print(f"\nBenchmark Unificado Concluído. Dados em: {csv_path}")

if __name__ == '__main__':
    run_unified_benchmark()