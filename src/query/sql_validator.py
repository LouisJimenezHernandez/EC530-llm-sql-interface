class SQLValidator:
    def __init__(self, schema_manager):
        """
        schema_manager: provides table + column info
        """
        self.schema_manager = schema_manager

    def validate(self, sql_query: str) -> tuple[bool, str]:
        """
        Validates a SQL query.

        Returns:
            (True, "") if valid
            (False, error_message) if invalid
        """
        if not sql_query or not sql_query.strip():
            return False, "Query cannot be empty"

        if not self._is_select_query(sql_query):
            return False, "Only SELECT queries are allowed"

        schema = self.schema_manager.get_schema()

        tables = self._extract_tables(sql_query)
        if not tables:
            return False, "Invalid query: missing FROM clause"

        table = tables[0]  # assume single-table for now

        if table not in schema:
            return False, f"Unknown table detected: {table}"

        columns = self._extract_columns(sql_query)

        if columns != ["*"]:
            valid_columns = schema[table]["columns"].keys()

            for col in columns:
                if col not in valid_columns:
                    return False, f"Unknown column detected: {col}"

        return True, ""

    def _is_select_query(self, sql: str) -> bool:
        return sql.strip().lower().startswith("select")

    def _extract_tables(self, sql: str) -> list[str]:
        sql_lower = sql.lower()

        if " from " not in sql_lower:
            return []

        after_from = sql_lower.split(" from ", 1)[1]
        table = after_from.strip().split()[0]

        return [table]

    def _extract_columns(self, sql: str) -> list[str]:
        sql_lower = sql.lower()

        if " from " not in sql_lower:
            return []

        select_part = sql_lower.split(" from ", 1)[0]
        columns_text = select_part.replace("select", "", 1).strip()

        columns = [col.strip() for col in columns_text.split(",")]

        return columns