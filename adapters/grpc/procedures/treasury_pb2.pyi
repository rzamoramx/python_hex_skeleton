from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReqInstructPayment(_message.Message):
    __slots__ = ["Type", "TransactionId", "OriginContract", "DestinationContract", "Timestamp", "Amount", "Concept", "Date", "MovementType", "GeoLoc"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TRANSACTIONID_FIELD_NUMBER: _ClassVar[int]
    ORIGINCONTRACT_FIELD_NUMBER: _ClassVar[int]
    DESTINATIONCONTRACT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CONCEPT_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    MOVEMENTTYPE_FIELD_NUMBER: _ClassVar[int]
    GEOLOC_FIELD_NUMBER: _ClassVar[int]
    Type: int
    TransactionId: str
    OriginContract: str
    DestinationContract: str
    Timestamp: int
    Amount: float
    Concept: str
    Date: str
    MovementType: str
    GeoLoc: Coordinates
    def __init__(self, Type: _Optional[int] = ..., TransactionId: _Optional[str] = ..., OriginContract: _Optional[str] = ..., DestinationContract: _Optional[str] = ..., Timestamp: _Optional[int] = ..., Amount: _Optional[float] = ..., Concept: _Optional[str] = ..., Date: _Optional[str] = ..., MovementType: _Optional[str] = ..., GeoLoc: _Optional[_Union[Coordinates, _Mapping]] = ...) -> None: ...

class Coordinates(_message.Message):
    __slots__ = ["Latitude", "Longitude"]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    Latitude: float
    Longitude: float
    def __init__(self, Latitude: _Optional[float] = ..., Longitude: _Optional[float] = ...) -> None: ...

class RespGeneric(_message.Message):
    __slots__ = ["status", "message"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: bool
    message: str
    def __init__(self, status: bool = ..., message: _Optional[str] = ...) -> None: ...
