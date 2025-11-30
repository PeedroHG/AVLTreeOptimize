import sys
import os
import time
import csv
import random

# Import core class
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from avl_tree import AVLTree

# --- CONFIGURATION ---
SIZES = [1000, 10000, 100000, 1000000] # 1k to 1M
REPETITIONS = 5

def run():
    data_dir = os.path.join(os.path.dirname(__file__), '../../data')
    if not os.path.exists(data_dir): os.makedirs(data_dir)
    
    csv_path = os.path.join(data_dir, 'results_time.csv')
    
    print(f"--- STARTING PHASE 1: CPU TIME BENCHMARK (N={SIZES}) ---")
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Size', 'Repetition', 'Method', 'Execution_Time_ms'])
        
        for n in SIZES:
            print(f"--> Testing Size N={n}...")
            
            # Create base data once per size to be fair
            base_data = list(range(n))
            
            for rep in range(1, REPETITIONS + 1):
                print(f"    Repetition {rep}/{REPETITIONS}...")
                
                # Shuffle for randomness
                random.shuffle(base_data)
                to_delete = base_data[:n//2] # Remove 50%
                
                # --- STANDARD ---
                avl = AVLTree('standard')
                # Insert is setup cost, we measure delete
                for x in base_data: avl.insert(x)
                
                start = time.perf_counter()
                for x in to_delete: avl.delete(x)
                end = time.perf_counter()
                
                writer.writerow([n, rep, 'Standard', (end-start)*1000])
                
                # --- OPTIMIZED ---
                avl = AVLTree('optimized')
                for x in base_data: avl.insert(x)
                
                start = time.perf_counter()
                for x in to_delete: avl.delete(x)
                end = time.perf_counter()
                
                writer.writerow([n, rep, 'Optimized', (end-start)*1000])
                
                # Force Garbage Collection (optional but good for large memory)
                del avl

    print(f"\nPhase 1 Completed. Data saved to {csv_path}")

if __name__ == '__main__':
    run()