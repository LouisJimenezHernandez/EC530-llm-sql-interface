from src.cli.cli_interface import CLIInterface


class MockQueryService:
    def __init__(self):
        self.sql_called = False
        self.nl_called = False

    def handle_sql_query(self, query):
        self.sql_called = True
        return "SQL result"

    def handle_nl_query(self, user_input):
        self.nl_called = True
        return "NL result"


class MockCSVLoader:
    def __init__(self):
        self.called = False

    def load_csv(self, file_path):
        self.called = True
        return "CSV loaded"


class MockSchemaManager:
    def get_schema(self):
        return {
            "pipelines": {
                "columns": {
                    "id": "INTEGER",
                    "name": "TEXT"
                }
            }
        }
    
class TestStep1_SQLCommand:

    def test_sql_command_routes_to_query_service(self):
        query_service = MockQueryService()
        csv_loader = MockCSVLoader()
        schema_manager = MockSchemaManager()

        cli = CLIInterface(query_service, csv_loader, schema_manager)

        result = cli.handle_command("sql SELECT * FROM pipelines")

        assert query_service.sql_called is True
        assert query_service.nl_called is False
        assert csv_loader.called is False

class TestStep2_NLCommand:

    def test_ask_command_routes_to_nl_query_service(self):
        query_service = MockQueryService()
        csv_loader = MockCSVLoader()
        schema_manager = MockSchemaManager()

        cli = CLIInterface(query_service, csv_loader, schema_manager)

        result = cli.handle_command("ask Show pipeline names")

        assert query_service.nl_called is True
        assert query_service.sql_called is False
        assert csv_loader.called is False