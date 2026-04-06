# LLM–SQL Interface

## System Overview

This project implements a **natural language interface for querying a SQLite database**.
Users can load CSV data, ask questions in plain English, and receive results generated through SQL queries.

### Architecture

The system is designed with a **modular, layered architecture**:

```
User (CLI)
   ↓
CLIInterface
   ↓
QueryService
   ↓
 ┌───────────────┬───────────────┐
 ↓               ↓               ↓
LLMAdapter   SQLValidator   SchemaManager
                                ↓
                            Database (SQLite)
                                ↑
                            CSVLoader
```

### Module Responsibilities

* **Database**

  * Handles SQLite operations (create tables, insert rows, execute queries)

* **SchemaManager**

  * Manages schema information
  * Infers schema from CSV files
  * Compares schemas

* **CSVLoader**

  * Loads CSV data into the database
  * Creates tables or appends data based on schema

* **LLMAdapter**

  * Converts natural language queries into SQL using an LLM

* **SQLValidator**

  * Ensures only safe, valid `SELECT` queries are executed

* **QueryService**

  * Orchestrates query execution flow
  * Handles both SQL and natural language inputs

* **CLIInterface**

  * Provides command-line interaction with the system

---

## How to Run the Project

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd EC530-llm-sql-interface
```

---

### 2. Install dependencies

```bash
pip install pandas openai pytest python-dotenv
```

---

### 3. Set your OpenAI API key

In PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

---

### 4. Run the application

```powershell
$env:PYTHONPATH="."
python src/main.py
```

---

### 5. Example CLI commands

```text
load data/pipelines.csv
tables
sql SELECT * FROM pipelines
ask Show me all pipeline names
exit
```

---

## How to Run Tests

From the project root:

```powershell
$env:PYTHONPATH="."
pytest -v
```

To run a specific test file:

```powershell
pytest tests/test_sql_validator.py -v
```

---

## Notes

* The system uses **SQLite** for storage.
* CSV ingestion is handled manually (no `.to_sql()` usage).
* The LLM output is validated before execution to ensure safety.
* Unit tests use mocks to isolate components.

---

## Summary

This project demonstrates:

* Clean modular design
* Safe integration of LLM-generated SQL
* End-to-end data ingestion and querying
* Strong unit testing practices

---

## Requirements

* Python 3.10+
* SQLite (built into Python)
* OpenAI API key (for LLM functionality)

---
