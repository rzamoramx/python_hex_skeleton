
from typing import Tuple
from pydantic import BaseModel
from decimal import Decimal
from utils.generic_models.enums import PeriodEnum


class Purchase(BaseModel):
    id: str
    subscription_id: int
    accounts_account_id: str = None
    ia_account_id: str
    price: Decimal
    period: PeriodEnum
    email: str
    device_id: str
    upd_from: str
    geo_loc: Tuple[float, float]

