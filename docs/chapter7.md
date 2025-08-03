# Chapter 7: 모듈화하기

이번 챕터에서는 지금까지 만든 KRenamer 애플리케이션을 체계적으로 모듈화하여 유지보수성과 확장성을 높여보겠습니다. 단일 파일로 구성된 애플리케이션을 여러 모듈로 분리하고 패키지 구조를 설계해보겠습니다.

## 🎯 학습 목표

- **모듈 분리**<!-- -->를 통한 코드 구조화
- **패키지 설계** 및 `__init__.py` 활용
- **의존성 관리** 및 import 최적화
- **설정 파일** 분리 및 관리
- **확장 가능한 아키텍처** 설계

## 🏗️ 모듈화 아키텍처 설계

### 목표 패키지 구조

```
krenamer/
├── __init__.py
├── main.py                 # 애플리케이션 진입점
├── gui/
│   ├── __init__.py
│   ├── main_window.py      # 메인 윈도우
│   ├── widgets.py          # 커스텀 위젯들
│   └── dialogs.py          # 대화상자들
├── core/
│   ├── __init__.py
│   ├── renamer.py          # 파일명 변경 엔진
│   ├── filters.py          # 조건 필터들
│   └── validators.py       # 유효성 검사
├── utils/
│   ├── __init__.py
│   ├── file_utils.py       # 파일 시스템 유틸리티
│   ├── string_utils.py     # 문자열 처리 유틸리티
│   └── format_utils.py     # 포맷팅 유틸리티
├── config/
│   ├── __init__.py
│   ├── settings.py         # 설정 관리
│   └── constants.py        # 상수 정의
└── resources/
    ├── icons/              # 아이콘 파일들
    └── themes/             # 테마 파일들
```

## 💻 모듈 분리 구현

### 1. 설정 및 상수 모듈

먼저 설정과 상수를 별도 모듈로 분리합니다.

```python title="src/krenamer-ch7/krenamer/config/constants.py"
"""
KRenamer 상수 정의
"""

# 애플리케이션 정보
APP_NAME = "KRenamer"
APP_VERSION = "1.0.0"
APP_AUTHOR = "KRenamer Team"

# GUI 설정
DEFAULT_WINDOW_SIZE = "1000x700"
MIN_WINDOW_SIZE = (800, 500)
DEFAULT_FONT = ("맑은 고딕", 9)
TITLE_FONT = ("맑은 고딕", 12, "bold")

# 파일 처리 설정
MAX_FILE_SIZE = 10 * 1024 * 1024 * 1024  # 10GB
SUPPORTED_EXTENSIONS = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
    'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.hwp'],
    'music': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
    'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz']
}

# 리네임 방식
RENAME_METHODS = {
    'prefix': '접두사 추가',
    'suffix': '접미사 추가', 
    'number': '순번 매기기',
    'replace': '찾기/바꾸기',
    'regex': '정규표현식',
    'case': '대소문자 변경'
}

# 기본값
DEFAULT_RENAME_METHOD = 'prefix'
DEFAULT_START_NUMBER = 1
DEFAULT_DIGITS = 3
DEFAULT_CASE_SENSITIVE = True

# UI 메시지
MESSAGES = {
    'no_files': '파일이 선택되지 않았습니다.',
    'add_success': '{count}개 파일이 추가되었습니다.',
    'remove_success': '{count}개 파일이 제거되었습니다.',
    'rename_success': '{count}개 파일의 이름이 변경되었습니다.',
    'rename_error': '파일명 변경 중 오류가 발생했습니다.',
    'duplicate_file': '같은 이름의 파일이 이미 존재합니다.',
    'file_not_found': '파일을 찾을 수 없습니다.',
    'permission_denied': '파일 접근 권한이 없습니다.'
}
```

