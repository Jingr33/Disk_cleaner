import os

from file_data.file_info import FileInfo
from console_writer import ConsoleWriter

class FilesAssistant():
    def __init__(self) -> None:
        pass

    def open_files(self, file_infos : tuple[FileInfo]) -> None:
        """Open specified files with internal system programs."""
        for file_info in file_infos:
            os.startfile(file_info.get_path())

    def is_file_occupied(self, file_infos : tuple[FileInfo]) -> None:
        """Check if file is locked by other user or system. Waiting until file is unlock."""
        while any(self._is_file_locked(file_info) for file_info in file_infos):
            ConsoleWriter.file_still_open()

    def _is_file_locked(self, file_info : FileInfo) -> bool:
        """Check, if file is actualy open."""
        try:
            with open(file_info.get_path(), 'a'):
                return False
        except IOError:
            return True

