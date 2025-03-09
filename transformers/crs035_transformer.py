import logging

logger = logging.getLogger(__name__)

class CRS035Transformer:
    def __init__(self):
        self._item = None

    def transform(self, row):
        if not row:
            return None

        self._item = row

        data = {
            "ITCL": self.get_product_group(),
            "TX40": self.get_description(),
            "TX15": self.get_name(),
            "SECU": self.get_seasonal_curve(),
            "CONF": self.get_conf(),

        }

        return data

    def get_product_group(self):
        return self._item.IMFGR.strip()

    def get_description(self):
        return self._item.MNAME.strip()

    def get_name(self):
        return ""

    def get_seasonal_curve(self):
        return ""

    def get_conf(self):
        return ""