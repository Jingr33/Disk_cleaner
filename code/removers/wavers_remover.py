from tqdm import tqdm

from file_data.file_info import FileInfo
from backuper.backuper import Backuper
from console_writer import ConsoleWriter

class WaversRemover():
    def __init__(self, file_infos : list[FileInfo], backuper : Backuper) -> None:
        self._backuper = backuper
        self._file_infos = file_infos
        self._delete_wavers()

    def _delete_wavers(self) -> list[FileInfo]:
        """Remove all files with tilda beginning names."""
        for i in range(len(self._file_infos) - 1, -1, -1):
            if '~' in self._file_infos[i].get_name():
                self._remove_file(i)
        return self._file_infos

    def _remove_file(self, index : int) -> None:
        """Move file to a bin and remove it form a file_infos."""
        file_info = self._file_infos.pop(index)
        self._backuper.move_to_bin(file_info)
        ConsoleWriter.file_deleted(file_info)
