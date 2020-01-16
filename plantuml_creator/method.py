from typing import Tuple, List, Dict, Callable

from plantuml_creator.data_types import DataType
from plantuml_creator.modifier import TypeModifier, AccessModifier, CommonAccessModifier
from plantuml_creator.uml_code import PlantUMLCode, CodeStyle
from plantuml_creator.code_generator import CodeGenerator
from plantuml_creator.error import Error
from plantuml_creator.uml_object import UMLObj, UMLObjType
from plantuml_creator.utils import ListJoiner, JoinItem
from plantuml_creator.variable import Variable

_DEFAULT_ARGS_BOUNDS = ("(", ")")


class Method(UMLObj):
    """
    Model a method or function
    i.e:
                     args
    return name     ___|___
     |      |      |       |
     v      v      v       v
    String foo(String a, int b)
    """
    _generators = {}
    
    def __init__(self, name: str, return_types: List[DataType], args: List[Variable],
                 modifiers: List[TypeModifier] = None):
        super().__init__(name, UMLObjType.METHOD, {})
        if modifiers is None:
            modifiers = []
        self.modifiers = modifiers
        self.args = args
        self.return_types = return_types
    
    @classmethod
    def _get_generators(cls) -> Dict[CodeStyle, Callable[['Method'], Tuple[PlantUMLCode, List[Error]]]]:
        if len(cls._generators.keys()) == 0:
            cls._generators = {
                CodeStyle.C: cls.gen_code_c_style,
                CodeStyle.GOLANG: cls.gen_code_golang_style,
                CodeStyle.PYTHON: cls.gen_code_python_style,
            }
        return cls._generators
    
    @staticmethod
    def gen_code_all_style(method: 'Method',
                           ctx: CodeGenerator.Context, ret_sep=None) -> Tuple[Dict[str, str], List[Error]]:
        if ret_sep is None:
            ret_sep = ("", "")
        return ListJoiner.join({
            "modifiers": JoinItem(method.modifiers, " ", ("", ""), "", ctx),
            "returns": JoinItem(method.return_types, ",", ret_sep, "", ctx),
            "args": JoinItem(method.args, ", ", _DEFAULT_ARGS_BOUNDS, "()", ctx),
        })
    
    @classmethod
    def gen_code_c_style(cls, method: 'Method', ctx: CodeGenerator.Context) -> Tuple[PlantUMLCode, List[Error]]:
        """
        Generate c-style code:
        :return:
        i.e:
        "public static String foo(String a, int b)";
        """
        d, errs = cls.gen_code_all_style(method, ctx=ctx)
        return f"{d['modifiers']} {d['returns']} {method.name}{d['args']}", errs
    
    @classmethod
    def gen_code_python_style(cls, method: 'Method', ctx: CodeGenerator.Context) -> Tuple[PlantUMLCode, List[Error]]:
        """
        Generate python-style code:
        :return:
        i.e:
        "def foo(a: str, b: int) -> String";
        """
        d, errs = cls.gen_code_all_style(method, ctx)
        if d['returns'] is None or len(d['returns']) == "":
            return_body = ""
        else:
            if d['returns'] == "void":
                d['returns'] = "None"
            return_body = f" -> {d['returns']}"
        if len(method.return_types) == 1:
            return_body = return_body.replace("(", "").replace(")", "")
        return f"def {method.name}{d['args']}{return_body}:", errs
    
    @classmethod
    def gen_code_golang_style(cls, method: 'Method', ctx: CodeGenerator.Context) -> Tuple[PlantUMLCode, List[Error]]:
        """
        Generate go-style code:
        :return:
        i.e:
        "func foo(a string, b int) string";
        """
        # Note: the modifiers are omitted when you have the golang style
        d, errs = cls.gen_code_all_style(method, ctx, ret_sep=("(", ")"))
        if len(method.return_types) == 1:
            d['returns'] = d['returns'].replace("(", "").replace(")", "")
        method.name = method.name[0].upper() + method.name[1:]
        if method.modifiers is not None:
            for i in range(len(method.modifiers)):
                if isinstance(method.modifiers[i], AccessModifier) and \
                        method.modifiers[i] in [CommonAccessModifier.PRIVATE.value, CommonAccessModifier.PROTECTED]:
                    method.name = method.name[0].lower() + method.name[1:]
        return f"func {method.name}{d['args']} {d['returns']}", errs
    
    def gen_code(self, ctx: CodeGenerator.Context) -> Tuple[PlantUMLCode, List[Error]]:
        return Method._get_generators()[ctx.code_style](self, ctx)
