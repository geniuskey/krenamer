"""
테스트 헬퍼 함수들 - Chapter 8 사양에 맞춘 버전
"""

import tempfile
from pathlib import Path
from typing import List, Dict, Union
from unittest.mock import Mock


def create_test_files(directory: Union[Path, str], file_specs: List[Dict]) -> List[str]:
    """테스트 파일들을 생성하고 경로 목록 반환
    
    Args:
        directory: 파일을 생성할 디렉토리
        file_specs: 파일 스펙 리스트
                   [{'name': 'file.txt', 'content': 'content', 'size': 1024}]
    
    Returns:
        생성된 파일 경로 목록
    """
    directory = Path(directory)
    file_paths = []
    
    for spec in file_specs:
        file_path = directory / spec['name']
        
        if 'content' in spec:
            content = spec['content']
        elif 'size' in spec:
            content = 'x' * spec['size']
        else:
            content = f"Test content for {spec['name']}"
        
        file_path.write_text(content, encoding='utf-8')
        file_paths.append(str(file_path))
    
    return file_paths


def assert_filename_pattern(filename: str, pattern: str) -> bool:
    """파일명이 패턴을 만족하는지 확인"""
    import re
    return bool(re.match(pattern, filename))


def count_files_by_extension(file_paths: List[str]) -> Dict[str, int]:
    """확장자별 파일 개수 계산"""
    from collections import Counter
    extensions = [Path(f).suffix.lower() for f in file_paths]
    return dict(Counter(extensions))


def create_sample_directory_structure(base_dir: Union[Path, str]) -> Dict[str, List[str]]:
    """샘플 디렉토리 구조 생성
    
    Returns:
        {'root_files': [...], 'sub_files': [...]}
    """
    base_dir = Path(base_dir)
    
    # 루트 파일들
    root_files = []
    root_specs = [
        {'name': 'document.pdf', 'content': 'PDF content'},
        {'name': 'image.jpg', 'content': 'JPEG content'},
        {'name': 'text file.txt', 'content': 'Text content'},
    ]
    root_files = create_test_files(base_dir, root_specs)
    
    # 서브디렉토리와 파일들
    sub_dir = base_dir / "subdirectory"
    sub_dir.mkdir()
    
    sub_specs = [
        {'name': 'sub_document.pdf', 'content': 'Sub PDF'},
        {'name': 'sub_image.png', 'content': 'Sub PNG'},
    ]
    sub_files = create_test_files(sub_dir, sub_specs)
    
    return {
        'root_files': root_files,
        'sub_files': sub_files
    }


def verify_rename_result(original_path: str, expected_new_name: str, 
                        actual_new_name: str, should_match: bool = True) -> bool:
    """리네임 결과 검증"""
    if should_match:
        return actual_new_name == expected_new_name
    else:
        return original_path == actual_new_name  # 변경되지 않아야 함


def create_files_with_patterns(directory: Union[Path, str], patterns: List[str]) -> List[str]:
    """특정 패턴의 파일들 생성
    
    Args:
        directory: 디렉토리
        patterns: 파일명 패턴들 ['IMG_{:03d}.jpg', 'DOC_{:03d}.pdf']
    
    Returns:
        생성된 파일 경로들
    """
    directory = Path(directory)
    files = []
    
    for i, pattern in enumerate(patterns):
        for j in range(3):  # 각 패턴당 3개 파일
            filename = pattern.format(j + 1)
            file_path = directory / filename
            file_path.write_text(f"Content for {filename}")
            files.append(str(file_path))
    
    return files


class MockFileSystem:
    """파일 시스템 모킹을 위한 헬퍼 클래스"""
    
    def __init__(self):
        self.files = {}
        self.directories = set()
    
    def add_file(self, path: str, content: str = ""):
        """가상 파일 추가"""
        self.files[path] = content
        # 디렉토리도 추가
        parent = str(Path(path).parent)
        self.directories.add(parent)
    
    def exists(self, path: str) -> bool:
        """파일/디렉토리 존재 여부"""
        return path in self.files or path in self.directories
    
    def is_file(self, path: str) -> bool:
        """파일 여부"""
        return path in self.files
    
    def is_dir(self, path: str) -> bool:
        """디렉토리 여부"""
        return path in self.directories
    
    def get_content(self, path: str) -> str:
        """파일 내용 가져오기"""
        return self.files.get(path, "")
    
    def list_files(self, directory: str = "/") -> List[str]:
        """디렉토리 내 파일 목록"""
        return [f for f in self.files.keys() if str(Path(f).parent) == directory]


def setup_mock_filesystem() -> MockFileSystem:
    """모킹된 파일 시스템 설정"""
    mock_fs = MockFileSystem()
    
    # 기본 테스트 파일들 추가
    test_files = [
        "/test/document.pdf",
        "/test/image.jpg",
        "/test/music.mp3",
        "/test/spaces in name.txt",
        "/test/UPPERCASE.DOC"
    ]
    
    for file_path in test_files:
        mock_fs.add_file(file_path, f"Content of {file_path}")
    
    return mock_fs


def create_unicode_test_files(directory: Union[Path, str]) -> List[str]:
    """유니코드 파일명 테스트 파일들 생성"""
    directory = Path(directory)
    unicode_files = []
    
    unicode_specs = [
        {'name': '한글파일.txt', 'content': '한글 내용'},
        {'name': 'Español.doc', 'content': 'Contenido español'},
        {'name': '日本語.pdf', 'content': '日本語の内容'},
        {'name': 'Русский.jpg', 'content': 'Русское содержание'},
    ]
    
    for spec in unicode_specs:
        try:
            file_path = directory / spec['name']
            file_path.write_text(spec['content'], encoding='utf-8')
            unicode_files.append(str(file_path))
        except (UnicodeError, OSError):
            # 일부 시스템에서는 유니코드 파일명을 지원하지 않을 수 있음
            continue
    
    return unicode_files


