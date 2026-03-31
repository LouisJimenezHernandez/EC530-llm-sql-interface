import sqlite3

class Database:
    def __init__(self, db_path: str):
        """
        db_path: path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None

    def connect(self) -> None:
        """Open a connection to the SQLite database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # allows dict-like access

    def close(self) -> None:
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute_query(self, sql_query: str, params: tuple = ()) -> list[tuple]:
        """
        Execute a read query and return results.
        Intended for validated SELECT queries.
        """
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Convert to list of dicts
        return [dict(row) for row in rows]


    def execute_script(self, sql_script: str) -> None:
        """
        Execute SQL statements such as CREATE TABLE.
        """
        cursor = self.conn.cursor()
        cursor.executescript(sql_script)
        self.conn.commit()

    def insert_rows(self, table_name: str, rows: list[dict]) -> None:
        """
        Insert multiple rows into a table.
        """
        if not rows:
            return

        columns = rows[0].keys()
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))

        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

        values = [tuple(row[col] for col in columns) for row in rows]

        cursor = self.conn.cursor()
        cursor.executemany(query, values)
        self.conn.commit()

    def get_table_names(self) -> list[str]:
        """
        Return all table names in the database.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [row[0] for row in cursor.fetchall()]


    def get_table_info(self, table_name: str) -> list[tuple]:
        """
        Return PRAGMA table_info(table_name) results.
        """
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        return cursor.fetchall()