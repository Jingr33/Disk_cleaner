from file_data.file_type_enum import FileType

SIM_THRESHOLDS = {
    FileType.TEXT : {
        'txt_min_sim' : 0.8,
        'img_min_sim' : None,
        'auto_remove_sim' : 1.0,
    },
        FileType.DOC : {
        'txt_min_sim' : 0.8,
        'img_min_sim' : None,
        'auto_remove_sim' : 1.0,
    },
    FileType.DOCX : {
        'txt_min_sim' : 0.96,
        'img_min_sim' : None,
        'auto_remove_sim' : 1.0,
    },
    FileType.HTML : {
        'txt_min_sim' : 0.8,
        'img_min_sim' : None,
        'auto_remove_sim' : 1.0,
    },
    FileType.SPREADSHEET : {
        'txt_min_sim' : 0.8,
        'img_min_sim' : None,
        'auto_remove_sim' : 1.0,
    },
    FileType.PDF : {
        'txt_min_sim' : 0.94,
        'img_min_sim' : 0.6,
        'auto_remove_sim' : 1.0,
    },
    FileType.PRESENTATION : {
        'txt_min_sim' : 0.9,
        'img_min_sim' : 0.7,
        'auto_remove_sim' : 1.0,
    },
    FileType.IMAGE : {
        'txt_min_sim' : None,
        'img_min_sim' : 0.935,
        'auto_remove_sim' : 1.0,
    },
}