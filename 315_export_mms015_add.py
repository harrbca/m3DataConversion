from database import Database
from template_helper import TemplateHelper
from plugin_manager import load_transformer
from config_reader import ConfigReader


def main():
    config = ConfigReader.get_instance()
    template_helper = TemplateHelper("API_MMS015MI_Add.xlsx")
    query_path = config.get('QUERIES', 'mms200_addItmBasic_sql_query_path')
    transformer = config.get("TRANSFORMER", "mms015_transformer")

    # load the SQL query
    with open(query_path, 'r') as file:
        query = file.read()

    # fetch data from DB
    with Database() as db:
        df = db.fetch_dataframe(query)

    # load the transformer (default or custom)
    transformer = load_transformer("mms015", transformer)

    for row in df.to_dict(orient='records'):
        data = transformer.transform(row)
        if data:
            for entries in data:
                template_helper.add_row(entries)

    template_helper.save('mms015_add_output_path')

if __name__ == "__main__":
    main()


