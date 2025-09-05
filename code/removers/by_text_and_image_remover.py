from removers.remover_base import RemoverBase
from file_data.file_info import FileInfo
from removers.type_simliarity_thresholds import SIM_THRESHOLDS
from removers.similarity_threshold_keys_enum import SimThreshold
from backuper.backuper import Backuper
from hashers.hasher import Hasher
from hashers.hash_type_enum import HashType

class ByTextAndImageRemover(RemoverBase):
    def __init__(self, file_infos : list[FileInfo], backuper : Backuper) -> None:
        super().__init__(file_infos, backuper)

    def hash_based_pruning_of_type(self, file_infos : list[FileInfo]) -> None:
        """Compare neighbour hashes in file_infos list (by text hashes).
        Manage remove depending on hash similarity."""
        text_sorted_file_infos = file_infos[HashType.TEXT]
        super().hash_based_pruning_of_type(text_sorted_file_infos)

    def _compare_two_files(self, file_infos : list[FileInfo], fi1_idx : int) -> None:
        """Compare file similarity with all remaining files (based on text hash).
        Remove one of files or not depending on hash simiarity."""
        fi2_idx = fi1_idx - 1
        file_info1 = file_infos[fi2_idx]
        file_info2 = file_infos[fi1_idx]

        simhash_score = Hasher.hamming_similarity_simhash(file_info2.get_text_hash(), file_info1.get_text_hash())
        phash_score = Hasher.hamming_similarity_simhash(file_info2.get_image_hash(), file_info1.get_image_hash())
        type = file_info1.get_type()
        if simhash_score >= SIM_THRESHOLDS[type][SimThreshold.SIMHASH_MIN]:
            levenshtein_score = Hasher.levenshtein_text_similarity(file_info1.get_text(), file_info2.get_text())
            if levenshtein_score >= SIM_THRESHOLDS[type][SimThreshold.LEVENSHTEIN_MIN]:
                print(simhash_score)
                print(levenshtein_score)
                self._manage_remove((levenshtein_score, phash_score), file_infos, file_info1, file_info2)

    def _manage_remove(self, sim_score : tuple[float], file_infos : list[FileInfo], file_info1 : FileInfo, file_info2 : FileInfo) -> None:
        """Based on sim_score it decides what type of removal to use and applies it."""
        (levenshtein_score, phash_score) = sim_score
        auto_remove_sim = SIM_THRESHOLDS[file_info1.get_type()][SimThreshold.AUTO_REMOVE]
        if ((levenshtein_score >= auto_remove_sim or phash_score >= auto_remove_sim)
            and file_info1.is_auto_removable() and file_info2.is_auto_removable()):
            file_infos = self._remove_file_automaticly(file_infos, file_info1)
        else:
            file_infos = self._ask_for_remove(file_infos, sim_score, file_info1, file_info2)