import pytest
from src.data_loader.csv_loader import CSVLoader


class MockDB:
    def __init__(self):
        self.created_table = False
        self.inserted_rows = False

    def execute_script(self, sql_script):
        self.created_table = True

    def insert_rows(self, table_name, rows):
        self.inserted_rows = True

class MockSchemaManager:
    def __init__(self, table_exists=False, compare_result="match"):
        self._table_exists = table_exists
        self._compare_result = compare_result

    def table_exists(self, table_name):
        return self._table_exists

    def infer_schema_from_csv(self, file_path):
        return {
            "table_name": "pipelines",
            "columns": {
                "id": "INTEGER",
                "name": "TEXT",
                "daily_oil_flow": "INTEGER"
            }
        }

    def compare_schema(self, table_name, new_schema):
        return self._compare_result
    
class TestStep1_CreateNewTable:

    def test_returns_table_created_rows_inserted_if_table_not_exist(self, tmp_path):
        csv_file = tmp_path / "horses.csv"
        csv_file.write_text("name,g1_wins\nDaitaku Helios,2\nMejiro Palmer,2\n")

        db = MockDB()
        schema_manager = MockSchemaManager(table_exists=False)
        loader = CSVLoader(db, schema_manager)

        loader.load_csv(str(csv_file))

        assert db.created_table is True
        assert db.inserted_rows is True

class TestStep2_AppendMatchingSchema:

    def test_return_row_insertion_no_table_created_if_schema_matches(self, tmp_path):
        csv_file = tmp_path / "horses.csv"
        csv_file.write_text("name,g1_wins\nDaitaku Helios,2\nMejiro Palmer,2\n")

        db = MockDB()
        schema_manager = MockSchemaManager(table_exists=True, compare_result="match")
        loader = CSVLoader(db, schema_manager)

        loader.load_csv(str(csv_file))

        assert db.created_table is False
        assert db.inserted_rows is True
        
class TestStep3_RejectMismatchedSchema:

    def test_return_no_row_insertion_no_table_created_if_schema_mismatches(self, tmp_path):
        csv_file = tmp_path / "horses.csv"
        csv_file.write_text("name,g1_wins\nDaitaku Helios,2\nMejiro Palmer,2\n")

        db = MockDB()
        schema_manager = MockSchemaManager(table_exists=True, compare_result="mismatch")
        loader = CSVLoader(db, schema_manager)

        loader.load_csv(str(csv_file))

        assert db.created_table is False
        assert db.inserted_rows is False