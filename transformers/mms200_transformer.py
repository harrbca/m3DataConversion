from m3.M3Types import (InventoryAccounting, AltUomInUse, MakeBuyCode, LotControlMethod, ReturnableMessage, LotNumberMethod, ReturnableIndicator)
from dancik.dancik_uom import UOMService
from m3.item_number_lookup import ItemNumberLookup

xref_item_number_lookup = ItemNumberLookup()

class MMS200Transformer:
    """
    Base Transformer class that defines methods for generating values in
    the 'MMS200 AddItmBasic' spreadsheet.
    Each method receives a 'row' object (from your pandas DataFrame).
    """

    def __init__(self):
        self.xref_item_number_lookup = xref_item_number_lookup
        self._item = None  # We'll store the "current row" here as item
        self._uom_service = None # We'll store the UOM service here

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

    def get_status(self):
        return 20

    def get_item_number(self):
        item_number = self._item["ITEMNUMBER"].strip()
        return self.xref_item_number_lookup.get_item_number(item_number)

    def get_item_name(self):
        return f"{self._item["INAME"].strip()} {self._item["INAME2"].strip()}"

    def get_item_description(self):
        return f"{self._item["ICOMM1"].strip()}"

    def get_responsible(self):
        return ""

    def get_basic_uom(self):
        if self._item["ICOMPO"] == 'R':
            return "LF"
        else:
            if self._item["IUM2"] is None:
                return self._item["IUNITS"].strip()
            else:
                return f"{self._item["IUM2"].strip()}"

    def get_item_group(self):
        return self._item["IPRCCD"].strip()

    def get_product_line(self):
        return self._item["IMFGR"].strip() + self._item["IPRODL"].strip()

    def get_product_group(self):
        return self._item["IMFGR"].strip()

    def get_alt_uom_in_use(self):
        return AltUomInUse.ITEM_UOM

    def get_make_buy_code(self):
        return MakeBuyCode.PURCHASED

    def get_lot_control_method(self):
        return LotControlMethod.IN_LOT_MASTER

    def get_lot_numbering_method(self):
        return LotNumberMethod.MANUAL_ENTRY

    def get_inventory_account(self):
        return InventoryAccounting.INV_ACCOUNTING

    def get_returnable_indicator(self):
        if self._item["IINVEN"].strip() == 'Y':
            return ReturnableIndicator.RETURNABLE
        return ReturnableIndicator.NOT_RETURNABLE

    def get_returnable_message(self):
        if self._item["IINVEN"].strip() == 'Y':
            return ReturnableMessage.NO_MESSAGES
        return ReturnableMessage.WARNING_WARN

    def get_net_weight(self):
        try:
            return self._uom_service.convert(1, self.get_basic_uom(), "LB")
        except Exception as e:
            print(f"Error: Unable to convert net weight for item number {self._item["ITEMNUMBER"]}: {e}")
            return ""

    def get_business_group(self):
        pass

    def get_item_type(self):
        pass

    def get_item_category(self):
        pass

    def get_configuration_code(self):
        pass

    def get_inventory_accounting(self):
        pass

    def get_gross_weight(self):
        pass

    def get_inspection_code(self):
        pass

    def get_hierarchy_1(self):
        pass

    def get_hierarchy_2(self):
        pass

    def get_hierarchy_3(self):
        pass

    def get_hierarchy_4(self):
        pass

    def get_hierarchy_5(self):
        pass

    def get_search_group_1(self):
        pass

    def get_search_group_2(self):
        pass

    def get_search_group_3(self):
        pass

    def get_search_group_4(self):
        pass

    def get_search_group_5(self):
        pass

    def get_text_identity(self):
        pass

    def get_procurement_group(self):
        pass

    def get_danger_indicator(self):
        pass

    def get_tax_code_customer_address(self):
        pass

    def get_attribute_model(self):
        pass

    def get_attribute_managed(self):
        pass

    def get_template_item(self):
        pass

    def get_attribute_controlled_item(self):
        pass

    def expiration_date_method(self):
        pass

    def get_goods_receiving_method(self):
        pass

    def get_vat_code_purchase(self):
        pass

    def get_vat_code_sales(self):
        pass

    def get_number_of_decimals(self):
        pass

    def get_number_of_price_decimals(self):
        pass

    def get_commission_group(self):
        pass

    def get_extended_item_number(self):
        pass

    def get_suppliers_abc_code(self):
        pass

    def get_supplier_rebate_generating(self):
        pass

    def get_sales_item(self):
        pass

    def get_fixed_or_dynamic_uom(self):
        pass