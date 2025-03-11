from database import Database
from template_helper import TemplateHelper
from plugin_manager import load_transformer
from config_reader import ConfigReader

def main():
    config = ConfigReader.get_instance()
    template_helper = TemplateHelper("API_MMS200MI_UpdItmBasic.xlsx")
    query_path = config.get('QUERIES', 'mms200_addItmBasic_sql_query_path')
    transformer = config.get("TRANSFORMER", "mms200_updItmBasic_transformer")

    # load the SQL query
    with open(query_path, 'r') as file:
        query = file.read()

    # fetch data from DB
    with Database() as db:
        df = db.fetch_dataframe(query)

    # load the transformer (default or custom)
    transformer = load_transformer("mms200_updItmBasic", transformer)

    for row in df.to_dict(orient='records'):
        data = transformer.transform(row)
        if data:
            template_helper.add_row(data)

    template_helper.save('mms200_updItmBasic_output_path')

if __name__ == "__main__":
    main()