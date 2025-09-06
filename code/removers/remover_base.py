import os
from abc import ABC, abstractmethod

from file_data.file_info import FileInfo
from backuper.backuper import Backuper
from files_assistant import FilesAssistant
from removers.type_simliarity_thresholds import SIM_THRESHOLDS
from removers.similarity_threshold_keys_enum import SimThreshold
from console_writer import ConsoleWriter

class RemoverBase(ABC):
    def __init__(self, file_infos : list[FileInfo],
                 backuper : Backuper,
                 files_assistant : FilesAssistant):
        self.file_infos = file_infos
        self._backuper = backuper
        self._file_assistant = files_assistant

    def hash_based_pruning_of_type(self, file_infos : list[FileInfo]) -> None:
        """Implemented in children classes -> Compare neighbour hashes in file_infos list.
        Manage remove depending on hash similarity."""
        for i in range(len(file_infos) - 1, -1, -1):
            self._compare_two_files(file_infos, i)

    @abstractmethod
    def _compare_two_files(self, file_infos : list[FileInfo], fi1_idx : int) -> None:
        """Implemented in children classes -> Compare file similarity with all remaining files.
        Remove one of files or not depending on hash simiarity."""
        pass

    def _manage_remove(self, sim_score : float, file_infos : list[FileInfo], file_info1 : FileInfo, file_info2 : FileInfo) -> None:
        """Based on sim_score it decides what type of removal to use and applies it."""
        if (sim_score >= SIM_THRESHOLDS[file_info1.get_type()][SimThreshold.AUTO_REMOVE]
        and file_info1.is_auto_removable()):
            file_infos = self._remove_file_automaticly(file_infos, file_info1)
        else:
            file_infos = self._ask_for_remove(file_infos, sim_score, file_info2, file_info1)

    def _remove_file_automaticly(self, file_infos : list[FileInfo], file_info : FileInfo) -> list[tuple]:
        """Remove file from the disk and from file_infos list automaticly."""
        file_infos.remove(file_info)        
        self._backuper.move_to_bin(file_info)
        ConsoleWriter.file_deleted(file_info)
        return file_infos

    def _ask_for_remove(self, file_infos : list[FileInfo], sim_score : float, file_info1 : FileInfo, file_info2 : FileInfo) -> list:
        """Ask user for remove. Manage remove depending on user input."""
        ConsoleWriter.file_similarity_score(sim_score, file_info1, file_info2)

        self._file_assistant.open_files((file_info1, file_info2))
        file_to_remove = ConsoleWriter.do_you_want_to_remove_file(file_info1, file_info2)
        if not file_to_remove:
            return file_infos
        
        self._file_assistant.is_file_occupied((file_info1, file_info2))
        return self._remove_file_automaticly(file_infos, file_to_remove)
