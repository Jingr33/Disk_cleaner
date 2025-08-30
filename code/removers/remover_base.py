import os
from abc import ABC, abstractmethod

from file_data.file_info import FileInfo
from removers.type_simliarity_thresholds import SIM_THRESHOLDS
from removers.similarity_threshold_keys_enum import SimThreshold
from backuper.backuper import Backuper
from console_writer import ConsoleWriter

class RemoverBase(ABC):
    def __init__(self, file_infos : list[FileInfo], backuper : Backuper):
        self.file_infos = file_infos
        self._backuper = backuper
        
    def delete_wavers(self) -> list[FileInfo]:
        """Remove all files with tilda beginning names."""
        for i in range(len(self.file_infos) - 1, -1, -1):
            if '~' in self.file_infos[i].get_name():
                file = self.file_infos.pop(i)
                file.unlink()
                ConsoleWriter.file_deleted(file)
        return self.file_infos

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

    def _manage_remove(self, sim_score : float, file_infos : list[FileInfo], fi1_idx : int, fi2_idx : int) -> None:
        """Based on sim_score it decides what type of removal to use and applies it."""
        if (sim_score >= SIM_THRESHOLDS[file_infos[fi1_idx].get_type()][SimThreshold.AUTO_REMOVE]
        and file_infos[fi1_idx].is_auto_removable()):
            file_infos = self._remove_file_automaticly(file_infos, fi1_idx)
        else:
            file_infos = self._ask_for_remove(file_infos, sim_score, fi2_idx, fi1_idx)

    def _remove_file_automaticly(self, file_infos : list[FileInfo], removing_idx : int) -> list[tuple]:
        """Remove file from the disk and from file_infos list automaticly."""
        file_info = file_infos.pop(removing_idx)
        self._backuper.move_to_bin(file_info)
        ConsoleWriter.file_deleted(file_info)
        return file_infos

    def _ask_for_remove(self, file_infos : list[FileInfo], sim_score : float, idx_fi1 : int, idx_fi2 : int) -> list:
        """Ask user for remove. Manage remove depending on user input."""
        ConsoleWriter.file_similarity_score(sim_score, file_infos[idx_fi1], file_infos[idx_fi2])
        os.startfile(file_infos[idx_fi1].get_path())
        os.startfile(file_infos[idx_fi2].get_path())

        if not ConsoleWriter.do_you_want_to_remove_file(file_infos[idx_fi2]):
            return file_infos
        
        while self._is_file_locked(file_infos[idx_fi1]) or self._is_file_locked(file_infos[idx_fi2]):
            ConsoleWriter.file_still_open()

        return self._remove_file_automaticly(file_infos, idx_fi2)

    def _is_file_locked(self, file_info : FileInfo) -> bool:
        """Check, if file is actualy open."""
        try:
            with open(file_info.get_path(), 'a'):
                return False
        except IOError:
            return True
