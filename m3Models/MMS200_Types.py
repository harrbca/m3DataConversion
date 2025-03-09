from enum import IntEnum

class InventoryAccounting(IntEnum):
    NO_INV_ACCOUNTING = 0
    INV_ACCOUNTING = 1
    NO_BUT_PLANNED = 2
    NO_BUT_AS_FUNCTION = 3

class AltUomInUse(IntEnum):
    NOT_USED = 0
    STANDARD_UOM = 1
    ITEM_UOM = 2

class MakeBuyCode(IntEnum):
    MANUFACTURED = 1
    PURCHASED = 2

class LotControlMethod(IntEnum):
    NOT_USED = 0
    LOT_NOT_DEFINED = 1
    LOT_NO_EQ_SER_NO = 2
    IN_LOT_MASTER = 3
    SERIAL_NO_SPEC = 5

class ReturnableMessage(IntEnum):
    NO_MESSAGES = 0
    WARNING_WARN = 1
    WARNING_ERROR = 2
    NO_MSG_WARNING = 3
    NO_MSG_ERROR = 4

class LotNumberMethod(IntEnum):
    MANUAL_ENTRY = 0
    AUTO_YYMM_SEQ = 1
    AUTO_YY_SEQ = 2
    AUTO_SEQ = 3
    MAN_RECV_NO = 4
    AUTO_ORDER_NO =5
    AUTO_YYYMMDD_SEQ = 6
    NUMBERING_RULE = 7
    SIMPLE_MAND = 8
    SIMPLEE_OPTI = 9

class ReturnableIndicator(IntEnum):
    RETURNABLE = 0
    RET_RESTRICTED = 1
    NOT_RET_SUPPLY = 2
    NOT_RETURNABLE = 3


