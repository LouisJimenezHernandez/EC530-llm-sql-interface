import pytest
from src.schema.schema_manager import SchemaManager


class MockDB:
    def get_table_names(self):
        return ["facilities", "pipelines"]

    def get_table_info(self, table_name):
        schemas = {
            #(cid, name, type, notnull, dflt_value, pk) is PRAGMA table_info() style
            "facilities": [
                (0, "id", "INTEGER", 0, None, 1),
                (1, "name", "TEXT", 0, None, 0),
                (2, "state", "TEXT", 0, None, 0),
            ],
            "pipelines": [
                (0, "id", "INTEGER", 0, None, 1),
                (1, "name", "TEXT", 0, None, 0),
                (2, "daily_oil_flow", "INTEGER", 0, None, 0),
            ],
        }
        return schemas.get(table_name, [])
    
class TestStep1_TableLookup:

    @pytest.mark.parametrize(
        "table_name",
        [
            "facilities",
            "pipelines"
        ]
    )
    def test_return_true_if_tables_exist(self, table_name):
        db = MockDB()
        schema_manager = SchemaManager(db)

        result = schema_manager.table_exists(table_name)

        assert result is True

    @pytest.mark.parametrize(
        "table_name",
        [
            "jellyous",
            "bustamove"
        ]
    )
    def test_return_false_if_tables_dont_exist(self, table_name):
        db = MockDB()
        schema_manager = SchemaManager(db)

        result = schema_manager.table_exists(table_name)

        assert result is False

class TestStep2_TableSchema:
    def test_return_expected_schema_for_pipelines(self):
        db = MockDB()
        schema_manager = SchemaManager(db)

        result = schema_manager.get_table_schema("pipelines")

        assert result == {
            "columns": {
                "id": "INTEGER",
                "name": "TEXT",
                "daily_oil_flow": "INTEGER"
            }
        }

    def test_return_expected_schema_for_facilities(self):
        db = MockDB()
        schema_manager = SchemaManager(db)

        result = schema_manager.get_table_schema("facilities")

        assert result == {
            "columns": {
                "id": "INTEGER",
                "name": "TEXT",
                "state": "TEXT"
            }
        }

class TestStep3_CompareSchemas:
    def test_returns_match_for_matching_schema(self):
        db = MockDB()
        schema_manager = SchemaManager(db)

        new_schema = {
            "columns": {
                "id": "INTEGER",
                "name": "TEXT",
                "daily_oil_flow": "INTEGER"
            }
        }

        result = schema_manager.compare_schema("pipelines", new_schema)

        assert result == "match"

    def test_returns_mismatch_for_mismatched_columns(self):
        db = MockDB()
        schema_manager = SchemaManager(db)

        new_schema = {
            "columns": {
                "Aid": "INTEGER",
                "Aname": "TEXT",
                "Adaily_oil_flow": "INTEGER"
            }
        }

        result = schema_manager.compare_schema("pipelines", new_schema)

        assert result == "mismatch"

    def test_returns_mismatch_for_mismatched_types(self):
        db = MockDB()
        schema_manager = SchemaManager(db)

        new_schema = {
            "columns": {
                "id": "TEXT",
                "name": "INTEGER",
                "daily_oil_flow": "TEXT"
            }
        }

        result = schema_manager.compare_schema("pipelines", new_schema)

        assert result == "mismatch"