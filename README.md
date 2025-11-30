python -m venv .venv <br>
source .venv/Scripts/activate <br>
pip install -r requirements.txt <br>
rm -rf venv <br> <br>

python src/part1_cpu_time/benchmark_time.py <br>
python src/part1_cpu_time/plot_time.py <br> <br>

python src/part1_structure_io/benchmark_io.py <br>
python src/part1_structure_io/plot_structure.py <br> <br>

python src/part1_search_performance/benchmark_search.py <br>
python src/part1_search_performance/plot_search.py