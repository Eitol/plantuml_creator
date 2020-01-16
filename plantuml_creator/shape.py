import enum
from typing import Dict

ShapeAttributeValue = str


class ContainerShapeType(enum.Enum):
    NAMESPACE = "namespace"
    NODE = "node"
    PACKAGE = "package"
    CLOUD = "cloud"
    DATABASE = "database"
    FRAME = "frame"
    FOLDER = "folder"


class ShapeAttributeName(enum.Enum):
    COLOR = 1
    CONTAINER_SHAPE_TYPE = 2


ShapeAttributes = Dict[ShapeAttributeName, ShapeAttributeValue]
