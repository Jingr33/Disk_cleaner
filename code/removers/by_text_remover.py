from removers.remover_base import RemoverBase
from file_data.file_info import FileInfo
from backuper import Backuper
from hashers.hasher import Hasher
from hashers.hash_type_enum import HashType
from config import MIN_SIMILARITY

class ByTextRemover(RemoverBase):
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
        sim_score = Hasher.hamming_similarity_simhash(file_info2.get_text_hash(), file_info1.get_text_hash())
        if sim_score >= MIN_SIMILARITY:
            self._manage_remove(sim_score, file_infos, fi1_idx, fi2_idx)