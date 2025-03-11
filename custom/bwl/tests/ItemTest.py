from database import Database

QUERY = "SELECT * FROM ITEMS where itemNumber = ?"

def _fetch_item_data(item_number):
    with Database() as db:
        result = db.fetch_dataframe(QUERY, (item_number,))
        return result.itertuples(index=False).__next__() if not result.empty else None


if __name__ == "__main__":
    item = _fetch_item_data("CASIMP10")

    print(f"Item Number: {item.ITEMNUMBER}")
    print(f"Lot#: {item['ILOT#']}")