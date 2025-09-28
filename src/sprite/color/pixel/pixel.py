import abc
from abc import ABC

from src.sprite.color.color_depth import ColorDepth


class Pixel(ABC):
    def __init__(self) -> None:
        self.color_depth: ColorDepth = ColorDepth.Unknown

    def __repr__(self) -> str:
        return "Pixel()"

    @abc.abstractmethod
    def to_rgba(self) -> tuple[int, int, int, int]:
        pass
