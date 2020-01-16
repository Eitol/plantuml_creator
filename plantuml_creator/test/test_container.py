import pytest

from plantuml_creator.code_generator import CodeGenerator
from plantuml_creator.color import Color
from plantuml_creator.component import Component
from plantuml_creator.container import Container
from plantuml_creator.shape import ShapeAttributeName

from plantuml_creator.uml_class import Class, ClassType
from plantuml_creator.uml_code import CodeStyle

c1 = Container(
    name="comp1",
    objs=[
        Class(
            name="i1",
            type_=ClassType.INTERFACE_LOLLIPOP
        ),
        Component(
            name="A",
            shape_attrs={ShapeAttributeName.COLOR: Color.LIGHT_BLUE.value, }
        )
    ]
)

# --------- EXPECTED ----------- #

c1_expected = """\
package "comp1" {
    interface "i1" as i1
    component "A" as A #ADD8E6
}"""


@pytest.mark.parametrize(
    "case, container, expected, expected_errors",
    [
        ("C1", c1, c1_expected, False),
    ],
)
def test_container_gen_code(case: str, container: Container, expected: str, expected_errors: bool):
    got_name, got_errors = container.gen_code(CodeGenerator.Context(code_style=CodeStyle.C))
    if expected_errors:
        assert got_errors is not None and len(got_errors) > 0
    assert got_name == expected
