from pathlib import Path
import argparse
from tqdm import tqdm

from hashers.hasher import Hasher
from  ai_comparer import AiComparer
from console_writer import ConsoleWriter
from config import AUTO_REMOVE_SIMILARITY, MIN_SIMILARITY

class Remover():
    def __init__(self, files : list[Path], 
               arg_minsim : argparse.Namespace, 
               arg_autosim : argparse.Namespace):
        self.files = files
        # self.ai_comparer = AiComparer()
        self._set_similarities_thresholds(arg_minsim, arg_autosim)


    def _set_similarities_thresholds(self, minsim : argparse.Namespace, autosim : argparse.Namespace) -> None:
        self.minimal_similarity = MIN_SIMILARITY
        self.auto_remove_similarity = AUTO_REMOVE_SIMILARITY
        if minsim:
            self.minimal_similarity = minsim
        if autosim:
            self.auto_remove_similarity = autosim
        
    def delete_wavers(self) -> list[Path]:
        """Remove all files with tilda beginning names."""
        for i in range(len(self.files) - 1, -1, -1):
            if '~' in self.files[i].name:
                file = self.files.pop(i)
                file.unlink()
                ConsoleWriter.file_deleted(file)
        return self.files

    def hash_based_pruning(self, all_hashed_files : dict) -> None:
        """Remove similar files (from all files dict) depends on percentual hash ratio of two files."""
        for ftype in all_hashed_files.keys():
            self._hash_based_pruning_of_type(all_hashed_files[ftype], ftype)

    def _hash_based_pruning_of_type(self, hashed_files : list[tuple], file_type : str) -> None:
        """Remove similar files (of one file type) depends on percentual hash ratio of two files."""
        # while len(hashed_files) > 1:
        #     print(len(hashed_files))
        #     (file1, hash1) = hashed_files.pop(-1)
        #     self._compare_hash_with_others(file1, hash1, hashed_files, file_type)¨
        for i in range(len(hashed_files) - 1, -1, -1):
            self._compare_two_files(hashed_files, i, file_type)

    def _compare_two_files(self,hashed_files : list[tuple], f1_idx : int, ftype : str) -> None:
        """compare entered file hash with all others and remove one of them depending on simiarity"""
        file1, hash1 = hashed_files[f1_idx]
        file2, hash2 = hashed_files[f1_idx - 1]
        sim_score = Hasher.similarity_score(hash1, hash2, ftype)

        if sim_score < self.minimal_similarity:
            return

        if sim_score >= self.auto_remove_similarity:
            hashed_files = self._remove_file_automaticly(hashed_files, f1_idx)
        else:
            hashed_files = self._ask_for_remove(hashed_files, file1, file2, sim_score, f1_idx)

    def _remove_file_automaticly(self, hashed_files : list[tuple], removing_idx : int) -> list[tuple]:
        """Remove file from the disk and from list."""
        (file, _) = hashed_files.pop(removing_idx)
        file.unlink()
        ConsoleWriter.file_deleted(file)
        return hashed_files

    def _ask_for_remove(self, hashed_files : list, fpath1 : Path, fpath2 : Path, sim_score, idx_file2 : int) -> list:
        """Ask user for remove, if the similarity is between AUTO_REMOVE value and MIN_SIMILARITY value."""
        ConsoleWriter.file_similarity_score(sim_score, fpath1, fpath2)
        # os.startfile(fpath1)
        # os.startfile(fpath2)

        # ai_response = self.ai_comparer.get_chat_gpt_recomandation()
        # print response

        if not ConsoleWriter.do_you_want_to_remove_file(fpath2):
            return hashed_files
        
        # while Remover._is_file_locked(fpath1) or Remover._is_file_locked(fpath2):
        #     ConsoleWriter.file_still_open()

        return self._remove_file_automaticly(hashed_files, idx_file2)

    def _is_file_locked(path: Path) -> bool:
        """Check, if file is actualy open."""
        try:
            with open(path, "a"):
                return False
        except IOError:
            return True

    def remove_same_name_files(self, sorted_files : dict) -> dict:
        """Manage removing of files with identical name."""
        ConsoleWriter.detect_same_name_files()
        duplicity_names = Remover._find_same_names_files(sorted_files)
        Remover._remove_duplicate_name_files(duplicity_names)


    def _find_same_names_files(files: dict) -> list[tuple]:
        """Find all pairs of files with identical names."""
        duplicities = []
        total_pairs = sum(
            len(flist) * (len(flist) - 1) // 2 for flist in files.values() if len(flist) > 1
        )
        with tqdm(total=total_pairs, desc=ConsoleWriter.detect_same_name_files(), unit="pair") as pbar:
            for _, one_type_files in files.items():
                if len(one_type_files) <= 1:
                    continue
                for f1_idx in range(len(one_type_files)):
                    path1 = one_type_files[f1_idx]
                    for f2_idx in range(f1_idx + 1, len(one_type_files)):
                        path2 = one_type_files[f2_idx]
                        if path1.name == path2.name:
                            duplicities.append((path1, path2))
                        pbar.update(1)
        ConsoleWriter.same_name_files_count(len(duplicities))
        return duplicities

    def _remove_duplicate_name_files(name_duplicities : list[tuple]) -> None:
        remove_all_automaticly = False
        while len(name_duplicities):
            (path1, path2) = name_duplicities[0]
            user_input = 'n'
            ConsoleWriter.duplicity_file_name_detected(path1, path2)
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
