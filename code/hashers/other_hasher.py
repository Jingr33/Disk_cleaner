from file_data.file_info import FileInfo
from hashers.hasher_base import HasherBase

class OtherHasher(HasherBase):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_text_hash(self, file_info : FileInfo) -> None:
        """Return None when unhashable file is entered."""
        return super().extract_text_hash(file_info)

    def extract_image_hash(self, file_info : FileInfo) -> None:
        """Return None when unhashable file is entered."""
        return super().extract_image_hash(file_info)