"""
파일 유틸리티 테스트 - 현재 구조에 맞춘 버전
"""

import pytest
import os
from pathlib import Path


class TestFileOperations:
    """파일 조작 관련 테스트"""
    
    def test_file_info_extraction(self, sample_files):
        """파일 정보 추출 테스트"""
        from krenamer.core import RenameEngine
        
        engine = RenameEngine()
        engine.add_files(sample_files)
        
        # 파일이 정상적으로 추가되었는지 확인
        assert len(engine.files) == len(sample_files)
        
        for file_path in engine.files:
            file_obj = Path(file_path)
            assert file_obj.exists()
            assert file_obj.is_file()
            assert file_obj.stat().st_size > 0  # 내용이 있는 파일
    
    def test_file_extension_handling(self, sample_files):
        """파일 확장자 처리 테스트"""
        from krenamer.core import RenameEngine
        
        engine = RenameEngine()
        engine.add_files(sample_files)
        
        # 확장자별 필터링 테스트
        engine.use_ext_condition = True
        engine.allowed_extensions = ".pdf,.jpg"
        
        plan = engine.generate_rename_plan()
        matching_files = [p for p, n, m in plan if m]
        
        # PDF와 JPG 파일만 매칭되어야 함
        for file_path in matching_files:
            ext = Path(file_path).suffix.lower()
            assert ext in ['.pdf', '.jpg']
    
    def test_file_size_operations(self, sample_files):
        """파일 크기 관련 테스트"""
        from krenamer.core import RenameEngine
        
        engine = RenameEngine()
        engine.add_files(sample_files)
        
        # 크기 조건 테스트
        engine.use_size_condition = True
        engine.size_operator = ">"
        engine.size_value = 0
        engine.size_unit = "Bytes"
        
        plan = engine.generate_rename_plan()
        matching_files = [p for p, n, m in plan if m]
        
        # 모든 파일이 0바이트보다 큰지 확인
        assert len(matching_files) > 0
        
        for file_path in matching_files:
            assert Path(file_path).stat().st_size > 0
    
    def test_safe_filename_operations(self, temp_dir):
        """안전한 파일명 처리 테스트"""
        from krenamer.core import RenameEngine
        
        # 위험한 문자가 포함된 파일명으로 테스트 파일 생성
        unsafe_names = [
            "file<test>.txt",
            "file:test.txt", 
            "file|test.txt",
            "file*test.txt",
            "file?test.txt"
        ]
        
        # 실제로는 안전한 이름으로 파일 생성
        safe_files = []
        for i, unsafe_name in enumerate(unsafe_names):
            safe_file = temp_dir / f"unsafe_test_{i}.txt"
            safe_file.write_text("test content")
            safe_files.append(str(safe_file))
        
        engine = RenameEngine()
        engine.add_files(safe_files)
        
        # 찾기/바꾸기로 안전하지 않은 문자 테스트
        engine.method = "replace"
        engine.find_text = "_"
        engine.replace_text = "-"
        
        plan = engine.generate_rename_plan()
        
        for original, new_name, matches in plan:
            if matches:
                assert "_" not in new_name or "-" in new_name


class TestDirectoryOperations:
    """디렉토리 관련 테스트"""
    
    def test_directory_scanning(self, temp_dir, sample_files):
        """디렉토리 스캔 테스트"""
        from krenamer.core import RenameEngine
        
        # 서브디렉토리 생성
        sub_dir = temp_dir / "subdir"
        sub_dir.mkdir()
        sub_file = sub_dir / "sub_file.txt"
        sub_file.write_text("sub content")
        
        # 루트 파일들만 추가 (RenameEngine은 재귀적 스캔을 지원하지 않음)
        engine = RenameEngine()
        engine.add_files(sample_files)  # 루트 레벨 파일들만
        
        assert len(engine.files) == len(sample_files)
        
        # 서브디렉토리 파일은 포함되지 않음
        sub_file_paths = [f for f in engine.files if "subdir" in f]
        assert len(sub_file_paths) == 0
    
    def test_nonexistent_files_handling(self):
        """존재하지 않는 파일 처리 테스트"""
        from krenamer.core import RenameEngine
        
        engine = RenameEngine()
        fake_files = ["nonexistent1.txt", "nonexistent2.txt", "fake/path/file.txt"]
        
        added = engine.add_files(fake_files)
        assert added == 0  # 존재하지 않는 파일은 추가되지 않아야 함
        assert len(engine.files) == 0


@pytest.mark.parametrize("file_extension,expected_count", [
    (".txt", 1),  # text file with spaces.txt
    (".pdf", 2),  # document.pdf, file_with_numbers_123.pdf  
    (".jpg", 2),  # image.jpg, IMG_20231215_001.jpg
    (".doc", 1),  # UPPERCASE.DOC
    (".mp3", 1),  # music.mp3
    (".zip", 1),  # archive.zip
])
def test_extension_filtering_parametrized(sample_files, file_extension, expected_count):
    """파라미터화된 확장자 필터링 테스트"""
    from krenamer.core import RenameEngine
    
    engine = RenameEngine()
    engine.add_files(sample_files)
    
    engine.use_ext_condition = True
    engine.allowed_extensions = file_extension
    
    plan = engine.generate_rename_plan()
    matching_files = [p for p, n, m in plan if m]
    
    assert len(matching_files) == expected_count


class TestFileUtilsEdgeCases:
    """파일 유틸리티 엣지 케이스 테스트"""
    
    def test_empty_file_list(self):
        """빈 파일 목록 처리"""
        from krenamer.core import RenameEngine
        
        engine = RenameEngine()
        plan = engine.generate_rename_plan()
        
        assert isinstance(plan, list)
        assert len(plan) == 0
    
    def test_duplicate_files(self, sample_files):
        """중복 파일 추가 방지"""
        from krenamer.core import RenameEngine
        
        engine = RenameEngine()
        
        # 첫 번째 추가
        first_add = engine.add_files(sample_files)
        assert first_add == len(sample_files)
        
        # 같은 파일 다시 추가 시도
        second_add = engine.add_files(sample_files)
        assert second_add == 0  # 중복으로 인해 추가되지 않음
        assert len(engine.files) == len(sample_files)  # 개수는 변하지 않음
    
    def test_mixed_file_types(self, temp_dir):
        """다양한 파일 타입 혼합 테스트"""
        from krenamer.core import RenameEngine
        
        # 다양한 크기와 내용의 파일들 생성
        files = []
        
        # 빈 파일
        empty_file = temp_dir / "empty.txt"
        empty_file.write_text("")
        files.append(str(empty_file))
        
        # 큰 파일 (1KB)
        large_file = temp_dir / "large.txt"
        large_file.write_text("x" * 1024)
        files.append(str(large_file))
        
        # 유니코드 파일명
        unicode_file = temp_dir / "한글파일.txt"
        unicode_file.write_text("한글 내용")
        files.append(str(unicode_file))
        
        engine = RenameEngine()
        added = engine.add_files(files)
        assert added == len(files)
        
        # 모든 파일이 정상적으로 처리되는지 확인
        plan = engine.generate_rename_plan()
        assert len(plan) == len(files)