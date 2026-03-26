class SQLValidator:
    def __init__(self, schema_manager):
        """
        schema_manager: provides table + column info
        """
        pass

    def validate(self, sql_query: str) -> tuple[bool, str]:
        """
        Validates a SQL query.

        Returns:
            (True, "") if valid
            (False, error_message) if invalid
        """
        pass

    def _is_select_query(self, sql: str) -> bool:
        pass

    def _extract_tables(self, sql: str) -> list[str]:
        pass

    def _extract_columns(self, sql: str) -> list[str]:
        pass