from database import Database
from config_reader import ConfigReader

class DancikRollsService:
    def __init__(self):
        self.db = Database()
        self.config = ConfigReader.get_instance()
        query_path = self.config.get("QUERIES", "rolls_sql_query_path")
        with open(query_path) as file:
            self.select_query = file.read()

    def load_rolls(self, item_number):
        query = f"select * from rolls where itemNumber = ? order by 'rware#', 'rloc1'"
        with self.db as db:
            return db.fetch_dataframe(query, (item_number,))



