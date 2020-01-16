from typing import Tuple, List, Callable, Dict, Union

import stringcase

from plantuml_creator.uml_code import PlantUMLCode, CodeStyle, CodeStyleChanger
from plantuml_creator.code_generator import CodeGenerator
from plantuml_creator.data_types import DataType
from plantuml_creator.error import Error
from plantuml_creator.modifier import TypeModifier
from plantuml_creator.uml_object import UMLObj, UMLObjType


class Variable(UMLObj):
    """
    Specify a variable declaration.
    It can mean a parameter or variable in any context
    
    example 1:
    in the following function:
    void f( const int a)
    The variable would be the "a" parameter
    
    example 2:
    in the following declaration:
    static const a;
    The variable would be the "a" parameter
    """
    
    _generators = {}
    
    def __init__(self, name: str, type_: DataType,  modifiers: List[TypeModifier] = None):
        super().__init__(name, UMLObjType.VARIABLE, {})
        if modifiers is None:
            modifiers = []
        self.type_ = type_
        self.modifiers = modifiers
        
    
    @classmethod
    def _get_generators(cls) -> Dict[CodeStyle, Callable[['Variable'], Tuple[PlantUMLCode, List[Error]]]]:
        if len(cls._generators.keys()) == 0:
            cls._generators = {
                CodeStyle.C: cls.gen_code_c_style,
                CodeStyle.GOLANG: cls.gen_code_golang_style,
                CodeStyle.PYTHON: cls.gen_code_python_style,
            }
        return cls._generators
    
    @staticmethod
    def gen_code_c_style(var: 'Variable') -> Tuple[PlantUMLCode, List[Error]]:
        """
        Generate c-style code:
        :return:
        i.e:
        "static int a";
        or
        "const String a";
        """
        modifiers = ""
        for mod in var.modifiers:
            if mod is not None:
                modifiers += mod + " "
        type_ = CodeStyleChanger.type_normalization(var.type_, CodeStyle.C)
        return f"{modifiers}{type_} {var.name}", []
    
    @staticmethod
    def gen_code_python_style(var: 'Variable') -> Tuple[PlantUMLCode, List[Error]]:
        """
        Generate c-style code:
        :return:
        i.e:
        "a: int";
        or
        "a: str";
        """
        # Note: the modifiers are omitted when you have the python style
        name = stringcase.snakecase(var.name)
        type_ = CodeStyleChanger.type_normalization(var.type_, CodeStyle.PYTHON)
        return f"{name}: {type_}", []
    
    @staticmethod
    def gen_code_golang_style(var: 'Variable') -> Tuple[PlantUMLCode, List[Error]]:
        """
        Generate c-style code:
        :return:
        i.e:
        "a int";
        or
        "a string";
        """
        # Note: the modifiers are omitted when you have the golang style
        type_ = CodeStyleChanger.type_normalization(var.type_, CodeStyle.GOLANG)
        return f"{var.name} {type_}", []
    
    def gen_code(self, ctx: CodeGenerator.Context) -> Tuple[PlantUMLCode, List[Error]]:
        return Variable._get_generators()[ctx.code_style](self)
