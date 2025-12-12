# 📊 Benchmarks em Python

Este projeto contém scripts para benchmark e visualização de desempenho relacionados a **tempo de CPU**, **estrutura de I/O** e **performance de busca**.

## 🛠️ Requisitos

* Python 3.8+
* `pip`

---

## 🚀 Setup do Ambiente Virtual

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente:

* **Windows (PowerShell):**

```powershell
.venv\Scripts\Activate
```

* **Linux / macOS / Git Bash:**

```bash
source .venv/Scripts/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## ▶️ Executando os Benchmarks

### 1️⃣ CPU Time

```bash
python src/part1_cpu_time/benchmark_time.py
python src/part1_cpu_time/plot_time.py
```

### 2️⃣ Estrutura e I/O

```bash
python src/part1_structure_io/benchmark_io.py
python src/part1_structure_io/plot_structure.py
```

### 3️⃣ Performance de Busca

```bash
python src/part1_search_performance/benchmark_search.py
python src/part1_search_performance/plot_search.py
```

---

## 🧹 Limpeza (opcional)

Para remover o ambiente virtual:

```bash
rm -rf venv
```

