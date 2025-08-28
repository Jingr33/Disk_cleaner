import os
from pathlib import Path

from file_data.file_info import FileInfo
from config import ROOT_FOLDER, BIN_FOLDER_NAME

class Backuper():
    def __init__(self) -> None:
        self._bin_folder = self._create_bin_folder()

    def _create_bin_folder(self) -> None:
        """Create bin folder if the folder doesnt exists."""
        bin_path = os.path.join(ROOT_FOLDER, BIN_FOLDER_NAME)
        if not os.path.exists(bin_path):
            os.mkdir(bin_path)
        return bin_path

    def move_to_bin(self, file_info : FileInfo) -> None:
        """Move file to a bin. Set restore path of the file."""
        file_info.set_restore_path()
        file_info.set_new_path(Path(os.path.join(self._bin_folder, file_info.get_name())))
        os.replace(file_info.get_restore_path(), file_info.get_path())
