from transformers.mms200_transformer import MMS200Transformer
from dancik.dancik_uom import UOMService

class MMS200UpdItmBasicTransformer(MMS200Transformer):
    def transform(self, row):
        if not row:
            return None
        self._item = row

        self._uom_service = UOMService(row["ITEMNUMBER"].strip())
        basic_uom = self.get_basic_uom()

        data = {
            "STAT": self.get_status(),
            "ITNO": self.get_item_number(),
            "ITDS": self.get_item_name(),
            "FUDS": self.get_item_description(),
            "RESP": self.get_responsible(),
            "UNMS": basic_uom,
            "ITGR": self.get_item_group(),
            "ITCL": self.get_product_group(),
            "BUAR": self.get_business_group(),
            "ITTY": self.get_item_type(),
            "TPCD": self.get_item_category(),
            "MABU": self.get_make_buy_code(),
            "CHCD": self.get_configuration_code(),
            "STCD": self.get_inventory_accounting(),
            "BACD": self.get_lot_numbering_method(),

            "NEWE": self.get_net_weight(),
            "GRWE": self.get_gross_weight(),

            "QACD": self.get_inspection_code(),

            "HIE1": self.get_hierarchy_1(),
            "HIE2": self.get_hierarchy_2(),
            "HIE3": self.get_hierarchy_3(),
            "HIE4": self.get_hierarchy_4(),
            "HIE5": self.get_hierarchy_5(),
            "GRP1": self.get_search_group_1(),
            "GRP2": self.get_search_group_2(),
            "GRP3": self.get_search_group_3(),
            "GRP4": self.get_search_group_4(),
            "GRP5": self.get_search_group_5(),

            "TXID": self.get_text_identity(),

            "PRGP": self.get_procurement_group(),
            "INDI": self.get_lot_control_method(),

            "ALUC": self.get_alt_uom_in_use(),
            "HAZI": self.get_danger_indicator(),
            "TAXC": self.get_tax_code_customer_address(),
            "ATMO": self.get_attribute_model(),
            "ATMN": self.get_attribute_managed(),
            "TPLI": self.get_template_item(),
            "IACP": self.get_attribute_controlled_item(),

            "EXPD": self.expiration_date_method(),
            "GRMT": self.get_goods_receiving_method(),

            "VTCP": self.get_vat_code_purchase(),
            "VTCS": self.get_vat_code_sales(),
            "DCCD": self.get_number_of_decimals(),
            "PDCC": self.get_number_of_price_decimals(),
            "PRVG": self.get_commission_group(),

            "ITNE": self.get_extended_item_number(),
            "RNRI": self.get_returnable_indicator(),
            "SAFC": self.get_suppliers_abc_code(),
            "RMSG": self.get_returnable_message(),
            "PDLN": self.get_product_line(),
            "SRGR": self.get_supplier_rebate_generating(),
            "SALE": self.get_sales_item(),
            "SPUC": self.get_fixed_or_dynamic_uom()
        }

        return data

    def get_item_type(self):
        return self._item["ItemType"].strip()

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

    def get_hierarchy_1(self):
        if self._item["H1"] is None:
            return ""
        return self._item["H1"].strip()

    def get_hierarchy_2(self):
        if self._item["H2"] is None:
            return ""
        return self.get_hierarchy_1() + self._item["H2"].strip()

    def get_hierarchy_3(self):
        if self._item["H3"] is None:
            return ""
        return self.get_hierarchy_2()+self._item["H3"].strip()

    def get_hierarchy_4(self):
        if self._item["H4"] is None:
            return ""
        return self.get_hierarchy_3()+self._item["H4"].strip()