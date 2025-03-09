from database import Database
from dancik.dancik_uom import UOMService
from m3.M3Types import ConversionForm, AltUomEntryType
from m3.mms015_entry import MMS015_Entry
import logging
import pandas as pd



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

QUERY = "SELECT * FROM ITEMS where itemNumber = ?"

def _fetch_item_data(item_number):
    with Database() as db:
        return db.fetch_dataframe(QUERY, (item_number,))

def _calculate_conversion_details(uom_service, basic_uom, uom):
    # calculate the conversion factor from the basic uom to the current uom
    # and determinate if multiplication or division is needed
    # this is a preference for whole numbers in the conversion factor
    conversion_factor = uom_service.convert(1, basic_uom, uom)
    conversion_form = ""
    if conversion_factor > 1:  # if the conversion factor is greater than 1, then it is a division operation
        conversion_form = ConversionForm.DIVISION
    else:  # otherwise reverse the flow of the conversion and multiply
        conversion_factor = uom_service.convert(1, uom, basic_uom)
        conversion_form = ConversionForm.MULTIPLICATION

    return conversion_factor, conversion_form

def _process_item(item) -> list[MMS015_Entry]:
    entries = []
    uom_service = UOMService(item.itemNumber.strip(), 6)

    # if this is a ROLL item and the pick uom is SY, then the basic_uom should be LF
    if item.ICOMPO == 'R' and item.IUM2 == 'SY':
        basic_uom  = "LF"
    else:
        basic_uom = item.IUM2.strip()

    # what should the m3 statistics UOM be?
    statistics_uom = item.IUNITS.strip()

    # what should the sales uom be?
    sales_uom = item.IUNITS.strip()

     # what should the m3 cost UOM be?
    cost_uom = item.IUNITC.strip()

    # get all the UOM's for the item
    uomList = uom_service.get_uom_list()
    # remove LB from the list if its present, and also remove the basic uom

    # wrap this in a try catch block. I found bad data in our packaging where have set
    # a pick uom on an item, but did not include that in the packaging file. 🤦

    try:
        uomList.remove("LB")
        uomList.remove(basic_uom)
    except ValueError:
        logging.error(f"🥴 UOM List does not contain uom: {basic_uom} or LB for item {item.itemNumber.strip()}")
        return []

    # and if this is a rolled good, remove the IN conversion ( and probably the SF conversion as well )
    if item.ICOMPO == 'R':
        uomList.remove("IN")
        uomList.remove("SF")

     # is there a no break policy set on the item?
    isNoBreak = item.IPOL1.strip() == "NB" or item.IPOL2.strip() == "NB" or item.IPOL3.strip() == "NB"

    for uom in uomList:
        isSalesUOM = sales_uom == uom
        isCostUOM = cost_uom == uom
        isStatisticsUOM = statistics_uom == uom
        isPurchaseUOM = item.IUNITC == uom

        conversion_factor, conversion_form = _calculate_conversion_details(uom_service, basic_uom, uom)

        # if the no break policy is not set, then order_multiple can be 0,
        # there is definitely some discussion needed here about the implication of this

        if isNoBreak:
            order_multiple = conversion_factor
        else:
            order_multiple = 0

        decimal_places = decimal_dict.get(uom, 0)

        # create and emit the Alt Qty UOM
        entries.append(MMS015_Entry(
            itemNumber=item.itemNumber.strip(),
            altUomType=AltUomEntryType.QUANTITY,
            altUom=uom,
            decimalPlaces=decimal_places,
            convFactor=conversion_factor,
            convForm=conversion_form,
            orderMultiple=order_multiple,
            isPurchaseUOM=isPurchaseUOM,
            isStatisticsUom=isStatisticsUOM,
            isCostUom=isCostUOM,
            isCustOrdUOM=isSalesUOM
        ))

        # create and emit the Alt Price UOM
        if uom == item.IUNITS.strip():
            entries.append(MMS015_Entry(
                itemNumber=item.itemNumber.strip(),
                altUomType=AltUomEntryType.PRICE,
                altUom=uom,
                decimalPlaces=decimal_places,
                convFactor=conversion_factor,
                convForm=conversion_form,
                isSalesPriceUOM=True,
                isPurchasePriceUOM=True
            ))

    # sort the entries by alt type
    sorted_entries = sorted(entries, key=lambda x: x.altUomType)
    return sorted_entries

def get_mms015_entries(item_number: str) -> list[MMS015_Entry]:
    item_data = _fetch_item_data(item_number)
    if item_data.empty:
        return []
    else:
        return _process_item(item_data.iloc[0])

def get_mms015_entries_from_item_data(item_data: pd.DataFrame) -> list[MMS015_Entry]:
    return _process_item(item_data)