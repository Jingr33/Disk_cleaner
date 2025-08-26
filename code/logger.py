import os
from pathlib import Path
import pandas as pd

from file_data.file_info import FileInfo
from config import CORRUPTED_FILES_LOG

class Logger():
    def __init__(self):
        self.log_file_name = Path(CORRUPTED_FILES_LOG)
        self.corrupted_files = []

    def add_to_corrupted(self, file_info : FileInfo, error = None) -> None:
        """Add file to corrupted files list."""
        if error:
            file_info.set_error(error)
        self.corrupted_files.append(file_info)

    def log_corrupted_files(self) -> None:
        """Print info about corrupted files in a log_file."""
        rows = []
        for file_info in self.corrupted_files:
            rows.append({
                "File" : str(file_info.get_path()),
                "Error" : file_info.get_error_or_default(),
            })
        df = pd.DataFrame(rows)

        log_file_exists = os.path.exists(self.log_file_name)
        df.to_csv(
            self.log_file_name,
            mode="a" if log_file_exists else "w",
            header=False,
            index=False,
            encoding="utf-8"
        )
