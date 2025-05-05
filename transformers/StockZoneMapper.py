import pandas as pd

class StockZoneMapper:
    def __init__(self, excel_path):
        df = pd.read_excel(excel_path)
        self._map = {
            (str(row["WAREHOUSE"]).strip(), str(row["AREA CODE"]).strip()): str(row["STOCK ZONE"]).strip()
            for _, row in df.iterrows()
            if pd.notna(row["STOCK ZONE"])
        }

    def get_zone(self, warehouse, area):
        return self._map.get((warehouse.strip(), area.strip()), "PA")