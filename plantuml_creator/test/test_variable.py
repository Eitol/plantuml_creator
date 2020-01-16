from typing import List

import pytest

from code_generator import CodeGenerator
from uml_code import CodeStyle
from error import Error
from modifier import CommonAccessModifier, CommonStorageClassSpecifier, CommonTypeQualifier
from variable import Variable

var_1 = Variable(name="a", type_="String", modifiers=[
    CommonAccessModifier.PUBLIC.value, CommonStorageClassSpecifier.STATIC.value, CommonTypeQualifier.CONST.value,
])

var_2 = Variable(name="customObject", type_="CustomClass", modifiers=[CommonAccessModifier.PRIVATE.value])


@pytest.mark.parametrize(
    "case, variable,style, expected, expected_errors",
    [
        # Simple
        ("simple python style", var_1, CodeStyle.PYTHON, "a: str", []),
        ("simple c style     ", var_1, CodeStyle.C, "public static const String a", []),
        ("simple golang style", var_1, CodeStyle.GOLANG, "a string", []),
        # More complex
        ("complex python style", var_2, CodeStyle.PYTHON, "custom_object: CustomClass", []),
        ("complex c style     ", var_2, CodeStyle.C, "private CustomClass customObject", []),
        ("complex golang style", var_2, CodeStyle.GOLANG, "customObject CustomClass", []),
    ],
)
def test_variable_gen_code(case: str, variable: Variable, style: CodeStyle, expected: str, expected_errors: List[Error]):
    got_name, got_errors = variable.gen_code(CodeGenerator.Context(code_style=style))
    assert len(got_errors) == len(expected_errors)
    assert got_name == expected
