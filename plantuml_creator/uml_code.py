import abc
import enum
from typing import Callable, Dict

from plantuml_creator.data_types import DataType

COMMENT_START = "/'"
COMMENT_END = "/'"
OBJ_CODE_HEADER = f"\n{COMMENT_START} ---- OBJECTS --- {COMMENT_END}\n"
REL_CODE_HEADER = f"\n{COMMENT_START} ---- RELATIONS --- {COMMENT_END}\n"

PlantUMLCode = str


class CodeStyle(enum.Enum):
    C = 1  # C/C++, Java, Javascript, Typescript, etc
    PYTHON = 2
    GOLANG = 3


class _CodeStyleChangerBase(metaclass=abc.ABCMeta):
    
    @staticmethod
    @abc.abstractmethod
    def type_normalization(data_type: str) -> str:
        raise NotImplementedError()


class _PythonCodeStyleChanger(_CodeStyleChangerBase):
    primitive_names_map = {
        "string": "str",
        "integer": "int",
        "double": "float",
        "boolean": "bool",
    }
    
    @staticmethod
    def type_normalization(data_type: str) -> str:
        if data_type.lower() in _PythonCodeStyleChanger.primitive_names_map:
            return _PythonCodeStyleChanger.primitive_names_map[data_type.lower()]
        return data_type


class _GolangCodeStyleChanger(_CodeStyleChangerBase):
    primitive_names_map = {
        "String": "string",
        "Integer": "int",
        "Double": "float",
        "Boolean": "bool",
        "boolean": "bool",
    }
    
    @staticmethod
    def type_normalization(data_type: str) -> str:
        if data_type in _GolangCodeStyleChanger.primitive_names_map:
            return _GolangCodeStyleChanger.primitive_names_map[data_type]
        return data_type


class CodeStyleChanger(metaclass=abc.ABCMeta):
    styles_map: Dict[CodeStyle, Callable[[str], str]] = {
        CodeStyle.PYTHON: _PythonCodeStyleChanger.type_normalization,
        CodeStyle.GOLANG: _GolangCodeStyleChanger.type_normalization,
    }
    
    @classmethod
    def type_normalization(cls, data_type: DataType, new_style: CodeStyle) -> str:
        """
        Normalize the name of the data type according to the language style.
        In case the style is not supported, then returns the original string
        """
        if new_style in cls.styles_map:
            return cls.styles_map[new_style](data_type)
        return data_type
