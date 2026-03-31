import os
import pandas as pd

class CSVLoader:
    def __init__(self, db, schema_manager):
        """
        db: database interface
        schema_manager: handles schema logic
        """
        self.db = db
        self.schema_manager = schema_manager

    def load_csv(self, file_path: str, table_name: str = None) -> str:
        """
        Loads a CSV file into the database.

        Args:
            file_path: path to CSV file
            table_name: optional override for table name

        Returns:
            Status message (success or error)
        """
        if not file_path or not os.path.exists(file_path):
            return f"Error: file not found: {file_path}"

        if not file_path.lower().endswith(".csv"):
            return "Error: only CSV files are supported"

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            return f"Error reading CSV: {e}"

        if df.empty:
            return "Error: CSV file is empty"

        # Normalize column names early so DB/schema comparisons stay consistent
        df.columns = [self._normalize_column_name(col) for col in df.columns]

        inferred_schema = self.schema_manager.infer_schema_from_csv(file_path)

        # If caller explicitly wants a different table name, allow it
        if table_name is None:
            table_name = inferred_schema["table_name"]
        else:
            table_name = self._normalize_table_name(table_name)

        rows = df.to_dict(orient="records")

        if not self.schema_manager.table_exists(table_name):
            create_sql = self._build_create_table_sql(table_name, inferred_schema["columns"])
            self.db.execute_script(create_sql)
            self.db.insert_rows(table_name, rows)
            return f"Created table '{table_name}' and inserted {len(rows)} rows"

        compare_result = self.schema_manager.compare_schema(table_name, inferred_schema)

        if compare_result == "match":
            self.db.insert_rows(table_name, rows)
            return f"Inserted {len(rows)} rows into existing table '{table_name}'"

        return f"Schema mismatch for table '{table_name}'"
    
    def _build_create_table_sql(self, table_name: str, columns: dict[str, str]) -> str:
        column_defs = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

        for column_name, column_type in columns.items():
            normalized_name = self._normalize_column_name(column_name)

            # Avoid duplicate id if inferred schema already contains one
            if normalized_name == "id":
                continue

            column_defs.append(f"{normalized_name} {column_type}")

        columns_sql = ", ".join(column_defs)
        return f"CREATE TABLE {table_name} ({columns_sql});"

    
    def _normalize_column_name(self, column_name: str) -> str:
        return str(column_name).strip().lower().replace(" ", "_")

    def _normalize_table_name(self, table_name: str) -> str:
        return str(table_name).strip().lower().replace(" ", "_").replace(".csv", "")