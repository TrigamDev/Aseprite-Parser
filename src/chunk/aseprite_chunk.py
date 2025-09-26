import abc
from abc import ABC


class AsepriteChunk(ABC):
    def __init__(self, frame, chunk_size: int, chunk_data: bytes):
        self.frame = frame
        self.chunk_size: int = chunk_size
        self.chunk_data: bytes = chunk_data

    @abc.abstractmethod
    def read(self):
        pass
