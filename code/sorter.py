from file_data.file_info import FileInfo
from file_data.file_type_enum import FileType
from hashers.hash_type_enum import HashType

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

    def sort_by_hash(self, file_type : FileType, file_infos_type : list[FileType]) -> dict:
        """Sort hashes of file_infos of one file type list, if it is possible."""
        sorted_by_hash = {}
        if 1 <= file_type.value <= 7:
            sorted_by_hash[HashType.TEXT] =  sorted(
                (file for file in file_infos_type if file.get_text_hash()),
                key=lambda file_info: file_info.get_text_hash()
            )
        if file_type.value >= 6:
            sorted_by_hash[HashType.IMAGE] = sorted(
                (file for file in file_infos_type if file.get_image_hash()),
                key=lambda file_info: file_info.get_image_hash()
            )
        return sorted_by_hash