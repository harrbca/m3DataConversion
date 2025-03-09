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

        self._uom_service = UOMService(row.itemNumber.strip())
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
            "PDLN": self.get_product_line(),
            "ALUC": self.get_alt_uom_in_use(),
            "MABU": self.get_make_buy_code(),
            "NEWE": self.get_net_weight()
        }

        return data

    def get_status(self):
        return 20

    def get_item_number(self):
        item_number = self._item.itemNumber.strip()
        return self.xref_item_number_lookup.get_item_number(item_number)

    def get_item_name(self):
        return f"{self._item.INAME.strip()} {self._item.INAME2.strip()}"

    def get_item_description(self):
        return f"{self._item.ICOMM1.strip()}"

    def get_responsible(self):
        return ""

    def get_basic_uom(self):
        if self._item.ICOMPO == 'R':
            return "LF"
        else:
            if self._item.IUM2 is None:
                return self._item.IUNITS.strip()
            else:
                return f"{self._item.IUM2.strip()}"

    def get_item_group(self):
        return self._item.IPRCCD.strip()

    def get_product_line(self):
        return self._item.IMFGR.strip() + self._item.IPRODL.strip()

    def get_product_group(self):
        return self._item.IMFGR.strip()

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
        if self._item.IINV.strip() == 'Y':
            return ReturnableIndicator.RETURNABLE
        return ReturnableIndicator.NOT_RETURNABLE

    def get_returnable_message(self):
        if self._item.IINV.strip() == 'Y':
            return ReturnableMessage.NO_MESSAGES
        return ReturnableMessage.WARNING_WARN

    def get_net_weight(self):
        try:
            return self._uom_service.convert(1, self.get_basic_uom(), "LB")
        except Exception as e:
            print(f"Error: Unable to convert net weight for item number {self._item.itemNumber}: {e}")
            return ""