
import time
from decimal import Decimal
from typing import Tuple
import grpc
import structlog
from adapters.grpc.procedures import clients_info_pb2_grpc, clients_info_pb2
from adapters.grpc.procedures import treasury_pb2_grpc, treasury_pb2
from config.constants import (
    GRPC_CLIENTS_INFO_HOST,
    GRPC_CLIENTS_INFO_PORT,
    GRPC_CB_MSG_ROUTER_HOST,
    GRPC_CB_MSG_ROUTER_API_KEY,
    GRPC_CB_MSG_ROUTER_PORT,
    GRPC_LB_POLICY_NAME,
    GRPC_ENABLE_RETRIES,
    GRPC_KEEPALIVE_TIME_MS,
    MOVEMENT_CONCEPT
)

CHANNEL_OPTIONS = [('grpc.lb_policy_name', GRPC_LB_POLICY_NAME),
                   ('grpc.enable_retries', GRPC_ENABLE_RETRIES),
                   ('grpc.keepalive_timeout_ms', GRPC_KEEPALIVE_TIME_MS),
                   ('grpc.keepalive_time_ms', GRPC_KEEPALIVE_TIME_MS)]
LOGGER = structlog.get_logger().bind(module="GRPC_CLIENTS_INFO_CLIENT")


class ClientsInfoClient:
    async def instruct_payment(self, client_contract_id: str, transaction_id: str, amount: Decimal,
                               geo_loc: Tuple[float, float]) -> (bool, str):
        LOGGER.info(f"Sending message to cb-msg-router: {GRPC_CB_MSG_ROUTER_HOST}:{GRPC_CB_MSG_ROUTER_PORT}")
        LOGGER.info(f"channel options: {CHANNEL_OPTIONS}")
        LOGGER.info(f"api key: {GRPC_CB_MSG_ROUTER_API_KEY}")
        LOGGER.info(f"client_contract_id: {client_contract_id}")

        if not client_contract_id:
            raise Exception("client_contract_id is required")

        try:
            async with grpc.aio.insecure_channel(target=f'{GRPC_CB_MSG_ROUTER_HOST}:{GRPC_CB_MSG_ROUTER_PORT}',
                                                 options=CHANNEL_OPTIONS) as channel:
                stub = treasury_pb2_grpc.TreasuryStub(channel)

                coordinates = treasury_pb2.Coordinates(
                    Latitude=geo_loc[0],
                    Longitude=geo_loc[1],
                )
                msg = treasury_pb2.ReqInstructPayment(
                    Type=201,
                    TransactionId=transaction_id,
                    Timestamp=round(time.time() * 1000),
                    OriginContract=client_contract_id,
                    Amount=float(amount),
                    Concept=MOVEMENT_CONCEPT,
                    GeoLoc=coordinates,
                    Date=time.strftime("%Y-%m-%d", time.localtime()),
                    MovementType="Commissions",
                )
                LOGGER.info(f"instruct_payment(): Sending message: {msg}")

                metadata = [('x-api-key', GRPC_CB_MSG_ROUTER_API_KEY)]
                LOGGER.info(f"metadata: {metadata}")
                response = await stub.InstructPayment(msg, timeout=50, metadata=metadata)
                LOGGER.info(f"response: {response}")

                return response.status, "" if not hasattr(response, 'message') else str(response.message)
        except Exception as e:
            LOGGER.error(f"Exception on stub.InstructPayment: ", exc_info=True, error=str(e), stack_trace=e.__traceback__)
            return False, "cannot send message to cb-msg-router"

    async def set_subscription(self, account_id: str, new_data: dict = None, prev_data: dict = None,
                               attempt: str = 'INITIAL' , upd_from: str = None, geo_loc: Tuple[float, float] = None) \
            -> (bool, str):
        async with grpc.aio.insecure_channel(target=f'{GRPC_CLIENTS_INFO_HOST}:{GRPC_CLIENTS_INFO_PORT}',
                                             options=CHANNEL_OPTIONS) as channel:
            stub = clients_info_pb2_grpc.ClientsInfoStub(channel)

            if prev_data is None:
                raise Exception("Previous data is required")

            if new_data is None:
                raise Exception("New data is required")

            coords = clients_info_pb2.Coordinates(
                latitude=geo_loc[0],
                longitude=geo_loc[1],
            )

            msg = clients_info_pb2.ReqUpdToFP(
                auto_renew=new_data['auto_renew'],
                expires_at=str(new_data['expires_at']),
                purchased_at=str(new_data['purchased_at']),
                premium_id=new_data['subscription_id'],
                account_id=account_id,
                previous_premium_id=prev_data['prev_premium_id'],
                previous_purchased_at=str(prev_data['prev_purchased_at']),
                previous_expires_at=str(prev_data['prev_expires_at']),
                period=new_data['period'].value,
                email=new_data['email'],
                attempt=attempt,
                upd_from=upd_from,
                geo_loc=coords
            )
            LOGGER.info(f"set_subscription(): Sending message: {msg}")

            response = await stub.SetPremium(msg, timeout=5000)

        LOGGER.info(f"status: {response.status}, message: {response.message}")
        return response.status, response.message
