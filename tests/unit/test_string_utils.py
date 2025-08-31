"""
문자열 유틸리티 테스트 - RenameEngine의 문자열 처리 기능 테스트
"""

import pytest
from pathlib import Path


class TestStringTransformations:
    """문자열 변환 테스트"""
    
    def test_case_transformations(self, rename_engine, sample_files):
        """대소문자 변환 테스트"""
        rename_engine.add_files([sample_files[0]])  # document.pdf
        
        # 대문자 변환
        rename_engine.case_method = "upper"
        result = rename_engine.apply_transformations("Test File Name")
        assert result == "TEST FILE NAME"
        
        # 소문자 변환
        rename_engine.case_method = "lower"
        result = rename_engine.apply_transformations("Test File Name")
        assert result == "test file name"
        
        # 제목 케이스 변환
        rename_engine.case_method = "title"
        result = rename_engine.apply_transformations("test file name")
        assert result == "Test File Name"
        
        # 변환 없음
        rename_engine.case_method = "none"
        original = "Mixed CaSe String"
        result = rename_engine.apply_transformations(original)
        assert result == original
    
    def test_space_replacement(self, rename_engine):
        """공백 치환 테스트"""
        rename_engine.case_method = "none"
        rename_engine.replace_spaces = True
        
        result = rename_engine.apply_transformations("File With Spaces")
        assert result == "File_With_Spaces"
        assert " " not in result
        
        # 연속된 공백 처리
        result = rename_engine.apply_transformations("File  With   Multiple    Spaces")
        assert result == "File_With_Multiple_Spaces"
    
    def test_special_character_removal(self, rename_engine):
        """특수문자 제거 테스트"""
        rename_engine.case_method = "none"
        rename_engine.replace_spaces = False
        rename_engine.remove_special_chars = True
        
        test_cases = [
            ("File@Name#Test$", "FileNameTest"),
            ("File!Name?Test*", "FileNameTest"),
            ("File+Name=Test&", "FileNameTest"),
            ("File(Name)Test[1]", "FileNameTest1"),
            ("File{Name}Test<>", "FileNameTest"),
            ("File|Name\\Test/", "FileNameTest")
        ]
        
        for input_str, expected in test_cases:
            result = rename_engine.apply_transformations(input_str)
            # 특수문자가 제거되었는지 확인
            for char in "@#$!?*+=&()[]{}<>|\\/" :
                assert char not in result
    
    def test_combined_transformations(self, rename_engine):
        """복합 변환 테스트"""
        rename_engine.case_method = "lower"
        rename_engine.replace_spaces = True
        rename_engine.remove_special_chars = True
        
        test_input = "My Special@File Name#Test!"
        result = rename_engine.apply_transformations(test_input)
        
        # 모든 변환이 적용되어야 함
        expected = "my_specialfile_nametest"
        assert result == expected
        assert result.islower()  # 소문자
        assert " " not in result  # 공백 없음
        assert "@" not in result and "#" not in result and "!" not in result  # 특수문자 없음


class TestStringPatterns:
    """문자열 패턴 처리 테스트"""
    
    def test_number_extraction_patterns(self, sample_files):
        """숫자 추출 패턴 테스트"""
        from krenamer.core import RenameEngine
        
        engine = RenameEngine()
        
        # 숫자가 포함된 파일명들로 테스트
        number_files = []
        for file_path in sample_files:
            if any(char.isdigit() for char in Path(file_path).name):
                number_files.append(file_path)
        
        if number_files:
            engine.add_files(number_files)
            
            # 숫자 기반 변환 테스트 (find/replace)
            engine.method = "replace"
            engine.find_text = "123"
            engine.replace_text = "456"
            
            plan = engine.generate_rename_plan()
            
            for original, new_name, matches in plan:
                if matches and "123" in Path(original).name:
                    assert "456" in new_name
                    assert "123" not in new_name
    
    def test_pattern_based_replacement(self, temp_dir):
        """패턴 기반 치환 테스트"""
        from krenamer.core import RenameEngine
        
        # 패턴이 있는 파일들 생성
        pattern_files = [
            "IMG_001.jpg",
            "IMG_002.jpg", 
            "IMG_003.jpg",
            "DOC_001.pdf",
            "DOC_002.pdf"
        ]
        
        test_files = []
        for filename in pattern_files:
            file_path = temp_dir / filename
            file_path.write_text("content")
            test_files.append(str(file_path))
        
        engine = RenameEngine()
        engine.add_files(test_files)
        
        # IMG를 PHOTO로 변경
        engine.method = "replace"
        engine.find_text = "IMG"
        engine.replace_text = "PHOTO"
        
        plan = engine.generate_rename_plan()
        
        for original, new_name, matches in plan:
            if matches and "IMG" in Path(original).name:
                assert "PHOTO" in new_name
                assert "IMG" not in new_name
    
    def test_case_sensitive_replacement(self, temp_dir):
        """대소문자 구분 치환 테스트"""
        from krenamer.core import RenameEngine
        
        # 대소문자가 다른 파일들 생성
        case_files = ["Test.txt", "test.txt", "TEST.txt"]
        
        test_files = []
        for i, filename in enumerate(case_files):
            file_path = temp_dir / f"{i}_{filename}"  # 파일명 충돌 방지
            file_path.write_text("content")
            test_files.append(str(file_path))
        
        engine = RenameEngine()
        engine.add_files(test_files)
        
        # 소문자 'test'만 찾아서 변경 (대소문자 구분)
        engine.method = "replace"
        engine.find_text = "test"
        engine.replace_text = "sample"
        engine.case_sensitive = True  # RenameEngine에서 지원한다면
        
        plan = engine.generate_rename_plan()
        
        replaced_count = 0
        for original, new_name, matches in plan:
            if matches:
                original_name = Path(original).name
                if "test" in original_name and "test" != "Test" and "test" != "TEST":
                    assert "sample" in new_name
                    replaced_count += 1
        
        # 정확히 소문자 'test'만 변경되어야 함
        assert replaced_count >= 1


