
import datetime
import structlog
import sendgrid
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from typing import Tuple
from domain.subscription.ports.SubscriptionPort import SubscriptionPort
from domain.subscription.models.PurchaseSubscriptionModel import PurchaseSubscriptionModel
from domain.subscription.ports.PurchaseSubsRepository import PurchaseSubsRepository
from domain.subscription.adapters.PurchaseSubsPersistence import PurchaseSubsPersistence
from domain.ports.NoSqlRepository import NoSqlRepository
from domain.clientsinfo.adapters.PlanPersistence import NoSqlPersistence
from application.models.SubscriptionModel import SubscriptionModel
from application.models.enums import AttemptEnum
from adapters.grpc.ClientsInfoClient import ClientsInfoClient
from config.constants import (
    SENDGRID_API_KEY,
    SENDGRID_TEMPL_FAILED_PAYMENT_PLAN,
    SENDGRID_EMAIL_SENDER,
    SENDGRID_TEMPL_FAILED_RENEW_INITIAL_ATTEMPT,
)
from utils.generic_models.enums import PeriodEnum
from domain.enums import PurchaseStatus, StoreId
from domain.ports.SqlRepository import SqlRepository

LOGGER = structlog.get_logger().bind(module="SubscriptionService")


class SubscriptionService(SubscriptionPort):
    _persistence: PurchaseSubsRepository
    _plans_db: NoSqlRepository
    _sgc = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    _fcm_db: SqlRepository

    def __init__(self):
        self._persistence = PurchaseSubsPersistence()
        self._grpc_clients_info = ClientsInfoClient()
        self._plans_db = NoSqlPersistence()

    async def process_purchase(self, data: SubscriptionModel, period: PeriodEnum) -> None:
        purchase = self._get_purchase_model(period, data)

        await self._persistence.save(purchase, data.upd_from, data.geo_loc)
        await self.do_purchase(purchase, data.upd_from, data.geo_loc)

    async def do_purchase(self, data: PurchaseSubscriptionModel, upd_from: str, geo_loc: Tuple[float, float]) -> None:
        LOGGER.info(f"DEBUG: geo_loc: {geo_loc}")
        assert geo_loc is not None, "geo_loc is None"

        upd_data = PurchaseSubscriptionModel(**data.dict())

        # get details of plan from catalog
        catalog = await self._plans_db.get_by_id(data.subscription_id)
        if not catalog:
            raise Exception('Catalog not found')

        if data.period == PeriodEnum.MONTHLY:
            price = catalog.price_monthly
        elif data.period == PeriodEnum.YEARLY:
            price = catalog.price_yearly
        else:
            raise Exception('Period not supported')

        if 0 < data.purchase_price != price:
            raise Exception('Price not match')

        # send intent of transfer money to a hypothetical grpc service
        LOGGER.info(f"DEBUG: do_purchase(): sending instruct_payment: {data.destination_cb_contract_id} {data.order_id} {price} {geo_loc}")
        res, msg = await self._grpc_clients_info.instruct_payment(data.destination_cb_contract_id, data.order_id,
                                                                  price, geo_loc)
        if res:
            upd_data.purchase_status = PurchaseStatus.PENDING

            # call to hypothetical grpc service to set subscription
            res, msg = self.set_subscription(upd_data, upd_from, geo_loc)

            if res:
                upd_data.purchase_status = PurchaseStatus.SUCCESSFUL
            
        if not res:
            upd_data.purchase_reject_reason = msg
            upd_data.purchase_status = PurchaseStatus.FAILED

        await self._persistence.save(upd_data, upd_from, geo_loc)
        if not res:
            raise ValueError(msg)

    async def set_subscription(self, data: PurchaseSubscriptionModel, upd_from: str, geo_loc: Tuple[float, float]) -> None:
        previous_subscription = await self._prepare_dict(data)

        # if data.expires_at comes as None or 0 calculate it based on period (MONTHLY or YEARLY)
        if not data.expires_at:
            if data.period == PeriodEnum.MONTHLY:
                data.expires_at = (data.purchased_at + relativedelta(months=1)).isoformat()
            elif data.period == PeriodEnum.YEARLY:
                data.expires_at = (data.purchased_at + relativedelta(years=1)).isoformat()
            else:
                raise Exception('Period not supported')

        # await self._persistence.save(data, upd_from, geo_loc)
        await self._grpc_clients_info.set_subscription(data.ia_account_id, data.dict(exclude_none=True),
                                                       previous_subscription, upd_from=upd_from, geo_loc=geo_loc)

    async def send_email_failed_payment(self, email: str):
        LOGGER.info(f"Sending email to client")
        data_to_send = {
            "personalizations": [{
                "to": [
                    {
                        "email": email
                    },
                ]
            },
            ],
            "from": {
                "email": SENDGRID_EMAIL_SENDER,
                "name": "Foo",
                "nickname": "Bar"
            },
            "template_id": SENDGRID_TEMPL_FAILED_PAYMENT_PLAN,
        }

        LOGGER.info(f"sendgrid api key: {SENDGRID_API_KEY}")
        LOGGER.info(f"sendgrid template id: {SENDGRID_TEMPL_FAILED_PAYMENT_PLAN}")
        LOGGER.info(f"sendgrid email sender: {SENDGRID_EMAIL_SENDER}")
        LOGGER.info(f"sendgrid email receiver: {email}")
        LOGGER.info(f"sendgrid data to send: {data_to_send}")

        result = self._sgc.client.mail.send.post(request_body=data_to_send)
        LOGGER.info(f"Result sending email (failed purchase), code: {result.status_code}, body: {result.body}")

    async def _prepare_dict(self, data: PurchaseSubscriptionModel) -> dict:
        last_subscription = await self._persistence.get_last_subscription(data.ia_account_id)

        previous_subscription = {
            'prev_premium_id': -1,
            'prev_purchased_at': None,
            'prev_expires_at': None
        }

        if last_subscription is not None:
            previous_subscription['prev_premium_id'] = last_subscription.subscription_id
            previous_subscription['prev_purchased_at'] = last_subscription.purchased_at
            previous_subscription['prev_expires_at'] = last_subscription.expires_at
        else:
            previous_subscription['prev_premium_id'] = 0

        return previous_subscription

    def _get_purchase_model(self, period: PeriodEnum, data: SubscriptionModel) -> PurchaseSubscriptionModel:
        # expires_at is set to now, with UTC timezone
        purchased_at = datetime.datetime.now(datetime.timezone.utc)
        if period == PeriodEnum.MONTHLY:
            expires_at = (purchased_at + relativedelta(months=1)).isoformat()
        elif period == PeriodEnum.YEARLY:
            expires_at = (purchased_at + relativedelta(years=1)).isoformat()
        else:
            raise Exception('Invalid period')

        return PurchaseSubscriptionModel(
            order_id=data.id,
            account_id=data.account_id,
            user_id=data.user_id,
            store_id=StoreId.APPLE,
            subscription_id=data.subscription_id,
            auto_renew=data.auto_renew,
            expires_at=expires_at,
            purchase_status=PurchaseStatus.PENDING,
            purchase_price=data.price_compare if data.price_compare is not None else 0,
            period=period,
            email=data.email,
            purchased_at=purchased_at.isoformat(),
            upd_from=data.upd_from,
            geo_loc=data.geo_loc
        )

    async def _send_email_failed_renew(self, email: str):
        LOGGER.info(f"Sending email (failed renew) to client")
        data_to_send = {
            "personalizations": [{
                "to": [
                    {
                        "email": email
                    },
                ]
            },
            ],
            "from": {
                "email": SENDGRID_EMAIL_SENDER,
                "name": "Foo",
                "nickname": "Bar"
            },
            "template_id": SENDGRID_TEMPL_FAILED_RENEW_INITIAL_ATTEMPT,
        }

        self._sgc.client.mail.send.post(request_body=data_to_send)
