
import os
import re
import string
import random

from fastapi import UploadFile

from config import get_settings
from enums import ResponseSignal

settings = get_settings()


def validate_uploaded_file(file: UploadFile):
    if file.content_type not in settings.FILE_ALLOWED_TYPES:
        return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

    return True, ResponseSignal.FILE_UPLOAD_SUCCESS.value


def generate_random_string(length: int = 12) -> str:
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def get_clean_file_name(orig_file_name: str) -> str:
    cleaned = re.sub(r"[^\w.]", "", orig_file_name.strip())
    return cleaned.replace(" ", "_")


def get_project_upload_dir(project_id: str) -> str:
    project_dir = os.path.join(settings.UPLOAD_DIR, project_id)
    os.makedirs(project_dir, exist_ok=True)
    return project_dir


def generate_unique_filepath(orig_file_name: str, project_id: str):
    project_dir = get_project_upload_dir(project_id)
    cleaned_name = get_clean_file_name(orig_file_name)

    random_key = generate_random_string()
    file_id = f"{random_key}_{cleaned_name}"
    file_path = os.path.join(project_dir, file_id)

    while os.path.exists(file_path):
        random_key = generate_random_string()
        file_id = f"{random_key}_{cleaned_name}"
        file_path = os.path.join(project_dir, file_id)

    return file_path, file_id


def find_file_path(file_id: str, project_id: str) -> str:
    """
    بندور على الملف جوا مجلد المشروع، لأن الـ file_id بيتخزن
    من غير معرفة المسار الكامل مسبقاً.
    """
    project_dir = get_project_upload_dir(project_id)
    file_path = os.path.join(project_dir, file_id)
    return file_path 

