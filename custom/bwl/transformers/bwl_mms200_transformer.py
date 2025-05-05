from m3.M3Types import SalesItem
from transformers.mms200_transformer import MMS200Transformer

class BWLMMS200Transformer(MMS200Transformer):



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