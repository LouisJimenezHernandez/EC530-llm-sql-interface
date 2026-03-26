import pytest
from src.query.query_service import QueryService


class MockDB:
    def __init__(self):
        self.called = False

    def execute_query(self, sql_query):
        self.called = True
        return [("Pipeline A", 1000)]


class MockValidator:
    def __init__(self, is_valid=True, error=""):
        self.is_valid = is_valid
        self.error = error

    def validate(self, sql_query):
        return self.is_valid, self.error


class MockLLMAdapter:
    def generate_sql(self, user_input, schema):
        return "SELECT name FROM pipelines"


class MockSchemaManager:
    def get_schema(self):
        return {
            "facilities": {
                "columns": {
                    "id": "INTEGER",
                    "name": "TEXT",
                    "state": "TEXT"
                }
            },
            "pipelines": {
                "columns": {
                    "id": "INTEGER",
                    "name": "TEXT",
                    "daily_oil_flow": "INTEGER"
                }
            }
        }
   
class TestStep1_SQLPath:

    @pytest.mark.parametrize(
        "query",
        [
            "SELECT * FROM pipelines",
            "SELECT id, name FROM facilities",
            "SELECT name from pipelines",
            "SELECT daily_oil_flow FROM pipelines"
        ]
    )
    def test_db_called_if_query_valid(self, query):
        db = MockDB()
        validator = MockValidator(is_valid=True)
        llm_adapter = MockLLMAdapter()
        schema_manager = MockSchemaManager()

        service = QueryService(db, validator, llm_adapter, schema_manager)

        service.handle_sql_query(query)

        assert db.called is True


    @pytest.mark.parametrize(
        "query",
        [
            "DROP TABLE pipelines",
            "DELETE FROM pipelines",
            "CREATE INDEX idx_pipelines on pipelines(state)"
        ]
    )
    def test_db_not_called_if_query_invalid(self, query):
        db = MockDB()
        validator = MockValidator(is_valid=False, error="Invalid query")
        llm_adapter = MockLLMAdapter()
        schema_manager = MockSchemaManager()

        service = QueryService(db, validator, llm_adapter, schema_manager)

        service.handle_sql_query(query)

        assert db.called is False

class TestStep2_NaturalLangPath:
    @pytest.mark.parametrize(
        "natLang",
        [
            "Show pipeline names",
            "Show facilities ids and names",
            "Show all properties of pipeline"
        ]
    )
    def test_db_called_if_natLang_creates_valid_sql(self,natLang):
        db = MockDB()
        validator = MockValidator(is_valid=True)
        llm_adapter = MockLLMAdapter()
        schema_manager = MockSchemaManager()

        service = QueryService(db, validator, llm_adapter, schema_manager)

        service.handle_nl_query(natLang)

        assert db.called is True

    @pytest.mark.parametrize(
        "natLang",
        [
            "This is a test message",
            "Good at Love",
            "Chrono Genesis"
        ]
    )
    def test_db_not_called_if_natLang_creates_invalid_sql(self,natLang):
        db = MockDB()
        validator = MockValidator(is_valid=False, error="invalid SQL")
        llm_adapter = MockLLMAdapter()
        schema_manager = MockSchemaManager()

        service = QueryService(db, validator, llm_adapter, schema_manager)

        service.handle_nl_query(natLang)

        assert db.called is False