```python title="src/krenamer-ch7/krenamer/config/settings.py"
"""
KRenamer 설정 관리
"""

import json
import os
from pathlib import Path
from .constants import *


class Settings:
    """설정 관리 클래스"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.krenamer'
        self.config_file = self.config_dir / 'settings.json'
        self.settings = self._load_default_settings()
        self.load()
    
    def _load_default_settings(self):
        """기본 설정 로드"""
        return {
            'window': {
                'size': DEFAULT_WINDOW_SIZE,
                'remember_size': True,
                'center_on_screen': True
            },
            'ui': {
                'font_family': DEFAULT_FONT[0],
                'font_size': DEFAULT_FONT[1],
                'theme': 'default',
                'language': 'ko'
            },
            'behavior': {
                'confirm_before_rename': True,
                'show_preview': True,
                'remember_last_method': True,
                'auto_refresh': True
            },
            'paths': {
                'last_directory': str(Path.home()),
                'recent_directories': []
            },
            'rename': {
                'default_method': DEFAULT_RENAME_METHOD,
                'case_sensitive': DEFAULT_CASE_SENSITIVE,
                'preserve_extension': True
            }
        }
    
    def load(self):
        """설정 파일에서 로드"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    self._merge_settings(loaded_settings)
        except Exception as e:
            print(f"설정 로드 실패: {e}")
    
    def save(self):
        """설정 파일에 저장"""
        try:
            self.config_dir.mkdir(exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"설정 저장 실패: {e}")
    
    def _merge_settings(self, loaded_settings):
        """로드된 설정을 기본 설정과 병합"""
        for category, values in loaded_settings.items():
            if category in self.settings:
                self.settings[category].update(values)
    
    def get(self, category, key, default=None):
        """설정값 가져오기"""
        return self.settings.get(category, {}).get(key, default)
    
    def set(self, category, key, value):
        """설정값 설정하기"""
        if category not in self.settings:
            self.settings[category] = {}
        self.settings[category][key] = value
    
    def get_window_settings(self):
        """윈도우 설정 반환"""
        return self.settings['window']
    
    def get_ui_settings(self):
        """UI 설정 반환"""
        return self.settings['ui']
    
    def get_behavior_settings(self):
        """동작 설정 반환"""
        return self.settings['behavior']


# 전역 설정 인스턴스
app_settings = Settings()
```

### 2. 유틸리티 모듈들

```python title="src/krenamer-ch7/krenamer/utils/file_utils.py"
"""
파일 시스템 관련 유틸리티
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional


def get_file_info(file_path: str) -> dict:
    """파일 정보 반환"""
    try:
        path = Path(file_path)
        stat = path.stat()
        
        return {
            'name': path.name,
            'stem': path.stem,
            'suffix': path.suffix,
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'created': datetime.fromtimestamp(stat.st_ctime),
            'parent': str(path.parent),
            'absolute': str(path.absolute())
        }
    except Exception as e:
        return {'error': str(e)}


def format_file_size(size_bytes: int) -> str:
    """파일 크기를 읽기 쉬운 형태로 변환"""
    if size_bytes == 0:
        return "0B"
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            if unit == 'B':
                return f"{int(size_bytes)}{unit}"
            else:
                return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f}PB"


def is_safe_filename(filename: str) -> bool:
    """안전한 파일명인지 확인"""
    forbidden_chars = '<>:"/\\|?*'
    forbidden_names = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }
    
    # 금지된 문자 확인
    if any(char in filename for char in forbidden_chars):
        return False
    
    # 금지된 이름 확인 (대소문자 무시)
    name_without_ext = Path(filename).stem.upper()
    if name_without_ext in forbidden_names:
        return False
    
    # 길이 확인 (Windows 기준)
    if len(filename) > 255:
        return False
    
    return True


def make_safe_filename(filename: str) -> str:
    """안전한 파일명으로 변환"""
    forbidden_chars = '<>:"/\\|?*'
    safe_filename = filename
    
    # 금지된 문자를 언더스코어로 치환
    for char in forbidden_chars:
        safe_filename = safe_filename.replace(char, '_')
    
    # 연속된 언더스코어 정리
    while '__' in safe_filename:
        safe_filename = safe_filename.replace('__', '_')
    
    # 앞뒤 공백 및 점 제거
    safe_filename = safe_filename.strip(' .')
    
    # 길이 제한
    if len(safe_filename) > 255:
        name, ext = os.path.splitext(safe_filename)
        safe_filename = name[:255-len(ext)] + ext
    
    return safe_filename


def scan_directory(directory: str, recursive: bool = False) -> List[str]:
    """디렉토리에서 파일 목록 스캔"""
    files = []
    try:
        path = Path(directory)
        
        if recursive:
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    files.append(str(file_path))
        else:
            for file_path in path.iterdir():
                if file_path.is_file():
                    files.append(str(file_path))
                    
    except Exception as e:
        print(f"디렉토리 스캔 오류: {e}")
    
    return sorted(files)


def backup_file(file_path: str, backup_dir: Optional[str] = None) -> bool:
    """파일 백업"""
    try:
        source = Path(file_path)
        if not source.exists():
            return False
        
        if backup_dir:
            backup_path = Path(backup_dir)
        else:
            backup_path = source.parent / 'backup'
        
        backup_path.mkdir(exist_ok=True)
        
        # 백업 파일명에 타임스탬프 추가
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"{source.stem}_{timestamp}{source.suffix}"
        backup_file_path = backup_path / backup_filename
        
        shutil.copy2(source, backup_file_path)
        return True
        
    except Exception as e:
        print(f"백업 실패: {e}")
        return False
```

