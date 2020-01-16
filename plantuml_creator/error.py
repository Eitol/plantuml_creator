from typing import List


class Error(Exception):
    def __init__(self, msg: str, involved_objs: List):
        self.involved_objs = involved_objs
        self.msg = msg
