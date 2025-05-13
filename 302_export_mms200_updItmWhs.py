from database import Database
from template_helper import TemplateHelper
from plugin_manager import load_transformer
from config_reader import ConfigReader
import re

def main():
    config = ConfigReader.get_instance()
    template_helper = TemplateHelper("API_MMS200MI_UpdItmWhs.xlsx")
    query_path = config.get('QUERIES', 'mms200_addItmBasic_sql_query_path')
    transformer_name = config.get("TRANSFORMER", "mms200_updItmWhs_transformer")
    BAD_CHAR_RE = re.compile(r'[^0-9A-Za-z-]')

    # load the SQL query
    with open(query_path, 'r') as file:
        query = file.read()

    # fetch data from DB
    with Database() as db:
        df = db.fetch_dataframe(query)

    # load the transformer (default or custom)
    transformer = load_transformer("mms200_updItmWhs", transformer_name)

    all_entries = []

    for row in df.to_dict(orient='records'):
        item_number = row["ITEMNUMBER"]
        #print (row["ITEMNUMBER"])
        if row["ITEMNUMBER"] is None:
            continue

        if BAD_CHAR_RE.search(item_number):
            print(f"{item_number} -> contains disallowed characters, skipping row")
            continue

        data = transformer.transform(row)
        if data:
            all_entries.extend(data)

    template_helper.add_all_rows(all_entries)
    template_helper.save('mms200_updItmWhs_output_path')

if __name__ == "__main__":
    main()