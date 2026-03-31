class QueryService:
    def __init__(self, db, validator, llm_adapter, schema_manager):
        """
        db: database interface
        validator: SQL validator
        llm_adapter: LLM adapter
        schema_manager: provides schema info
        """
        self.db = db
        self.validator = validator
        self.llm_adapter = llm_adapter
        self.schema_manager = schema_manager

    def handle_nl_query(self, user_input: str) -> str:
        """
        Takes natural language input and returns formatted results.
        """
        schema = self.schema_manager.get_schema()
        sql_query = self.llm_adapter.generate_sql(user_input, schema)

        is_valid, error = self.validator.validate(sql_query)

        if not is_valid:
            return error

        results = self.db.execute_query(sql_query)
        return results

    def handle_sql_query(self, sql_query: str) -> str:
        """
        Takes raw SQL input (for testing phase) and returns results.
        """
        is_valid, error = self.validator.validate(sql_query)

        if not is_valid:
            return error

        results = self.db.execute_query(sql_query)
        return results