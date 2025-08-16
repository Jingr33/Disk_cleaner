from file_data.file_info import FileInfo
from file_data.file_type_enum import FileType

class Sorter():
    def __init__(self, unsorted_files : list[FileInfo]):
        self.unsorted_file_infos = unsorted_files
        self.sorted_file_infos = {}

    def sort_by_file_type(self) -> dict:
        """Sort files into groups by file type."""
        self.sorted_file_infos = {file_type: [] for file_type in FileType}
        for file_info in self.unsorted_file_infos:
            self.sorted_file_infos[file_info.get_type()].append(file_info)            
        return self.sorted_file_infos

    def sort_by_hash(self, file_infos_type : list[FileType]) -> list[FileType]:
        """Sort hashes of file_info
        s of one file type list, if it is possible."""
        return sorted(
            (file for file in file_infos_type if file.get_hash() >= 0),
            key=lambda file_info: file_info.get_hash()
        )