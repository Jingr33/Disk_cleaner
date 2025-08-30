from abc import ABC, abstractmethod
from PIL import ImageFile
import imagehash

from hashers.hasher_base import HasherBase
from file_data.file_info import FileInfo

class PhashHasherBase(HasherBase, ABC):
    def __init__(self, sorter, logger) -> None:
        super().__init__(sorter, logger)

    def extract_hashes(self, file_info : FileInfo):
        """Extract image hash of the file, set hashes into file_info object."""
        file_info.set_image_hash(self._extract_image_hash(file_info))

    @abstractmethod
    def _extract_image_hash(self, file_info: FileInfo) -> int:
        """Abstract -> Count percentual hash of a file."""
        pass

    def _get_phash_value(self, img : ImageFile) -> int:
        """Return phash of specified image."""
        return int(str(imagehash.phash(img)), 16)
