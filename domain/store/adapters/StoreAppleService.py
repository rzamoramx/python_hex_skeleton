
import base64
import json
import os
import requests
import time
import jwt
from domain.store.ports.StorePort import StorePort
from domain.store.models.StoreModel import StoreModel
from domain.store.models.enums import (
    EnumAppleStatuses,
    EnumLocalStatuses,
)
from config.constants import (
    APPLE_BASE_URL,
    APPLE_ISSUER_ID,
    APPLE_KEY_ID,
    APPLE_BUNDLE_ID
)


class StoreAppleService(StorePort[StoreModel]):
    def __init__(self):
        pass

    async def retrieve_details_purchase(self, subscription_id: str, order_id: str, token: str, auto_renew: bool) \
            -> StoreModel:
        url = APPLE_BASE_URL + f'/inApps/v1/subscriptions/{order_id}'
        headers = {
            'Authorization': f'Bearer {self._generate_jwt()}',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(response.text)

        r = response.json()
        print(f'r: {r}')

        last_status = r['data']['lastTransactions'][0]['status']
        last_status_str = next(value for key, value in vars(EnumAppleStatuses).items() if value == last_status)

        # signedRenewalInfo is a base64 encoded string (JWS) with 3 parts: headers, payload and signature
        signed_renewal_info = r['data']['lastTransactions'][0]['signedRenewalInfo']

        # TODO: verify signature to validate if apple signed this info
        # headers = json.loads(base64.b64decode(signed_renewal_info.split(b'.')[0]))
        # signature = base64.b64decode(signed_renewal_info.split(b'.')[2])
        payload = json.loads(base64.b64decode(signed_renewal_info.split(b'.')[1]))

        return StoreModel(
            order_id=order_id,
            original_status=last_status_str,
            local_status=EnumLocalStatuses.from_apple(last_status_str),
            auto_renew_status=False if payload['autoRenewStatus'] == 0 else True,
            expires_at=payload['gracePeriodExpiresDate'],
        )

    def _generate_jwt(self) -> str:
        # TODO move service_account.json to s3
        private_key_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/../AuthKey_2W8GY842CR.p8'

        with open(private_key_path, 'r') as f:
            private_key = f.read()

        time_now = time.time()
        time_expired = time_now + 3600

        payload = {
            'iss': APPLE_ISSUER_ID,
            'iat': time_now,
            'exp': time_expired,
            'aud': 'appstoreconnect-v1',
            'bid': APPLE_BUNDLE_ID
        }

        headers = {
            'alg': 'ES256',
            'kid': APPLE_KEY_ID,
            'typ': 'JWT'
        }

        return jwt.encode(payload, private_key, algorithm='ES256', headers=headers)
