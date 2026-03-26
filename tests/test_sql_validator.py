import pytest
from src.query.sql_validator import SQLValidator

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

@pytest.fixture
def validator():
    schema_manager = MockSchemaManager()
    return SQLValidator(schema_manager)

@pytest.mark.parametrize(
    "query",
    [
        "SELECT * FROM pipelines",
        "SELECT id, name FROM facilities",
        "SELECT name from pipelines",
        "SELECT daily_oil_flow FROM pipelines"
    ]
)
def test_returns_true_if_select_query(validator, query):
    is_valid, error = validator.validate(query)
    assert is_valid is True
    assert error == ""

@pytest.mark.parametrize(
    "query",
    [
        "DROP TABLE pipelines",
        "DELETE FROM pipelines",
        "CREATE INDEX idx_pipelines on pipelines(state)"
    ]
)
def test_return_error_if_non_select_query(validator, query):
    is_valid, error = validator.validate(query)
    assert is_valid is False
    assert "Only SELECT queries are allowed" in error 

@pytest.mark.parametrize(
    "query",
    [
       "SELECT * FROM twice",
        "SELECT id, name FROM underscores",
        "SELECT name from nmixx",
        "SELECT daily_oil_flow FROM jvb"
    ]
)
def test_return_error_if_unknown_table(validator, query):
    is_valid, error = validator.validate(query)
    assert is_valid is False
    assert "Unknown tables detected" in error 

@pytest.mark.parametrize(
    "query",
    [
       "SELECT songs FROM pipelines",
        "SELECT friends, name FROM facilities",
        "SELECT dracula from pipelines",
        "SELECT legend_changers FROM pipelines"
    ]
)
def test_return_error_if_unknown_column(validator, query):
    is_valid, error = validator.validate(query)
    assert is_valid is False
    assert "Unknown columns detected" in error 
