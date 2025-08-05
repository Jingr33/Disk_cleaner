import os
from pathlib import Path
import pandas as pd

from config import CORRUPTED_FILES_LOG

class Logger():
    def __init__(self):
        self.log_file_name = Path(CORRUPTED_FILES_LOG)
        self.corrupted_files = []

    def add_to_corrupted(self, path : Path) -> None:
        """Add file to corrupted files list."""
        self.corrupted_files.append(path)

    def log_corrupted_files(self) -> None:
        log_file_exists = os.path.exists(self.log_file_name)

        df = pd.DataFrame(self.corrupted_files)
        df.to_csv(
            self.log_file_name,
            mode="a" if log_file_exists else "w",
            header=False,
            index=False,
            encoding="utf-8"
        )
