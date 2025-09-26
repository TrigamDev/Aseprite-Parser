import abc
from abc import ABC


class Chunk(ABC):
    def __init__(self, sprite, chunk_size: int, chunk_data: bytes):
        self.sprite = sprite
        self.chunk_size: int = chunk_size
        self.chunk_data: bytes = chunk_data

    @abc.abstractmethod
    def read(self):
        pass
