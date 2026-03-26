class CSVLoader:
    def __init__(self, db, schema_manager):
        """
        db: database interface
        schema_manager: handles schema logic
        """
        pass

    def load_csv(self, file_path: str, table_name: str = None) -> str:
        """
        Loads a CSV file into the database.

        Args:
            file_path: path to CSV file
            table_name: optional override for table name

        Returns:
            Status message (success or error)
        """
        pass