
import structlog
from typing import Tuple
from pymongo.errors import PyMongoError
from utils.exceptions import SubscriptionVersionChangedException
from domain.subscription.ports.PurchaseSubsRepository import PurchaseSubsRepository, T
from domain.subscription.models.PurchaseSubscriptionModel import PurchaseSubscriptionModel
from config.constants import (
    MONGO_DB,
    MONGO_PURCHASE_SUBS_COLL,
)
from motor.motor_asyncio import AsyncIOMotorClient
from utils.mongodb.MongoClient import MongoClient
from utils.utils import prepare_update_object

LOGGER = structlog.get_logger().bind(module="SubscriptionPersistence")


class PurchaseSubsPersistence(PurchaseSubsRepository[PurchaseSubscriptionModel]):
    _client: AsyncIOMotorClient = MongoClient.get_client()

    async def get_by_filters(self, filters: dict) -> [T]:
        LOGGER.info(f"Getting subscriptions by filters: {filters}")
        result = await self._client[MONGO_DB][MONGO_PURCHASE_SUBS_COLL].find(filters).to_list(length=None)
        if len(result) > 0:
            return [PurchaseSubscriptionModel(**item) for item in result]
        return []

    async def get_by_order_id(self, order_id: str) -> PurchaseSubscriptionModel:
        LOGGER.info(f"Getting subscription by order_id: {order_id}")
        result = await self._client[MONGO_DB][MONGO_PURCHASE_SUBS_COLL].find_one({'order_id': order_id})
        if result:
            return PurchaseSubscriptionModel(**result)
        return None

    async def get_last_subscription(self, account_id: str) -> PurchaseSubscriptionModel:
        LOGGER.info(f"Getting last subscription by {account_id}")
        # get by account_id and order by purchase_at desc
        result = await self._client[MONGO_DB][MONGO_PURCHASE_SUBS_COLL]\
            .find_one(
                {'account_id': account_id}
            , sort=[('purchase_at', -1)])

        if result:
            return PurchaseSubscriptionModel(**result)
        return None

    async def get_by_account_id(self, account_id: str, subscription_id: str) -> PurchaseSubscriptionModel:
        LOGGER.info(f"Getting subscription by {account_id} and {subscription_id}")
        # get by ia_account_id and subscription_id and order by purchase_at desc
        result = await self._client[MONGO_DB][MONGO_PURCHASE_SUBS_COLL]\
            .find_one(
                {'account_id': account_id, 'subscription_id': subscription_id}
            , sort=[('purchase_at', -1)])

        if len(result) > 0:
            return PurchaseSubscriptionModel(**result[0])
        return None

    async def update(self, data: PurchaseSubscriptionModel, prev: PurchaseSubscriptionModel,
                     upd_from: str, geo_loc: Tuple[float, float]) -> None:
        LOGGER.info(f"Updating subscription: {data.dict()}")
        update = prepare_update_object(data, prev, upd_from, geo_loc, has_history=True)

        try:
            await self._client[MONGO_DB][MONGO_PURCHASE_SUBS_COLL].update_one(
                {'order_id': data.order_id, 'version': data.version},
                {'$set': update, '$inc': {'version': 1}},
                upsert=False
            )
        except PyMongoError as e:
            LOGGER.error(f'Error update_client_info(): {e}')
            raise SubscriptionVersionChangedException

    async def save(self, data: PurchaseSubscriptionModel, upd_from: str, geo_loc: Tuple[float, float]) -> None:
        prev = PurchaseSubscriptionModel()
        update = prepare_update_object(data, prev, upd_from, geo_loc, has_history=True)
        update['version'] = 1

        LOGGER.info(f"Saving PurchaseSubscriptionModel: {update}")
        # to considered concurrency scenarios, we should use upsert=True and use replace_one instead of insert_one
        await self._client[MONGO_DB][MONGO_PURCHASE_SUBS_COLL].replace_one(
            {'order_id': data.order_id},  # 'subscription_id': data.subscription_id},
            update,
            upsert=True
        )

    @classmethod
    async def init_indexes(cls):
        LOGGER.info("Creating indexes for subscription collection")
        try:
            await cls._client[MONGO_DB][MONGO_PURCHASE_SUBS_COLL].create_index([('account_id', 1)])
            await cls._client[MONGO_DB][MONGO_PURCHASE_SUBS_COLL].create_index([('subscription_id', 1)])
            await cls._client[MONGO_DB][MONGO_PURCHASE_SUBS_COLL].create_index([('order_id', 1)], unique=True)
        except Exception as err:
            LOGGER.error(f"mongo indexes subscription collection, w/error: {err}")
