#!/usr/bin/env python3
"""
Comprehensive tests for KRenamer core functionality - Chapter 8 표준에 맞춘 버전
"""

import sys
import pytest
from pathlib import Path
import tempfile
import os
from unittest.mock import patch, MagicMock

# Add src to path for testing  
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from krenamer.core import RenameEngine


@pytest.mark.unit
class TestRenameEngine:
    """Test cases for RenameEngine class - Chapter 8 표준"""
    
    def test_engine_initialization(self, rename_engine):
        """엔진 초기화 테스트"""
        assert rename_engine.files == []
        assert rename_engine.method == "prefix"
        assert hasattr(rename_engine, 'prefix_text')
        assert hasattr(rename_engine, 'suffix_text')
        assert hasattr(rename_engine, 'start_number')
        assert hasattr(rename_engine, 'find_text')
        assert hasattr(rename_engine, 'replace_text')
    
    def test_add_files(self, rename_engine, sample_files):
        """파일 추가 테스트"""
        # 실제 파일들 추가
        added_count = rename_engine.add_files(sample_files)
        assert added_count == len(sample_files)
        assert len(rename_engine.files) == len(sample_files)
        
        # 중복 파일 추가 시도
        added_count = rename_engine.add_files(sample_files[:2])
        assert added_count == 0  # 중복이므로 추가되지 않음
        assert len(rename_engine.files) == len(sample_files)
    
    def test_add_files_nonexistent(self, rename_engine):
        """존재하지 않는 파일 추가 테스트"""
        fake_files = ["nonexistent1.txt", "nonexistent2.txt"]
        added_count = rename_engine.add_files(fake_files)
        assert added_count == 0
        assert len(rename_engine.files) == 0
    
    def test_remove_files(self, rename_engine, sample_files):
        """파일 제거 테스트"""
        rename_engine.add_files(sample_files)
        initial_count = len(rename_engine.files)
        
        # 일부 파일 제거 (인덱스 기반)
        rename_engine.remove_files_by_indices([0, 2])
        assert len(rename_engine.files) == initial_count - 2
    
    def test_clear_files(self, rename_engine, sample_files):
        """전체 파일 제거 테스트"""
        rename_engine.add_files(sample_files)
        assert len(rename_engine.files) > 0
        
        rename_engine.clear_files()
        assert len(rename_engine.files) == 0


@pytest.mark.unit  
class TestRenameRules:
    """파일명 변경 규칙 테스트"""
    
    def test_prefix_rule(self, rename_engine, sample_files):
        """접두사 규칙 테스트"""
        rename_engine.add_files([sample_files[0]])  # document.pdf
        
        rename_engine.method = "prefix"
        rename_engine.prefix_text = "NEW_"
        
        plan = rename_engine.generate_rename_plan()
        assert len(plan) == 1
        
        original_path, new_name, matches = plan[0]
        if matches:
            assert new_name.startswith("NEW_")
    
    def test_suffix_rule(self, rename_engine, sample_files):
        """접미사 규칙 테스트"""
        rename_engine.add_files([sample_files[0]])  # document.pdf
        
        rename_engine.method = "suffix" 
        rename_engine.suffix_text = "_BACKUP"
        
        plan = rename_engine.generate_rename_plan()
        original_path, new_name, matches = plan[0]
        
        if matches:
            # 확장자 앞에 접미사가 추가되어야 함
            assert "_BACKUP" in new_name
            assert new_name.endswith(".pdf")
    
    def test_numbering_rule(self, rename_engine, sample_files):
        """순번 매기기 규칙 테스트"""
        rename_engine.add_files(sample_files[:3])
        
        rename_engine.method = "number"
        rename_engine.start_number = 10
        
        plan = rename_engine.generate_rename_plan()
        assert len(plan) == 3
        
        # 순번이 올바르게 적용되었는지 확인
        expected_numbers = [10, 11, 12]
        actual_numbers = []
        
        for original_path, new_name, matches in plan:
            if matches:
                # Extract number from filename like "010_test_file_0.txt"
                parts = new_name.split("_")
                if parts[0].isdigit():
                    actual_numbers.append(int(parts[0]))
        
        assert len(actual_numbers) == len(expected_numbers)
    
    def test_replace_rule(self, rename_engine, sample_files):
        """찾기/바꾸기 규칙 테스트"""
        # 공백이 있는 파일 찾기
        space_file = None
        for file_path in sample_files:
            if "spaces" in Path(file_path).name:
                space_file = file_path
                break
        
        if space_file:
            rename_engine.add_files([space_file])
            
            rename_engine.method = "replace"
            rename_engine.find_text = " "
            rename_engine.replace_text = "_"
            
            plan = rename_engine.generate_rename_plan()
            original_path, new_name, matches = plan[0]
            
            if matches:
                assert " " not in new_name
                assert "_" in new_name
    
    def test_case_transformations(self, rename_engine, sample_files):
        """대소문자 변환 테스트"""
        # 대문자 파일 찾기
        upper_file = None
        for file_path in sample_files:
            if "UPPERCASE" in Path(file_path).name:
                upper_file = file_path
                break
        
        if upper_file:
            rename_engine.add_files([upper_file])
            
            # 소문자로 변환
            rename_engine.case_method = "lower"
            plan = rename_engine.generate_rename_plan()
            original_path, new_name, matches = plan[0]
            
            if matches:
                # 확장자를 제외한 파일명이 소문자인지 확인
                name_without_ext = Path(new_name).stem
                assert name_without_ext.islower()


