from file_data.file_info import FileInfo
from hashers.hasher_base import HasherBase

class OtherHasher(HasherBase):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_hashes(self, file_info : FileInfo):
        """Pass hash extraction for other type files."""
        pass
