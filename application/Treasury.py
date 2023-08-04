
import structlog
from application.models.SubscriptionModel import SubscriptionModel
from domain.clientsinfo.adapters.ClientsInfoPersistence import ClientsInfoPersistence
from domain.ports.NoSqlRepository import NoSqlRepository
from domain.subscription.ports.SubscriptionPort import SubscriptionPort
from domain.subscription.ports.PurchaseSubsRepository import PurchaseSubsRepository
from domain.subscription.adapters.PurchaseSubsPersistence import PurchaseSubsPersistence
from domain.subscription.models.PurchaseSubscriptionModel import PurchaseSubscriptionModel
from domain.subscription.adapters.SubscriptionService import SubscriptionService
from domain.business_core.ports.CorePort import CorePort
from domain.business_core.adapters.CoreService import CoreService

LOGGER = structlog.get_logger().bind(module="TreasuryApp")


class Treasury:
    _subscription_srv: SubscriptionPort
    _purchase_db: PurchaseSubsRepository
    _core_srv: CorePort
    clients_info_db: NoSqlRepository

    def __init__(self):
        self._subscription_srv = SubscriptionService()
        self._purchase_db = PurchaseSubsPersistence()
        self._core_srv = CoreService()
        self.clients_info_db = ClientsInfoPersistence()

    async def get_purchase_status(self, order_id: str) -> PurchaseSubscriptionModel:
        result = await self._purchase_db.get_by_order_id(order_id)
        if not result:
            raise ValueError('Purchase not found')
        return result

    async def purchase_premium(self, subscription: SubscriptionModel, store_id: str) -> None:
        if subscription.accounts_account_id is None:
            client = await self._clients_info_db.get_by_id(subscription.ia_account_id)
            if client is None:
                raise ValueError('Client not found')
            subscription.account_id = client.account_id
            subscription.users_user_id = client.users_user_id

        await self._subscription_srv.process_purchase(subscription, subscription.period)
        await self._core_srv.create_movement(subscription, store_id)



    