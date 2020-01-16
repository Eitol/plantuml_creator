from typing import List

import pytest

from plantuml_creator.code_generator import CodeGenerator
from plantuml_creator.relation import Relation, RelationType
from plantuml_creator.uml_code import CodeStyle
from plantuml_creator.error import Error
from plantuml_creator.modifier import CommonAccessModifier, CommonStorageClassSpecifier, CommonTypeQualifier
from plantuml_creator.variable import Variable

rel1 = Relation(
    obj1="animal",
    rel_type=RelationType.Extension,
    obj2="dog",
)

rel2 = Relation(
    obj1="person",
    rel_type=RelationType.Association,
    obj2="account",
    stereotypes=["use"],
    quantifiers=("1", "*")
)


@pytest.mark.parametrize(
    "case, relation, expected",
    [
        # Simple
        ("case 1", rel1, "animal --|> dog"),
        ("case 2", rel2, 'person "1" -- "*" account: <<use>>'),
    ],
)
def test_variable_gen_code(case: str, relation: Relation, expected: str):
    """
    Test the gen_code method
    """
    got_name, got_errors = relation.gen_code(CodeGenerator.Context(code_style=CodeStyle.C))
    assert got_name == expected
