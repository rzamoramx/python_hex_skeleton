from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReqUpdToFP(_message.Message):
    __slots__ = ["account_id", "premium_id", "expires_at", "purchased_at", "auto_renew", "previous_premium_id", "previous_purchased_at", "previous_expires_at", "period", "upd_from", "email", "attempt", "geo_loc"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PREMIUM_ID_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    PURCHASED_AT_FIELD_NUMBER: _ClassVar[int]
    AUTO_RENEW_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_PREMIUM_ID_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_PURCHASED_AT_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    UPD_FROM_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ATTEMPT_FIELD_NUMBER: _ClassVar[int]
    GEO_LOC_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    premium_id: int
    expires_at: str
    purchased_at: str
    auto_renew: bool
    previous_premium_id: int
    previous_purchased_at: str
    previous_expires_at: str
    period: str
    upd_from: str
    email: str
    attempt: str
    geo_loc: Coordinates
    def __init__(self, account_id: _Optional[str] = ..., premium_id: _Optional[int] = ..., expires_at: _Optional[str] = ..., purchased_at: _Optional[str] = ..., auto_renew: bool = ..., previous_premium_id: _Optional[int] = ..., previous_purchased_at: _Optional[str] = ..., previous_expires_at: _Optional[str] = ..., period: _Optional[str] = ..., upd_from: _Optional[str] = ..., email: _Optional[str] = ..., attempt: _Optional[str] = ..., geo_loc: _Optional[_Union[Coordinates, _Mapping]] = ...) -> None: ...

class Coordinates(_message.Message):
    __slots__ = ["latitude", "longitude"]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    latitude: float
    longitude: float
    def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ...) -> None: ...

class RespGeneric(_message.Message):
    __slots__ = ["status", "message"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: str
    message: str
    def __init__(self, status: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...
