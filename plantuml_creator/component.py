from typing import List, Tuple

from plantuml_creator.code_generator import CodeGenerator
from plantuml_creator.uml_code import PlantUMLCode
from plantuml_creator.error import Error
from plantuml_creator.shape import ShapeAttributes, ShapeAttributeName, ContainerShapeType
from plantuml_creator.uml_object import UMLObj, UMLObjType


class Component(UMLObj):
    """
    i.e:
    component "<b>BS_UT_BCO_PropertyHandler.biz</b>" as BS_UT_BCO_PropertyHandler.biz #LightGray
    """
    
    def __init__(self, name: str,
                 shape_attrs: ShapeAttributes = None):
        super().__init__(name, UMLObjType.COMPONENT, shape_attrs)
    
    @staticmethod
    def get_component_diagram(attr_name: str) -> str:
        if attr_name in [ContainerShapeType.DATABASE.value]:
            return ContainerShapeType.DATABASE.value
        return attr_name
    
    def gen_code(self, ctx: CodeGenerator.Context) -> Tuple[PlantUMLCode, List[Error]]:
        name_to_show = self.name.replace("\"", self.name_replacement_char)
        color, err = self.extract_color_by_shape_attrs(self.shape_attrs)
        shape_type = "component"
        if ShapeAttributeName.CONTAINER_SHAPE_TYPE in self.shape_attrs:
            shape_type = self.shape_attrs[ShapeAttributeName.CONTAINER_SHAPE_TYPE]
            shape_type = self.get_component_diagram(shape_type)
        if err is not None:
            color = ""
        
        return f'{shape_type} "{name_to_show}" as {self.convert_to_variable_name(self.name)} {color}', []
