from enum import Enum


class FieldType(Enum):
    EDITABLE = 1
    DENORMALIZED = 2
    READ_ONLY = 3
    UNKNOWN = 4
