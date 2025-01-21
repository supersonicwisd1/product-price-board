# app/core/utils.py
from app.core.config import settings

def get_file_url(file_path: str | None) -> str | None:
    """Convert relative file path to absolute URL"""
    if not file_path:
        return None
    return f"{settings.BASE_URL}/{file_path}"