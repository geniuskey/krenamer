"""
공통 테스트 픽스처 - Chapter 8 사양에 맞춘 개선된 버전
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from krenamer.core import RenameEngine


@pytest.fixture
def temp_dir():
    """임시 디렉토리 픽스처"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_files(temp_dir):
    """샘플 파일들 생성"""
    files = [
        "document.pdf",
        "image.jpg", 
        "music.mp3",
        "archive.zip",
        "text file with spaces.txt",
        "UPPERCASE.DOC",
        "file_with_numbers_123.pdf",
        "IMG_20231215_001.jpg"
    ]
    
    file_paths = []
    for filename in files:
        file_path = temp_dir / filename
        file_path.write_text(f"Sample content for {filename}")
        file_paths.append(str(file_path))
    
    return file_paths


@pytest.fixture
def rename_engine():
    """RenameEngine 인스턴스"""
    return RenameEngine()


@pytest.fixture
def temp_files():
    """기존 픽스처 호환성 유지"""
    import tempfile
    import shutil
    
    temp_dir = Path(tempfile.mkdtemp())
    test_files = []
    
    # Create some test files
    for i in range(3):
        test_file = temp_dir / f"test_{i}.txt"
        test_file.write_text(f"Test content {i}")
        test_files.append(str(test_file))
    
    yield test_files, temp_dir
    
    # Cleanup
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


@pytest.fixture
def krenamer_engine():
    """기존 픽스처 호환성 유지"""
    from krenamer.core import RenameEngine
    return RenameEngine()


@pytest.fixture
def mock_settings():
    """Mock 설정 객체 - 향후 설정 시스템 구현 시 사용"""
    settings = Mock()
    settings.get.return_value = "default_value"
    settings.get_window_settings.return_value = {
        'size': '800x600',
        'center_on_screen': True
    }
    return settings