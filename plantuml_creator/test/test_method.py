from typing import List

import pytest

from plantuml_creator.code_generator import CodeGenerator
from plantuml_creator.data_types import DataType
from plantuml_creator.error import Error
from plantuml_creator.method import Method
from plantuml_creator.modifier import CommonAccessModifier, CommonTypeQualifier, CommonStorageClassSpecifier
from plantuml_creator.uml_code import CodeStyle
from plantuml_creator.variable import Variable

m1 = Method(
    name="func1",
    return_types=[DataType("String")],
    args=[
        Variable(name="a", type_="String", modifiers=[CommonTypeQualifier.CONST.value]),
        Variable(name="b", type_="int"),
    ],
    modifiers=[CommonAccessModifier.PUBLIC.value, CommonStorageClassSpecifier.STATIC.value],
)

m2 = Method(
    name="func2",
    return_types=[],
    args=[],
    modifiers=[],
)

m3 = Method(
    name="func3",
    return_types=[],
    args=[],
    modifiers=[CommonAccessModifier.PRIVATE.value],
)


@pytest.mark.parametrize(
    "case, method ,style, expected, expected_errors",
    [
        ("simple python style", m1, CodeStyle.PYTHON, "def func1(a: str, b: int) -> str:", []),
        ("simple c style", m1, CodeStyle.C, "public static String func1(const String a, int b)", []),
        ("simple golang style", m1, CodeStyle.GOLANG, "func Func1(a string, b int) string", []),
        ("simple golang style", m2, CodeStyle.GOLANG, "func Func2() ", []),
        ("simple golang style", m3, CodeStyle.GOLANG, "func func3() ", []),
    ],
)
def test_method_gen_code(case: str, method: Method, style: CodeStyle, expected: str, expected_errors: List[Error]):
    """
    Test the gen_code method
    """
    got_name, got_errors = method.gen_code(CodeGenerator.Context(code_style=style))
    assert len(got_errors) == len(expected_errors)
    assert got_name == expected
