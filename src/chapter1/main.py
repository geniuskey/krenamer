#!/usr/bin/env python3
"""
KRenamer Chapter 1: Python Basics for GUI Development
KRenamer 프로젝트를 위한 파이썬 기초

이 챕터에서는 KRenamer 개발에 필요한 파이썬 기초 개념들을 배웁니다:
- 파이썬 기본 문법과 데이터 타입
- 파일 시스템 조작 (os, pathlib)
- 문자열 처리와 정규표현식
- 예외 처리
- 클래스와 객체지향 프로그래밍
- 모듈과 패키지
"""

import os
import re
from pathlib import Path
from datetime import datetime


def demonstrate_basic_syntax():
    """파이썬 기본 문법 데모"""
    print("=== 파이썬 기본 문법 ===")
    
    # 변수와 데이터 타입
    name = "KRenamer"
    version = 1.0
    is_ready = True
    files = ["file1.txt", "file2.jpg", "file3.pdf"]
    
    print(f"프로젝트: {name} v{version}")
    print(f"준비 상태: {is_ready}")
    print(f"파일 목록: {files}")
    print()


def demonstrate_string_operations():
    """문자열 처리 데모"""
    print("=== 문자열 처리 ===")
    
    filename = "My Document (Copy).txt"
    print(f"원본 파일명: {filename}")
    
    # 문자열 분리
    name, ext = os.path.splitext(filename)
    print(f"이름: '{name}', 확장자: '{ext}'")
    
    # 문자열 변환
    cleaned = filename.replace(" ", "_").replace("(", "").replace(")", "")
    print(f"정리된 파일명: {cleaned}")
    
    # 대소문자 변환
    print(f"소문자: {filename.lower()}")
    print(f"대문자: {filename.upper()}")
    
    # 접두사/접미사 추가
    prefix = "NEW_"
    suffix = "_BACKUP"
    new_name = f"{prefix}{name}{suffix}{ext}"
    print(f"접두사+접미사: {new_name}")
    print()


def demonstrate_regex():
    """정규표현식 데모"""
    print("=== 정규표현식 ===")
    
    filenames = [
        "IMG_20231215_001.jpg",
        "IMG_20231215_002.jpg", 
        "Document_v1.2.pdf",
        "backup_2023_12_15.zip"
    ]
    
    print("원본 파일명들:")
    for filename in filenames:
        print(f"  {filename}")
    
    # 날짜 패턴 찾기
    date_pattern = r'\d{4}_?\d{2}_?\d{2}'
    print(f"\n날짜 패턴 '{date_pattern}' 검색:")
    for filename in filenames:
        match = re.search(date_pattern, filename)
        if match:
            print(f"  {filename} -> 날짜: {match.group()}")
    
    # 패턴 치환
    print("\nIMG_ 패턴을 PHOTO_로 치환:")
    for filename in filenames:
        new_name = re.sub(r'IMG_', 'PHOTO_', filename)
        if new_name != filename:
            print(f"  {filename} -> {new_name}")
    print()


def demonstrate_file_operations():
    """파일 시스템 조작 데모"""
    print("=== 파일 시스템 조작 ===")
    
    # 현재 디렉토리 정보
    current_dir = os.getcwd()
    print(f"현재 디렉토리: {current_dir}")
    
    # pathlib 사용
    path = Path(__file__)
    print(f"현재 파일: {path.name}")
    print(f"디렉토리: {path.parent}")
    print(f"확장자: {path.suffix}")
    
    # 가상의 파일 정보 처리
    demo_files = [
        "C:/Users/user/Documents/report.pdf",
        "C:/Users/user/Pictures/vacation.jpg",
        "C:/Users/user/Music/song.mp3"
    ]
    
    print("\n파일 정보 분석:")
    for file_path in demo_files:
        path = Path(file_path)
        print(f"  파일: {path.name}")
        print(f"    디렉토리: {path.parent}")
        print(f"    확장자: {path.suffix}")
        print(f"    크기: {path.stat().st_size if path.exists() else 'N/A'} bytes")
    print()


def demonstrate_file_size_formatting():
    """파일 크기 포맷팅 데모"""
    print("=== 파일 크기 포맷팅 ===")
    
    def format_file_size(size_bytes):
        """파일 크기를 읽기 쉬운 형태로 변환"""
        if size_bytes == 0:
            return "0B"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                if unit == 'B':
                    return f"{int(size_bytes)}{unit}"
                else:
                    return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.1f}TB"
    
    # 다양한 크기 테스트
    sizes = [0, 512, 1024, 1536, 1048576, 1073741824, 1099511627776]
    for size in sizes:
        formatted = format_file_size(size)
        print(f"  {size:>12} bytes = {formatted}")
    print()


def demonstrate_error_handling():
    """예외 처리 데모"""
    print("=== 예외 처리 ===")
    
    def safe_file_rename(old_path, new_path):
        """안전한 파일명 변경"""
        try:
            # 파일 존재 확인
            if not os.path.exists(old_path):
                raise FileNotFoundError(f"파일을 찾을 수 없습니다: {old_path}")
            
            # 대상 파일 중복 확인
            if os.path.exists(new_path):
                raise FileExistsError(f"같은 이름의 파일이 이미 존재합니다: {new_path}")
            
            # 파일명 변경 시뮬레이션
            print(f"  ✓ {old_path} -> {new_path}")
            return True
            
        except FileNotFoundError as e:
            print(f"  ✗ 오류: {e}")
            return False
        except FileExistsError as e:
            print(f"  ✗ 오류: {e}")
            return False
        except PermissionError as e:
            print(f"  ✗ 권한 오류: {e}")
            return False
        except Exception as e:
            print(f"  ✗ 예상치 못한 오류: {e}")
            return False
    
    # 테스트 케이스들
    test_cases = [
        ("existing_file.txt", "new_name.txt"),  # 성공 사례
        ("nonexistent.txt", "renamed.txt"),     # 파일 없음
        ("source.txt", "source.txt"),          # 중복 파일명
    ]
    
    print("파일명 변경 시뮬레이션:")
    for old_name, new_name in test_cases:
        safe_file_rename(old_name, new_name)
    print()


