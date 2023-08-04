
import structlog
from fastapi import APIRouter, Header, Depends
from fastapi.responses import JSONResponse
from typing import Union, Optional
from application.Treasury import Treasury
from domain.enums import StoreId
from application.models.SubscriptionModel import SubscriptionModel
from adapters.api.v1.models.subscriptions import (
    Purchase
)
from utils.security import api_key_scopes_required

router = APIRouter()
LOGGER = structlog.get_logger().bind(module="API_REST_V1")
treasury_app = Treasury()


async def inject_scope_read_purchase(api_key: str = Header(None)):
    return await api_key_scopes_required(api_key=api_key, scopes=["purchase:read"])


async def inject_scope_write_purchase(api_key: str = Header(None)):
    return await api_key_scopes_required(api_key=api_key, scopes=["purchase:write", "purchase:read"])


@router.get("/subscriptions/purchase_intent/status/{order_id}",
            dependencies=[Depends(inject_scope_read_purchase)])
async def get_purchase_status(order_id: str, dependency=treasury_app):
    LOGGER.info("GET /subscriptions/purchase_intent/status")
    LOGGER.info("Order ID: {order_id}")

    try:
        status = await dependency.get_purchase_status(order_id)
        return JSONResponse(status_code=200, content={'success': True,
                                                      'data': {'status': status.purchase_status,
                                                               'reason': status.purchase_reject_reason}
                                                      })
    except ValueError as e:
        LOGGER.error(f'Error: {e}', exc_info=True, error=str(e), stack_trace=e.__traceback__)
        return JSONResponse(status_code=400, content={'success': False, 'error': str(e)})
    except Exception as e:
        LOGGER.error(f'Error: {e}', exc_info=True, error=str(e), stack_trace=e.__traceback__)
        return JSONResponse(status_code=500, content={'success': False, 'error': str(e)})


@router.post("/subscriptions/purchase_intent/{store_id}",
             dependencies=[Depends(inject_scope_write_purchase)])
async def post_purchase_intent(body: Purchase, store_id: StoreId, dependency=treasury_app):
    LOGGER.info("POST /subscriptions/purchase_intent")
    LOGGER.info("Body: {body}")
    LOGGER.info("Store ID: {store_id}")

    """if store_id not in StoreId.__members__:
        return JSONResponse(status_code=400, content={'Success': False, 'Error': 'Invalid store ID'})"""

    subscription = SubscriptionModel(**body.dict())
    subscription.auto_renew = True
    subscription.price_compare = body.price

    try:
        await dependency.purchase_premium(subscription, store_id)
        return JSONResponse(status_code=200, content={'success': True})
    except ValueError as e:
        LOGGER.error(f'Error: {e}', exc_info=True, error=str(e), stack_trace=e.__traceback__)
        return JSONResponse(status_code=400, content={'success': False, 'error': str(e)})
    except Exception as e:
        LOGGER.error(f'Error: {e}', exc_info=True, error=str(e), stack_trace=e.__traceback__)
        return JSONResponse(status_code=500, content={'success': False, 'error': str(e)})


