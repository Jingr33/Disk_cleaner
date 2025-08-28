from abc import ABC, abstractmethod

from file_data.file_info import FileInfo
from sorter import Sorter
from logger import Logger

class HasherBase(ABC):
    def __init__(self, sorter : Sorter, logger : Logger):
        self._sorter = sorter
        self.logger = logger

    @abstractmethod
    def extract_text_hash(self, file_info : FileInfo) -> int:
        """Extract text hash from a file."""
        pass

    @abstractmethod
    def extract_image_hash(self, file_info : FileInfo) -> int:
        """Extract image phash from a file."""
        pass