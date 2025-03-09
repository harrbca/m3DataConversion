import logging

logger = logging.getLogger(__name__)

class CRS025Transformer:
    def __init__(self):
        self._item = None

    def transform(self, row):
        if not row:
            return None

        self._item = row

        data = {
            "ITGR": self.get_item_group(),
            "TX40": self.get_description(),
            "TX15": self.get_name(),
            "SECU": self.get_seasonal_curve(),
            "TECU": self.get_trend_curve(),
            "TCWP": self.get_tolerance_catch_weight_percent(),
            "TCWQ": self.get_tolerance_catch_weight()
        }

        return data


    def get_item_group(self):
        return self._item.priceClass.strip()

    def get_description(self):
        return self._item.description.strip()

    def get_name(self):
        return ""

    def get_seasonal_curve(self):
        return ""

    def get_trend_curve(self):
        return ""

    def get_tolerance_catch_weight_percent(self):
        return ""

    def get_tolerance_catch_weight(self):
        return ""