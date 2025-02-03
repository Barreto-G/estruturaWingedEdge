from enum import Enum, auto

class RenderMode(Enum):
    WIREFRAME = auto()
    SOLID = auto()
    SOLID_WIREFRAME = auto()


class Colors:
    FACE_COLOR = (0.0, 0.9, 1.0)    
    WIRE_COLOR = (0.0, 0.0, 0.0) 