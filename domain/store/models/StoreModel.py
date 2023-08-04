
from pydantic import BaseModel
from datetime import datetime


class StoreModel(BaseModel):
    order_id: str
    original_status: str
    local_status: str
    auto_renew: bool
    expires_at: datetime = None
