
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Tuple

T = TypeVar('T')


class PurchaseSubsRepository(Generic[T], ABC):
    @abstractmethod
    async def get_by_filters(self, filters: dict) -> [T]:
        pass

    @abstractmethod
    async def get_by_order_id(self, order_id: str) -> T:
        pass

    @abstractmethod
    async def get_last_subscription(self, ia_account_id: str) -> T:
        pass

    @abstractmethod
    async def get_by_account_id(self, ia_account_id: str, subscription_id: str) -> T:
        pass

    @abstractmethod
    async def save(self, data: T, upd_from: str, geo_loc: Tuple[float, float]) -> None:
        pass

    @abstractmethod
    async def update(self, data: T, prev: T, upd_from: str, geo_loc: Tuple[float, float]) -> None:
        pass
