from removers.remover_base import RemoverBase
from file_data.file_info import FileInfo
from backuper.backuper import Backuper
from hashers.hasher import Hasher
from hashers.hash_type_enum import HashType
from config import AUTO_REMOVE_SIMILARITY, MIN_SIMILARITY

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
        text_sim_score = Hasher.hamming_similarity_simhash(file_info2.get_text_hash(), file_info1.get_text_hash())
        img_sim_score = Hasher.hamming_similarity_simhash(file_info2.get_image_hash(), file_info1.get_image_hash())

        if text_sim_score >= MIN_SIMILARITY:
            self._manage_remove((text_sim_score, img_sim_score), file_infos, fi1_idx, fi2_idx)

    def _manage_remove(self, sim_score : tuple[float], file_infos : list[FileInfo], fi1_idx : int, fi2_idx : int) -> None:
        """Based on sim_score it decides what type of removal to use and applies it."""
        (text_sim_score, img_sim_score) = sim_score
        if ((text_sim_score >= AUTO_REMOVE_SIMILARITY or img_sim_score >= AUTO_REMOVE_SIMILARITY)
            and file_infos[fi1_idx].is_auto_removable() and file_infos[fi2_idx].is_auto_removable()):
            file_infos = self._remove_file_automaticly(file_infos, fi1_idx)
        else:
            file_infos = self._ask_for_remove(file_infos, sim_score, fi1_idx - 1, fi1_idx)