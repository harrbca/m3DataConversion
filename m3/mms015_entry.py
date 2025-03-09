from dataclasses import dataclass, field
from decimal import Decimal

@dataclass
class MMS015_Entry:
    itemNumber: str
    altUomType: int
    altUom: str
    decimalPlaces: int
    convFactor: Decimal
    convForm: int


    priceAdjustFactor: Decimal = field(default_factory=lambda: Decimal("1.0"))
    orderMultiple:  Decimal = field(default_factory=lambda: Decimal("0"))
    isPurchaseUOM:bool = False
    isCustOrdUOM: bool  = False
    isStatisticsUom: bool = False
    isSalesPriceUOM: bool = False
    isPurchasePriceUOM:bool = False
    isCostUom: bool = False
