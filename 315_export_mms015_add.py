from config_reader import ConfigReader
from database import Database
from template_helper import TemplateHelper
from m3.mms015_converter import get_mms015_entries_from_item_data, AltUomEntryType

config = ConfigReader.get_instance()

query_path = config.get('QUERIES', 'mms200_addItmBasic_sql_query_path')
query = None

try:
    with open(query_path, 'r') as file:
        query = file.read()
except Exception as e:
    print(f"Error reading query file: {e}")
    exit()

with Database() as db:
    df = db.fetch_dataframe(query)

template_helper = TemplateHelper("API_MMS015_Add.xlsx")

for row in df.itertuples(index = False):

    entries = get_mms015_entries_from_item_data(row)
    for(entry) in entries:
        data = {
            "ITNO": row.itemNumber.strip(),
            "AUTP": entry.altUomType,
            "ALUN": entry.altUom,
            "COFA": entry.convFactor,
            "DMCF": entry.convForm
        }

        if entry.altUomType == AltUomEntryType.QUANTITY:
            data["DCCD"] = entry.decimalPlaces
            data["UNMU"] = entry.orderMultiple
            data["AUS2"] = 1 if entry.isCustOrdUOM else 0
            data["AUS6"] = 1 if entry.isStatisticsUom else 0
            data["AUSB"] = 1 if entry.isCostUom else 0

        if entry.altUomType == AltUomEntryType.PRICE:
            data["AUS5"] = 1 if entry.isPurchasePriceUOM else 0
            data["AUS9"] = 1 if entry.isSalesPriceUOM else 0

        template_helper.add_row(data)

template_helper.save('mms215_add_output_path')
