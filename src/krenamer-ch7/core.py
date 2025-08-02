#!/usr/bin/env python3
"""
KRenamer Core Module - Chapter 6
모듈화된 파일 처리 엔진
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import logging

# 로깅 설정
logger = logging.getLogger(__name__)


class RenameOperation(Enum):
    """리네임 작업 유형"""
    PREFIX = "prefix"
    SUFFIX = "suffix"
    REPLACE = "replace"
    REGEX = "regex"
    NUMBERING = "numbering"
    CASE_CHANGE = "case_change"


@dataclass
class RenameRule:
    """리네임 규칙 정의"""
    operation: RenameOperation
    parameters: Dict[str, Any]
    enabled: bool = True
    priority: int = 0


@dataclass
class FileInfo:
    """파일 정보 구조체"""
    path: Path
    name: str
    stem: str
    suffix: str
    size: int
    modified_time: float
    
    @classmethod
    def from_path(cls, file_path: str) -> 'FileInfo':
        """파일 경로로부터 FileInfo 생성"""
        path = Path(file_path)
        try:
            stat = path.stat()
            return cls(
                path=path,
                name=path.name,
                stem=path.stem,
                suffix=path.suffix,
                size=stat.st_size,
                modified_time=stat.st_mtime
            )
        except OSError as e:
            logger.error(f"Failed to get file info for {file_path}: {e}")
            raise


class RenameStrategy(ABC):
    """리네임 전략 인터페이스"""
    
    @abstractmethod
    def apply(self, file_info: FileInfo, parameters: Dict[str, Any]) -> str:
        """리네임 규칙 적용"""
        pass
    
    @abstractmethod
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """매개변수 유효성 검증"""
        pass


class PrefixStrategy(RenameStrategy):
    """접두사 추가 전략"""
    
    def apply(self, file_info: FileInfo, parameters: Dict[str, Any]) -> str:
        prefix = parameters.get('prefix', '')
        return f"{prefix}{file_info.name}"
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        return 'prefix' in parameters and isinstance(parameters['prefix'], str)


class SuffixStrategy(RenameStrategy):
    """접미사 추가 전략"""
    
    def apply(self, file_info: FileInfo, parameters: Dict[str, Any]) -> str:
        suffix = parameters.get('suffix', '')
        return f"{file_info.stem}{suffix}{file_info.suffix}"
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        return 'suffix' in parameters and isinstance(parameters['suffix'], str)


class ReplaceStrategy(RenameStrategy):
    """찾기/바꾸기 전략"""
    
    def apply(self, file_info: FileInfo, parameters: Dict[str, Any]) -> str:
        find_text = parameters.get('find', '')
        replace_text = parameters.get('replace', '')
        
        new_stem = file_info.stem.replace(find_text, replace_text)
        return f"{new_stem}{file_info.suffix}"
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        return 'find' in parameters and 'replace' in parameters


class RegexStrategy(RenameStrategy):
    """정규표현식 전략"""
    
    def apply(self, file_info: FileInfo, parameters: Dict[str, Any]) -> str:
        pattern = parameters.get('pattern', '')
        replacement = parameters.get('replacement', '')
        flags = parameters.get('flags', 0)
        
        try:
            new_stem = re.sub(pattern, replacement, file_info.stem, flags=flags)
            return f"{new_stem}{file_info.suffix}"
        except re.error as e:
            logger.error(f"Regex error: {e}")
            return file_info.name
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        pattern = parameters.get('pattern', '')
        try:
            re.compile(pattern)
            return True
        except re.error:
            return False


class NumberingStrategy(RenameStrategy):
    """순번 매기기 전략"""
    
    def apply(self, file_info: FileInfo, parameters: Dict[str, Any]) -> str:
        index = parameters.get('index', 0)
        start = parameters.get('start', 1)
        digits = parameters.get('digits', 3)
        position = parameters.get('position', 'prefix')
        
        number = f"{start + index:0{digits}d}"
        
        if position == 'prefix':
            return f"{number}_{file_info.name}"
        else:  # suffix
            return f"{file_info.stem}_{number}{file_info.suffix}"
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        required_params = ['start', 'digits', 'position']
        return all(param in parameters for param in required_params)


class CaseChangeStrategy(RenameStrategy):
    """대소문자 변경 전략"""
    
    def apply(self, file_info: FileInfo, parameters: Dict[str, Any]) -> str:
        case_type = parameters.get('case_type', 'none')
        
        new_stem = file_info.stem
        if case_type == 'upper':
            new_stem = file_info.stem.upper()
        elif case_type == 'lower':
            new_stem = file_info.stem.lower()
        elif case_type == 'title':
            new_stem = file_info.stem.title()
        
        return f"{new_stem}{file_info.suffix}"
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        valid_cases = ['none', 'upper', 'lower', 'title']
        case_type = parameters.get('case_type', 'none')
        return case_type in valid_cases


class RenameEngine:
    """모듈화된 파일 리네임 엔진"""
    
    def __init__(self):
        self.files: List[FileInfo] = []
        self.rules: List[RenameRule] = []
        self.strategies: Dict[RenameOperation, RenameStrategy] = {
            RenameOperation.PREFIX: PrefixStrategy(),
            RenameOperation.SUFFIX: SuffixStrategy(),
            RenameOperation.REPLACE: ReplaceStrategy(),
            RenameOperation.REGEX: RegexStrategy(),
            RenameOperation.NUMBERING: NumberingStrategy(),
            RenameOperation.CASE_CHANGE: CaseChangeStrategy(),
        }
        
        # 이벤트 콜백들
        self.progress_callback: Optional[Callable[[int, int], None]] = None
        self.error_callback: Optional[Callable[[str, str], None]] = None
        
        logger.info("RenameEngine initialized")
    
    def add_file(self, file_path: str) -> bool:
        """파일 추가"""
        try:
            file_info = FileInfo.from_path(file_path)
            
            # 중복 체크
            if not any(f.path == file_info.path for f in self.files):
                self.files.append(file_info)
                logger.info(f"Added file: {file_path}")
                return True
            else:
                logger.warning(f"File already exists: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to add file {file_path}: {e}")
            if self.error_callback:
                self.error_callback(file_path, str(e))
            return False
    
    def remove_file(self, file_path: str) -> bool:
        """파일 제거"""
        initial_count = len(self.files)
        self.files = [f for f in self.files if str(f.path) != file_path]
        
        removed = len(self.files) < initial_count
        if removed:
            logger.info(f"Removed file: {file_path}")
        return removed
    
    def clear_files(self):
        """모든 파일 제거"""
        count = len(self.files)
        self.files.clear()
        logger.info(f"Cleared {count} files")
    
    def add_rule(self, rule: RenameRule) -> None:
        """리네임 규칙 추가"""
        self.rules.append(rule)
        # 우선순위로 정렬
        self.rules.sort(key=lambda r: r.priority)
        logger.info(f"Added rule: {rule.operation}")
    
    def remove_rule(self, operation: RenameOperation) -> bool:
        """리네임 규칙 제거"""
        initial_count = len(self.rules)
        self.rules = [r for r in self.rules if r.operation != operation]
        
        removed = len(self.rules) < initial_count
        if removed:
            logger.info(f"Removed rule: {operation}")
        return removed
    
    def clear_rules(self):
        """모든 규칙 제거"""
        count = len(self.rules)
        self.rules.clear()
        logger.info(f"Cleared {count} rules")
    
    def register_strategy(self, operation: RenameOperation, strategy: RenameStrategy):
        """새로운 전략 등록 (플러그인 지원)"""
        self.strategies[operation] = strategy
        logger.info(f"Registered strategy for: {operation}")
    
    def generate_preview(self) -> List[Tuple[str, str, bool]]:
        """미리보기 생성"""
        preview = []
        
        for i, file_info in enumerate(self.files):
            try:
                new_name = self._apply_rules(file_info, i)
                is_valid = self._validate_filename(new_name, file_info.path.parent)
                preview.append((file_info.name, new_name, is_valid))
                
            except Exception as e:
                logger.error(f"Preview generation failed for {file_info.name}: {e}")
                preview.append((file_info.name, file_info.name, False))
        
        return preview
    
    def _apply_rules(self, file_info: FileInfo, index: int) -> str:
        """모든 규칙을 순서대로 적용"""
        current_name = file_info.name
        current_stem = file_info.stem
        
        # 임시 FileInfo 생성 (규칙 적용 중 변경사항 반영)
        temp_info = FileInfo(
            path=file_info.path,
            name=current_name,
            stem=current_stem,
            suffix=file_info.suffix,
            size=file_info.size,
            modified_time=file_info.modified_time
        )
        
        for rule in self.rules:
            if not rule.enabled:
                continue
                
            strategy = self.strategies.get(rule.operation)
            if not strategy:
                logger.warning(f"No strategy found for: {rule.operation}")
                continue
            
            if not strategy.validate_parameters(rule.parameters):
                logger.warning(f"Invalid parameters for {rule.operation}: {rule.parameters}")
                continue
            
            # 순번 매기기의 경우 인덱스 추가
            params = rule.parameters.copy()
            if rule.operation == RenameOperation.NUMBERING:
                params['index'] = index
            
            try:
                new_name = strategy.apply(temp_info, params)
                
                # 다음 규칙을 위해 temp_info 업데이트
                temp_path = temp_info.path.parent / new_name
                temp_info = FileInfo(
                    path=temp_path,
                    name=new_name,
                    stem=Path(new_name).stem,
                    suffix=Path(new_name).suffix,
                    size=temp_info.size,
                    modified_time=temp_info.modified_time
                )
                
            except Exception as e:
                logger.error(f"Rule application failed {rule.operation}: {e}")
                continue
        
        return temp_info.name
    
    def _validate_filename(self, filename: str, directory: Path) -> bool:
        """파일명 유효성 검증"""
        # 빈 파일명
        if not filename.strip():
            return False
        
        # 금지된 문자 (Windows 기준)
        forbidden_chars = '<>:"/\\|?*'
        if any(char in filename for char in forbidden_chars):
            return False
        
        # 예약된 이름 (Windows)
        reserved_names = {
            'CON', 'PRN', 'AUX', 'NUL',
            'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
            'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
        }
        
        name_without_ext = Path(filename).stem.upper()
        if name_without_ext in reserved_names:
            return False
        
        # 길이 제한
        if len(filename) > 255:
            return False
        
        # 기존 파일과 충돌 체크
        target_path = directory / filename
        if target_path.exists():
            # 자기 자신과 같은 경우는 허용
            original_paths = [f.path for f in self.files]
            if target_path not in original_paths:
                return False
        
        return True
    
    def execute_rename(self) -> Dict[str, Any]:
        """리네임 실행"""
        results = {
            'success': 0,
            'failed': 0,
            'errors': [],
            'renamed_files': []
        }
        
        preview = self.generate_preview()
        total_files = len(preview)
        
        for i, (original_name, new_name, is_valid) in enumerate(preview):
            # 진행률 콜백
            if self.progress_callback:
                self.progress_callback(i + 1, total_files)
            
            if not is_valid:
                results['failed'] += 1
                error_msg = f"{original_name}: 유효하지 않은 파일명"
                results['errors'].append(error_msg)
                
                if self.error_callback:
                    self.error_callback(original_name, "Invalid filename")
                continue
            
            # 실제 파일명 변경
            file_info = self.files[i]
            old_path = file_info.path
            new_path = old_path.parent / new_name
            
            if old_path == new_path:
                # 변경사항이 없는 경우
                results['success'] += 1
                continue
            
            try:
                old_path.rename(new_path)
                results['renamed_files'].append((str(old_path), str(new_path)))
                results['success'] += 1
                
                # 내부 파일 정보 업데이트
                self.files[i] = FileInfo.from_path(str(new_path))
                
                logger.info(f"Renamed: {old_path} -> {new_path}")
                
            except OSError as e:
                results['failed'] += 1
                error_msg = f"{original_name}: {str(e)}"
                results['errors'].append(error_msg)
                
                if self.error_callback:
                    self.error_callback(original_name, str(e))
                
                logger.error(f"Rename failed: {old_path} -> {new_path}: {e}")
        
        logger.info(f"Rename completed: {results['success']} success, {results['failed']} failed")
        return results
    
    def set_progress_callback(self, callback: Callable[[int, int], None]):
        """진행률 콜백 설정"""
        self.progress_callback = callback
    
    def set_error_callback(self, callback: Callable[[str, str], None]):
        """오류 콜백 설정"""
        self.error_callback = callback
    
    def get_file_count(self) -> int:
        """파일 개수 반환"""
        return len(self.files)
    
    def get_rule_count(self) -> int:
        """규칙 개수 반환"""
        return len(self.rules)
    
    def get_statistics(self) -> Dict[str, Any]:
        """통계 정보 반환"""
        if not self.files:
            return {}
        
        total_size = sum(f.size for f in self.files)
        extensions = {}
        for f in self.files:
            ext = f.suffix.lower()
            extensions[ext] = extensions.get(ext, 0) + 1
        
        return {
            'file_count': len(self.files),
            'total_size': total_size,
            'extensions': extensions,
            'rule_count': len(self.rules)
        }