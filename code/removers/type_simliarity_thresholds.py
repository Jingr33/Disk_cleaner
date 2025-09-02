from file_data.file_type_enum import FileType
from removers.similarity_threshold_keys_enum import SimThreshold

SIM_THRESHOLDS = {
    FileType.TEXT : {
        SimThreshold.SIMHASH_MIN : 0.7,
        SimThreshold.LEVENSHTEIN_MIN : 0.7,
        SimThreshold.PHASH_MIN : None,
        SimThreshold.AUTO_REMOVE : 1.0,
    },
    FileType.WORD : {
        SimThreshold.SIMHASH_MIN : 0.65,
        SimThreshold.LEVENSHTEIN_MIN : 0.7,
        SimThreshold.PHASH_MIN : None,
        SimThreshold.AUTO_REMOVE : 1.0,
    },
    FileType.HTML : {
        SimThreshold.SIMHASH_MIN : 0.7,
        SimThreshold.LEVENSHTEIN_MIN : 0.7,
        SimThreshold.PHASH_MIN : None,
        SimThreshold.AUTO_REMOVE : 1.0,
    },
    FileType.SPREADSHEET : {
        SimThreshold.SIMHASH_MIN : 0.7,
        SimThreshold.LEVENSHTEIN_MIN : 0.7,
        SimThreshold.PHASH_MIN : None,
        SimThreshold.AUTO_REMOVE : 1.0,
    },
    FileType.PDF : {
        SimThreshold.SIMHASH_MIN : 0.65,
        SimThreshold.LEVENSHTEIN_MIN : 0.7,
        SimThreshold.PHASH_MIN : 0.6,
        SimThreshold.AUTO_REMOVE : 1.0,
    },
    FileType.PRESENTATION : {
        SimThreshold.SIMHASH_MIN : 0.6,
        SimThreshold.LEVENSHTEIN_MIN : 0.65,
        SimThreshold.PHASH_MIN : 0.50,
        SimThreshold.AUTO_REMOVE : 1.0,
    },
    FileType.IMAGE : {
        SimThreshold.SIMHASH_MIN : None,
        SimThreshold.LEVENSHTEIN_MIN : None,
        SimThreshold.PHASH_MIN : 0.92,
        SimThreshold.AUTO_REMOVE : 0.98,
    },
}