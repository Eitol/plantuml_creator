from typing import List

import pytest

from code_generator import CodeGenerator
from data_types import CommonDataType
from method import Method
from modifier import CommonAccessModifier, CommonTypeQualifier, CommonStorageClassSpecifier
from uml_class import Class, ClassType
from uml_code import CodeStyle
from variable import Variable

var_1 = Variable(name="a", type_="String", modifiers=[
    CommonAccessModifier.PUBLIC.value, CommonStorageClassSpecifier.STATIC.value, CommonTypeQualifier.CONST.value,
])

class_1 = Class(
    name="KubernetesCluster",
    type_=ClassType.ABSTRACT,
    attrs=[
        Variable(
            name="clusterName",
            type_=CommonDataType.STRING.value,
            modifiers=[
                CommonAccessModifier.PRIVATE.value
            ]
        ),
        Variable(
            name="startedTime",
            type_=CommonDataType.INT.value,
            modifiers=[
                CommonAccessModifier.PRIVATE.value
            ]
        ),
    ],
    methods=[
        Method(
            name="listPods",
            return_types=["List<Pod>"],
            args=[
                Variable(
                    name="filter",
                    type_="QueryFilter",
                ),
            ],
            modifiers=[
                CommonAccessModifier.PUBLIC.value
            ]
        ),
    ],
)

# --------- EXPECTED ----------- #

class_1_c_style_expected = """\
abstract class KubernetesCluster  {
    /' Attributes '/
    private String clusterName
    private int startedTime

    /' Methods '/
    public List<Pod> listPods(QueryFilter filter)
}
"""

class_1_python_style_expected = """\
abstract class KubernetesCluster  {
    /' Attributes '/
    cluster_name: str
    started_time: int

    /' Methods '/
    def listPods(filter: QueryFilter) -> List<Pod>:
}
"""

class_1_golang_style_expected = """\
abstract class KubernetesCluster  {
    /' Attributes '/
    clusterName string
    startedTime int

    /' Methods '/
    func ListPods(filter QueryFilter) List<Pod>
}
"""


@pytest.mark.parametrize(
    "case, class_,style, expected, expected_errors",
    [
        ("Simple class c style     ", class_1, CodeStyle.C, class_1_c_style_expected, False),
        ("Simple class python style", class_1, CodeStyle.PYTHON, class_1_python_style_expected, False),
        ("Simple class golang style", class_1, CodeStyle.GOLANG, class_1_golang_style_expected, False),
    ],
)
def test_method_gen_code(case: str, class_: Class, style: CodeStyle, expected: str, expected_errors: bool):
    got_name, got_errors = class_.gen_code(CodeGenerator.Context(code_style=style))
    if expected_errors:
        assert got_errors is not None and len(got_errors) > 0
    assert got_name == expected
