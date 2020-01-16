from typing import Any, Tuple, Union, List, Dict, Optional

from plantuml_creator.code_generator import CodeGenerator
from plantuml_creator.data_types import DataType
from plantuml_creator.error import Error
from plantuml_creator.uml_code import CodeStyleChanger

EMPTY_BOUND = ("", "")


class JoinItem(object):
    def __init__(self, list_: Any, sep: str, bounds: Optional[Tuple[str, str]],
                 default_: str, ctx: CodeGenerator.Context):
        self.ctx = ctx
        self.default_ = default_
        if bounds is None:
            bounds = EMPTY_BOUND
        self.bounds = bounds
        self.sep = sep
        self.list_ = list_


class ListJoiner(object):
    
    @staticmethod
    def to_str(obj: Any, ctx: CodeGenerator.Context) -> Tuple[str, List[Error]]:
        if isinstance(obj, CodeGenerator):
            return obj.gen_code(ctx)
        if isinstance(obj, DataType):
            return CodeStyleChanger.type_normalization(obj, ctx.code_style), []
        return str(obj), []
    
    @staticmethod
    def _join(it: JoinItem) -> Tuple[str, List[Error]]:
        if it.list_ is None or len(it.list_) == 0:
            return (f"{it.bounds[0]}{it.bounds[1]}" if it.default_ is None else it.default_), []
        out, errors = ListJoiner.to_str(it.list_[0], it.ctx)
        if len(it.list_) > 1:
            for i in range(1, len(it.list_)):
                out_aux, errors_aux = ListJoiner.to_str(it.list_[i], it.ctx)
                if len(errors_aux) > 0:
                    errors.extend(errors_aux)
                if len(out_aux) > 0:
                    out += it.sep + out_aux
        return f"{it.bounds[0]}{out}{it.bounds[1]}", errors
    
    @classmethod
    def join(cls, items: Dict[str, JoinItem]) -> Tuple[Dict[str, str], List[Error]]:
        out_val: Dict[str, str] = {}
        out_errs = []
        for name, it in items.items():
            str_val, errs = cls._join(it)
            out_errs.extend(errs)
            out_val[name] = str_val
        return out_val, out_errs
