from removers.by_text_remover import ByTextRemover
from removers.by_image_remover import ByImageRemover
from removers.by_text_and_image_remover import ByTextAndImageRemover
from removers.by_text_or_image_remover import ByTextOrImageRemover
from removers.duplicity_names_remover import DuplicityNamesRemover
from removers.wavers_remover import WaversRemover
from backuper.backuper import Backuper
from files_assistant import FilesAssistant
from file_data.file_info import FileInfo

class Remover():
    def __init__(self, file_infos : list[FileInfo],
                 backuper : Backuper,
                 files_assistant : FilesAssistant) -> None:
        self._backuper = backuper
        self._files_assistant = files_assistant
        self._by_text_remover = ByTextRemover(file_infos, self._backuper, self._files_assistant)
        self._by_image_remover = ByImageRemover(file_infos, self._backuper, self._files_assistant)
        self._by_text_and_image_remover = ByTextAndImageRemover(file_infos, self._backuper, self._files_assistant)
        self._by_text_or_image_remover = ByTextOrImageRemover(file_infos, self._backuper, self._files_assistant)

    def hash_based_pruning(self, sorted_file_infos : dict) -> None:
        """Remove similar files (in all file types) depends on phash ratio between two files."""
        for file_type in sorted_file_infos.keys():
            if 1 <= file_type.value <= 4:
                self._by_text_remover.hash_based_pruning_of_type(sorted_file_infos[file_type])
            elif file_type.value == 5:
                self._by_text_and_image_remover.hash_based_pruning_of_type(sorted_file_infos[file_type])
            elif file_type.value == 6:
                self._by_text_or_image_remover.hash_based_pruning_of_type(sorted_file_infos[file_type])
            elif file_type.value == 7:
                self._by_image_remover.hash_based_pruning_of_type(sorted_file_infos[file_type])

    def delete_duplicity_name_files(self, sorted_file_infos : dict) -> None:
        DuplicityNamesRemover(sorted_file_infos, self._backuper, self._files_assistant)

    def delete_wavers(self, file_infos : list[FileInfo]) -> list[FileInfo]:
        return WaversRemover(file_infos, self._backuper)