class FileRenamer:
    """파일 리네이머 클래스 데모"""
    
    def __init__(self):
        self.files = []
        self.rename_count = 0
    
    def add_file(self, file_path):
        """파일 추가"""
        if file_path not in self.files:
            self.files.append(file_path)
            print(f"파일 추가됨: {file_path}")
    
    def remove_file(self, file_path):
        """파일 제거"""
        if file_path in self.files:
            self.files.remove(file_path)
            print(f"파일 제거됨: {file_path}")
    
    def clear_files(self):
        """모든 파일 제거"""
        count = len(self.files)
        self.files.clear()
        print(f"{count}개 파일이 모두 제거됨")
    
    def apply_prefix(self, prefix):
        """접두사 추가"""
        renamed_files = []
        for file_path in self.files:
            path = Path(file_path)
            new_name = f"{prefix}{path.name}"
            new_path = path.parent / new_name
            renamed_files.append(str(new_path))
            print(f"  {path.name} -> {new_name}")
        return renamed_files
    
    def apply_suffix(self, suffix):
        """접미사 추가"""
        renamed_files = []
        for file_path in self.files:
            path = Path(file_path)
            name_without_ext = path.stem
            new_name = f"{name_without_ext}{suffix}{path.suffix}"
            new_path = path.parent / new_name
            renamed_files.append(str(new_path))
            print(f"  {path.name} -> {new_name}")
        return renamed_files
    
    def apply_numbering(self, start=1, digits=3):
        """순번 매기기"""
        renamed_files = []
        for i, file_path in enumerate(self.files):
            path = Path(file_path)
            number = start + i
            new_name = f"{number:0{digits}d}_{path.name}"
            new_path = path.parent / new_name
            renamed_files.append(str(new_path))
            print(f"  {path.name} -> {new_name}")
        return renamed_files
    
    def get_file_count(self):
        """파일 개수 반환"""
        return len(self.files)


def demonstrate_class_usage():
    """클래스 사용 데모"""
    print("=== 클래스와 객체지향 프로그래밍 ===")
    
    # FileRenamer 인스턴스 생성
    renamer = FileRenamer()
    
    # 파일 추가
    print("1. 파일 추가:")
    test_files = [
        "C:/Documents/report.pdf",
        "C:/Pictures/photo.jpg", 
        "C:/Music/song.mp3"
    ]
    
    for file_path in test_files:
        renamer.add_file(file_path)
    
    print(f"\n현재 파일 개수: {renamer.get_file_count()}")
    
    # 접두사 추가 시뮬레이션
    print("\n2. 접두사 'NEW_' 추가:")
    new_names = renamer.apply_prefix("NEW_")
    
    # 접미사 추가 시뮬레이션  
    print("\n3. 접미사 '_BACKUP' 추가:")
    new_names = renamer.apply_suffix("_BACKUP")
    
    # 순번 매기기 시뮬레이션
    print("\n4. 순번 매기기 (001, 002, ...):")
    new_names = renamer.apply_numbering(start=1, digits=3)
    
    # 파일 제거
    print("\n5. 파일 제거:")
    renamer.remove_file("C:/Pictures/photo.jpg")
    print(f"남은 파일 개수: {renamer.get_file_count()}")
    
    # 전체 제거
    print("\n6. 전체 제거:")
    renamer.clear_files()
    print()


def demonstrate_list_comprehensions():
    """리스트 컴프리헨션과 고급 파이썬 기법 데모"""
    print("=== 리스트 컴프리헨션과 고급 기법 ===")
    
    files = [
        "document.pdf",
        "image.jpg",
        "music.mp3", 
        "archive.zip",
        "text.txt",
        "photo.png"
    ]
    
    print(f"원본 파일들: {files}")
    
    # 리스트 컴프리헨션으로 확장자 필터링
    image_files = [f for f in files if f.endswith(('.jpg', '.png'))]
    print(f"이미지 파일들: {image_files}")
    
    # 파일명에서 확장자 제거
    names_only = [os.path.splitext(f)[0] for f in files]
    print(f"확장자 제거: {names_only}")
    
    # 조건부 변환
    uppercased = [f.upper() if f.endswith('.txt') else f for f in files]
    print(f"txt 파일만 대문자: {uppercased}")
    
    # 딕셔너리 컴프리헨션
    file_info = {f: os.path.splitext(f)[1] for f in files}
    print(f"파일-확장자 매핑: {file_info}")
    
    # 필터링과 변환을 함께
    processed = [f"processed_{f}" for f in files if len(f) > 8]
    print(f"8글자 이상 파일에 접두사: {processed}")
    print()


def main():
    """메인 함수"""
    print("KRenamer Chapter 1: Python Basics for GUI Development")
    print("=" * 60)
    print("KRenamer 프로젝트를 위한 파이썬 기초 개념들을 학습합니다.")
    print()
    
    # 각 개념 데모 실행
    demonstrate_basic_syntax()
    demonstrate_string_operations()
    demonstrate_regex()
    demonstrate_file_operations()
    demonstrate_file_size_formatting()
    demonstrate_error_handling()
    demonstrate_class_usage()
    demonstrate_list_comprehensions()
    
    print("=" * 60)
    print("✅ Python 기초 학습 완료!")


if __name__ == "__main__":
    main()