# Chapter 8: 단위 테스트

이번 챕터에서는 Chapter 6에서 모듈화한 KRenamer 애플리케이션에 체계적인 테스트 시스템을 구축해보겠습니다. pytest를 활용한 단위 테스트, 통합 테스트, 그리고 테스트 자동화까지 전문적인 테스트 환경을 만들어보겠습니다.

## 🎯 학습 목표

- **pytest 프레임워크** 활용한 테스트 작성
- **단위 테스트와 통합 테스트** 구분 및 구현
- **테스트 픽스처와 모킹** 활용
- **코드 커버리지** 측정 및 개선
- **테스트 자동화** 및 CI/CD 연동

## 🧪 테스트 환경 설정

### 필요한 패키지 설치

```bash
# 테스트 관련 패키지 설치
pip install pytest pytest-cov pytest-mock pytest-qt
pip install coverage
```

### 테스트 디렉토리 구조

```
tests/
├── __init__.py
├── conftest.py                 # 공통 픽스처
├── unit/                      # 단위 테스트
│   ├── __init__.py
│   ├── test_file_utils.py     # 파일 유틸리티 테스트
│   ├── test_string_utils.py   # 문자열 유틸리티 테스트
│   ├── test_renamer.py        # 리네임 엔진 테스트
│   └── test_settings.py       # 설정 시스템 테스트
├── integration/               # 통합 테스트
│   ├── __init__.py
│   ├── test_rename_workflow.py # 전체 워크플로우 테스트
│   └── test_gui_integration.py # GUI 통합 테스트
├── fixtures/                  # 테스트 데이터
│   ├── sample_files/          # 샘플 파일들
│   └── test_data.json        # 테스트 데이터
└── utils/                     # 테스트 유틸리티
    ├── __init__.py
    └── helpers.py             # 테스트 헬퍼 함수들
```

## 💻 테스트 구현

### 1. 공통 픽스처 설정

```python title="tests/conftest.py"
"""
공통 테스트 픽스처
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src/chapter8"))

from krenamer.core.renamer import RenameEngine
from krenamer.config.settings import Settings


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
def mock_settings():
    """Mock 설정 객체"""
    settings = Mock(spec=Settings)
    settings.get.return_value = "default_value"
    settings.get_window_settings.return_value = {
        'size': '800x600',
        'center_on_screen': True
    }
    return settings
```

### 2. 유틸리티 모듈 테스트