```python title="src/krenamer-ch7/krenamer/utils/string_utils.py"
"""
문자열 처리 관련 유틸리티
"""

import re
import unicodedata
from typing import List, Dict, Optional


def clean_string(text: str) -> str:
    """문자열 정리"""
    # 유니코드 정규화
    text = unicodedata.normalize('NFC', text)
    
    # 불필요한 공백 제거
    text = ' '.join(text.split())
    
    return text


def remove_accents(text: str) -> str:
    """악센트 제거"""
    return ''.join(
        char for char in unicodedata.normalize('NFD', text)
        if unicodedata.category(char) != 'Mn'
    )


def to_snake_case(text: str) -> str:
    """스네이크 케이스로 변환"""
    # 카멜케이스를 스네이크케이스로
    text = re.sub('([a-z0-9])([A-Z])', r'\1_\2', text)
    
    # 공백과 특수문자를 언더스코어로
    text = re.sub(r'[^\w\s]', '_', text)
    text = re.sub(r'\s+', '_', text)
    
    # 연속된 언더스코어 정리
    text = re.sub(r'_+', '_', text)
    
    return text.lower().strip('_')


def to_camel_case(text: str) -> str:
    """카멜케이스로 변환"""
    # 언더스코어와 공백으로 단어 분리
    words = re.split(r'[_\s]+', text.lower())
    
    # 첫 단어는 소문자, 나머지는 첫 글자 대문자
    if words:
        return words[0] + ''.join(word.capitalize() for word in words[1:])
    return text


def extract_numbers(text: str) -> List[int]:
    """문자열에서 숫자 추출"""
    return [int(match) for match in re.findall(r'\d+', text)]


def natural_sort_key(text: str):
    """자연 정렬을 위한 키 생성"""
    def convert(text):
        return int(text) if text.isdigit() else text.lower()
    
    return [convert(c) for c in re.split('([0-9]+)', text)]


def find_common_prefix(strings: List[str]) -> str:
    """문자열 목록의 공통 접두사 찾기"""
    if not strings:
        return ""
    
    min_string = min(strings)
    max_string = max(strings)
    
    for i, char in enumerate(min_string):
        if char != max_string[i]:
            return min_string[:i]
    
    return min_string


def find_common_suffix(strings: List[str]) -> str:
    """문자열 목록의 공통 접미사 찾기"""
    if not strings:
        return ""
    
    # 문자열들을 뒤집어서 접두사 찾기
    reversed_strings = [s[::-1] for s in strings]
    common_prefix = find_common_prefix(reversed_strings)
    
    return common_prefix[::-1]


def batch_replace(text: str, replacements: Dict[str, str]) -> str:
    """일괄 치환"""
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def regex_replace(text: str, pattern: str, replacement: str, flags: int = 0) -> str:
    """정규표현식 치환"""
    try:
        return re.sub(pattern, replacement, text, flags=flags)
    except re.error as e:
        print(f"정규표현식 오류: {e}")
        return text


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """문자열 길이 제한"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def validate_regex_pattern(pattern: str) -> bool:
    """정규표현식 패턴 유효성 검사"""
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False
```

### 3. 코어 모듈 - 파일명 변경 엔진

