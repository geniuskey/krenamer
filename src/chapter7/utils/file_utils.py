"""
파일 관련 유틸리티 함수들
"""

import os
from datetime import datetime


def get_file_size_mb(file_path):
    """파일 크기를 MB 단위로 반환"""
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except:
        return 0


def format_file_size(size_bytes):
    """파일 크기를 읽기 쉬운 형태로 포맷"""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f}MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f}GB"


def get_file_modified_date(file_path):
    """파일 수정 날짜를 datetime 객체로 반환"""
    try:
        timestamp = os.path.getmtime(file_path)
        return datetime.fromtimestamp(timestamp)
    except:
        return None


def convert_size_to_bytes(size_value, size_unit):
    """크기 값과 단위를 바이트로 변환"""
    if size_unit == "KB":
        return size_value * 1024
    elif size_unit == "MB":
        return size_value * 1024 * 1024
    elif size_unit == "GB":
        return size_value * 1024 * 1024 * 1024
    else:
        return size_value