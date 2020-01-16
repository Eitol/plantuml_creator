import enum
from typing import List

DataType = str


class CommonDataType(enum.Enum):
    STRING = DataType("String")
    INT = DataType("int")
    FLOAT = DataType("float")
    DOUBLE = DataType("double")
    BOOLEAN = DataType("boolean")
    MAP = DataType("Map")
    SET = DataType("Set")
    List = DataType("List")



