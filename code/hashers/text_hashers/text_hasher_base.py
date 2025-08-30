from abc import ABC, abstractmethod
from simhash import Simhash

from hashers.hasher_base import HasherBase
from file_data.file_info import FileInfo

class TextHasherBase(HasherBase, ABC):
    def __init__(self, sorter, logger) -> None:
        super().__init__(sorter, logger)

    def extract_hashes(self, file_info : FileInfo) -> None:
        """Extract text hashes of the file, set hashes into file_info object."""
        text = self._extract_text(file_info)
        file_info.set_text(text)
        file_info.set_text_hash(self._extract_hash_from_text(text))

    @abstractmethod
    def _extract_text(self, file_info : FileInfo) -> str:
        """Abstract -> Extract text file, return simhash of a file."""
        pass

    def _extract_hash_from_text(self, text : str) -> int:
        """Count simhash from text."""
        if not text:
            return None
        return Simhash(text.split()).value
