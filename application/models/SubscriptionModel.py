import uuid
from typing import Tuple
from pydantic import BaseModel, Field
from decimal import Decimal
from utils.generic_models.enums import PeriodEnum


class SubscriptionModel(BaseModel):
    order_id: str = Field(default_factory=lambda: str(uuid.uuid4()))  
    token: str = None 
    subscription_id: str = None  
    account_id: str = None
    users_user_id: str = None
    fcm_registration_id: str = None
    fcm_type: str = None
    subscription_id: int = None
    auto_renew: bool = True
    price_compare: Decimal = None
    email: str = None
    upd_from: str = None
    device_id: str = None
    geo_loc: Tuple[float, float] = None
    period: PeriodEnum = None
