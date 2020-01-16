import enum
from typing import Union

StorageClassSpecifier = str
TypeQualifier = str
AccessModifier = str


class CommonStorageClassSpecifier(enum.Enum):
    """
    A storage class specifier is used to refine the declaration of a variable, a function,
    and parameters. Storage classes determine whether:
    The object has internal, external, or no linkage
    The object is to be stored in memory or in a register, if available
    The object receives the default initial value of 0 or an indeterminate default initial value
    The object can be referenced throughout a program or only within the function, block, or source
        file where the variable is defined
    The storage duration for the object is maintained throughout program run time or only during
        the execution of the block where the object is defined
    """
    AUTO = StorageClassSpecifier("auto")
    STATIC = StorageClassSpecifier("static")
    EXTERN = StorageClassSpecifier("extern")
    MUTABLE = StorageClassSpecifier("mutable")
    REGISTER = StorageClassSpecifier("register")


class CommonTypeQualifier(enum.Enum):
    CONST = TypeQualifier("const")
    UNSIGNED = TypeQualifier("unsigned")
    FINAL = TypeQualifier("final")
    VOLATILE = TypeQualifier("volatile")
    RESTRICT = TypeQualifier("restrict")
    ATOMIC = TypeQualifier("atomic")
    IMMUTABLE = TypeQualifier("immutable")
    SHARED = TypeQualifier("shared")
    INOUT = TypeQualifier("inout")
    SYNC = TypeQualifier("sync")
    ASYNC = TypeQualifier("async")


class CommonAccessModifier(enum.Enum):
    EMPTY = AccessModifier("")
    DEFAULT = AccessModifier("default")
    PRIVATE = AccessModifier("private")
    PROTECTED = AccessModifier("protected")
    PUBLIC = AccessModifier("public")
    FRIEND = AccessModifier("friend")

    
TypeModifier = Union[TypeQualifier, StorageClassSpecifier, AccessModifier]
