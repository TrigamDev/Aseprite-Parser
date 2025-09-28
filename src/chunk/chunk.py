import abc
from abc import ABC
from typing import Any


class Chunk(ABC):
    def __init__(self, sprite, chunk_size: int, chunk_data: bytes) -> None:
        self.sprite = sprite
        self.chunk_size: int = chunk_size
        self.chunk_data: bytes = chunk_data

    @abc.abstractmethod
    def read(self) -> Any:
        pass
