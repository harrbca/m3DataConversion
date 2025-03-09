import sqlite3
import pandas as pd
from config_reader import ConfigReader
from path_manager import PathManager
import config_keys

config = ConfigReader.get_instance()
path_manager = PathManager()

#prompt that this will overwrite the database and ask if they want to continue
response = input("⚠️ This will overwrite the database. Do you want to continue? y/n: ")
if response.lower() != "y":
    print("Exiting...")
    exit()


file_path = path_manager.get_path("PATHS", "active_item_path")
print(f"Loading Excel file from {file_path}")
df = pd.read_excel(file_path)
print("Excel file loaded!")

db_path = path_manager.get_path("PATHS", "db_path")
print(f"Saving to database at {db_path}")

conn = sqlite3.connect(db_path)
df.to_sql(config.get("DB", "active_items_table_name"), conn, if_exists="replace", index=False)
print("Done!")
