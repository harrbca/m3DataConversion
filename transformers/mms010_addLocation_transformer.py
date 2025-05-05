from transformers.StockZoneMapper import StockZoneMapper


class MMS010AddLocationTransformer:

    def __init__(self):
        self._location = None
        self._stock_zone_mapper = StockZoneMapper(
            excel_path="c:\\infor_migration\\spreadsheets\\STOCK_LOCATION.xlsx"
        )

    def transform(self, row):
        if not row:
            return None

        self._location = row
        entries = []

        data = {
            "WHLO": self.get_warehouse(),
            "WHSL": self.get_location(),
            "SLDS": self.get_location(),
            "RESP": "KFEHR",
            "SLTP": self.get_stock_zone(),
            "SLDV": self.get_multi_storage_location(),
            "ALOC": self.get_allocatable(),
            "DEST": self.get_status_proposal(),
            "AUDE": self.get_automatic_deletion(),
            "PISE": self.get_warehouse_equipment(),
            "ABFC": self.get_abc_class_frequency(),
            "WHLT": self.get_location_type(),
        }
        entries.append(data)

        return entries

    def get_warehouse(self):
        return self._location["W6WARE"].strip()

    def get_location(self):
        return self._location["W6LOCID"].strip()

    def get_stock_zone(self):
        return self._stock_zone_mapper.get_zone(
            self.get_warehouse(), self._location["W6AREA"].strip()
        )

    def get_multi_storage_location(self):
        return 1

    def get_allocatable(self):
        return 1

    def get_status_proposal(self):
        return 2

    def get_automatic_deletion(self):
        return 1

    def get_automatic_deletion_delay(self):
        pass

    def get_warehouse_equipment(self):
        return "Z0"

    def get_abc_class_frequency(self):
        return "A"

    def get_location_type(self):
        return "P0"

    def get_transaction_statistics(self):
        pass