```python title="tests/unit/test_file_utils.py"
"""
파일 유틸리티 테스트
"""

import pytest
import os
from pathlib import Path

from krenamer.utils.file_utils import (
    get_file_info, format_file_size, is_safe_filename, 
    make_safe_filename, scan_directory
)


class TestFileUtils:
    """파일 유틸리티 테스트 클래스"""
    
    def test_format_file_size(self):
        """파일 크기 포맷팅 테스트"""
        assert format_file_size(0) == "0B"
        assert format_file_size(512) == "512B"
        assert format_file_size(1024) == "1.0KB"
        assert format_file_size(1536) == "1.5KB"
        assert format_file_size(1048576) == "1.0MB"
        assert format_file_size(1073741824) == "1.0GB"
    
    def test_is_safe_filename(self):
        """안전한 파일명 검사 테스트"""
        # 안전한 파일명들
        assert is_safe_filename("normal_file.txt") == True
        assert is_safe_filename("file-with-dash.pdf") == True
        assert is_safe_filename("123numbers.jpg") == True
        
        # 위험한 파일명들
        assert is_safe_filename("file<with>brackets.txt") == False
        assert is_safe_filename("file:with:colons.txt") == False
        assert is_safe_filename("file/with/slashes.txt") == False
        assert is_safe_filename("file|with|pipes.txt") == False
        assert is_safe_filename("file?with?questions.txt") == False
        assert is_safe_filename("file*with*stars.txt") == False
        
        # 금지된 이름들
        assert is_safe_filename("CON.txt") == False
        assert is_safe_filename("PRN.pdf") == False
        assert is_safe_filename("AUX.doc") == False
        assert is_safe_filename("NUL.jpg") == False
        assert is_safe_filename("COM1.txt") == False
        assert is_safe_filename("LPT1.txt") == False
    
    def test_make_safe_filename(self):
        """안전한 파일명 생성 테스트"""
        assert make_safe_filename("file<test>.txt") == "file_test_.txt"
        assert make_safe_filename("file:test.txt") == "file_test.txt"
        assert make_safe_filename("file/test\\file.txt") == "file_test_file.txt"
        assert make_safe_filename("file|test|file.txt") == "file_test_file.txt"
        assert make_safe_filename("file?test*file.txt") == "file_test_file.txt"
        
        # 연속된 언더스코어 정리
        assert make_safe_filename("file<<>>test.txt") == "file_test.txt"
        
        # 앞뒤 공백과 점 제거
        assert make_safe_filename("  file.txt  ") == "file.txt"
        assert make_safe_filename("...file.txt...") == "file.txt"
    
    def test_get_file_info(self, sample_files):
        """파일 정보 가져오기 테스트"""
        file_path = sample_files[0]  # document.pdf
        info = get_file_info(file_path)
        
        assert 'error' not in info
        assert info['name'] == "document.pdf"
        assert info['stem'] == "document"
        assert info['suffix'] == ".pdf"
        assert info['size'] > 0
        assert 'modified' in info
        assert 'created' in info
        assert 'parent' in info
        assert 'absolute' in info
    
    def test_get_file_info_nonexistent(self):
        """존재하지 않는 파일 정보 테스트"""
        info = get_file_info("nonexistent_file.txt")
        assert 'error' in info
    
    def test_scan_directory(self, temp_dir, sample_files):
        """디렉토리 스캔 테스트"""
        # 비재귀 스캔
        files = scan_directory(str(temp_dir), recursive=False)
        assert len(files) == len(sample_files)
        
        # 서브디렉토리 생성
        sub_dir = temp_dir / "subdir"
        sub_dir.mkdir()
        sub_file = sub_dir / "sub_file.txt"
        sub_file.write_text("sub content")
        
        # 재귀 스캔
        files_recursive = scan_directory(str(temp_dir), recursive=True)
        assert len(files_recursive) == len(sample_files) + 1
        assert str(sub_file) in files_recursive


@pytest.mark.parametrize("size,expected", [
    (0, "0B"),
    (1, "1B"),
    (1023, "1023B"),
    (1024, "1.0KB"),
    (1536, "1.5KB"),
    (1048576, "1.0MB"),
    (1073741824, "1.0GB"),
    (1099511627776, "1.0TB")
])
def test_format_file_size_parametrized(size, expected):
    """파라미터화된 파일 크기 포맷팅 테스트"""
    assert format_file_size(size) == expected
```

