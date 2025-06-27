import os
import uuid
import shutil
from typing import Optional

from fastapi import UploadFile
from pathlib import Path
from datetime import datetime
from src.core.config import settings

UPLOAD_DIR = Path("../static/avatars")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg"]

async def save_avatar(file: UploadFile, user_id: int) -> str:
    # Проверяем тип файла
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError(f"Неподдерживаемый тип файла. Разрешены только: {', '.join(ALLOWED_IMAGE_TYPES)}")
    # Создаем уникальное имя файла
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{user_id}_{uuid.uuid4()}.{file_extension}"
    # Полный путь для сохранения файла
    file_path = UPLOAD_DIR / unique_filename
    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Формируем URL для доступа к файлу
    file_url = f"/static/avatars/{unique_filename}"
    return file_url

async def save_avatar(file: UploadFile, user_id: int, current_avatar_url: Optional[str] = None) -> str:
    # Проверяем тип файла
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError(f"Неподдерживаемый тип файла. Разрешены только: {', '.join(ALLOWED_IMAGE_TYPES)}")
    # Удаляем старый аватар, если он существует
    if current_avatar_url:
        old_avatar_path = UPLOAD_DIR / os.path.basename(current_avatar_url)
        if old_avatar_path.exists():
            old_avatar_path.unlink()
    # Создаем уникальное имя файла
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{user_id}_{uuid.uuid4()}.{file_extension}"
    # Полный путь для сохранения файла
    file_path = UPLOAD_DIR / unique_filename
    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Формируем URL для доступа к файлу
    file_url = f"/static/avatars/{unique_filename}"
    return file_url