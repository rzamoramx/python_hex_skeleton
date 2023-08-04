
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class SqlRepository(Generic[T], ABC):
    @abstractmethod
    async def get_by(self, id: str) -> T:
        pass

    @abstractmethod
    async def save(self, model: T) -> None:
        pass

    @abstractmethod
    async def update_field(self, id: str, field: str, value: str) -> None:
        pass
