# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: treasury.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0etreasury.proto\x12\x08treasury\"\xed\x01\n\x12ReqInstructPayment\x12\x0c\n\x04Type\x18\x01 \x01(\x05\x12\x15\n\rTransactionId\x18\x02 \x01(\t\x12\x16\n\x0eOriginContract\x18\x03 \x01(\t\x12\x1b\n\x13\x44\x65stinationContract\x18\x04 \x01(\t\x12\x11\n\tTimestamp\x18\x05 \x01(\x03\x12\x0e\n\x06\x41mount\x18\x06 \x01(\x02\x12\x0f\n\x07\x43oncept\x18\x07 \x01(\t\x12\x0c\n\x04\x44\x61te\x18\x08 \x01(\t\x12\x14\n\x0cMovementType\x18\t \x01(\t\x12%\n\x06GeoLoc\x18\n \x01(\x0b\x32\x15.treasury.Coordinates\"2\n\x0b\x43oordinates\x12\x10\n\x08Latitude\x18\x01 \x01(\x01\x12\x11\n\tLongitude\x18\x02 \x01(\x01\".\n\x0bRespGeneric\x12\x0e\n\x06status\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2T\n\x08Treasury\x12H\n\x0fInstructPayment\x12\x1c.treasury.ReqInstructPayment\x1a\x15.treasury.RespGeneric\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'treasury_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_REQINSTRUCTPAYMENT']._serialized_start=29
  _globals['_REQINSTRUCTPAYMENT']._serialized_end=266
  _globals['_COORDINATES']._serialized_start=268
  _globals['_COORDINATES']._serialized_end=318
  _globals['_RESPGENERIC']._serialized_start=320
  _globals['_RESPGENERIC']._serialized_end=366
  _globals['_TREASURY']._serialized_start=368
  _globals['_TREASURY']._serialized_end=452
# @@protoc_insertion_point(module_scope)