```python title="tests/unit/test_string_utils.py"
"""
문자열 유틸리티 테스트
"""

import pytest
from krenamer.utils.string_utils import (
    clean_string, to_snake_case, to_camel_case,
    extract_numbers, natural_sort_key, find_common_prefix,
    find_common_suffix, validate_regex_pattern
)


class TestStringUtils:
    """문자열 유틸리티 테스트 클래스"""
    
    def test_clean_string(self):
        """문자열 정리 테스트"""
        assert clean_string("  hello   world  ") == "hello world"
        assert clean_string("\\t\\ntest\\r\\n") == "test"
        assert clean_string("multiple    spaces") == "multiple spaces"
    
    def test_to_snake_case(self):
        """스네이크 케이스 변환 테스트"""
        assert to_snake_case("CamelCase") == "camel_case"
        assert to_snake_case("camelCase") == "camel_case"
        assert to_snake_case("UPPERCASE") == "uppercase"
        assert to_snake_case("lowercase") == "lowercase"
        assert to_snake_case("Mixed Case String") == "mixed_case_string"
        assert to_snake_case("file-name.txt") == "file_name_txt"
        assert to_snake_case("file__name") == "file_name"
    
    def test_to_camel_case(self):
        """카멜 케이스 변환 테스트"""
        assert to_camel_case("snake_case") == "snakeCase"
        assert to_camel_case("multiple_words_here") == "multipleWordsHere"
        assert to_camel_case("single") == "single"
        assert to_camel_case("UPPER_CASE") == "upperCase"
        assert to_camel_case("space separated") == "spaceSeparated"
    
    def test_extract_numbers(self):
        """숫자 추출 테스트"""
        assert extract_numbers("file123.txt") == [123]
        assert extract_numbers("IMG_20231215_001.jpg") == [20231215, 1]
        assert extract_numbers("no numbers here") == []
        assert extract_numbers("1 and 2 and 3") == [1, 2, 3]
        assert extract_numbers("version_1.2.3") == [1, 2, 3]
    
    def test_natural_sort_key(self):
        """자연 정렬 키 테스트"""
        files = ["file1.txt", "file10.txt", "file2.txt", "file20.txt"]
        sorted_files = sorted(files, key=natural_sort_key)
        expected = ["file1.txt", "file2.txt", "file10.txt", "file20.txt"]
        assert sorted_files == expected
    
    def test_find_common_prefix(self):
        """공통 접두사 찾기 테스트"""
        assert find_common_prefix(["test1", "test2", "test3"]) == "test"
        assert find_common_prefix(["abc", "def"]) == ""
        assert find_common_prefix(["same", "same"]) == "same"
        assert find_common_prefix([]) == ""
        assert find_common_prefix(["single"]) == "single"
    
    def test_find_common_suffix(self):
        """공통 접미사 찾기 테스트"""
        assert find_common_suffix(["file1.txt", "file2.txt", "file3.txt"]) == ".txt"
        assert find_common_suffix(["abc", "def"]) == ""
        assert find_common_suffix(["same", "same"]) == "same"
        assert find_common_suffix([]) == ""
    
    def test_validate_regex_pattern(self):
        """정규표현식 패턴 검증 테스트"""
        # 유효한 패턴들
        assert validate_regex_pattern(r"\\d+") == True
        assert validate_regex_pattern(r"[a-zA-Z]+") == True
        assert validate_regex_pattern(r"file_\\w+\\.txt") == True
        
        # 잘못된 패턴들
        assert validate_regex_pattern(r"[") == False
        assert validate_regex_pattern(r"*") == False
        assert validate_regex_pattern(r"(?P<>)") == False


class TestStringUtilsEdgeCases:
    """문자열 유틸리티 엣지 케이스 테스트"""
    
    def test_empty_strings(self):
        """빈 문자열 처리 테스트"""
        assert clean_string("") == ""
        assert to_snake_case("") == ""
        assert to_camel_case("") == ""
        assert extract_numbers("") == []
    
    def test_unicode_handling(self):
        """유니코드 처리 테스트"""
        assert clean_string("한글 테스트") == "한글 테스트"
        assert to_snake_case("한글Test") == "한글test"
    
    @pytest.mark.parametrize("input_str,expected", [
        ("", []),
        ("abc", []),
        ("123", [123]),
        ("a1b2c3", [1, 2, 3]),
        ("100,200,300", [100, 200, 300])
    ])
    def test_extract_numbers_parametrized(self, input_str, expected):
        """파라미터화된 숫자 추출 테스트"""
        assert extract_numbers(input_str) == expected
```

### 3. 핵심 모듈 테스트

