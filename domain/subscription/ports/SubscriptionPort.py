
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Tuple
from domain.subscription.models.PurchaseSubscriptionModel import PurchaseSubscriptionModel
from application.models.SubscriptionModel import SubscriptionModel
from utils.generic_models.enums import PeriodEnum


class SubscriptionPort(ABC):
    @abstractmethod
    async def process_purchase(self, data: SubscriptionModel, period: PeriodEnum) -> None:
        pass

    @abstractmethod
    async def do_purchase(self, data: PurchaseSubscriptionModel, upd_from: str, geo_loc: Tuple[float, float]) -> None:
        pass

    @abstractmethod
    async def set_subscription(self, data: PurchaseSubscriptionModel, upd_from: str, geo_loc: Tuple[float, float]) -> None:
        pass
