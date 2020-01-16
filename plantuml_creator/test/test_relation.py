from typing import List

import pytest

from code_generator import CodeGenerator
from relation import Relation, RelationType
from uml_code import CodeStyle
from error import Error
from modifier import CommonAccessModifier, CommonStorageClassSpecifier, CommonTypeQualifier
from variable import Variable

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
    got_name, got_errors = relation.gen_code(CodeGenerator.Context(code_style=CodeStyle.C))
    assert got_name == expected
