from strategies.base_item_number_strategy import ItemNumberStrategy

class BWLGetItemNumberStrategy(ItemNumberStrategy):
    def get_item_number(self, item: dict) -> str:
        item_number = item["ITEMNUMBER"].strip()
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