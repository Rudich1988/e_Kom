from enum import Enum

class Types(str, Enum):
    EMAIL = 'email'
    PHONE = 'phone'
    TEXT = 'text'
    DATE = 'date'
