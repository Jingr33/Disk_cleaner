import os
from pathlib import Path
import pandas as pd

from file_data.file_info import FileInfo
from logger import Logger
from config import ROOT_FOLDER, BIN_FOLDER_NAME

class Backuper():
    def __init__(self, logger : Logger) -> None:
        self._logger = logger
        self._bin_folder = self._create_bin_folder()
        BASE_DIR = Path(__file__).resolve().parent
        self._deleted_files_path = os.path.join(BASE_DIR, 'deleted_files.csv')
        self._deleted_files = []
        self._set_deleted_files()

    def _create_bin_folder(self) -> Path:
        """Create bin folder if the folder doesn't exists and return it."""
        bin_path = os.path.join(ROOT_FOLDER, BIN_FOLDER_NAME)
        if not os.path.exists(bin_path):
            os.mkdir(bin_path)
        return Path(bin_path)

    def move_to_bin(self, file_info : FileInfo) -> None:
        """Move file to a bin. Set restore path of the file."""
        file_info.set_restore_path()
        file_info.set_new_path(self._set_bin_path(file_info))
        os.replace(file_info.get_restore_path(), file_info.get_path())
        self._deleted_files.append(file_info)
        self._write_file_to_deleted_files_db(file_info)        

    def restore_bin(self) -> None:
        """Restore all files from bin their original destinations."""
        while len(self._deleted_files):
            file_info = self._deleted_files.pop(0)
            restore_path = file_info.get_restore_path()
            bin_path = file_info.get_path()
            if not restore_path or not os.path.exists(bin_path):
                self._logger.add_to_corrupted(file_info, 'File was not found in the disk bin.')
                continue
            os.replace(bin_path, restore_path)
            file_info.set_new_path(restore_path)

        df = pd.DataFrame(columns=["name", "restore_path"])
        df.to_csv(self._deleted_files_path, index=False, encoding="utf-8")

    def _set_bin_path(self, file_info : FileInfo) -> Path:
        """Set correct bin path of a deleted file."""
        bin_path = os.path.join(self._bin_folder, file_info.get_name())
        new_bin_path = bin_path
        counter = 0
        while os.path.exists(new_bin_path):
            counter += 1
            new_bin_path = f"{bin_path} ({counter})"
        return Path(new_bin_path)

    def _write_file_to_deleted_files_db(self, file_info : FileInfo) -> None:
        """Write info about deletion of this file into deleted files daatbase."""
        name = file_info.get_name()
        restore_path = file_info.get_restore_path()
        df = pd.DataFrame([[name, restore_path]], columns=["name", "restore_path"])
        csv_path = Path(self._deleted_files_path)
        file_exists = csv_path.exists() and csv_path.stat().st_size > 0           
        df.to_csv(csv_path, mode="a", header=False, index=False, encoding="utf-8")

    def _set_deleted_files(self) -> None:
        """Create FileInfo object of all items in the disk bin and set it info self.delete_files list."""
        df = pd.read_csv(self._deleted_files_path, encoding="utf-8")
        for file_name in os.listdir(self._bin_folder):
            file_path = os.path.join(self._bin_folder, file_name)
            file_info = FileInfo(Path(file_path))
            if not os.path.isfile(file_path):
                continue

            self._deleted_files.append(file_info)
            if file_name in df["name"].values:
                row = df[df["name"] == file_name].iloc[0]
                file_info.set_restore_path(row["restore_path"])
            self._deleted_files.append(file_info)

