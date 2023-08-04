
import structlog
from domain.ports.NoSqlRepository import NoSqlRepository, T
from domain.clientsinfo.models.ClientsInfo import ClientsInfo
from motor.motor_asyncio import AsyncIOMotorClient
from utils.mongodb.MongoClient import MongoClient
from config.constants import (
    MONGO_DB,
    MONGO_CLIENTS_INFO_COLLECTION,
)

LOGGER = structlog.get_logger().bind(module="ClientsInfoPersistence")


class ClientsInfoPersistence(NoSqlRepository[ClientsInfo]):
    _client: AsyncIOMotorClient = MongoClient.get_client()

    async def get_by_id(self, account_id: str) -> ClientsInfo:
        LOGGER.info(f"Getting client info by {account_id}")
        LOGGER.info(f"MONGO_DB: {MONGO_DB}")
        LOGGER.info(f"MONGO_CLIENTS_INFO_COLLECTION: {MONGO_CLIENTS_INFO_COLLECTION}")
        result = await self._client[MONGO_DB][MONGO_CLIENTS_INFO_COLLECTION].find_one({'trading_iaaccount_id': account_id})
        if result:
            return ClientsInfo(**result)
        return None

    async def get_by_field(self, field: str, value: str) -> ClientsInfo:
        pass
