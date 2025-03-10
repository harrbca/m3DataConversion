from config_reader import ConfigReader
from database import Database
import pandas as pd

from path_manager import PathManager

config = ConfigReader.get_instance()
path_manager = PathManager()


def load_to_table(table_name, df):
    print(f"Saving data to {table_name} table")
    with Database() as db:
        df.to_sql(table_name, db.conn, if_exists="replace", index=False)

def load_from_excel(excel_path):
    print(f"Loading data from {excel_path}")
    return pd.read_excel(excel_path)

def main():
    response = input("⚠️ This will overwrite the database. Do you want to continue? y/n: ")
    if response.lower() != "y":
        print("Exiting...")
        return

    wm0002f_excel_path = path_manager.get_path("PATHS", "whse_wm0002f_path")
    wm0002f_df = load_from_excel(wm0002f_excel_path)
    load_to_table("wm0002f", wm0002f_df)

    wm0003f_excel_path = path_manager.get_path("PATHS", "whse_wm0003f_path")
    wm0003f_df = load_from_excel(wm0003f_excel_path)
    load_to_table("wm0003f", wm0003f_df)

    wm0005f_excel_path = path_manager.get_path("PATHS", "whse_wm0005f_path")
    wm0005f_df = load_from_excel(wm0005f_excel_path)
    load_to_table("wm0005f", wm0005f_df)

    wm0006f_excel_path = path_manager.get_path("PATHS", "whse_wm0006f_path")
    wm0006f_df = load_from_excel(wm0006f_excel_path)
    load_to_table("wm0006f", wm0006f_df)

if __name__ == "__main__":
    main()