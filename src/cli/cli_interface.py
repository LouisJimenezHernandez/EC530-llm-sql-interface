class CLIInterface:
    def __init__(self, query_service, csv_loader, schema_manager):
        """
        query_service: handles query processing
        csv_loader: handles CSV ingestion
        schema_manager: optional for schema display commands
        """
        pass

    def run(self) -> None:
        """
        Start the main CLI loop.
        """
        pass

    def handle_command(self, command: str) -> str:
        """
        Process a single user command and return a response message.
        """
        pass