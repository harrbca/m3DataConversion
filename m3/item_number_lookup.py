import os
import logging
import pandas as pd
from config_reader import ConfigReader
from path_manager import PathManager

logger = logging.getLogger(__name__)

class ItemNumberLookup:
    """
    A helper class for looking up M3 item numbers based on Dancik item numbers
    using a pre-defined mapping from an Excel file.

    Attributes:
        map (dict): A dictionary mapping Dancik item numbers to M3 item numbers.
    """
    def __init__(self):
        """
         Initializes the ItemNumberLookup class by loading an Excel file containing
        Dancik-to-M3 item mappings.

        Note:
            If the specified Excel file exists, it is loaded into a dictionary for quick lookups.
            If the file does not exist, the mapping remains empty.
        """
        config = ConfigReader.get_instance()
        path_manager = PathManager()
        item_xref_path = path_manager.get_path("PATHS", "item_xref_path")
        self.map = {}

        # check if there is a item_xref
        # if there is, load it and save to the map
        if item_xref_path is not None and os.path.exists(item_xref_path):

            df = pd.read_excel(item_xref_path)

            # Ensure the required columns exist before creating the mapping
            if 'dancik_item_number' in df.columns and 'm3_item_number' in df.columns:
                self.map = dict(zip(df['dancik_item_number'], df['m3_item_number']))
                logger.info(f"Loaded {len(self.map)} item mappings from {item_xref_path}")
            else:
                logger.warning("Excel file does not contain 'dancik_item_number' and 'm3_item_number' columns.")
                raise ValueError("Excel file must contain 'dancik_item_number' and 'm3_item_number' columns.")


    def get_item_number(self, dancik_item_number):
        """
        Retrieves the corresponding M3 item number for a given Dancik item number.

        Args:
            dancik_item_number (str): The Dancik item number to look up.

        Returns:
            str: The corresponding M3 item number if found; otherwise, returns the input `dancik_item_number`.
        """
        return self.map.get(dancik_item_number, dancik_item_number)