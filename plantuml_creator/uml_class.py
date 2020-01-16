import enum
from typing import List, Tuple

from code_generator import CodeGenerator
from color import ColorHelper

from uml_code import PlantUMLCode
from error import Error
from method import Method
from shape import ShapeAttributes, ShapeAttributeName
from uml_object import UMLObj, UMLObjType
from utils import ListJoiner, JoinItem
from variable import Variable


class ClassType(enum.Enum):
    REGULAR_CLASS = "class"
    ABSTRACT = "abstract class"
    INTERFACE = "interface"
    INTERFACE_LOLLIPOP = "interface"
    
    def __str__(self):
        return ""


class Class(UMLObj):
    ADD_DIVIDER = True
    ATTRIBUTES_ZONE_DIVIDER = r"/' Attributes '/"
    METHODS_ZONE_DIVIDER = r"/' Methods '/"
    
    """
    Model a uml class object.
    It generates a code like the following:
    class ClassName {
        /' Attributes '/
        String a
        String b
        
        /' Methods '/
        void methodA()
        void methodB()
    }
    """
    
    def __init__(self, name: str, type_: ClassType = ClassType.REGULAR_CLASS,
                 attrs: List[Variable] = None,
                 methods: List[Method] = None,
                 shape_attrs: ShapeAttributes = None):
        super().__init__(name, UMLObjType.CLASS, shape_attrs)
        self.type_ = type_
        if attrs is None:
            attrs = []
        if methods is None:
            methods = []
        self.attrs = attrs
        self.methods = methods
    
    def gen_lollipop(self, color: str = "") -> str:
        """
        interface "CctFccActTipEnt" as CctFccActTipEnt #red
        :return:
        """
        alias = self.convert_to_variable_name(self.name)
        if color != "":
            color = " " + color
        return f'interface "{self.name}" as {alias}{color}'
    
    def gen_code(self, ctx: CodeGenerator.Context) -> Tuple[PlantUMLCode, List[Error]]:
        err: List[Error] = []
        style = ""
        if ShapeAttributeName.COLOR in self.shape_attrs:
            color, err_color = ColorHelper.normalize(self.shape_attrs[ShapeAttributeName.COLOR])
            if err_color is not None:
                err.extend(err)
            else:
                style += color
        if self.type_ == ClassType.INTERFACE_LOLLIPOP:
            return self.gen_lollipop(style), []
        
        d, err = ListJoiner.join({
            "attrs": JoinItem(self.attrs, "\n    ", None, "", ctx),
            "methods": JoinItem(self.methods, "\n    ", None, "", ctx),
        })
        
        return f"{str(self.type_.value)} {self.name} {style} {{\n" \
               f"    {self.ATTRIBUTES_ZONE_DIVIDER}\n" \
               f"    {d['attrs']}\n\n" \
               f"    {self.METHODS_ZONE_DIVIDER}\n" \
               f"    {d['methods']}\n" \
               f"}}\n", err
