
import structlog
from domain.ports.NoSqlRepository import NoSqlRepository
from domain.clientsinfo.models.CatalogPremium import CatalogPremium
from motor.motor_asyncio import AsyncIOMotorClient
from utils.mongodb.MongoClient import MongoClient
from config.constants import (
    MONGO_DB,
    MONGO_PLAN_COLLECTION,
)

LOGGER = structlog.get_logger().bind(module="PlanPersistence")


class NoSqlPersistence(NoSqlRepository[CatalogPremium]):
    _client: AsyncIOMotorClient = MongoClient.get_client()

    async def get_by_id(self, plan_id: str) -> CatalogPremium:
        LOGGER.info(f"Getting plan by {plan_id}")
        result = await self._client[MONGO_DB][MONGO_PLAN_COLLECTION].find_one({'premium_id': int(plan_id)})
        if result:
            return CatalogPremium(**result)
        return None

    async def get_by_field(self, field: str, value: str) -> CatalogPremium:
        LOGGER.info(f'Getting catalog premium by {field}: {value}')
        result = await self._client[MONGO_DB][MONGO_PLAN_COLLECTION].find_one({field: value})
        if result is None:
            return None
        return CatalogPremium(**result)