```python title="src/krenamer-ch7/krenamer/core/krenamer.py"
"""
파일명 변경 엔진
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

from ..utils.file_utils import get_file_info, is_safe_filename, make_safe_filename
from ..utils.string_utils import regex_replace, natural_sort_key
from ..config.constants import RENAME_METHODS


@dataclass
class RenameRule:
    """파일명 변경 규칙"""
    method: str
    parameters: Dict
    enabled: bool = True


@dataclass
class RenameResult:
    """파일명 변경 결과"""
    original_path: str
    new_path: str
    success: bool
    error_message: Optional[str] = None


class RenameEngine:
    """파일명 변경 엔진"""
    
    def __init__(self):
        self.files = []
        self.rules = []
        self.preview_mode = False
    
    def add_files(self, file_paths: List[str]) -> int:
        """파일 목록에 추가"""
        added_count = 0
        for file_path in file_paths:
            if os.path.isfile(file_path) and file_path not in self.files:
                self.files.append(file_path)
                added_count += 1
        return added_count
    
    def remove_files(self, file_paths: List[str]) -> int:
        """파일 목록에서 제거"""
        removed_count = 0
        for file_path in file_paths:
            if file_path in self.files:
                self.files.remove(file_path)
                removed_count += 1
        return removed_count
    
    def clear_files(self):
        """모든 파일 제거"""
        self.files.clear()
    
    def add_rule(self, rule: RenameRule):
        """변경 규칙 추가"""
        self.rules.append(rule)
    
    def clear_rules(self):
        """모든 규칙 제거"""
        self.rules.clear()
    
    def generate_new_names(self) -> List[Tuple[str, str]]:
        """새로운 파일명 생성"""
        if not self.files:
            return []
        
        # 파일 정보 수집
        file_infos = []
        for file_path in self.files:
            info = get_file_info(file_path)
            if 'error' not in info:
                file_infos.append((file_path, info))
        
        # 자연 정렬
        file_infos.sort(key=lambda x: natural_sort_key(x[1]['name']))
        
        result = []
        for i, (file_path, file_info) in enumerate(file_infos):
            new_name = self._apply_rules(file_info, i, len(file_infos))
            new_path = os.path.join(file_info['parent'], new_name)
            result.append((file_path, new_path))
        
        return result
    
    def _apply_rules(self, file_info: Dict, index: int, total: int) -> str:
        """규칙들을 순차적으로 적용"""
        current_name = file_info['name']
        
        for rule in self.rules:
            if not rule.enabled:
                continue
                
            current_name = self._apply_single_rule(
                current_name, file_info, rule, index, total
            )
        
        # 안전한 파일명으로 변환
        return make_safe_filename(current_name)
    
    def _apply_single_rule(self, filename: str, file_info: Dict, 
                          rule: RenameRule, index: int, total: int) -> str:
        """단일 규칙 적용"""
        method = rule.method
        params = rule.parameters
        
        if method == 'prefix':
            return self._apply_prefix(filename, params)
        elif method == 'suffix':
            return self._apply_suffix(filename, params)
        elif method == 'number':
            return self._apply_numbering(filename, params, index)
        elif method == 'replace':
            return self._apply_replace(filename, params)
        elif method == 'regex':
            return self._apply_regex(filename, params)
        elif method == 'case':
            return self._apply_case_change(filename, params)
        
        return filename
    
    def _apply_prefix(self, filename: str, params: Dict) -> str:
        """접두사 추가"""
        prefix = params.get('text', '')
        name, ext = os.path.splitext(filename)
        return f"{prefix}{name}{ext}"
    
    def _apply_suffix(self, filename: str, params: Dict) -> str:
        """접미사 추가"""
        suffix = params.get('text', '')
        name, ext = os.path.splitext(filename)
        return f"{name}{suffix}{ext}"
    
    def _apply_numbering(self, filename: str, params: Dict, index: int) -> str:
        """순번 매기기"""
        start = params.get('start', 1)
        digits = params.get('digits', 3)
        separator = params.get('separator', '_')
        position = params.get('position', 'prefix')  # prefix, suffix
        
        number = start + index
        number_str = f"{number:0{digits}d}"
        
        if position == 'prefix':
            name, ext = os.path.splitext(filename)
            return f"{number_str}{separator}{name}{ext}"
        else:  # suffix
            name, ext = os.path.splitext(filename)
            return f"{name}{separator}{number_str}{ext}"
    
    def _apply_replace(self, filename: str, params: Dict) -> str:
        """찾기/바꾸기"""
        find_text = params.get('find', '')
        replace_text = params.get('replace', '')
        case_sensitive = params.get('case_sensitive', True)
        
        if not find_text:
            return filename
        
        if case_sensitive:
            return filename.replace(find_text, replace_text)
        else:
            # 대소문자 구분 없는 치환
            pattern = re.compile(re.escape(find_text), re.IGNORECASE)
            return pattern.sub(replace_text, filename)
    
    def _apply_regex(self, filename: str, params: Dict) -> str:
        """정규표현식 적용"""
        pattern = params.get('pattern', '')
        replacement = params.get('replacement', '')
        flags = params.get('flags', 0)
        
        return regex_replace(filename, pattern, replacement, flags)
    
    def _apply_case_change(self, filename: str, params: Dict) -> str:
        """대소문자 변경"""
        case_type = params.get('type', 'lower')  # lower, upper, title, sentence
        preserve_extension = params.get('preserve_extension', True)
        
        if preserve_extension:
            name, ext = os.path.splitext(filename)
            if case_type == 'lower':
                return name.lower() + ext
            elif case_type == 'upper':
                return name.upper() + ext
            elif case_type == 'title':
                return name.title() + ext
            elif case_type == 'sentence':
                return name.capitalize() + ext
        else:
            if case_type == 'lower':
                return filename.lower()
            elif case_type == 'upper':
                return filename.upper()
            elif case_type == 'title':
                return filename.title()
            elif case_type == 'sentence':
                return filename.capitalize()
        
        return filename
    
    def execute_rename(self, confirm_callback=None) -> List[RenameResult]:
        """파일명 변경 실행"""
        if self.preview_mode:
            return []
        
        new_names = self.generate_new_names()
        results = []
        
        for original_path, new_path in new_names:
            try:
                # 확인 콜백 호출
                if confirm_callback and not confirm_callback(original_path, new_path):
                    results.append(RenameResult(
                        original_path=original_path,
                        new_path=new_path,
                        success=False,
                        error_message="사용자가 취소함"
                    ))
                    continue
                
                # 파일명이 동일한 경우 건너뛰기
                if original_path == new_path:
                    results.append(RenameResult(
                        original_path=original_path,
                        new_path=new_path,
                        success=True
                    ))
                    continue
                
                # 대상 파일이 이미 존재하는지 확인
                if os.path.exists(new_path):
                    results.append(RenameResult(
                        original_path=original_path,
                        new_path=new_path,
                        success=False,
                        error_message="같은 이름의 파일이 이미 존재합니다"
                    ))
                    continue
                
                # 파일명 변경 실행
                os.rename(original_path, new_path)
                
                results.append(RenameResult(
                    original_path=original_path,
                    new_path=new_path,
                    success=True
                ))
                
                # 내부 파일 목록 업데이트
                if original_path in self.files:
                    index = self.files.index(original_path)
                    self.files[index] = new_path
                
            except Exception as e:
                results.append(RenameResult(
                    original_path=original_path,
                    new_path=new_path,
                    success=False,
                    error_message=str(e)
                ))
        
        return results
    
    def get_file_count(self) -> int:
        """파일 개수 반환"""
        return len(self.files)
    
    def get_files(self) -> List[str]:
        """파일 목록 반환"""
        return self.files.copy()
```

