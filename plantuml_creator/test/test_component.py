from typing import List

import pytest

from plantuml_creator.code_generator import CodeGenerator
from plantuml_creator.color import Color
from plantuml_creator.component import Component
from plantuml_creator.shape import ShapeAttributeName
from plantuml_creator.uml_code import CodeStyle


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
    """
    Test the Component.gen_code method
    """
    got_name, got_errors = component.gen_code(CodeGenerator.Context(code_style=CodeStyle.C))
    assert (len(got_errors) > 0 and expected_errors) or (len(got_errors) == 0 and not expected_errors)
    assert got_name == expected
