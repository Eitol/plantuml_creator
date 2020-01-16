import enum


class DiagramType(enum.Enum):
    UNKNOWN = 0
    SEQUENCE = 1
    CLASS = 2
    USE_CASE = 3
    ACTIVITY = 4
    COMPONENT = 5
    STATE = 5
    OBJECT = 6
    DEPLOY = 7
    TIMING = 8
    
    # Non UML
    
    WIREFRAME = 9
    ARCHIMATE = 10
    SDL = 11
    DITAA = 12
    GANTT = 13
    MINDMAP = 14
    WORK_BREAKDOWN_STRUCTURE = 15
    MATH = 16
    ENTITY_RELATIONSHIP = 17