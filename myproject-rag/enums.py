
from enum import Enum 


class ResponseSignal(Enum):
    
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"

    PROCESSING_SUCCESS = "processing_success"
    PROCESSING_FAILED = "processing_failed"
    FILE_NOT_FOUND = "file_not_found"
    FILE_NOT_PROCESSED_YET = "file_not_processed_yet"

    QUESTION_ANSWERED = "question_answered"
    NO_RELEVANT_INFO_FOUND = "no_relevant_info_found"
