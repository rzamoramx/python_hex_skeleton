
from pydantic import BaseModel, validator, root_validator
from typing import List, Dict
from decimal import Decimal
from enum import Enum


class PremiumProductsEnum(str, Enum):
    def __new__(cls, code: str, description: str = ""):
        obj = str.__new__(cls, code)
        obj._value_ = code

        obj.hex_code = description
        obj.description = description
        return obj

    EQ_MARKET = ('EQ_MARKET', 'Ordenes de mercado')
    EQ_RECURRENT = ('EQ_RECURRENT', 'Ordenes recurrentes')

    class Config:
        use_enum_values = False


class CatalogPremium(BaseModel):
    premium_id: int  
    name: str = None
    description: str = None
    fx_segment: int = None
    repos_segment: int = None  # 1=2%, 2=4%, 3=6% interest
    eq_segment: int = None
    eq_cashback_segment: int = None
    support_type: str = None
    eq_data_type: str = None
    sell_eq_bp_disponibility: str = None
    promotions_level: int = None
    advisory_level: int = None
    eq_level: int = None
    crypto_level: int = None
    functionalities: List[PremiumProductsEnum] = None
    created_at: int = None
    last_modified: int = None
    color: str = None
    active: bool = None
    default: bool = None
    code: str = None
    update_history: List[Dict] = []
    eq_company_count: int = None
    crypto_company_count: int = None
    repos_rates: int = None
    fx_rates: int = None
    eq_rates: int = None
    price_yearly: Decimal = None
    price_monthly: Decimal = None

    @validator('default')
    def default_value(cls, v):
        return v

    @validator('active')
    def active_value(cls, v):
        return v

    @root_validator
    def check_default_active_relationship(cls, values):
        if values.get('default') is not None and values.get('default') and \
                values.get('active') is not None and not values.get('active'):
            raise ValueError('if default is true, active must be true')
        return values

    def to_dict(self):
        # exclude fields that is None, for example in updates is required to prevent override with None
        data = self.dict(exclude_none=True)  # exclude_unset=True)
        return data
