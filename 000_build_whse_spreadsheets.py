import os
import pandas as pd
import pyodbc
import pymssql
from config_reader import ConfigReader
import config_keys
from path_manager import PathManager

# Initialize configuration and path manager
config = ConfigReader.get_instance()
path_manager = PathManager()

db_type = config.get("CONNECTION", "DB_TYPE").lower()  # 'as400' or 'mssql'


def connect_as400():
    """Establish a connection to the AS400 DB2 database."""
    conn_str = (
        f"DRIVER={{iSeries Access ODBC Driver}};"
        f"SYSTEM={config.get_connection('AS400_HOST')};"
        f"UID={config.get_connection('AS400_USERNAME')};"
        f"PWD={config.get_connection('AS400_PASSWORD')};"
        f"naming=1;"
        f"READONLY=1;"
    )
    return pyodbc.connect(conn_str)


def connect_mssql():
    """Establish a connection to the MSSQL database."""
    return pymssql.connect(
        server=config.get_connection('DB_SERVER'),
        user=config.get_connection('DB_USERNAME'),
        password=config.get_connection('DB_PASSWORD'),
        database=config.get_connection('DB_DATABASE')
    )


def fetch_data(select_query):
    """Fetch data from the selected database."""
    conn = None
    try:
        if db_type == 'as400':
            print("Connecting to AS400 DB2...")
            conn = connect_as400()
            print("✅ Connected to AS400 DB2 successfully!")
            cursor = conn.cursor()
            print("Executing SQL query...")
            cursor.execute(select_query)
            columns = [column[0] for column in cursor.description]  # Fetch column names
            data = cursor.fetchall()

            # Ensure each row is a list instead of a tuple
            data = [list(row) for row in data]  # Convert from tuple to list
            cursor.close()
            conn.close()
            return pd.DataFrame(data, columns=columns)
        elif db_type == 'mssql':
            print("Connecting to MSSQL...")
            conn = connect_mssql()
            cursor = conn.cursor(as_dict=True)
            print("Executing SQL query...")
            cursor.execute(select_query)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return pd.DataFrame(data)
        else:
            print("Invalid database type. Please choose 'as400' or 'mssql'.")
            return None



    except Exception as e:
        print(f"❌ Error: {e}")
        return None



def save_to_excel(excel_path, df):
    """Save the extracted data into an Excel file."""
    print(f"Saving data to Excel file at {excel_path}...")
    df.to_excel(excel_path, index=False)
    print("✅ Data successfully saved to Excel!")


def load_query(query_path):
    """Load the SQL query from the specified file."""
    with open(query_path, 'r') as file:
        return file.read()

def do_data_load(query_path, excel_path):
    if os.path.exists(excel_path):
        overwrite = input(f"⚠️ File {excel_path} already exists. Overwrite? (y/n) ")
        if overwrite.lower() != "y":
            print("Skipping.")
            return

    select_query = load_query(query_path)
    data_frame = fetch_data(select_query)
    save_to_excel(excel_path, data_frame)


def main():
    wm0002f_query_path = config.get("QUERIES", "whse_wm0002f_sql_query_path")
    wm0002f_excel_path = path_manager.get_path("PATHS", "whse_wm0002f_path")
    do_data_load(wm0002f_query_path, wm0002f_excel_path)

    wm0003f_query_path = config.get("QUERIES", "whse_wm0003f_sql_query_path")
    wm0003f_excel_path = path_manager.get_path("PATHS", "whse_wm0003f_path")
    do_data_load(wm0003f_query_path, wm0003f_excel_path)

    wm0005f_query_path = config.get("QUERIES", "whse_wm0005f_sql_query_path")
    wm0005f_excel_path = path_manager.get_path("PATHS", "whse_wm0005f_path")
    do_data_load(wm0005f_query_path, wm0005f_excel_path)

    wm0006f_query_path = config.get("QUERIES", "whse_wm0006f_sql_query_path")
    wm0006f_excel_path = path_manager.get_path("PATHS", "whse_wm0006f_path")
    do_data_load(wm0006f_query_path, wm0006f_excel_path)
    print("✅ Done!")


if __name__ == "__main__":
    main()
