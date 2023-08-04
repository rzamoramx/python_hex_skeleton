
from domain.ports.SqlRepository import SqlRepository
from domain.business_core.models.Movements import Movements


class MovementsPersistence(SqlRepository[Movements]):
    async def get_by(self, id: str) -> Movements:
        pass

    async def save(self, movement: Movements) -> None:
        await movement.save()

    async def update_field(self, id: str, field: str, value: str) -> None:
        await Movements.update({field: value}).where(Movements.id == id)
