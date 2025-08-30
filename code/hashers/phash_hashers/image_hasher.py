from PIL import Image

from file_data.file_info import FileInfo
from hashers.phash_hashers.phash_hasher_base import PhashHasherBase

class ImageHasher(PhashHasherBase):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def _extract_image_hash(self, file_info: FileInfo) -> int:
        """Count percentual hash of an image."""
        try:
            img = Image.open(file_info.get_path())
            return self._get_phash_value(img)
        except Exception as e:
            self.logger.add_to_corrupted(file_info, e)
            return None
