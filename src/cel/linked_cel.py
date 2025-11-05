from PIL import Image
from src.cel.cel import Cel
from src.cel.cel_type import CelType
from src.color.color_depth import ColorDepth
from src.frame.frame import Frame


class LinkedCel(Cel):
    def __init__(
        self,
        cel_type: CelType,
        layer_index: int,
        x: int,
        y: int,
        opacity: int,
        z_index: int,
        color_depth: ColorDepth,
        linked_frame_index: int,
    ):
        super().__init__(cel_type, layer_index, x, y, opacity, z_index, color_depth)

        self.linked_frame_index: int = linked_frame_index

    def __repr__(self):
        return f"LinkedCel({self.linked_frame_index})"

    def render(self, frame: Frame) -> Image.Image:
        raise NotImplementedError()
