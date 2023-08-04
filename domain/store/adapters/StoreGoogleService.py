
import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from domain.store.ports.StorePort import StorePort
from domain.store.models.StoreModel import StoreModel
from domain.store.models.enums import (
    EnumGoogleStatuses,
    EnumLocalStatuses,
)
from config.constants import (
    GOOGLE_APP_BUNDLE_ID,
)


class StoreGoogleService(StorePort[StoreModel]):
    def __init__(self):
        # TODO move service_account.json to s3
        path_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        credentials = service_account.Credentials.from_service_account_file(
            filename=path_root + '/../service_account.json',
            scopes=['https://www.googleapis.com/auth/androidpublisher']
        )
        self._service = build('androidpublisher', 'v3', credentials=credentials)

    async def retrieve_details_purchase(self, subscription_id: str, order_id: str, token: str, auto_renew: bool) \
            -> StoreModel:
        response = self._service.purchases().subscriptions().get(
            packageName=GOOGLE_APP_BUNDLE_ID,
            subscription_id=subscription_id,
            token=token
        ).execute()
        r = json.loads(response)
        print(f'r: {r}')

        original_status = next(value for key, value in vars(EnumGoogleStatuses).items() if value == r['paymentState'])

        return StoreModel(
            order_id=order_id,
            original_status=original_status,
            local_status=EnumLocalStatuses.from_google(original_status),
            expires_at=r['expiryTimeMillis'],
        )
