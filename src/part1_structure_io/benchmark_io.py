import sys
import os
import csv
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from avl_tree import AVLTree

# --- CONFIGURATION ---
SIZES = [1000, 10000, 100000, 1000000]
REPETITIONS = 5
LONG_RUN_SIZE = 100000 # Fixed size for long running to keep it feasible
LONG_RUN_OPS = 1000000 # 1 Million Ops

def run_scaling_tests(writer):
    """Runs Random and Sorted scenarios across different sizes"""
    for n in SIZES:
        print(f"--> Testing Structure Scaling N={n}...")
        base_data = list(range(n))
        
        for rep in range(1, REPETITIONS + 1):
            # --- SCENARIO: RANDOM ---
            random.shuffle(base_data)
            to_delete = base_data[:n//2]
            
            # Standard
            avl = AVLTree('standard')
            for x in base_data: avl.insert(x)
            avl.reset_stats()
            for x in to_delete: avl.delete(x)
            writer.writerow(['Random', n, rep, 'Standard', avl.stats['rotations'], avl.get_height(avl.root)])
            
            # Optimized
            avl = AVLTree('optimized')
            for x in base_data: avl.insert(x)
            avl.reset_stats()
            for x in to_delete: avl.delete(x)
            writer.writerow(['Random', n, rep, 'Optimized', avl.stats['rotations'], avl.get_height(avl.root)])
            
            # --- SCENARIO: SORTED (Worst Case) ---
            # Insert 0..N (Sorted), Delete Randomly
            
            # Standard
            avl = AVLTree('standard')
            for i in range(n): avl.insert(i) # Sorted Insert
            avl.reset_stats()
            for x in to_delete: avl.delete(x) # Random Delete
            writer.writerow(['Sorted', n, rep, 'Standard', avl.stats['rotations'], avl.get_height(avl.root)])
            
            # Optimized
            avl = AVLTree('optimized')
            for i in range(n): avl.insert(i)
            avl.reset_stats()
            for x in to_delete: avl.delete(x)
            writer.writerow(['Sorted', n, rep, 'Optimized', avl.stats['rotations'], avl.get_height(avl.root)])

def run_long_running(writer):
    """Runs the database simulation"""
    print(f"--> Running Long-Running Simulation (1M Ops) x {REPETITIONS} reps...")
    
    for rep in range(1, REPETITIONS + 1):
        print(f"    ... Repetition {rep}/{REPETITIONS}")
        
        # --- STANDARD ---
        # Generate fresh pool for this repetition
        pool = list(range(LONG_RUN_SIZE * 2))
        random.shuffle(pool)
        
        avl = AVLTree('standard')
        # Initial Population
        for i in range(LONG_RUN_SIZE): avl.insert(pool[i])
        avl.reset_stats()
        
        # Steady State Ops
        for k in range(LONG_RUN_OPS):
            rem = pool[k % LONG_RUN_SIZE]
            add = pool[(k + LONG_RUN_SIZE) % len(pool)]
            avl.delete(rem)
            avl.insert(add)
            pool[k % LONG_RUN_SIZE] = add
            
        writer.writerow(['Long_Running', LONG_RUN_SIZE, rep, 'Standard', avl.stats['rotations'], avl.get_height(avl.root)])
        
        # --- OPTIMIZED ---
        # Generate fresh pool again to ensure fairness and independence
        pool = list(range(LONG_RUN_SIZE * 2)) 
        random.shuffle(pool)

        avl = AVLTree('optimized')
        # Initial Population
        for i in range(LONG_RUN_SIZE): avl.insert(pool[i])
        avl.reset_stats()
        
        # Steady State Ops
        for k in range(LONG_RUN_OPS):
            rem = pool[k % LONG_RUN_SIZE]
            add = pool[(k + LONG_RUN_SIZE) % len(pool)]
            avl.delete(rem)
            avl.insert(add)
            pool[k % LONG_RUN_SIZE] = add

        writer.writerow(['Long_Running', LONG_RUN_SIZE, rep, 'Optimized', avl.stats['rotations'], avl.get_height(avl.root)])

def main():
    data_dir = os.path.join(os.path.dirname(__file__), '../../data')
    if not os.path.exists(data_dir): os.makedirs(data_dir)
    csv_path = os.path.join(data_dir, 'results_structure.csv')
    
    print(f"--- STARTING PHASE 2: STRUCTURE & I/O BENCHMARK ---")

    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Scenario', 'Size', 'Repetition', 'Method', 'Total_Rotations', 'Final_Height'])
        
        run_scaling_tests(writer)
        run_long_running(writer)
        
    print(f"\nPhase 2 Completed. Data saved to {csv_path}")

if __name__ == '__main__':
    main()