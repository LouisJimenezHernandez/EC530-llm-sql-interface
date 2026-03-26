class SchemaManager:
    def __init__(self, db):
        """
        db: database interface (for schema queries only)
        """
        pass

    def get_schema(self) -> dict:
        """
        Returns the full database schema.

        Example:
        {
            "users": ["id", "name", "email"],
            "orders": ["id", "user_id", "amount"]
        }
        """
        pass

    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database"""
        pass

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
        pass

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
        pass

    def compare_schema(self, table_name: str, new_schema: dict) -> str:
        """
        Compares existing table schema with new schema.

        Returns:
            "match" → append
            "mismatch" → create new / conflict
        """
        pass