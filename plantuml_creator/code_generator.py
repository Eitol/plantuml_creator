"""
Contains the code generation interface
"""
import abc
from typing import List, Tuple

from plantuml_creator import settings
from plantuml_creator.diagram_type import DiagramType

from plantuml_creator.uml_code import PlantUMLCode, CodeStyle
from plantuml_creator.error import Error


class CodeGenerator(metaclass=abc.ABCMeta):
    """
    It is the generation interface.
    The classes that perform it must generate valid plantuml code
    """
    
    class Context(object):
        """
        The generation context
        """
        
        def __init__(self, parent: 'CodeGenerator' = None, indent_level: int = 0,
                     diagram_type: DiagramType = DiagramType.UNKNOWN,
                     code_style: CodeStyle = settings.CODE_STYLE):
            self.code_style = code_style
            self.diagram_type = diagram_type
            self.parent = parent
            self.indent_level = indent_level
        
        def increase_indent_level(self) -> int:
            self.indent_level += 1
            return self.indent_level
    
    """
    Class that must generate valid plantuml code
    """
    
    @abc.abstractmethod
    def gen_code(self, ctx: Context) -> Tuple[PlantUMLCode, List[Error]]:
        """
        This method when implemented must generate valid plantuml code.
        :return: A tuple where:
        El primer elemento será un código de plantuml válido
        The second element will be a list of errors that occurred during the code generation process
        """
        raise NotImplementedError("")
