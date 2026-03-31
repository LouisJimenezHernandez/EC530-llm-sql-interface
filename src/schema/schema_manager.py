import os
import pandas as pd

class SchemaManager:
    def __init__(self, db):
        """
        db: database interface (for schema queries only)
        """
        self.db = db

    def get_schema(self) -> dict:
        """
        Returns the full database schema.

        Example:
        {
            "users": ["id", "name", "email"],
            "orders": ["id", "user_id", "amount"]
        }
        """
        schema = {}
        table_names = self.db.get_table_names()

        for table_name in table_names:
            schema[table_name] = self.get_table_schema(table_name)

        return schema


    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database"""
        return table_name in self.db.get_table_names()

    def get_table_schema(self, table_name: str) -> dict:
        """
        Returns schema for a specific table.

        Example:
        {
            "columns": {
                "id": "INTEGER",
                "name": "TEXT"
            }
        }
        """
        table_info = self.db.get_table_info(table_name)

        columns = {}
        for column in table_info:
            column_name = column[1]
            column_type = column[2]
            columns[column_name] = column_type

        return {"columns": columns}

    def infer_schema_from_csv(self, file_path: str) -> dict:
        """
        Infers schema from a CSV file.

        Returns:
            {
                "table_name": str,
                "columns": {
                    "column_name": "SQL_TYPE"
                }
            }
        """
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError("CSV file is empty")

        df.columns = [self._normalize_name(col) for col in df.columns]

        table_name = self._infer_table_name(file_path)

        columns = {}
        for column_name, dtype in df.dtypes.items():
            columns[column_name] = self._map_dtype_to_sql(dtype)

        return {
            "table_name": table_name,
            "columns": columns
        }

    def compare_schema(self, table_name: str, new_schema: dict) -> str:
        """
        Compares existing table schema with new schema.

        Returns:
            "match" → append
            "mismatch" → create new / conflict
        """
        existing_schema = self.get_table_schema(table_name)

        existing_columns = existing_schema["columns"]
        new_columns = new_schema["columns"]

        if existing_columns == new_columns:
            return "match"

        return "mismatch"

    def _infer_table_name(self, file_path: str) -> str:
        file_name = os.path.basename(file_path)
        return os.path.splitext(file_name)[0].strip().lower().replace(" ", "_")

    def _normalize_name(self, name: str) -> str:
        return str(name).strip().lower().replace(" ", "_")

    def _map_dtype_to_sql(self, dtype) -> str:
        dtype_str = str(dtype).lower()

        if "int" in dtype_str:
            return "INTEGER"
        if "float" in dtype_str:
            return "REAL"

        return "TEXT"