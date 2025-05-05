

from strategy_loader import load_item_number_strategy


class MMS200UpdItmWhsTransformer:

    def __init__(self):
        self._item = None
        self._item_number_strategy = load_item_number_strategy()
        self._warehouses = ["SAS", "CAL", "EDM", "REG", "VAN", "WIN", "POR", "TUK", "SPO"]

    def transform(self, row):
        entries = []
        self._item = row

        if not row:
            return entries

        for wh in self._warehouses:
            data = {
                "WHLO": wh,
                "ITNO": self.get_item_number(),
                "SUNO": self.get_supplier_number(),
                "STAT": self.get_status()
            }
            entries.append(data)

        return entries


    def get_item_number(self):
        return self._item_number_strategy.get_item_number(self._item)

    def get_supplier_number(self):
        return self._item["ISUPP#"].strip()

    def get_status(self):
        return 20


