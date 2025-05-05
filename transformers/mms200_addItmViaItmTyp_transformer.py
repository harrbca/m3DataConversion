from transformers.mms200_transformer import MMS200Transformer
from strategy_loader import load_item_number_strategy

class MMS200AddItmViaItmTypTransformer(MMS200Transformer):

    def __init__(self):
        super().__init__()


    def transform(self, row):
        if not row:
            return None
        self._item = row

        data = {
            "ITNO": self.get_item_number(),
            "ITTY": self.get_item_type(),
            "ITDS": self.get_item_name(),
            "FUDS": self.get_item_description(),
            "ITNE": self.get_extended_item_number()
        }

        return data

    def get_item_type(self):
        return self._item["ItemType"].strip()

    def get_extended_item_number(self):
        return self._item["ITEMNUMBER"]

