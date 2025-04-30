import logging

logger = logging.getLogger(__name__)

class CRS099Transformer:
    def __init__(self):
        self._item = None

    def transform(self, row):
        if not row:
            return None

        self._item = row

        data = {
            "PDLN": self.get_product_line(),
            "TX40": self.get_description(),
            "TX15": self.get_name()
        }

        return data


    def get_product_line(self):
        return self._item.prodLine

    def get_description(self):
        return self._item.lname.strip()

    def get_name(self):
        return self._item.lname[:15].strip()  # Limit to 15 characters