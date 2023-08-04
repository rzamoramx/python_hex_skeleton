
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class NoSqlRepository(Generic[T], ABC):
    @abstractmethod
    async def get_by_id(self, id: str) -> T:
        pass

    @abstractmethod
    async def get_by_field(self, field: str, value: str) -> T:
        pass