def create_edge_case_files(directory: Union[Path, str]) -> Dict[str, List[str]]:
    """엣지 케이스 테스트용 파일들 생성"""
    directory = Path(directory)
    
    edge_cases = {
        'empty_files': [],
        'large_files': [],
        'special_chars': [],
        'long_names': []
    }
    
    # 빈 파일들
    for i in range(3):
        file_path = directory / f"empty_{i}.txt"
        file_path.write_text("")
        edge_cases['empty_files'].append(str(file_path))
    
    # 큰 파일들 (1KB)
    for i in range(2):
        file_path = directory / f"large_{i}.txt"
        file_path.write_text("x" * 1024)
        edge_cases['large_files'].append(str(file_path))
    
    # 특수 문자가 있는 파일명들 (실제로는 안전한 이름으로 생성)
    special_names = [
        "file_with_underscores.txt",
        "file-with-dashes.txt", 
        "file.with.dots.txt"
    ]
    for name in special_names:
        file_path = directory / name
        file_path.write_text("special content")
        edge_cases['special_chars'].append(str(file_path))
    
    # 긴 파일명들
    long_name = "very_" * 20 + "long_filename.txt"
    file_path = directory / long_name
    file_path.write_text("long name content")
    edge_cases['long_names'].append(str(file_path))
    
    return edge_cases


def verify_plan_consistency(plan: List, expected_count: int = None, 
                          should_all_match: bool = None) -> bool:
    """리네임 계획의 일관성 검증"""
    if not isinstance(plan, list):
        return False
    
    if expected_count is not None and len(plan) != expected_count:
        return False
    
    # 각 항목이 올바른 형태인지 확인
    for item in plan:
        if not isinstance(item, tuple) or len(item) != 3:
            return False
        
        original, new_name, matches = item
        if not isinstance(original, str) or not isinstance(new_name, str):
            return False
        if not isinstance(matches, bool):
            return False
    
    if should_all_match is not None:
        actual_matches = [matches for _, _, matches in plan]
        if should_all_match and not all(actual_matches):
            return False
        if not should_all_match and any(actual_matches):
            return False
    
    return True


def create_duplicate_prone_files(directory: Union[Path, str]) -> List[str]:
    """중복이 발생하기 쉬운 파일들 생성"""
    directory = Path(directory)
    
    # 비슷한 이름의 파일들 생성
    files = [
        "test.txt",
        "test_1.txt", 
        "test_2.txt",
        "Test.txt",  # 대소문자만 다름
        "test (1).txt",  # 윈도우 스타일 중복
        "test_copy.txt"
    ]
    
    file_paths = []
    for i, name in enumerate(files):
        try:
            file_path = directory / name
            file_path.write_text(f"Content {i}")
            file_paths.append(str(file_path))
        except OSError:
            # 일부 파일명이 시스템에서 지원되지 않을 수 있음
            continue
    
    return file_paths


class TestDataGenerator:
    """테스트 데이터 생성기"""
    
    @staticmethod
    def generate_file_size_variants(directory: Union[Path, str]) -> Dict[str, List[str]]:
        """다양한 크기의 파일들 생성"""
        directory = Path(directory)
        
        size_variants = {
            'tiny': [],      # < 100 bytes
            'small': [],     # 100B - 1KB
            'medium': [],    # 1KB - 10KB
            'large': []      # > 10KB
        }
        
        # Tiny files
        for i in range(3):
            file_path = directory / f"tiny_{i}.txt"
            file_path.write_text("x" * (10 + i * 10))
            size_variants['tiny'].append(str(file_path))
        
        # Small files
        for i in range(3):
            file_path = directory / f"small_{i}.txt"
            file_path.write_text("x" * (200 + i * 100))
            size_variants['small'].append(str(file_path))
        
        # Medium files
        for i in range(2):
            file_path = directory / f"medium_{i}.txt"
            file_path.write_text("x" * (2000 + i * 1000))
            size_variants['medium'].append(str(file_path))
        
        # Large files
        file_path = directory / "large_0.txt"
        file_path.write_text("x" * 15000)
        size_variants['large'].append(str(file_path))
        
        return size_variants
    
    @staticmethod
    def generate_date_variants(directory: Union[Path, str]) -> List[str]:
        """다양한 날짜의 파일들 생성 (실제로는 모두 현재 날짜)"""
        directory = Path(directory)
        
        # 실제 파일 시스템에서는 파일의 생성/수정 날짜를 임의로 설정하기 어려우므로
        # 파일명에 날짜를 포함시켜 날짜 기반 테스트를 위한 파일들 생성
        date_files = [
            "file_20231201.txt",
            "file_20231215.txt", 
            "file_20240101.txt",
            "file_20240215.txt"
        ]
        
        file_paths = []
        for name in date_files:
            file_path = directory / name
            file_path.write_text(f"Content for {name}")
            file_paths.append(str(file_path))
        
        return file_paths


def cleanup_test_files(*file_paths):
    """테스트 파일들 정리"""
    for file_path in file_paths:
        try:
            Path(file_path).unlink(missing_ok=True)
        except Exception:
            # 정리 실패는 무시
            pass