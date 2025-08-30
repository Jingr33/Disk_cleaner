from abc import ABC, abstractmethod

from file_data.file_info import FileInfo
from sorter import Sorter
from logger import Logger

class HasherBase(ABC):
    def __init__(self, sorter : Sorter, logger : Logger):
        self._sorter = sorter
        self.logger = logger

    @abstractmethod
    def extract_hashes(self, file_info : FileInfo) -> None:
        """Abstract -> Extract hashes of the file, set hashes into file_info object."""
        pass