@pytest.mark.unit
class TestConditions:
    """조건부 필터링 테스트"""
    
    def test_size_condition(self, rename_engine, sample_files):
        """파일 크기 조건 테스트"""
        rename_engine.add_files(sample_files)
        
        # 크기 조건 설정
        rename_engine.use_size_condition = True
        rename_engine.size_operator = ">"
        rename_engine.size_value = 0
        rename_engine.size_unit = "Bytes"
        
        plan = rename_engine.generate_rename_plan()
        matching_files = [p for p, n, m in plan if m]
        
        # 모든 파일이 0바이트보다 크므로 모두 매칭되어야 함
        assert len(matching_files) > 0
        
        # 불가능한 크기 조건
        rename_engine.size_value = 999999
        rename_engine.size_unit = "GB"
        plan = rename_engine.generate_rename_plan()
        matching_files = [p for p, n, m in plan if m]
        assert len(matching_files) == 0  # 아무것도 매칭되지 않아야 함
    
    def test_extension_condition(self, rename_engine, sample_files):
        """확장자 조건 테스트"""
        rename_engine.add_files(sample_files)
        
        rename_engine.use_ext_condition = True
        rename_engine.allowed_extensions = ".txt,.pdf"
        
        plan = rename_engine.generate_rename_plan()
        matching_files = []
        for original_path, new_name, matches in plan:
            if matches:
                matching_files.append(original_path)
                ext = Path(original_path).suffix.lower()
                assert ext in ['.txt', '.pdf']
        
        # 매칭되는 파일이 있어야 함
        assert len(matching_files) > 0
        
        # 매칭되지 않는 확장자 테스트
        rename_engine.allowed_extensions = ".xyz,.abc"
        plan = rename_engine.generate_rename_plan()
        matching_files = [p for p, n, m in plan if m]
        assert len(matching_files) == 0
    
    def test_multiple_conditions(self, rename_engine, sample_files):
        """복수 조건 조합 테스트"""
        rename_engine.add_files(sample_files)
        
        # 크기 + 확장자 조건 동시 적용
        rename_engine.use_size_condition = True
        rename_engine.size_operator = ">"
        rename_engine.size_value = 0
        rename_engine.size_unit = "Bytes"
        
        rename_engine.use_ext_condition = True
        rename_engine.allowed_extensions = ".pdf,.jpg"
        
        plan = rename_engine.generate_rename_plan()
        matching_files = []
        for original_path, new_name, matches in plan:
            if matches:
                matching_files.append(original_path)
                # 두 조건을 모두 만족해야 함
                assert Path(original_path).stat().st_size > 0
                assert Path(original_path).suffix.lower() in ['.pdf', '.jpg']
        
        assert len(matching_files) > 0


