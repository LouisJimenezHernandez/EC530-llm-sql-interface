class CLIInterface:
    def __init__(self, query_service, csv_loader, schema_manager):
        """
        query_service: handles query processing
        csv_loader: handles CSV ingestion
        schema_manager: optional for schema display commands
        """
        self.query_service = query_service
        self.csv_loader = csv_loader
        self.schema_manager = schema_manager

    def handle_command(self, command: str):
        command = command.strip()

        if not command:
            return "Invalid command"

        if command.lower() == "exit":
            return "exit"

        if command.lower() == "tables":
            schema = self.schema_manager.get_schema()
            if not schema:
                return "No tables found"
            return ", ".join(schema.keys())

        if command.lower().startswith("load "):
            file_path = command[5:].strip()
            return self.csv_loader.load_csv(file_path)

        if command.lower().startswith("sql "):
            sql_query = command[4:].strip()
            return self.query_service.handle_sql_query(sql_query)

        if command.lower().startswith("ask "):
            user_input = command[4:].strip()
            return self.query_service.handle_nl_query(user_input)

        return "Invalid command"

    def run(self):
        print("Welcome to the LLM SQL Interface.")
        print("Commands: load <file>, sql <query>, ask <question>, tables, exit")

        while True:
            command = input("> ")
            result = self.handle_command(command)

            if result == "exit":
                print("Goodbye!")
                break

            print(result)