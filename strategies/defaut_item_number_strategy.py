from strategies.base_item_number_strategy import ItemNumberStrategy

class DefaultItemNumberStrategy(ItemNumberStrategy):
    def get_item_number(self, item: dict) -> str:
        return item["ITEMNUMBER"].strip()
