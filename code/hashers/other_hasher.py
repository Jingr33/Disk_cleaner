from pathlib import Path

from hashers.hasher_base import HasherBase

class OtherHasher(HasherBase):
    def __init__(self, sorter, logger):
        super().__init__(sorter, logger)

    def extract_hash(path : Path) -> None:
        """Return None when unhashable file is entered."""
        return None