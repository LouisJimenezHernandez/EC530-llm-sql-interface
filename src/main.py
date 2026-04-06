import os

from src.db.database import Database
from src.schema.schema_manager import SchemaManager
from src.query.sql_validator import SQLValidator
from src.llm.llm_adapter import LLMAdapter
from src.query.query_service import QueryService
from src.data_loader.csv_loader import CSVLoader
from src.cli.cli_interface import CLIInterface


def main():
    db_path = os.path.join("database", "app.db")

    os.makedirs("database", exist_ok=True)

    db = Database(db_path)
    db.connect()

    schema_manager = SchemaManager(db)
    validator = SQLValidator(schema_manager)
    llm_adapter = LLMAdapter()
    query_service = QueryService(db, validator, llm_adapter, schema_manager)
    csv_loader = CSVLoader(db, schema_manager)
    cli = CLIInterface(query_service, csv_loader, schema_manager)

    try:
        cli.run()
    finally:
        db.close()


if __name__ == "__main__":
    main()