### 4. GUI 모듈화

```python title="src/krenamer-ch7/krenamer/gui/main_window.py"
"""
메인 윈도우 GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox

from ..core.renamer import RenameEngine, RenameRule
from ..config.settings import app_settings
from ..config.constants import *
from .widgets import FileListWidget, RenameOptionsWidget


class MainWindow:
    """메인 윈도우 클래스"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.engine = RenameEngine()
        self.setup_window()
        self.setup_widgets()
        self.setup_bindings()
        
    def setup_window(self):
        """윈도우 설정"""
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        
        # 설정에서 윈도우 크기 가져오기
        window_settings = app_settings.get_window_settings()
        self.root.geometry(window_settings.get('size', DEFAULT_WINDOW_SIZE))
        self.root.minsize(*MIN_WINDOW_SIZE)
        
        if window_settings.get('center_on_screen', True):
            self.center_window()
    
    def center_window(self):
        """윈도우 중앙 배치"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_widgets(self):
        """위젯 설정"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 파일 목록 위젯
        self.file_list = FileListWidget(main_frame, self.engine)
        self.file_list.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 이름 변경 옵션 위젯
        self.rename_options = RenameOptionsWidget(main_frame, self.engine)
        self.rename_options.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 버튼 프레임
        self.setup_buttons(main_frame)
        
        # 상태바
        self.setup_status_bar(main_frame)
        
        # 그리드 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def setup_buttons(self, parent):
        """버튼 설정"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, pady=(0, 10))
        
        # 미리보기 버튼
        self.preview_btn = ttk.Button(
            button_frame,
            text="미리보기",
            command=self.show_preview
        )
        self.preview_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 실행 버튼
        self.execute_btn = ttk.Button(
            button_frame,
            text="이름 변경 실행",
            command=self.execute_rename
        )
        self.execute_btn.pack(side=tk.LEFT)
    
    def setup_status_bar(self, parent):
        """상태바 설정"""
        self.status_var = tk.StringVar()
        self.status_var.set("준비")
        
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=DEFAULT_FONT
        )
        status_label.pack(side=tk.LEFT)
        
        # 파일 개수 표시
        self.file_count_var = tk.StringVar()
        self.update_file_count()
        
        count_label = ttk.Label(
            status_frame,
            textvariable=self.file_count_var,
            font=DEFAULT_FONT
        )
        count_label.pack(side=tk.RIGHT)
    
    def setup_bindings(self):
        """이벤트 바인딩"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 파일 목록 변경 이벤트
        self.file_list.bind_file_change(self.on_file_list_changed)
    
    def on_file_list_changed(self):
        """파일 목록 변경 시 호출"""
        self.update_file_count()
        self.update_button_states()
    
    def update_file_count(self):
        """파일 개수 업데이트"""
        count = self.engine.get_file_count()
        self.file_count_var.set(f"파일: {count}개")
    
    def update_button_states(self):
        """버튼 상태 업데이트"""
        has_files = self.engine.get_file_count() > 0
        state = tk.NORMAL if has_files else tk.DISABLED
        
        self.preview_btn.config(state=state)
        self.execute_btn.config(state=state)
    
    def show_preview(self):
        """미리보기 표시"""
        if not self.engine.get_files():
            messagebox.showwarning("경고", MESSAGES['no_files'])
            return
        
        # 규칙 적용
        self.apply_current_rules()
        
        # 미리보기 생성
        new_names = self.engine.generate_new_names()
        
        # 미리보기 다이얼로그 표시
        self.show_preview_dialog(new_names)
    
    def execute_rename(self):
        """파일명 변경 실행"""
        if not self.engine.get_files():
            messagebox.showwarning("경고", MESSAGES['no_files'])
            return
        
        # 확인 대화상자
        behavior_settings = app_settings.get_behavior_settings()
        if behavior_settings.get('confirm_before_rename', True):
            count = self.engine.get_file_count()
            if not messagebox.askyesno("확인", f"{count}개 파일의 이름을 변경하시겠습니까?"):
                return
        
        # 규칙 적용
        self.apply_current_rules()
        
        # 실행
        results = self.engine.execute_rename()
        
        # 결과 처리
        self.handle_rename_results(results)
    
    def apply_current_rules(self):
        """현재 설정된 규칙들 적용"""
        self.engine.clear_rules()
        rules = self.rename_options.get_rules()
        
        for rule in rules:
            self.engine.add_rule(rule)
    
    def handle_rename_results(self, results):
        """변경 결과 처리"""
        success_count = sum(1 for r in results if r.success)
        error_count = len(results) - success_count
        
        if error_count == 0:
            message = MESSAGES['rename_success'].format(count=success_count)
            messagebox.showinfo("완료", message)
        else:
            errors = [r.error_message for r in results if not r.success]
            error_summary = "\\n".join(errors[:5])
            if len(errors) > 5:
                error_summary += f"\\n... 외 {len(errors)-5}개"
            
            messagebox.showwarning(
                "완료", 
                f"{success_count}개 성공, {error_count}개 실패\\n\\n{error_summary}"
            )
        
        self.status_var.set(f"완료: {success_count}개 성공")
        self.file_list.refresh()
    
    def show_preview_dialog(self, new_names):
        """미리보기 다이얼로그 표시"""
        from .dialogs import PreviewDialog
        
        dialog = PreviewDialog(self.root, new_names)
        dialog.show()
    
    def on_closing(self):
        """앱 종료 시 호출"""
        # 현재 윈도우 크기 저장
        geometry = self.root.geometry()
        app_settings.set('window', 'size', geometry)
        app_settings.save()
        
        self.root.destroy()
    
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()
```

