
from abc import ABC, abstractmethod
from decimal import Decimal


class CorePort(ABC):
    @abstractmethod
    async def create_movement(self, order_id: str, amount: Decimal, account_id: str) -> None:
        pass

    @abstractmethod
    async def upd_movement(self, order_id: str, status: str) -> None:
        pass
