import concurrent.futures
from database import Database
from template_helper import TemplateHelper
from plugin_manager import load_transformer
from config_reader import ConfigReader
from tqdm import tqdm  # For nice progress bar
import logging
from datetime import datetime

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


def transform_row(transformer, row):
    return transformer.transform(row)

def main():
    config = ConfigReader.get_instance()
    template_helper = TemplateHelper("API_MMS015MI_Add.xlsx")
    query_path = config.get('QUERIES', 'mms200_addItmBasic_sql_query_path')
    transformer_name = config.get("TRANSFORMER", "mms015_transformer")

    # load the SQL query
    with open(query_path, 'r') as file:
        query = file.read()

    # fetch data from DB
    with Database() as db:
        df = db.fetch_dataframe(query)

    # load the transformer (default or custom)
    transformer = load_transformer("mms015", transformer_name)

    rows = df.to_dict(orient='records')

    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit transform tasks
        futures = {executor.submit(transform_row, transformer, row): row for row in rows}

        # Collect results with a nice progress bar
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Transforming rows"):
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                print(f"Error processing row: {e}")

    # Sequentially write the results to Excel
    print("Writing results to Excel...")

    for data in results:
        for entries in data:
            template_helper.add_row(entries)

    template_helper.save('mms015_add_output_path')

if __name__ == "__main__":
    main()