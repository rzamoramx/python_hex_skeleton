
from enum import Enum


class PurchaseStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"


class StoreId(str, Enum):
    GOOGLE = "GOOGLE"
    APPLE = "APPLE"
    HUAWEI = "HUAWEI"
