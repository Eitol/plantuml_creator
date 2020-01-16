import re
from typing import List, Tuple

from code_generator import CodeGenerator
from uml_code import PlantUMLCode
from error import Error
from relation import Relation
from shape import ShapeAttributes, ContainerShapeType
from uml_object import UMLObj, UMLObjType
from utils import ListJoiner, JoinItem

ContainerContent = Tuple[List[UMLObj], List[Relation]]


class Container(UMLObj):
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
    
    def __init__(self, name: str,
                 objs: List[UMLObj],
                 container_type: ContainerShapeType = ContainerShapeType.PACKAGE,
                 shape_attrs: ShapeAttributes = None):
        super().__init__(name, UMLObjType.CONTAINER, shape_attrs)
        self.objs = objs
        self.container_type = container_type
    
    def gen_code(self, ctx: CodeGenerator.Context) -> Tuple[PlantUMLCode, List[Error]]:
        d, err = ListJoiner.join({
            "objs": JoinItem(self.objs, "\n    ", None, "", ctx),
        })
        syb_type = ""
        if self.container_type in [ContainerShapeType.NAMESPACE,
                                   ContainerShapeType.CLOUD,
                                   ContainerShapeType.DATABASE]:
            type_ = self.container_type.value
        else:
            type_ = "package"
            if self.container_type != ContainerShapeType.PACKAGE:
                syb_type = f"<<{self.container_type.value}>>"
        
        color, err_color = self.extract_color_by_shape_attrs(self.shape_attrs)
        header = re.sub(' +', ' ', f"{type_} \"{self.name}\" {syb_type} {color} {{").strip()
        out = f"{header}\n" \
              f"    {d['objs']}\n" \
              f"}}"
        return out, err
