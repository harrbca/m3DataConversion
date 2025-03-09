import path_manager
from config_reader import ConfigReader
from database import Database
import pandas as pd
from path_manager import PathManager


config = ConfigReader.get_instance()
path_manager = PathManager()

query_path = config.get('QUERIES', 'identify_long_item_numbers_sql_query_path')
query = None

try:
    with open(query_path, 'r') as file:
        query = file.read()
except Exception as e:
    print(f"Error reading query file: {e}")
    exit()

with Database() as db:
    df = db.fetch_dataframe(query)

# output to an excel file
df.to_excel(path_manager.get_path("PATHS", "long_item_numbers_path"), index = False)