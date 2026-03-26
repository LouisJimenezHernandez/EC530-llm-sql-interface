class Database:
    def __init__(self, db_path: str):
        """
        db_path: path to SQLite database file
        """
        pass

    def connect(self) -> None:
        """Open a connection to the SQLite database"""
        pass

    def close(self) -> None:
        """Close the database connection"""
        pass

    def execute_query(self, sql_query: str, params: tuple = ()) -> list[tuple]:
        """
        Execute a read query and return results.
        Intended for validated SELECT queries.
        """
        pass

    def execute_script(self, sql_script: str) -> None:
        """
        Execute SQL statements such as CREATE TABLE.
        """
        pass

    def insert_rows(self, table_name: str, rows: list[dict]) -> None:
        """
        Insert multiple rows into a table.
        """
        pass

    def get_table_names(self) -> list[str]:
        """
        Return all table names in the database.
        """
        pass

    def get_table_info(self, table_name: str) -> list[tuple]:
        """
        Return PRAGMA table_info(table_name) results.
        """
        pass