```python title="tests/unit/test_renamer.py"
"""
리네임 엔진 테스트
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from krenamer.core.renamer import RenameEngine, RenameRule, RenameResult


class TestRenameEngine:
    """리네임 엔진 테스트 클래스"""
    
    def test_init(self):
        """초기화 테스트"""
        engine = RenameEngine()
        assert engine.files == []
        assert engine.rules == []
        assert engine.preview_mode == False
    
    def test_add_files(self, rename_engine, sample_files):
        """파일 추가 테스트"""
        # 실제 파일들 추가
        added_count = rename_engine.add_files(sample_files)
        assert added_count == len(sample_files)
        assert rename_engine.get_file_count() == len(sample_files)
        
        # 중복 파일 추가 시도
        added_count = rename_engine.add_files(sample_files[:2])
        assert added_count == 0  # 중복이므로 추가되지 않음
        assert rename_engine.get_file_count() == len(sample_files)
    
    def test_add_files_nonexistent(self, rename_engine):
        """존재하지 않는 파일 추가 테스트"""
        fake_files = ["nonexistent1.txt", "nonexistent2.txt"]
        added_count = rename_engine.add_files(fake_files)
        assert added_count == 0
        assert rename_engine.get_file_count() == 0
    
    def test_remove_files(self, rename_engine, sample_files):
        """파일 제거 테스트"""
        # 파일 추가
        rename_engine.add_files(sample_files)
        initial_count = rename_engine.get_file_count()
        
        # 일부 파일 제거
        files_to_remove = sample_files[:2]
        removed_count = rename_engine.remove_files(files_to_remove)
        assert removed_count == 2
        assert rename_engine.get_file_count() == initial_count - 2
        
        # 이미 제거된 파일 제거 시도
        removed_count = rename_engine.remove_files(files_to_remove)
        assert removed_count == 0
    
    def test_clear_files(self, rename_engine, sample_files):
        """전체 파일 제거 테스트"""
        rename_engine.add_files(sample_files)
        assert rename_engine.get_file_count() > 0
        
        rename_engine.clear_files()
        assert rename_engine.get_file_count() == 0
    
    def test_add_rule(self, rename_engine):
        """규칙 추가 테스트"""
        rule = RenameRule(method='prefix', parameters={'text': 'NEW_'})
        rename_engine.add_rule(rule)
        assert len(rename_engine.rules) == 1
        assert rename_engine.rules[0] == rule
    
    def test_clear_rules(self, rename_engine):
        """규칙 제거 테스트"""
        rule1 = RenameRule(method='prefix', parameters={'text': 'NEW_'})
        rule2 = RenameRule(method='suffix', parameters={'text': '_OLD'})
        
        rename_engine.add_rule(rule1)
        rename_engine.add_rule(rule2)
        assert len(rename_engine.rules) == 2
        
        rename_engine.clear_rules()
        assert len(rename_engine.rules) == 0


class TestRenameRules:
    """리네임 규칙 테스트 클래스"""
    
    def test_prefix_rule(self, rename_engine, sample_files):
        """접두사 규칙 테스트"""
        rename_engine.add_files([sample_files[0]])  # document.pdf
        
        rule = RenameRule(method='prefix', parameters={'text': 'NEW_'})
        rename_engine.add_rule(rule)
        
        new_names = rename_engine.generate_new_names()
        assert len(new_names) == 1
        
        original_path, new_path = new_names[0]
        new_filename = os.path.basename(new_path)
        assert new_filename == "NEW_document.pdf"
    
    def test_suffix_rule(self, rename_engine, sample_files):
        """접미사 규칙 테스트"""
        rename_engine.add_files([sample_files[0]])  # document.pdf
        
        rule = RenameRule(method='suffix', parameters={'text': '_BACKUP'})
        rename_engine.add_rule(rule)
        
        new_names = rename_engine.generate_new_names()
        original_path, new_path = new_names[0]
        new_filename = os.path.basename(new_path)
        assert new_filename == "document_BACKUP.pdf"
    
    def test_numbering_rule(self, rename_engine, sample_files):
        """순번 매기기 규칙 테스트"""
        rename_engine.add_files(sample_files[:3])
        
        rule = RenameRule(
            method='number', 
            parameters={'start': 1, 'digits': 3, 'separator': '_', 'position': 'prefix'}
        )
        rename_engine.add_rule(rule)
        
        new_names = rename_engine.generate_new_names()
        assert len(new_names) == 3
        
        # 첫 번째 파일 확인
        original_path, new_path = new_names[0]
        new_filename = os.path.basename(new_path)
        assert new_filename.startswith("001_")
    
    def test_replace_rule(self, rename_engine, sample_files):
        """찾기/바꾸기 규칙 테스트"""
        # 공백이 있는 파일 사용
        space_file = None
        for file_path in sample_files:
            if "spaces" in file_path:
                space_file = file_path
                break
        
        assert space_file is not None
        rename_engine.add_files([space_file])
        
        rule = RenameRule(
            method='replace',
            parameters={'find': ' ', 'replace': '_', 'case_sensitive': True}
        )
        rename_engine.add_rule(rule)
        
        new_names = rename_engine.generate_new_names()
        original_path, new_path = new_names[0]
        new_filename = os.path.basename(new_path)
        assert ' ' not in new_filename
        assert '_' in new_filename
    
    def test_case_insensitive_replace(self, rename_engine, sample_files):
        """대소문자 구분 없는 찾기/바꾸기 테스트"""
        # 대문자 파일 사용
        upper_file = None
        for file_path in sample_files:
            if "UPPERCASE" in file_path:
                upper_file = file_path
                break
        
        assert upper_file is not None
        rename_engine.add_files([upper_file])
        
        rule = RenameRule(
            method='replace',
            parameters={'find': 'uppercase', 'replace': 'lowercase', 'case_sensitive': False}
        )
        rename_engine.add_rule(rule)
        
        new_names = rename_engine.generate_new_names()
        original_path, new_path = new_names[0]
        new_filename = os.path.basename(new_path)
        assert "lowercase" in new_filename.lower()
    
    def test_multiple_rules(self, rename_engine, sample_files):
        """복수 규칙 적용 테스트"""
        rename_engine.add_files([sample_files[0]])  # document.pdf
        
        # 접두사 추가 후 접미사 추가
        rule1 = RenameRule(method='prefix', parameters={'text': 'NEW_'})
        rule2 = RenameRule(method='suffix', parameters={'text': '_BACKUP'})
        
        rename_engine.add_rule(rule1)
        rename_engine.add_rule(rule2)
        
        new_names = rename_engine.generate_new_names()
        original_path, new_path = new_names[0]
        new_filename = os.path.basename(new_path)
        assert new_filename == "NEW_document_BACKUP.pdf"
    
    def test_disabled_rule(self, rename_engine, sample_files):
        """비활성화된 규칙 테스트"""
        rename_engine.add_files([sample_files[0]])
        
        rule = RenameRule(
            method='prefix', 
            parameters={'text': 'NEW_'}, 
            enabled=False
        )
        rename_engine.add_rule(rule)
        
        new_names = rename_engine.generate_new_names()
        original_path, new_path = new_names[0]
        
        # 비활성화된 규칙이므로 파일명이 변경되지 않아야 함
        assert original_path == new_path


class TestRenameExecution:
    """파일명 변경 실행 테스트"""
    
    @patch('os.rename')
    def test_execute_rename_success(self, mock_rename, rename_engine, sample_files):
        """성공적인 파일명 변경 테스트"""
        rename_engine.add_files([sample_files[0]])
        
        rule = RenameRule(method='prefix', parameters={'text': 'NEW_'})
        rename_engine.add_rule(rule)
        
        # os.rename이 성공적으로 실행되도록 mock 설정
        mock_rename.return_value = None
        
        results = rename_engine.execute_rename()
        assert len(results) == 1
        assert results[0].success == True
        assert results[0].error_message is None
        
        # os.rename이 호출되었는지 확인
        mock_rename.assert_called_once()
    
    @patch('os.rename')
    @patch('os.path.exists')
    def test_execute_rename_file_exists(self, mock_exists, mock_rename, rename_engine, sample_files):
        """대상 파일이 이미 존재하는 경우 테스트"""
        rename_engine.add_files([sample_files[0]])
        
        rule = RenameRule(method='prefix', parameters={'text': 'NEW_'})
        rename_engine.add_rule(rule)
        
        # 대상 파일이 이미 존재한다고 설정
        mock_exists.return_value = True
        
        results = rename_engine.execute_rename()
        assert len(results) == 1
        assert results[0].success == False
        assert "이미 존재" in results[0].error_message
        
        # os.rename이 호출되지 않았는지 확인
        mock_rename.assert_not_called()
    
    @patch('os.rename')
    def test_execute_rename_permission_error(self, mock_rename, rename_engine, sample_files):
        """권한 오류 테스트"""
        rename_engine.add_files([sample_files[0]])
        
        rule = RenameRule(method='prefix', parameters={'text': 'NEW_'})
        rename_engine.add_rule(rule)
        
        # os.rename에서 권한 오류 발생하도록 설정
        mock_rename.side_effect = PermissionError("Permission denied")
        
        results = rename_engine.execute_rename()
        assert len(results) == 1
        assert results[0].success == False
        assert "Permission denied" in results[0].error_message
    
    def test_execute_rename_preview_mode(self, rename_engine, sample_files):
        """미리보기 모드 테스트"""
        rename_engine.preview_mode = True
        rename_engine.add_files([sample_files[0]])
        
        rule = RenameRule(method='prefix', parameters={'text': 'NEW_'})
        rename_engine.add_rule(rule)
        
        results = rename_engine.execute_rename()
        assert len(results) == 0  # 미리보기 모드에서는 실행하지 않음
    
    def test_execute_rename_with_callback(self, rename_engine, sample_files):
        """확인 콜백과 함께 실행 테스트"""
        rename_engine.add_files([sample_files[0]])
        
        rule = RenameRule(method='prefix', parameters={'text': 'NEW_'})
        rename_engine.add_rule(rule)
        
        # 확인 콜백이 False 반환하도록 설정
        def confirm_callback(original, new):
            return False
        
        with patch('os.rename') as mock_rename:
            results = rename_engine.execute_rename(confirm_callback=confirm_callback)
            assert len(results) == 1
            assert results[0].success == False
            assert "사용자가 취소" in results[0].error_message
            
            # os.rename이 호출되지 않았는지 확인
            mock_rename.assert_not_called()


@pytest.fixture
def rename_rule_factory():
    """RenameRule 팩토리 픽스처"""
    def _create_rule(method, **params):
        return RenameRule(method=method, parameters=params)
    return _create_rule


def test_rename_rule_creation(rename_rule_factory):
    """RenameRule 생성 테스트"""
    rule = rename_rule_factory('prefix', text='NEW_')
    assert rule.method == 'prefix'
    assert rule.parameters['text'] == 'NEW_'
    assert rule.enabled == True
```

