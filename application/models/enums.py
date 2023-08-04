
from enum import Enum


class AttemptEnum(str, Enum):
    INITIAL = 'INITIAL'
    INTERMEDIATE = 'INTERMEDIATE'
    FINAL = 'FINAL'
