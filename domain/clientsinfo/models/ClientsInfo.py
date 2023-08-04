
from datetime import datetime
import uuid
from pydantic import BaseModel
from typing import List, Dict
from utils.generic_models.enums import PeriodEnum


class Premium(BaseModel):
    premium_id: int = None
    expires_at: datetime = None
    purchased_at: datetime = None
    period: PeriodEnum = None
    auto_renew: bool = None
    fx_segment: int = None
    repos_segment: int = None
    sec_lending_intent: bool = None
    extended_hours: bool = None
    sec_lending_intent_already_sent: bool = None
    extended_hours_already_sent: bool = None


class ClientsInfo(BaseModel):
    client_info_id: str = uuid.uuid4().__str__()  # Field(default_factory=uuid4)
    user_id: str = None
    account_id: str = None
    name: str = None
    name2: str = None
    last_name: str = None
    last_name2: str = None
    email: str = None
    premium: Premium = None
    update_history: List[Dict] = []
    created_at: int = None
    last_modified: int = None
    version: int = 0
    fcm_type: str = None
    fcm_device_id: str = None
    fcm_registration_id: str = None