### 5. 패키지 초기화 파일들

```python title="src/krenamer-ch7/krenamer/__init__.py"
"""
KRenamer - 한국형 파일 리네이머

모듈화된 구조로 설계된 파일명 변경 도구
"""

from .config.constants import APP_NAME, APP_VERSION, APP_AUTHOR
from .core.renamer import RenameEngine, RenameRule
from .gui.main_window import MainWindow

__version__ = APP_VERSION
__author__ = APP_AUTHOR

__all__ = [
    'APP_NAME',
    'APP_VERSION', 
    'APP_AUTHOR',
    'RenameEngine',
    'RenameRule',
    'MainWindow'
]
```

```python title="src/krenamer-ch7/krenamer/main.py"
"""
KRenamer 애플리케이션 진입점
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from krenamer.gui.main_window import MainWindow
from krenamer.config.constants import APP_NAME


def main():
    """메인 함수"""
    try:
        app = MainWindow()
        app.run()
    except KeyboardInterrupt:
        print(f"\\n{APP_NAME}이 사용자에 의해 종료되었습니다.")
    except Exception as e:
        print(f"{APP_NAME} 실행 중 오류 발생: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## 🧪 모듈화 테스트

### 구조 확인

```bash
# 패키지 구조 확인
cd src/krenamer-ch7
find krenamer -name "*.py" | head -20

