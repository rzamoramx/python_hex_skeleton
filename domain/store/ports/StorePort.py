
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class StorePort(Generic[T], ABC):
    @abstractmethod
    async def retrieve_details_purchase(self, subscription_id: str, order_id: str, token: str, auto_renew: bool) -> T:
        pass

