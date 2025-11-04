from src.cel.cel_type import CelType
from src.color.color_depth import ColorDepth


class Cel:
    def __init__(
        self,
        cel_type: CelType,
        layer_index: int,
        x: int,
        y: int,
        opacity: int,
        z_index: int,
        color_depth: ColorDepth
    ) -> None:
        self.cel_type: CelType = cel_type
        self.layer_index: int = layer_index

        self.x: int = x
        self.y: int = y

        self.opacity: int = opacity
        self.z_index: int = z_index
        self.color_depth: ColorDepth = color_depth

    def __repr__(self) -> str:
        return f"Cel({self.layer_index})"