### 4. 통합 테스트

```python title="tests/integration/test_rename_workflow.py"
"""
전체 워크플로우 통합 테스트
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from krenamer.core.renamer import RenameEngine, RenameRule


class TestRenameWorkflow:
    """리네임 워크플로우 통합 테스트"""
    
    def test_complete_rename_workflow(self, temp_dir):
        """완전한 리네임 워크플로우 테스트"""
        # 1. 테스트 파일들 생성
        test_files = []
        for i in range(3):
            file_path = temp_dir / f"test_file_{i}.txt"
            file_path.write_text(f"Content {i}")
            test_files.append(str(file_path))
        
        # 2. 엔진 초기화 및 파일 추가
        engine = RenameEngine()
        added_count = engine.add_files(test_files)
        assert added_count == 3
        
        # 3. 규칙 추가
        prefix_rule = RenameRule(method='prefix', parameters={'text': 'NEW_'})
        number_rule = RenameRule(
            method='number', 
            parameters={'start': 1, 'digits': 2, 'separator': '_', 'position': 'suffix'}
        )
        
        engine.add_rule(prefix_rule)
        engine.add_rule(number_rule)
        
        # 4. 미리보기 생성
        new_names = engine.generate_new_names()
        assert len(new_names) == 3
        
        # 5. 파일명 확인
        for i, (original, new) in enumerate(new_names):
            new_filename = Path(new).name
            # 접두사와 순번이 모두 적용되어야 함
            assert new_filename.startswith("NEW_")
            assert f"_{i+1:02d}_" in new_filename
        
        # 6. 실제 실행 (mocking)
        with patch('os.rename') as mock_rename:
            results = engine.execute_rename()
            
            # 모든 파일이 성공적으로 처리되어야 함
            assert len(results) == 3
            assert all(r.success for r in results)
            
            # os.rename이 3번 호출되어야 함
            assert mock_rename.call_count == 3
    
    def test_complex_rename_scenario(self, temp_dir):
        """복잡한 리네임 시나리오 테스트"""
        # 다양한 형태의 파일들 생성
        files_data = [
            ("IMG_20231215_001.jpg", "Image content"),
            ("Document with spaces.pdf", "PDF content"),
            ("UPPERCASE_FILE.TXT", "Text content"),
            ("file_with_123_numbers.doc", "Doc content")
        ]
        
        test_files = []
        for filename, content in files_data:
            file_path = temp_dir / filename
            file_path.write_text(content)
            test_files.append(str(file_path))
        
        engine = RenameEngine()
        engine.add_files(test_files)
        
        # 복잡한 규칙 체인 적용
        rules = [
            # 1. 공백을 언더스코어로 변경
            RenameRule(method='replace', parameters={'find': ' ', 'replace': '_', 'case_sensitive': True}),
            # 2. IMG를 PHOTO로 변경
            RenameRule(method='replace', parameters={'find': 'IMG', 'replace': 'PHOTO', 'case_sensitive': True}),
            # 3. 대문자를 소문자로 변경
            RenameRule(method='case', parameters={'type': 'lower', 'preserve_extension': True}),
            # 4. 접두사 추가
            RenameRule(method='prefix', parameters={'text': 'processed_'})
        ]
        
        for rule in rules:
            engine.add_rule(rule)
        
        new_names = engine.generate_new_names()
        
        # 결과 확인
        new_filenames = [Path(new).name for _, new in new_names]
        
        # 모든 파일이 processed_ 접두사를 가져야 함
        assert all(name.startswith('processed_') for name in new_filenames)
        
        # 공백이 언더스코어로 변경되어야 함
        assert any('document_with_spaces' in name.lower() for name in new_filenames)
        
        # IMG가 PHOTO로 변경되어야 함
        assert any('photo_' in name.lower() for name in new_filenames)
        
        # 모든 파일명이 소문자여야 함 (확장자 제외)
        for name in new_filenames:
            stem = Path(name).stem
            assert stem.islower()
    
    def test_error_handling_workflow(self, temp_dir):
        """오류 처리 워크플로우 테스트"""
        # 테스트 파일 생성
        file_path = temp_dir / "test.txt"
        file_path.write_text("content")
        
        engine = RenameEngine()
        engine.add_files([str(file_path)])
        
        # 접두사 규칙 추가
        rule = RenameRule(method='prefix', parameters={'text': 'NEW_'})
        engine.add_rule(rule)
        
        # 대상 파일이 이미 존재하는 상황 시뮬레이션
        target_path = temp_dir / "NEW_test.txt"
        target_path.write_text("existing content")
        
        # 실행
        results = engine.execute_rename()
        
        # 오류가 적절히 처리되어야 함
        assert len(results) == 1
        assert results[0].success == False
        assert "이미 존재" in results[0].error_message
    
    def test_partial_success_workflow(self, temp_dir):
        """부분 성공 워크플로우 테스트"""
        # 여러 테스트 파일 생성
        test_files = []
        for i in range(3):
            file_path = temp_dir / f"file_{i}.txt"
            file_path.write_text(f"content {i}")
            test_files.append(str(file_path))
        
        engine = RenameEngine()
        engine.add_files(test_files)
        
        rule = RenameRule(method='prefix', parameters={'text': 'NEW_'})
        engine.add_rule(rule)
        
        # 하나의 대상 파일이 이미 존재하도록 설정
        existing_file = temp_dir / "NEW_file_1.txt"
        existing_file.write_text("existing")
        
        with patch('os.rename') as mock_rename:
            # 첫 번째와 세 번째 파일은 성공, 두 번째는 실패
            def side_effect(old, new):
                if "file_1" in old:
                    raise FileExistsError("File exists")
                return None
            
            mock_rename.side_effect = side_effect
            
            results = engine.execute_rename()
            
            # 부분 성공 결과 확인
            success_count = sum(1 for r in results if r.success)
            error_count = sum(1 for r in results if not r.success)
            
            assert success_count == 2
            assert error_count == 1


class TestRenameEngineIntegration:
    """RenameEngine 통합 테스트"""
    
    def test_file_list_management(self, temp_dir):
        """파일 목록 관리 통합 테스트"""
        # 초기 파일들 생성
        initial_files = []
        for i in range(5):
            file_path = temp_dir / f"initial_{i}.txt"
            file_path.write_text(f"content {i}")
            initial_files.append(str(file_path))
        
        engine = RenameEngine()
        
        # 파일 추가
        added = engine.add_files(initial_files)
        assert added == 5
        assert engine.get_file_count() == 5
        
        # 일부 파일 제거
        removed = engine.remove_files(initial_files[:2])
        assert removed == 2
        assert engine.get_file_count() == 3
        
        # 추가 파일들 생성 및 추가
        additional_files = []
        for i in range(2):
            file_path = temp_dir / f"additional_{i}.txt"
            file_path.write_text(f"additional content {i}")
            additional_files.append(str(file_path))
        
        added = engine.add_files(additional_files)
        assert added == 2
        assert engine.get_file_count() == 5
        
        # 전체 파일 목록 확인
        all_files = engine.get_files()
        assert len(all_files) == 5
        
        # 중복 방지 확인
        added = engine.add_files(additional_files)
        assert added == 0  # 이미 존재하므로 추가되지 않음
        assert engine.get_file_count() == 5
        
        # 전체 제거
        engine.clear_files()
        assert engine.get_file_count() == 0
```

