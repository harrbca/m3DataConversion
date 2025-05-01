from transformers.mms200_transformer import MMS200Transformer

class MMS200AddItmViaItmTypTransformer(MMS200Transformer):
    def transform(self, row):
        if not row:
            return None
        self._item = row

        data = {
            "ITNO": self.get_item_number,
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

    def get_item_number(self):
        item_number = self._item["ITEMNUMBER"].strip()
        if len(item_number) < 3:
            return item_number  # Return as is if item_number is too short

        mfgr_prefix = item_number[:3]  # Get the first three characters
        item_suffix = item_number[3:]  # The rest of the item number

        # Define special cases for manufacturer prefixes
        special_prefixes = {"CAS": "CA", "CAR": "CR", "CAP": "CP"}

        # Determine new prefix
        new_prefix = special_prefixes.get(mfgr_prefix, mfgr_prefix[:2])

        # Construct the new item number
        return new_prefix + item_suffix