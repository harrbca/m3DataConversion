import concurrent.futures
from database import Database
from template_helper import TemplateHelper
from plugin_manager import load_transformer
from config_reader import ConfigReader
from tqdm import tqdm
import logging
import re

def transform_row(transformer_name, row):
    if row["ITEMNUMBER"] is None:
        return None
    transformer = load_transformer("mms200_updItmBasic", transformer_name)
    return transformer.transform(row)

def main():
    config = ConfigReader.get_instance()
    template_helper = TemplateHelper("API_MMS200MI_UpdItmBasic.xlsx")
    query_path = config.get('QUERIES', 'mms200_addItmBasic_sql_query_path')
    transformer_name = config.get("TRANSFORMER", "mms200_updItmBasic_transformer")
    BAD_CHAR_RE = re.compile(r'[^0-9A-Za-z-]')

    # Load the SQL query
    with open(query_path, 'r') as file:
        query = file.read()

    # Fetch data from DB
    with Database() as db:
        df = db.fetch_dataframe(query)

    rows = [
        row
        for row in df.to_dict(orient="records")
        if row.get("ITEMNUMBER") is not None  # keep non‑null
           and not BAD_CHAR_RE.search(str(row["ITEMNUMBER"]).rstrip())  # screen out bad chars
    ]


    all_entries = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(transform_row, transformer_name, row): row
            for row in rows if row["ITEMNUMBER"] is not None
        }

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Transforming rows"):
            try:
                result = future.result()
                if result:
                    all_entries.extend(result if isinstance(result, list) else [result])
            except Exception as e:
                logging.error(f"Error processing row: {e}")

    # Write all at once
    template_helper.add_all_rows(all_entries)
    template_helper.save("mms200_updItmBasic_output_path")

if __name__ == "__main__":
    main()