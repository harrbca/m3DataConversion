from m3.M3Types import SalesItem
from transformers.mms200_transformer import MMS200Transformer

class BWLMMS200Transformer(MMS200Transformer):

    def get_item_number_DONOTUSE(self):
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

    def get_responsible(self):
        return ""

    def get_commission_group(self):
        return "Y1"

    def get_inventory_accounting(self):
        return "1"

    def get_number_of_price_decimals(self):
        return 3

    def get_sales_item(self):
        return SalesItem.YES

    def get_attribute_managed(self):
        return 2

    def get_fixed_or_dynamic_uom(self):
        return 2