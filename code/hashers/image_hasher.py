from pathlib import Path
from PIL import Image, ImageFile
import imagehash

from hashers.hasher_base import HasherBase

class ImageHasher(HasherBase):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_hash(self, path: Path) -> int:
        """Count percentual hash of an image."""
        try:
            img = Image.open(path)
            return self.get_phash_value(img)
        except Exception as e:
            self.logger.add_to_corrupted(path)
            return None

    def get_phash_value(self, img : ImageFile) -> int:
        """Return phash of specified image."""
        return int(str(imagehash.phash(img)), 16)
