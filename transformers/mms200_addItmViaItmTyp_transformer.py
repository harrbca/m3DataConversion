from transformers.mms200_transformer import MMS200Transformer

class MMS200AddItmViaItmTypTransformer(MMS200Transformer):
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
        return "VIN"
