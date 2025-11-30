import sys
import os
import time
import csv
import random

# Setup path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from avl_tree import AVLTree

# --- CONFIGURATION ---
# Usamos o cenário Long Running pois foi onde houve diferença de altura (19 vs 20)
TREE_SIZE = 100000 
LONG_RUN_OPS = 500000 
SEARCH_OPS = 1000000 # 1 Milhão de buscas para ter precisão

def run_search_benchmark():
    # Create data dir
    data_dir = os.path.join(os.path.dirname(__file__), '../../data')
    if not os.path.exists(data_dir): os.makedirs(data_dir)
    csv_path = os.path.join(data_dir, 'results_search.csv')

    print(f"--- PHASE 3: SEARCH PERFORMANCE (Read Latency) ---")
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Method', 'Final_Height', 'Total_Search_Time_ms', 'Avg_Search_Time_ns'])

        # Pool setup for Long Running
        pool = list(range(TREE_SIZE * 2))
        random.shuffle(pool)
        
        # --- 1. STANDARD METHOD ---
        print("1. Building Standard Tree (Long Running State)...")
        avl_std = AVLTree('standard')
        # Fill
        for i in range(TREE_SIZE): avl_std.insert(pool[i])
        # Stress (Long Running)
        for k in range(LONG_RUN_OPS):
            rem = pool[k % TREE_SIZE]
            add = pool[(k + TREE_SIZE) % len(pool)]
            avl_std.delete(rem)
            avl_std.insert(add)
            pool[k % TREE_SIZE] = add
            
        h_std = avl_std.get_height(avl_std.root)
        print(f"   -> Standard Height: {h_std}")
        
        # Measure Search
        print(f"   -> Running {SEARCH_OPS} searches...")
        # Search for keys that exist (first half of pool)
        search_keys = pool[:TREE_SIZE] 
        
        start = time.perf_counter()
        for _ in range(SEARCH_OPS // TREE_SIZE): # Repeat to reach 1M ops
            for k in search_keys:
                avl_std.search(k)
        end = time.perf_counter()
        
        time_std_ms = (end - start) * 1000
        writer.writerow(['Standard', h_std, time_std_ms, (time_std_ms * 1e6) / SEARCH_OPS])
        
        del avl_std # Free memory

        # --- 2. OPTIMIZED METHOD ---
        # Reset Pool to ensure fairness
        random.shuffle(pool) 
        
        print("2. Building Optimized Tree (Long Running State)...")
        avl_opt = AVLTree('optimized')
        for i in range(TREE_SIZE): avl_opt.insert(pool[i])
        
        for k in range(LONG_RUN_OPS):
            rem = pool[k % TREE_SIZE]
            add = pool[(k + TREE_SIZE) % len(pool)]
            avl_opt.delete(rem)
            avl_opt.insert(add)
            pool[k % TREE_SIZE] = add

        h_opt = avl_opt.get_height(avl_opt.root)
        print(f"   -> Optimized Height: {h_opt}")
        
        print(f"   -> Running {SEARCH_OPS} searches...")
        search_keys = pool[:TREE_SIZE]
        
        start = time.perf_counter()
        for _ in range(SEARCH_OPS // TREE_SIZE):
            for k in search_keys:
                avl_opt.search(k)
        end = time.perf_counter()
        
        time_opt_ms = (end - start) * 1000
        writer.writerow(['Optimized', h_opt, time_opt_ms, (time_opt_ms * 1e6) / SEARCH_OPS])

    print(f"\nSearch Benchmark Completed. Data: {csv_path}")

if __name__ == '__main__':
    run_search_benchmark()