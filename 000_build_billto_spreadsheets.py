import os
from decimal import Decimal

import pandas as pd
import pyodbc
import pymssql
from config_reader import ConfigReader
import config_keys
from path_manager import PathManager
import re
from database import Database

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
    ILLEGAL_CHARACTERS_RE = re.compile(r"[\x00-\x08\x0b-\x0c\x0e-\x1f]")
    for col in data_frame.columns:
        if data_frame[col].dtype == object:
            for i, val in enumerate(data_frame[col]):
                if isinstance(val, str) and ILLEGAL_CHARACTERS_RE.search(val):
                    print(f"Illegal character found in column '{col}', row {i}: {repr(val)}")

    save_to_excel(excel_path, data_frame)

    # convert any decimal instances to strings.  SQLLITE does not support decimal types
    df = data_frame.applymap(lambda x: str(x) if isinstance(x, Decimal) else x)

    # Load the data into the database
    with Database() as db:
        df.to_sql("billto", db.conn, if_exists="replace", index=False)
        print(f"✅ Data successfully loaded into the database table")


def main():
    query_path = config.get("QUERIES", "billto_sql_query_path")
    excel_path = path_manager.get_path("PATHS", "billto_path")
    do_data_load(query_path, excel_path)
    print("✅ Done!")


if __name__ == "__main__":
    main()