# 모듈 import 테스트
python -c "from krenamer import APP_NAME, APP_VERSION; print(f'{APP_NAME} v{APP_VERSION}')"

# 설정 시스템 테스트  
python -c "from krenamer.config.settings import app_settings; print(app_settings.get('ui', 'font_family'))"
```

### 단위별 테스트

```python title="tests/test_modules.py"
"""모듈 단위 테스트"""

def test_constants_import():
    from krenamer.config.constants import APP_NAME, RENAME_METHODS
    assert APP_NAME == "KRenamer"
    assert 'prefix' in RENAME_METHODS

def test_settings_basic():
    from krenamer.config.settings import Settings
    settings = Settings()
    assert settings.get('ui', 'font_family') is not None

def test_file_utils():
    from krenamer.utils.file_utils import format_file_size, is_safe_filename
    assert format_file_size(1024) == "1.0KB"
    assert is_safe_filename("test.txt") == True
    assert is_safe_filename("con.txt") == False

def test_string_utils():
    from krenamer.utils.string_utils import to_snake_case, clean_string
    assert to_snake_case("CamelCase") == "camel_case"
    assert clean_string("  test  ") == "test"

def test_rename_engine():
    from krenamer.core.renamer import RenameEngine, RenameRule
    engine = RenameEngine()
    assert engine.get_file_count() == 0
    
    rule = RenameRule(method='prefix', parameters={'text': 'NEW_'})
    engine.add_rule(rule)
    assert len(engine.rules) == 1
```

## 🎯 다음 단계 미리보기

모듈화를 완료한 KRenamer는 이제 다음과 같은 고급 기능들을 추가하기 좋은 구조가 되었습니다:

- **Chapter 7**: 단위 테스트 작성 및 테스트 자동화
- **Chapter 8**: MkDocs를 활용한 문서화 시스템  
- **Chapter 9**: GitHub Actions를 통한 CI/CD 파이프라인
- **Chapter 10**: PyPI 패키지 배포
- **Chapter 11**: PyInstaller로 실행 파일 생성

---

!!! success "모듈화 완료!"
    KRenamer가 체계적인 패키지 구조로 모듈화되었습니다!
    
    **달성한 것들:**
    - 기능별 모듈 분리 (GUI, Core, Utils, Config)
    - 설정 시스템 구축
    - 확장 가능한 아키텍처 설계
    - 재사용 가능한 컴포넌트 개발

!!! tip "모듈화의 장점"
    - **유지보수성**: 기능별로 분리되어 수정이 용이
    - **테스트 용이성**: 각 모듈을 독립적으로 테스트 가능
    - **확장성**: 새로운 기능 추가가 간단
    - **재사용성**: 다른 프로젝트에서도 모듈 재사용 가능
    - **협업 효율성**: 팀원들이 각자 다른 모듈 담당 가능