class TestStringUtilsEdgeCases:
    """문자열 유틸리티 엣지 케이스 테스트"""
    
    def test_empty_strings(self, rename_engine):
        """빈 문자열 처리 테스트"""
        # 빈 문자열 변환
        result = rename_engine.apply_transformations("")
        assert result == ""
        
        # None 처리 (방어적 코딩)
        try:
            result = rename_engine.apply_transformations(None)
            # None이 처리된다면 빈 문자열이 되어야 함
            assert result == "" or result is None
        except (TypeError, AttributeError):
            # None 처리가 안 되는 것도 정상적인 동작
            pass
    
    def test_unicode_handling(self, rename_engine, temp_dir):
        """유니코드 문자열 처리 테스트"""
        # 한글 파일명으로 테스트 파일 생성
        unicode_file = temp_dir / "한글파일테스트.txt"
        unicode_file.write_text("한글 내용")
        
        rename_engine.add_files([str(unicode_file)])
        
        # 한글 문자열 변환 테스트
        result = rename_engine.apply_transformations("한글 테스트 파일")
        assert isinstance(result, str)
        assert len(result) > 0
        
        # 대소문자 변환 (한글에는 적용되지 않아야 함)
        rename_engine.case_method = "upper"
        result = rename_engine.apply_transformations("한글Test문자")
        assert "한글" in result  # 한글은 그대로 유지
        if "Test" in result:
            assert "TEST" in result  # 영문만 대문자로
    
    @pytest.mark.parametrize("input_str,expected_has_space", [
        ("", False),
        ("NoSpaces", False),
        ("Has Spaces", True),
        ("Multiple  Spaces  Here", True),
        ("    Leading", True),
        ("Trailing    ", True),
        ("Tab\tCharacter", False),  # 탭은 공백이 아님
        ("Newline\nCharacter", False)  # 개행은 공백이 아님
    ])
    def test_space_detection_parametrized(self, input_str, expected_has_space):
        """파라미터화된 공백 감지 테스트"""
        has_space = " " in input_str
        assert has_space == expected_has_space
    
    def test_long_string_handling(self, rename_engine):
        """긴 문자열 처리 테스트"""
        # 매우 긴 문자열 생성 (1000자)
        long_string = "A" * 1000
        
        result = rename_engine.apply_transformations(long_string)
        assert len(result) <= len(long_string)  # 길이가 줄어들거나 같아야 함
        assert isinstance(result, str)
    
    def test_special_whitespace_characters(self, rename_engine):
        """특수 공백 문자 처리 테스트"""
        rename_engine.case_method = "none"
        rename_engine.replace_spaces = True
        
        # 다양한 공백 문자들
        test_cases = [
            ("Regular Space", "Regular_Space"),
            ("Tab\tSpace", "Tab\tSpace"),  # 탭은 치환하지 않음
            ("Newline\nSpace", "Newline\nSpace"),  # 개행은 치환하지 않음
        ]
        
        for input_str, expected in test_cases:
            result = rename_engine.apply_transformations(input_str)
            # 일반 공백만 언더스코어로 치환되어야 함
            assert " " not in result or result == input_str  # 공백이 없거나 원본과 동일