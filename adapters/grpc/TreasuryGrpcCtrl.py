
import grpc
import structlog
from adapters.grpc.procedures import treasury_pb2_grpc, treasury_pb2
from config.constants import GEO_LOC

LOGGER = structlog.get_logger().bind(module="TREASURY_GRPC_SERVER")


class TreasuryGrpcCtrl(treasury_pb2_grpc.TreasuryServicer):
    def __init__(self, app=None):
        if app is None:
            raise TypeError("app is None")
        self._app = app

    async def ResultPayment(self, request: treasury_pb2.ReqResultPayment, context: grpc.aio.ServicerContext):
        LOGGER.info(f"ResultPayment(): request: {request}")
        if request.Status not in ["Received", "Rejected", "Settled"]:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid Status")
            return treasury_pb2.RespGeneric(status=False, message="Invalid Status")

        if (request.Status == "Received" and not request.Action == "Withdrawal") or \
                (request.Status == "Settled" and not request.Action == "Withdrawal"):
            return treasury_pb2.RespGeneric(status=True, message="OK")

        try:
            geo_loc = GEO_LOC.split(",")
            await self._app.result_payment(request.TransactionId, request.Status, request.RejectedReason,
                                           request.ContractId, "CB", (float(geo_loc[0]), float(geo_loc[1])))
            return treasury_pb2.RespGeneric(status=True, message="OK")
        except Exception as e:
            LOGGER.error(f"Error: {e}", exc_info=True, error=str(e), stack_trace=e.__traceback__)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return treasury_pb2.RespGeneric(status=False, message=str(e))

