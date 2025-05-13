import concurrent.futures
from database import Database
from template_helper import TemplateHelper
from plugin_manager import load_transformer
from config_reader import ConfigReader
from tqdm import tqdm  # For nice progress bar
import logging
from datetime import datetime
import re

# Set up logging to file
log_filename = f"mms015_transform_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, mode='w'),
        #logging.StreamHandler()  # Optional: keep this if you also want console output
    ]
)


def transform_row(transformer_name, row):
    transformer = load_transformer("mms015", transformer_name)  # Create a fresh instance per thread
    return transformer.transform(row)

def main():
    config = ConfigReader.get_instance()
    template_helper = TemplateHelper("API_MMS015MI_Add.xlsx")
    query_path = config.get('QUERIES', 'mms200_addItmBasic_sql_query_path')
    transformer_name = config.get("TRANSFORMER", "mms015_transformer")
    BAD_CHAR_RE = re.compile(r'[^0-9A-Za-z-]')

    # load the SQL query
    with open(query_path, 'r') as file:
        query = file.read()

    # fetch data from DB
    with Database() as db:
        df = db.fetch_dataframe(query)

    rows = [
        row
        for row in df.to_dict(orient="records")
        if row.get("ITEMNUMBER") is not None  # keep non‑null
           and not BAD_CHAR_RE.search(str(row["ITEMNUMBER"]).rstrip())  # screen out bad chars
    ]

    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(transform_row, transformer_name, row): row
            for row in rows
        }

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Transforming rows"):
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                logging.error(f"Error processing row: {e}")

    # Sequential write to Excel
    all_entries = []
    for data in results:
        if isinstance(data, list):
            all_entries.extend(data)
        else:
            logging.error(f"Unexpected result type in results: {type(data)} — {data}")

    template_helper.add_all_rows(all_entries)
    template_helper.save("mms015_add_output_path")

if __name__ == "__main__":
    main()