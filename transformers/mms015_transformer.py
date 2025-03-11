from typing import List

from dancik.dancik_uom import UOMService
from m3.M3Types import ConversionForm, AltUomEntryType
from m3.item_number_lookup import ItemNumberLookup
import logging


decimal_dict = {
    "SF": 3,
    "RL": 3,
    "CT": 0,
    "PA": 0,
    "SY": 3,
    "PC": 0,
    "EA": 0,
    "PL": 0,
    "LF": 3
}

class MMS015Transformer:

    def __init__(self):
        self.xref_item_number_lookup = ItemNumberLookup()
        self._item = None
        self._uom_service = None

    def transform(self, row) -> List[dict]:
        self._item = row
        self._uom_service = UOMService(self._item["ITEMNUMBER"].strip(), 6)
        entries = []

        # calculate the basic uom
        basic_uom = self.get_basic_uom()

        statistics_uom = self.get_statistics_uom()
        sales_uom = self.get_sales_uom()
        cost_uom = self.get_cost_uom()
        uom_list = self.get_all_uoms()

        # remove LB from the list if its present, and also remove the basic uom

        # wrap this in a try catch block. I found bad data in our packaging where have set
        # a pick uom on an item, but did not include that in the packaging file. 🤦

        try:
            uom_list.remove("LB")
            uom_list.remove(basic_uom)
        except ValueError:
            logging.error(f"🥴 UOM List does not contain uom: {basic_uom} or LB for item {self._item.ITEMNUMBER.strip()}")
            return []

        # and if this is a rolled good, remove the IN conversion ( and probably the SF conversion as well )
        if self._item["ICOMPO"] == 'R':
            uom_list.remove("IN")
            uom_list.remove("SF")

        # is there a no break policy set on the item?
        is_no_break = self.get_is_no_break()

        # loop through the uom list and calculate the conversion details
        for uom in uom_list:
            is_sales_uom = sales_uom == uom
            is_cost_uom = cost_uom == uom
            is_statistics_uom = statistics_uom == uom
            is_purchase_uom = self.get_purchase_uom() == uom

            conversion_factor, conversion_form = self._calculate_conversion_details(basic_uom, uom)

            # if the no break policy is not set, then order_multiple can be 0,
            # there is definitely some discussion needed here about the implication of this

            order_multiple = self.calculate_order_multiple(is_no_break, conversion_factor)

            # lookup decimal_places by UOM ( default to 0 if no UOM found )
            decimal_places = decimal_dict.get(uom, 0)

            data = {
                "ITNO": self.get_item_number(),
                "AUTP": AltUomEntryType.QUANTITY.value,
                "ALUN": uom,
                "DCCD": decimal_places,
                "COFA": conversion_factor,
                "DMCF": conversion_form,
                "PCOF": 1,
                "AUS1": 1 if is_purchase_uom else 0,
                "AUS2": 1 if sales_uom == uom else 0,
                "AUS6": 1 if is_statistics_uom else 0,
                "UNMU": order_multiple,
                "AUSB": 1 if is_cost_uom else 0
            }

            entries.append(data)

            if uom == sales_uom:
                data = {
                    "ITNO": self.get_item_number(),
                    "AUTP": AltUomEntryType.PRICE.value,
                    "ALUN": uom,
                    "DCCD": decimal_places,
                    "COFA": conversion_factor,
                    "DMCF": conversion_form,
                    "AUS5": 1 if is_purchase_uom else 0,
                    "AUS9": 1 if is_sales_uom else 0
                }
                entries.append(data)


        # remove any entries that have a ALUN of CO ( skip container converstions )
        entries = [entry for entry in entries if entry["ALUN"] != "CO"]
        # sort the entries byu AUTP
        entries.sort(key=lambda x: x["AUTP"])
        return entries


    def _calculate_conversion_details(self, basic_uom, uom):
        # calculate the conversion factor from the basic uom to the current uom
        # and determinate if multiplication or division is needed
        # this is a preference for whole numbers in the conversion factor
        conversion_factor = self._uom_service.convert(1, basic_uom, uom)
        conversion_form = ""
        if conversion_factor > 1:  # if the conversion factor is greater than 1, then it is a division operation
            conversion_form = ConversionForm.DIVISION
        else:  # otherwise reverse the flow of the conversion and multiply
            conversion_factor = self._uom_service.convert(1, uom, basic_uom)
            conversion_form = ConversionForm.MULTIPLICATION

        return conversion_factor, conversion_form

    def get_statistics_uom(self):
        if self.get_basic_uom() == "CT":
            return "SF"
        return self._item["IUNITS"].strip()

    def get_purchase_uom(self):
        if self.get_basic_uom() == "CT":
            return "SF"
        return self._item["IUNITC"].strip

    def get_sales_uom(self):
        if self.get_basic_uom() == "CT":
            return "SF"
        return self._item["IUNITS"].strip()

    def get_cost_uom(self):
        if self.get_basic_uom() == "CT":
            return "SF"
        return self._item["IUNITC"].strip()

    def get_all_uoms(self):
        return self._uom_service.get_uom_list()

    def get_is_no_break(self):
        return self._item["IPOL1"].strip() == "NB" or self._item["IPOL2"].strip() == "NB" or self._item["IPOL3"].strip() == "NB"

    def calculate_order_multiple(self, is_no_break, conversion_factor):
        if is_no_break:
            return conversion_factor
        else:
            return 0

    def get_item_number(self):
        item_number = self._item["ITEMNUMBER"].strip()
        return self.xref_item_number_lookup.get_item_number(item_number)

    def get_basic_uom(self):
        if self._item["ICOMPO"] == 'R':
            return "LF"
        else:
            if self._item["IUM2"] is None:
                return self._item["IUNITS"].strip()
            else:
                return f"{self._item["IUM2"].strip()}"

