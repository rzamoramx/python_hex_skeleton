
import uuid
from typing import List, Dict, Tuple
from pydantic import BaseModel, root_validator, Field
from decimal import Decimal
from domain.enums import (
    StoreId,
    PurchaseStatus
)
from datetime import datetime, timezone
from utils.generic_models.enums import PeriodEnum
from application.models.enums import AttemptEnum


class PurchaseSubscriptionModel(BaseModel):
    order_id: str = Field(default_factory=lambda: str(uuid.uuid4()))  
    store_id: StoreId = None
    subscription_id: str = None
    token: str = None
    account_id: str = None
    users_user_id: str = None
    fcm_registration_id: str = None
    fcm_type: str = None
    subscription_id: int = None
    auto_renew: bool = None
    expires_at: datetime = None
    purchased_at: datetime = None
    status: int = None
    period: PeriodEnum = None
    purchase_status: PurchaseStatus = None
    purchase_reject_reason: str = None
    purchase_price: Decimal = None
    attempt: AttemptEnum = AttemptEnum.FINAL
    renewing: bool = False
    email: str = None
    device_id: str = None
    version: int = 1
    update_history: List[Dict] = []
    geo_loc: Tuple[float, float] = None

    @root_validator(pre=True)
    def parse_dates(cls, values):
        for field in ['expires_at', 'purchased_at']:
            value = values.get(field)
            if isinstance(value, datetime):
                values[field] = value.astimezone(timezone.utc)
        return values

    def to_dict(self) -> dict:
        data = self.dict(exclude_none=True)

        def convert_decimal(value):
            if isinstance(value, Decimal):
                return str(value)
            return value

        def convert_datetime(value):
            if isinstance(value, datetime):
                return value.isoformat()
            return value

        def convert_nested(item):
            if not hasattr(item, 'items'):
                return item

            for key, value in item.items():
                if isinstance(value, dict):
                    item[key] = convert_nested(value)
                elif isinstance(value, list):
                    item[key] = [convert_nested(i) for i in value]
                else:
                    item[key] = convert_datetime(convert_decimal(value))
            return item

        data = convert_nested(data)
        return data
