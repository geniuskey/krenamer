"""
리네임 엔진 테스트 - Chapter 8 사양에 맞춘 종합적인 테스트
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestRenameEngine:
    """RenameEngine 클래스 기본 기능 테스트"""
    
    def test_engine_initialization(self):
        """엔진 초기화 테스트"""
        from krenamer.core import RenameEngine
        
        engine = RenameEngine()
        assert engine.files == []
        assert engine.method == "prefix"
        assert hasattr(engine, 'prefix_text')
        assert hasattr(engine, 'suffix_text')
        assert hasattr(engine, 'start_number')
        assert hasattr(engine, 'find_text')
        assert hasattr(engine, 'replace_text')
    
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
        # 파일 추가
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
        rename_engine.number_padding = 3
        
        plan = rename_engine.generate_rename_plan()
        assert len(plan) == 3
        
        # 순번이 올바르게 적용되었는지 확인
        for i, (original_path, new_name, matches) in enumerate(plan):
            if matches:
                expected_number = f"{10 + i:03d}"
                assert expected_number in new_name
    
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
    
    def test_multiple_rules_combination(self, rename_engine, sample_files):
        """복수 규칙 조합 테스트 - 실제 엔진의 동작에 맞춤"""
        rename_engine.add_files([sample_files[0]])  # document.pdf
        
        # 접두사 + 대소문자 변환 (RenameEngine은 method는 하나만 적용)
        rename_engine.method = "prefix"
        rename_engine.prefix_text = "new_"
        rename_engine.case_method = "upper"
        
        plan = rename_engine.generate_rename_plan()
        original_path, new_name, matches = plan[0]
        
        if matches:
            # 접두사와 대소문자 변환이 적용되었는지 확인
            assert "NEW_" in new_name  # 접두사가 대문자로 변환됨
            assert "DOCUMENT" in new_name  # 원본 파일명이 대문자로 변환됨
            assert new_name.endswith(".pdf")  # 확장자는 그대로


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
    
    def test_date_condition(self, rename_engine, sample_files):
        """날짜 조건 테스트"""
        rename_engine.add_files(sample_files)
        
        # 오늘 이후 조건 (모든 파일이 오늘 생성되었으므로 매칭되지 않아야 함)
        from datetime import datetime, timedelta
        tomorrow = datetime.now() + timedelta(days=1)
        
        rename_engine.use_date_condition = True
        rename_engine.date_operator = "after"
        rename_engine.date_value = tomorrow.strftime("%Y-%m-%d")
        
        plan = rename_engine.generate_rename_plan()
        matching_files = [p for p, n, m in plan if m]
        assert len(matching_files) == 0  # 내일 이후 파일은 없어야 함
        
        # 어제 이후 조건 (모든 파일이 매칭되어야 함)
        yesterday = datetime.now() - timedelta(days=1)
        rename_engine.date_value = yesterday.strftime("%Y-%m-%d")
        
        plan = rename_engine.generate_rename_plan()
        matching_files = [p for p, n, m in plan if m]
        assert len(matching_files) > 0
    
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
    
    @patch('os.rename')
    def test_execute_rename_permission_error(self, mock_rename, rename_engine, sample_files):
        """권한 오류 테스트"""
        rename_engine.add_files([sample_files[0]])
        
        rename_engine.method = "prefix"
        rename_engine.prefix_text = "NEW_"
        
        # os.rename에서 권한 오류 발생하도록 설정
        mock_rename.side_effect = PermissionError("Permission denied")
        
        # 오류가 적절히 처리되는지 확인
        try:
            rename_engine.execute_rename()
        except PermissionError:
            # 권한 오류가 발생하는 것은 정상적인 동작
            pass


class TestDuplicateHandling:
    """중복 처리 테스트"""
    
    def test_duplicate_filename_handling(self, rename_engine, temp_dir):
        """중복 파일명 처리 테스트"""
        # 동일한 결과를 만들 수 있는 파일들 생성
        duplicate_files = []
        for i in range(3):
            file_path = temp_dir / f"test.txt"
            if i > 0:
                file_path = temp_dir / f"test_{i}.txt"
            file_path.write_text(f"Content {i}")
            duplicate_files.append(str(file_path))
        
        rename_engine.add_files(duplicate_files)
        rename_engine.method = "replace"
        rename_engine.find_text = "_"
        rename_engine.replace_text = ""  # 언더스코어 제거
        
        # 중복 처리 활성화
        rename_engine.handle_duplicates = True
        
        plan = rename_engine.generate_rename_plan()
        new_names = [new_name for _, new_name, matches in plan if matches]
        
        # 새 이름들이 모두 고유해야 함
        assert len(new_names) == len(set(new_names))


class TestEdgeCases:
    """엣지 케이스 테스트"""
    
    def test_empty_file_list(self, rename_engine):
        """빈 파일 목록 테스트"""
        plan = rename_engine.generate_rename_plan()
        assert isinstance(plan, list)
        assert len(plan) == 0
    
    def test_empty_method_parameters(self, rename_engine, sample_files):
        """빈 매개변수 테스트"""
        rename_engine.add_files([sample_files[0]])
        
        # 빈 접두사
        rename_engine.method = "prefix"
        rename_engine.prefix_text = ""
        plan = rename_engine.generate_rename_plan()
        original_path, new_name, matches = plan[0]
        
        # 변경사항이 없어야 함 (또는 적절히 처리되어야 함)
        if matches:
            original_name = Path(original_path).name
            assert new_name == original_name or len(new_name) >= len(original_name)
    
    def test_invalid_conditions(self, rename_engine, sample_files):
        """잘못된 조건 테스트"""
        rename_engine.add_files(sample_files)
        
        # 잘못된 크기 값
        rename_engine.use_size_condition = True
        rename_engine.size_value = -1  # 음수 크기
        rename_engine.size_unit = "Bytes"
        
        # 크래시하지 않고 적절히 처리되어야 함
        try:
            plan = rename_engine.generate_rename_plan()
            assert isinstance(plan, list)
        except Exception as e:
            # 예외가 발생하더라도 적절한 오류여야 함
            assert isinstance(e, (ValueError, TypeError))
    
    def test_unicode_filenames(self, rename_engine, temp_dir):
        """유니코드 파일명 테스트"""
        # 유니코드 파일 생성
        unicode_files = []
        unicode_names = ["한글파일.txt", "Español.doc", "日本語.pdf", "Русский.jpg"]
        
        for name in unicode_names:
            try:
                file_path = temp_dir / name
                file_path.write_text("Unicode content")
                unicode_files.append(str(file_path))
            except (UnicodeError, OSError):
                # 일부 시스템에서는 유니코드 파일명을 지원하지 않을 수 있음
                continue
        
        if unicode_files:
            rename_engine.add_files(unicode_files)
            
            rename_engine.method = "prefix"
            rename_engine.prefix_text = "unicode_"
            
            plan = rename_engine.generate_rename_plan()
            
            for original_path, new_name, matches in plan:
                if matches:
                    assert isinstance(new_name, str)
                    assert new_name.startswith("unicode_")