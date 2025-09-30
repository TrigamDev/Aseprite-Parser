from src.cel.cel_type import CelType


class Cel:
    def __init__(
        self,
        cel_type: CelType,
        layer_index: int,
        x: int,
        y: int,
        opacity: int,
        z_index: int,
    ) -> None:
        self.cel_type: CelType = cel_type
        self.layer_index: int = layer_index

        self.x: int = x
        self.y: int = y

        self.opacity: int = opacity
        self.z_index: int = z_index

    def __repr__(self) -> str:
        return f"Cel({self.layer_index})"
