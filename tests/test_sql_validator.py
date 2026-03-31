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
    "query, table",
    [
        ("SELECT * FROM twice", "twice"),
        ("SELECT id, name FROM underscores", "underscores"),
        ("SELECT name from nmixx", "nmixx"),
        ("SELECT daily_oil_flow FROM jvb", "jvb")
    ]
)
def test_return_error_if_unknown_table(validator, query, table):
    is_valid, error = validator.validate(query)
    assert is_valid is False
    assert "Unknown table detected: " in error
    assert table in error 

@pytest.mark.parametrize(
    "query, column",
    [
        ("SELECT songs FROM pipelines", "songs"),
        ("SELECT friends, name FROM facilities", "friends"),
        ("SELECT dracula from pipelines", "dracula"),
        ("SELECT legend_changers FROM pipelines", "legend_changers")
    ]
)
def test_return_error_if_unknown_column(validator, query, column):
    is_valid, error = validator.validate(query)
    assert is_valid is False
    assert "Unknown column detected: " in error
    assert column in error 
