from PIL import Image, ImageFile
import imagehash

from file_data.file_info import FileInfo
from hashers.hasher_base import HasherBase

class ImageHasher(HasherBase):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_text_hash(self, file_info : FileInfo):
        """Extract text hash from a file -> None in this case."""
        return super().extract_text_hash(file_info)

    def extract_image_hash(self, file_info: FileInfo) -> int:
        """Count percentual hash of an image."""
        try:
            img = Image.open(file_info.get_path())
            return self.get_phash_value(img)
        except Exception as e:
            self.logger.add_to_corrupted(file_info, e)
            return None

    def get_phash_value(self, img : ImageFile) -> int:
        """Return phash of specified image."""
        return int(str(imagehash.phash(img)), 16)
