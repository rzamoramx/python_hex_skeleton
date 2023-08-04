
import structlog
from domain.business_core.ports.CorePort import IaCorePort
from domain.ports.SqlRepository import SqlRepository
from domain.business_core.models.Movements import Movements
from domain.business_core.adapters.MovementsPersistence import MovementsPersistence
from decimal import Decimal
from config.constants import MOVEMENT_CONCEPT

LOGGER = structlog.get_logger().bind(module="IaCoreService")


class CoreService(IaCorePort):
    _cb_movements: SqlRepository

    def __init__(self):
        self._cb_movements = MovementsPersistence()

    async def create_movement(self, order_id: str, amount: Decimal, contract_id: str) -> None:
        movement = Movements(
            id=order_id,
            name="SO",
            concept=MOVEMENT_CONCEPT,
            amount=amount,
            status="P",
        )
        LOGGER.info(f'saving movement: {movement}')
        await self._cb_movements.save(movement)

    async def upd_movement(self, order_id: str, status: str) -> None:
        LOGGER.info(f'updating movement: {order_id} with status: {status}')
        await self._cb_movements.update_field(order_id, 'status', status)
