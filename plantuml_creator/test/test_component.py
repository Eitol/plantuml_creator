from typing import List

import pytest

from code_generator import CodeGenerator
from color import Color
from component import Component
from data_types import DataType
from error import Error
from method import Method
from modifier import CommonAccessModifier, CommonTypeQualifier, CommonStorageClassSpecifier
from shape import ShapeAttributeName
from uml_code import CodeStyle
from variable import Variable

component_1 = Component(
    name="ejb://VeryRare.\"Name", shape_attrs={
        ShapeAttributeName.COLOR: Color.BLUE.value
    }
)

component_1_expected = f"""\
component "ejb://VeryRare._Name" as ejb___VeryRare__Name {Color.BLUE.value}\
"""


@pytest.mark.parametrize(
    "case, component, expected, expected_errors",
    [
        ("component 1", component_1, component_1_expected, False),
    ],
)
def test_component_gen_code(case: str, component: Component, expected: str, expected_errors: bool):
    got_name, got_errors = component.gen_code(CodeGenerator.Context(code_style=CodeStyle.C))
    assert (len(got_errors) > 0 and expected_errors) or (len(got_errors) == 0 and not expected_errors)
    assert got_name == expected
