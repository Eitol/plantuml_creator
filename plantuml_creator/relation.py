import enum
from typing import Tuple, List, Dict

from plantuml_creator.uml_code import PlantUMLCode
from plantuml_creator.code_generator import CodeGenerator
from plantuml_creator.error import Error
from plantuml_creator.stereotype import Stereotype
from plantuml_creator.uml_object import ObjectName, UMLObj, UMLObjType

Quantifier = Tuple[str, str]


class RelationType(enum.Enum):
    Association = 1
    ReflexiveAssociation = 2
    
    Dependency = 4
    
    Realization = 6
    RealizationCanonical = 7
    RealizationElided = 8
    
    Composition = 9
    Aggregation = 10
    Extension = 11
    Call = 12


class Orientation(enum.Enum):
    UNDEFINED = ""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class Relation(UMLObj):
    default_shape = "-{}-"
    default_stereotype_start = "<<"
    default_stereotype_end = ">>"
    relation_shape_map: Dict[RelationType, str] = {
        # Principals
        RelationType.Aggregation: "o-{}-",
        RelationType.Composition: "*-{}-",
        RelationType.Extension: "-{}-|>",
        RelationType.Association: "-{}-",
        
        RelationType.ReflexiveAssociation: "-{}-",
        
        RelationType.Dependency: "-{}->",
        RelationType.Call: "-{}->",
        
        RelationType.Realization: ".{}..|>",
        RelationType.RealizationCanonical: ".{}.|>",
        RelationType.RealizationElided: ".{}.|>",  # TODO: Change to circle
    }
    
    def __init__(self, obj1: ObjectName, rel_type: RelationType, obj2: ObjectName,
                 stereotypes: List[Stereotype] = None, quantifiers: Quantifier = None,
                 orientation: Orientation = Orientation.UNDEFINED):
        super().__init__("", UMLObjType.RELATION, {})
        self.orientation = orientation
        if quantifiers is None:
            quantifiers = ("", "")
        if stereotypes is None:
            stereotypes = []
        self.obj1 = self.convert_to_variable_name(obj1)
        self.rel_type = rel_type
        self.obj2 = self.convert_to_variable_name(obj2)
        self.quantifiers = quantifiers
        self.stereotypes = stereotypes
    
    def gen_code(self, ctx: CodeGenerator.Context) -> Tuple[PlantUMLCode, List[Error]]:
        """
        Generate the code of a relationship
        :return: i.e:
        Relation(
            obj1="person",
            rel_type=RelationType.Association,
            obj2="account",
            stereotypes=["use"],
            quantifiers=("1", "*")
        ).gen_code()
        >> person "1" -- "*" account : <<use>>
        """
        shape = Relation.default_shape
        if self.rel_type in Relation.relation_shape_map:
            shape = Relation.relation_shape_map[self.rel_type]
        if len(self.stereotypes) > 0:
            stereotypes = f": {self._format_stereotypes(self.stereotypes)}"
        else:
            stereotypes = ""
        q1, q2 = self._format_quantifier(self.quantifiers)
        
        shape = shape.replace("{}", str(self.orientation.value))
        out = f"{self.obj1} {q1} {shape} {q2} {self.obj2}{stereotypes}"
        # Remove all duplicates spaces
        out = " ".join(out.split()).strip()
        return out, []
    
    @staticmethod
    def _format_quantifier(quantifier: Quantifier) -> Quantifier:
        q1 = f"\"{quantifier[0]}\"" if quantifier[0] is not None and len(quantifier[0]) > 0 else ""
        q2 = f"\"{quantifier[1]}\"" if quantifier[1] is not None and len(quantifier[1]) > 0 else ""
        return q1, q2
    
    @staticmethod
    def _format_stereotypes(stereotypes: List[Stereotype]) -> str:
        out_st = ""
        for i in range(len(stereotypes)):
            st = stereotypes[i]
            out_st += f"{Relation.default_stereotype_start}{st}{Relation.default_stereotype_end}"
            if i != len(stereotypes) - 1:
                out_st += "\n"
        return out_st
