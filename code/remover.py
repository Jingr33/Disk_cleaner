from pathlib import Path
from tqdm import tqdm

from hashers.hasher import Hasher
from file_data.file_info import FileInfo
from file_data.file_type_enum import FileType
from console_writer import ConsoleWriter
from config import AUTO_REMOVE_SIMILARITY, MIN_SIMILARITY

class Remover():
    def __init__(self, file_infos : list[FileInfo]):
        self.file_infos = file_infos
        
    def delete_wavers(self) -> list[FileInfo]:
        """Remove all files with tilda beginning names."""
        for i in range(len(self.file_infos) - 1, -1, -1):
            if '~' in self.file_infos[i].get_name():
                file = self.file_infos.pop(i)
                file.unlink()
                ConsoleWriter.file_deleted(file)
        return self.file_infos

    def hash_based_pruning(self, sorted_file_infos : dict) -> None:
        """Remove similar files (in all file types) depends on phash ratio between two files."""
        for ftype in sorted_file_infos.keys():
            self._hash_based_pruning_of_type(sorted_file_infos[ftype], ftype)

    def _hash_based_pruning_of_type(self, file_infos : list[FileInfo], file_type : FileType) -> None:
        """Compare neighbour hashes in file_infos list.
        manage remove depending on hash similarity."""
        for i in range(len(file_infos) - 1, -1, -1):
            self._compare_two_files(file_infos, i, file_type)

    def _compare_two_files(self, file_infos : list[FileInfo], fi1_idx : int, file_type : FileType) -> None:
        """Compare file similarity with all remaining files.
        Remove one of files or not depending on hash simiarity."""
        file_info1 = file_infos[fi1_idx - 1]
        file_info2 = file_infos[fi1_idx]
        sim_score = Hasher.similarity_score(file_info2.get_hash(), file_info1.get_hash(), file_type)

        if sim_score < MIN_SIMILARITY:
            return

        if sim_score >= AUTO_REMOVE_SIMILARITY and file_info1.is_auto_removable():
            file_infos = self._remove_file_automaticly(file_infos, fi1_idx)
        else:
            file_infos = self._ask_for_remove(file_infos, sim_score, fi1_idx - 1, fi1_idx)

    def _remove_file_automaticly(self, file_infos : list[FileInfo], removing_idx : int) -> list[tuple]:
        """Remove file from the disk and from file_infos list automaticly."""
        file_info = file_infos.pop(removing_idx)
        file_info.get_path().unlink()
        ConsoleWriter.file_deleted(file_info)
        return file_infos

    def _ask_for_remove(self, file_infos : list[FileInfo], sim_score : float, idx_fi1 : int, idx_fi2 : int) -> list:
        """Ask user for remove.
        MAnage remove depending on user input."""
        ConsoleWriter.file_similarity_score(sim_score, file_infos[idx_fi1], file_infos[idx_fi2])
        # os.startfile(fpath1)
        # os.startfile(fpath2)

        if not ConsoleWriter.do_you_want_to_remove_file(file_infos[idx_fi2]):
            return file_infos
        
        # while Remover._is_file_locked(fpath1) or Remover._is_file_locked(fpath2):
        #     ConsoleWriter.file_still_open()

        return self._remove_file_automaticly(file_infos, idx_fi2)

    def _is_file_locked(path: Path) -> bool:
        """Check, if file is actualy open."""
        try:
            with open(path, 'a'):
                return False
        except IOError:
            return True

    def remove_same_name_files(self, sorted_file_infos : dict) -> dict:
        """Manage removing of files with identical name."""
        ConsoleWriter.detect_same_name_files()
        duplicity_names = Remover._find_same_names_files(sorted_file_infos)
        Remover._remove_duplicate_name_files(duplicity_names)

    def _find_same_names_files(sorted_file_infos: dict) -> list[tuple]:
        """Find all pairs of files with identical names."""
        duplicities = []
        total_pairs = sum(
            len(file_info) * (len(file_info) - 1) // 2 for file_info in sorted_file_infos.values() if len(file_info) > 1
        )
        with tqdm(total=total_pairs, desc=ConsoleWriter.detect_same_name_files(), unit='pair') as pbar:
            for _, file_infos in sorted_file_infos.items():
                if len(file_infos) <= 1:
                    continue
                for fi1_idx in range(len(file_infos)):
                    name1 = file_infos[fi1_idx].get_name()
                    for f2_idx in range(fi1_idx + 1, len(file_infos)):
                        name2 = file_infos[f2_idx].get_name()
                        if name1 == name2:
                            duplicities.append((file_infos[fi1_idx], file_infos[f2_idx]))
                        pbar.update(1)
        ConsoleWriter.same_name_files_count(len(duplicities))
        return duplicities

    def _remove_duplicate_name_files(name_duplicities : list[tuple]) -> None:
        remove_all_automaticly = False
        while len(name_duplicities):
            (fi1, fi2) = name_duplicities[0]
            user_input = 'n'
            ConsoleWriter.duplicity_file_name_detected(fi1, fi2)
            if not remove_all_automaticly:
                user_input = ConsoleWriter.ask_remove_duplicity_name_files()

            if user_input == 'All' or remove_all_automaticly:
                    name_duplicities = Remover._remove_duplicate_name_file(name_duplicities, 0)
                    remove_all_automaticly = True
            elif user_input == 'Y':
                name_duplicities = Remover._remove_duplicate_name_file(name_duplicities, 0)
            else:
                del name_duplicities[0]
        ConsoleWriter.duplicity_names_removing_completed()

    def _remove_duplicate_name_file(duplicities : list[tuple], index : int) -> list[tuple]:
        duplicity = duplicities.pop(index)
        duplicity[1].unlink()
        ConsoleWriter.file_deleted(duplicity[1], True)
        return duplicities
