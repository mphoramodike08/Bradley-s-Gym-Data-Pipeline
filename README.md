# 🏋️ Bradley's Gym Data Pipeline

An end-to-end data engineering pipeline built in Python, Pandas, and DuckDB. This project simulates a high-volume enterprise gym dataset containing 10,000+ members and 100,000+ check-in events, handling data auditing, data quality enforcement, ETL transformations, and SQL analytics.

---

## 🛠️ Tech Stack & Tools
* **Language:** Python 3.14
* **Data Processing & Manipulation:** Pandas, NumPy, Faker
* **Analytical Database / Data Warehouse:** DuckDB (In-Memory SQL)
* **Version Control:** Git, GitHub

---

## 🏗️ Architecture & Pipeline Lifecycle

1. **Stage 1: Raw Data Generation (`pipeline.py`)**
   * Generates `10,015` raw member records and `100,000` check-in logs with intentional data quality flaws (negative fees/durations, casing inconsistencies, duplicate records, and orphan foreign keys).

2. **Stage 2: Data Auditing & Profiling (`audit_data.py`)**
   * Programmatically scans raw CSVs to detect missing values, duplicates, negative numbers, and foreign key violations before ETL execution.

3. **Stage 3: Data Cleaning & Standardization (`clean_data.py`)**
   * Removes duplicate rows and normalizes categorical text casing.
   * Converts negative fees and workout durations to positive absolute values.
   * Enforces referential integrity by dropping orphan check-in logs.

4. **Stage 4: Data Warehousing & Analytics (`analyze_data.py`)**
   * Registers cleaned DataFrames as SQL tables inside DuckDB.
   * Executes analytical queries calculating Monthly Recurring Revenue (MRR), peak workout hours, popular activities, and top member engagement.

---

## 🚀 How to Run the Pipeline

### 1. Prerequisites
Install required dependencies:
```bash
pip install pandas numpy faker duckdb