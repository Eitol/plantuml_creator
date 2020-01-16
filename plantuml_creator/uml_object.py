import abc
import enum

from typing import List, Tuple, Optional

from color import ColorHelper
from uml_code import PlantUMLCode
from code_generator import CodeGenerator
from error import Error
from shape import ShapeAttributes, ShapeAttributeName

ObjectName = str


class UMLObjType(enum.Enum):
    CLASS = 1
    USE_CASE = 2
    CONTAINER = 3
    COMPONENT = 4
    DIAGRAM = 5
    VARIABLE = 6
    METHOD = 7
    RELATION = 8


class UMLObj(CodeGenerator):
    allowed_variable_chars = ["A"]
    name_replacement_char = "_"
    
    def __init__(self, name: str, obj_type: UMLObjType, shape_attrs: ShapeAttributes):
        super().__init__()
        if name is None or len(name) == 0:
            name = " "
        if shape_attrs is None:
            shape_attrs = {}
        self.shape_attrs = shape_attrs
        self.obj_type = obj_type
        self.name = name
    
    @staticmethod
    def is_a_to_z(c: str) -> bool:
        return (ord("a") <= ord(c) <= ord("z")) or (ord("A") <= ord(c) <= ord("Z"))
    
    @classmethod
    def convert_to_variable_name(cls, name: str) -> str:
        out = ""
        for c in name:
            if c.isnumeric() or cls.is_a_to_z(c):
                out += c
            else:
                out += cls.name_replacement_char
        return out
    
    @staticmethod
    def extract_color_by_shape_attrs(shape_attrs: ShapeAttributes) -> Tuple[str, Optional[Exception]]:
        if ShapeAttributeName.COLOR not in shape_attrs:
            return "", None
        color, err_color = ColorHelper.normalize(shape_attrs[ShapeAttributeName.COLOR])
        if err_color is not None:
            return "", err_color
        return color, None
    
    @staticmethod
    def gen_for_generators_list(generators: List[List[CodeGenerator]]):
        out_codes: PlantUMLCode = ""
        out_errors = []
        for gen in generators:
            for gen_i in gen:
                code_lines, obj_errors = gen_i.gen_code()
                out_codes = code_lines + "\n"
                if len(obj_errors) > 0:
                    out_errors.extend(out_errors)
        return out_codes, out_errors
    
    @abc.abstractmethod
    def gen_code(self, ctx: CodeGenerator.Context) -> Tuple[PlantUMLCode, List[Error]]:
        """
        Generate the code for all objects and relationships that are in the diagram.
        If any object or relationship has an error, then add it
        """
        raise NotImplementedError()
