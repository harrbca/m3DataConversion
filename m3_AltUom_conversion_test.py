from database import Database
from plugin_manager import load_transformer
from config_reader import ConfigReader
from dancik.dancik_uom import UOMService
from tabulate import tabulate

QUERY = "SELECT * FROM ITEMS where itemNumber = ?"

def _fetch_item_data(item_number):
    with Database() as db:
        result = db.fetch_dataframe(QUERY, (item_number,))
        return result.itertuples(index=False).__next__() if not result.empty else None


def format_item_data(item_data):
    if not item_data:
        print("No item data available.")
        return

    headers = ["Item Number", "Pick UOM", "Price UOM", "Cost UOM", "Component"]
    table = [[getattr(item_data, attr, "") for attr in ["itemNumber", "IUM2", "IUNITS", "IUNITC", "ICOMPO"]]]

    print("\nItem Data:")
    print(tabulate(table, headers=headers, tablefmt="grid"))

def format_mms015_data(mms015_data):
    if not mms015_data:
        print("No MMS015 data available.")
        return

    headers = ["ITNO", "AUTP", "ALUN", "DCCD", "COFA", "DMCF", "PCOF", "AUS1", "AUS2", "AUS6", "UNMU", "AUSB", "AUS5", "AUS9"]
    table = [[entry.get(h, "") for h in headers] for entry in mms015_data]

    print("\nMMS015 Data:")
    print(tabulate(table, headers=headers, tablefmt="pipe"))


def format_graph_data(graph_data):
    """Formats and displays graph data in a table format."""
    table = []

    # Extract source and target units with conversion values
    for source_unit, conversions in graph_data.items():
        for target_unit, value in conversions.items():
            table.append([source_unit, target_unit, f"{value:.6f}"])  # Limit to 6 decimal places

    headers = ["From Unit", "To Unit", "Conversion Factor"]
    print("\nUnit Conversion Table:")
    print(tabulate(table, headers=headers, tablefmt="pipe"))


def main():
    config = ConfigReader.get_instance()
    mms015_transformer = load_transformer("mms015", config.get("TRANSFORMER", "mms015_transformer"))
    mms200_transformer = load_transformer("mms200", config.get("TRANSFORMER", "mms200_transformer"))

    while True:
        item_number = input("Enter an item number (or type 'exit' to quit): ").strip()
        if item_number.lower() == "exit":
            break

        item = _fetch_item_data(item_number.upper().strip())
        if item is None:
            print(f"Item {item_number} not found.")
            continue

        uom_service = UOMService(item.ITEMNUMBER.strip())


        mms200_data = mms200_transformer.transform(item)
        mms015_data = mms015_transformer.transform(item)
        format_item_data(item)
        print(f"MMS200 Data: {mms200_data}")
        format_graph_data(uom_service.graph)
        format_mms015_data(mms015_data)




if __name__ == "__main__":
    main()