### 5. 테스트 설정 및 자동화

```python title="tests/utils/helpers.py"
"""
테스트 헬퍼 함수들
"""

import tempfile
from pathlib import Path
from typing import List, Dict


def create_test_files(directory: Path, file_specs: List[Dict]) -> List[str]:
    """테스트 파일들을 생성하고 경로 목록 반환
    
    Args:
        directory: 파일을 생성할 디렉토리
        file_specs: 파일 스펙 리스트
                   [{'name': 'file.txt', 'content': 'content', 'size': 1024}]
    
    Returns:
        생성된 파일 경로 목록
    """
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


def setup_mock_filesystem():
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
```

```yaml title="pytest.ini"
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --tb=short
    --cov=krenamer
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    unit: 단위 테스트
    integration: 통합 테스트
    slow: 느린 테스트
    gui: GUI 테스트
```

```makefile title="Makefile"
# 테스트 자동화를 위한 Makefile

.PHONY: test test-unit test-integration test-coverage test-watch clean

# 전체 테스트 실행
test:
	pytest

# 단위 테스트만 실행
test-unit:
	pytest tests/unit/ -m unit

# 통합 테스트만 실행  
test-integration:
	pytest tests/integration/ -m integration

# 커버리지 포함 테스트
test-coverage:
	pytest --cov=krenamer --cov-report=html --cov-report=term

# 테스트 감시 모드
test-watch:
	pytest-watch

# 빠른 테스트 (실패 시 즉시 중단)
test-fast:
	pytest -x --ff

# 병렬 테스트
test-parallel:
	pytest -n auto

# 테스트 결과 정리
clean:
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	find . -name "__pycache__" -type d -exec rm -rf {} +
```
---

!!! success "테스트 시스템 완성!"
    KRenamer에 전문적인 테스트 시스템을 구축했습니다!
    
    **구축한 테스트 시스템:**
    - 유닛 테스트: 개별 모듈 및 함수 테스트
    - 통합 테스트: 전체 워크플로우 테스트
    - 모킹과 픽스처: 안정적이고 격리된 테스트 환경
    - 커버리지 측정: 테스트 품질 관리
    - 자동화 도구: 지속적인 테스트 실행

!!! tip "테스트 베스트 프랙티스"
    - **AAA 패턴**: Arrange, Act, Assert 구조로 테스트 작성
    - **격리된 테스트**: 각 테스트는 독립적으로 실행 가능
    - **의미있는 이름**: 테스트 함수명으로 의도를 명확히 표현
    - **엣지 케이스**: 경계 조건과 예외 상황도 테스트
    - **지속적 실행**: 코드 변경 시마다 자동으로 테스트 실행