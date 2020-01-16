import enum
from typing import List, Tuple, Dict, Union

from plantuml_creator.code_generator import CodeGenerator
from plantuml_creator.diagram_type import DiagramType
from plantuml_creator.error import Error
from plantuml_creator.shape import ShapeAttributes
from plantuml_creator.uml_code import PlantUMLCode
from plantuml_creator.uml_object import UMLObj, UMLObjType
from plantuml_creator.utils import ListJoiner, JoinItem

OBJECTS_SEPARATOR = "/' OBJECTS '/"
RELATION_SEPARATOR = "/' RELATIONS '/"

DEFAULT_ADD_SEPARATORS = True


class DiagramOptName(enum.Enum):
    AUTO_NUMBER = 1
    AUTO_NUMBER_START = 2
    TITLE = 5
    # Not supported
    HEADER_PAGE = 3
    FOOTER_PAGE = 4
    # If is true then adds the OBJECTS_SEPARATOR and RELATION_SEPARATOR
    # To the plantuml code
    ADD_SEPARATORS = 6


DiagramOptValue = Union[str, bool, int, float]

DiagramOpts = Dict[DiagramOptName, DiagramOptValue]

Wrapper = Tuple[str, str]

_standard_wrapper = ("@startuml", "@enduml")
_wireframe_wrapper = ("@startsalt", "@endsalt")
_work_breakdown_wrapper = ("@startwbs", "@endwbs")
_mindmap_wrapper = ("@startmindmap", "@endmindmap")
_gantt_wrapper = ("@startgantt", "@endgantt")
_ditaa_wrapper = ("@startditaa", "@endditaa")


class Diagram(UMLObj):
    """
    Return a valid UML diagram
    """
    
    standard_headers_by_types = [
        DiagramType.SEQUENCE,
        DiagramType.USE_CASE,
        DiagramType.CLASS,
        DiagramType.ACTIVITY,
        DiagramType.COMPONENT,
        DiagramType.STATE,
        DiagramType.OBJECT,
        DiagramType.DEPLOY,
        DiagramType.TIMING,
        DiagramType.ENTITY_RELATIONSHIP,
        DiagramType.MATH,
        DiagramType.ARCHIMATE,
        DiagramType.TIMING,
        DiagramType.DEPLOY,
    
    ]
    
    def __init__(self, name: str, opts: DiagramOpts, type_: DiagramType, objs: List[UMLObj], relations: List[UMLObj],
                 attr: ShapeAttributes = None):
        super().__init__(name, UMLObjType.DIAGRAM, attr)
        if opts is None:
            opts = {}
        self.opts = opts
        self.objs = objs
        if relations is None:
            relations = []
        if objs is None:
            objs = []
        self.objects = objs
        self.relations = relations
        self._wrapper: Wrapper = self._get_wrapper(type_)
        self.type = type_
        if DiagramOptName.ADD_SEPARATORS not in self.opts and DEFAULT_ADD_SEPARATORS:
            self.opts[DiagramOptName.ADD_SEPARATORS] = True
    
    @classmethod
    def _get_wrapper(cls, type_: DiagramType) -> Wrapper:
        if type_ in cls.standard_headers_by_types:
            return _standard_wrapper
        if type_ in DiagramType.WIREFRAME:
            return _wireframe_wrapper
        if type_ in DiagramType.WORK_BREAKDOWN_STRUCTURE:
            return _work_breakdown_wrapper
        if type_ in DiagramType.MINDMAP:
            return _mindmap_wrapper
        if type_ in DiagramType.GANTT:
            return _gantt_wrapper
        if type_ in DiagramType.DITAA:
            return _ditaa_wrapper
        return _standard_wrapper
    
    @classmethod
    def _generate_optionals(cls, type_: DiagramType, opts: DiagramOpts) -> PlantUMLCode:
        out = ""
        if DiagramOptName.TITLE in opts:
            out += f'title "{opts[DiagramOptName.TITLE]}"\n'
        auto_number_start = ""
        if type_ == DiagramType.SEQUENCE:
            if DiagramOptName.AUTO_NUMBER_START in opts:
                auto_number_start = opts[DiagramOptName.AUTO_NUMBER_START]
            if opts[DiagramOptName.AUTO_NUMBER] or len(auto_number_start) > 0:
                out += f'autonumber {auto_number_start}\n'
        return out
    
    def _generate_header(self) -> PlantUMLCode:
        optionals = self._generate_optionals(self.type, self.opts)
        return f"{self._wrapper[0]}\n" \
               f"{optionals}\n"
    
    def gen_code(self, ctx: CodeGenerator.Context) -> Tuple[PlantUMLCode, List[Error]]:
        """
        Generate the code for the entire diagram
        """
        ctx.increase_indent_level()
        d, err = ListJoiner.join({
            "objs": JoinItem(self.objs, "\n", None, "", ctx),
            "relations": JoinItem(self.relations, "\n", None, "", ctx),
        })
        header = self._generate_header()
        obj_sep = ""
        rel_sep = ""
        if DiagramOptName.ADD_SEPARATORS in self.opts and self.opts[DiagramOptName.ADD_SEPARATORS]:
            obj_sep = OBJECTS_SEPARATOR
            rel_sep = RELATION_SEPARATOR
        return f'{header}\n' \
               f'{obj_sep}\n' \
               f'{d["objs"]}\n' \
               f'{rel_sep}\n' \
               f'{d["relations"]}\n' \
               f'{self._wrapper[1]}\n', err