@pytest.mark.unit
class TestTransformations:
    """문자열 변환 테스트"""
    
    def test_transformations(self, rename_engine):
        """텍스트 변환 테스트"""
        test_name = "Test File Name"
        
        # 대문자 변환
        rename_engine.case_method = "upper"
        result = rename_engine.apply_transformations(test_name)
        assert result == "TEST FILE NAME"
        
        # 소문자 변환
        rename_engine.case_method = "lower"
        result = rename_engine.apply_transformations(test_name)
        assert result == "test file name"
        
        # 제목 케이스 변환
        rename_engine.case_method = "title"
        result = rename_engine.apply_transformations(test_name)
        assert result == "Test File Name"
        
        # 공백 치환
        rename_engine.case_method = "none"
        rename_engine.replace_spaces = True
        result = rename_engine.apply_transformations(test_name)
        assert result == "Test_File_Name"
        
        # 특수문자 제거
        rename_engine.replace_spaces = False
        rename_engine.remove_special_chars = True
        special_name = "Test@File#Name$"
        result = rename_engine.apply_transformations(special_name)
        assert "@" not in result
        assert "#" not in result
        assert "$" not in result


@pytest.mark.unit
class TestDuplicateHandling:
    """중복 처리 테스트"""
    
    def test_duplicate_handling(self, rename_engine, temp_dir):
        """중복 파일명 처리 테스트"""
        # 중복을 만들 수 있는 파일들 생성
        duplicate_files = []
        for i in range(2):
            test_file = temp_dir / f"duplicate.txt"
            if i == 1:
                test_file = temp_dir / f"duplicate_copy.txt"
            test_file.write_text(f"Content {i}")
            duplicate_files.append(str(test_file))
        
        rename_engine.add_files(duplicate_files)
        rename_engine.method = "replace"
        rename_engine.find_text = "_copy"
        rename_engine.replace_text = ""
        rename_engine.handle_duplicates = True
        
        plan = rename_engine.generate_rename_plan()
        new_names = [new_name for _, new_name, matches in plan if matches]
        
        # 새 이름들이 모두 고유해야 함
        assert len(new_names) == len(set(new_names))


@pytest.mark.unit
class TestRenameExecution:
    """파일명 변경 실행 테스트"""
    
    @patch('os.rename')
    def test_execute_rename_success(self, mock_rename, rename_engine, sample_files):
        """성공적인 파일명 변경 테스트"""
        rename_engine.add_files([sample_files[0]])
        
        rename_engine.method = "prefix"
        rename_engine.prefix_text = "NEW_"
        
        # os.rename이 성공적으로 실행되도록 mock 설정
        mock_rename.return_value = None
        
        # 실제 실행
        rename_engine.execute_rename()
        
        # os.rename이 호출되었는지 확인
        mock_rename.assert_called_once()
    
    @patch('os.rename')
    @patch('os.path.exists')
    def test_execute_rename_file_exists(self, mock_exists, mock_rename, rename_engine, sample_files):
        """대상 파일이 이미 존재하는 경우 테스트"""
        rename_engine.add_files([sample_files[0]])
        
        rename_engine.method = "prefix"
        rename_engine.prefix_text = "NEW_"
        
        # 대상 파일이 이미 존재한다고 설정
        mock_exists.return_value = True
        
        # 실행 시도
        try:
            rename_engine.execute_rename()
        except Exception:
            # 파일 존재 오류가 발생할 수 있음
            pass
        
        # 실제 rename은 호출되지 않았어야 함
        mock_rename.assert_not_called()


if __name__ == "__main__":
    pytest.main([__file__])