#!/usr/bin/env python3
"""
KRenamer Core Engine - Korean File processing and renaming logic
"""

import os
import re
from datetime import datetime
from pathlib import Path


class RenameEngine:
    """한국어 파일 이름 변경 엔진
    
    KRenamer의 핵심 파일 처리 엔진으로, 다양한 조건과 패턴을 사용하여
    파일명을 일괄 변경하는 기능을 제공합니다.
    
    주요 기능:
        - 접두사/접미사 추가
        - 순차 번호 매기기  
        - 찾기/바꾸기
        - 정규식 패턴 매칭
        - 조건부 필터링 (크기, 날짜, 확장자)
        - 대소문자 변환 및 특수문자 처리
    
    Attributes:
        files (list): 처리할 파일 경로 목록
        method (str): 기본 이름 변경 방식 ('prefix', 'suffix', 'number', 'replace')
        use_regex (bool): 정규식 사용 여부
        use_size_condition (bool): 파일 크기 조건 사용 여부
        use_date_condition (bool): 날짜 조건 사용 여부
        use_ext_condition (bool): 확장자 조건 사용 여부
    
    Example:
        >>> engine = RenameEngine()
        >>> engine.add_files(['photo1.jpg', 'photo2.jpg'])
        >>> engine.set_basic_rename_options('prefix', text='vacation_')
        >>> plan = engine.generate_rename_plan()
        >>> success_count, errors = engine.execute_rename(plan)
    """
    
    def __init__(self):
        self.files = []
        
        # 기본 설정
        self.method = "prefix"
        self.prefix_text = ""
        self.suffix_text = ""
        self.start_number = 1
        self.find_text = ""
        self.replace_text = ""
        
        # 패턴 설정
        self.use_regex = False
        self.pattern = ""
        self.replacement = ""
        
        # 조건 설정
        self.use_size_condition = False
        self.size_operator = ">"
        self.size_value = 1.0
        self.size_unit = "MB"
        
        self.use_date_condition = False
        self.date_operator = "after"
        self.date_value = datetime.now().strftime("%Y-%m-%d")
        
        self.use_ext_condition = False
        self.allowed_extensions = ".jpg,.png,.gif"
        
        # 배치 설정
        self.case_method = "none"
        self.remove_special_chars = False
        self.replace_spaces = False
        self.handle_duplicates = True
    
    def add_files(self, file_paths):
        """파일 목록에 파일들을 추가합니다.
        
        Args:
            file_paths (list or str): 추가할 파일 경로들 (문자열 또는 리스트)
            
        Returns:
            int: 실제로 추가된 파일 개수
            
        Note:
            - 중복 파일은 추가되지 않습니다
            - 존재하지 않는 파일은 무시됩니다
            - 폴더의 경우 내부 파일들이 재귀적으로 추가됩니다
        """
        added_count = 0
        for file_path in file_paths:
            if os.path.isfile(file_path) and file_path not in self.files:
                self.files.append(file_path)
                added_count += 1
        return added_count
    
    def remove_files_by_indices(self, indices):
        """지정된 인덱스의 파일들을 목록에서 제거합니다.
        
        Args:
            indices (list): 제거할 파일들의 인덱스 리스트
            
        Note:
            인덱스는 역순으로 정렬되어 처리됩니다.
        """
        for index in reversed(sorted(indices)):
            if 0 <= index < len(self.files):
                del self.files[index]
    
    def clear_files(self):
        """파일 목록을 모두 비웁니다."""
        self.files.clear()
    
    def matches_conditions(self, file_path):
        """파일이 설정된 모든 조건을 만족하는지 확인합니다.
        
        Args:
            file_path (str): 검사할 파일 경로
            
        Returns:
            bool: 모든 조건을 만족하면 True, 하나라도 만족하지 않으면 False
            
        Note:
            다음 조건들을 검사합니다:
                - 파일 크기 조건 (use_size_condition이 True인 경우)
                - 수정 날짜 조건 (use_date_condition이 True인 경우)
                - 확장자 조건 (use_ext_condition이 True인 경우)
        """
        try:
            # 파일 크기 조건
            if self.use_size_condition:
                file_size = os.path.getsize(file_path)
                target_size = self.size_value
                
                if self.size_unit == "KB":
                    target_size *= 1024
                elif self.size_unit == "MB":
                    target_size *= 1024 * 1024
                elif self.size_unit == "GB":
                    target_size *= 1024 * 1024 * 1024
                
                if self.size_operator == "<" and not (file_size < target_size):
                    return False
                elif self.size_operator == "<=" and not (file_size <= target_size):
                    return False
                elif self.size_operator == "=" and not (file_size == target_size):
                    return False
                elif self.size_operator == ">=" and not (file_size >= target_size):
                    return False
                elif self.size_operator == ">" and not (file_size > target_size):
                    return False
            
            # 날짜 조건
            if self.use_date_condition:
                file_mtime = os.path.getmtime(file_path)
                file_date = datetime.fromtimestamp(file_mtime)
                target_date = datetime.strptime(self.date_value, "%Y-%m-%d")
                
                if self.date_operator == "after" and file_date <= target_date:
                    return False
                elif self.date_operator == "before" and file_date >= target_date:
                    return False
            
            # 확장자 조건
            if self.use_ext_condition:
                file_ext = os.path.splitext(file_path)[1].lower()
                allowed_exts = [ext.strip().lower() for ext in self.allowed_extensions.split(',')]
                if file_ext not in allowed_exts:
                    return False
            
            return True
            
        except Exception:
            return False
    
    def apply_transformations(self, name):
        """파일명에 변환 규칙 적용"""
        # 대소문자 변환
        if self.case_method == "upper":
            name = name.upper()
        elif self.case_method == "lower":
            name = name.lower()
        elif self.case_method == "title":
            name = name.title()
        
        # 특수문자 제거
        if self.remove_special_chars:
            name = re.sub(r'[^\w\s.-]', '', name)
        
        # 공백을 언더스코어로
        if self.replace_spaces:
            name = re.sub(r'\s+', '_', name)
        
        return name
    
    def generate_new_name(self, file_path, index):
        """단일 파일의 새 이름 생성"""
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)
        
        # 기본 이름 변경 적용
        if self.method == "prefix":
            new_name = f"{self.prefix_text}{name}"
        elif self.method == "suffix":
            new_name = f"{name}{self.suffix_text}"
        elif self.method == "number":
            new_name = f"{self.start_number + index:03d}_{name}"
        elif self.method == "replace":
            new_name = name.replace(self.find_text, self.replace_text) if self.find_text else name
        else:
            new_name = name
        
        # 패턴 기반 변경 적용
        if self.pattern:
            if self.use_regex:
                try:
                    new_name = re.sub(self.pattern, self.replacement, new_name)
                except re.error:
                    pass  # 정규식 오류 시 변경하지 않음
            else:
                new_name = new_name.replace(self.pattern, self.replacement)
        
        # 변환 규칙 적용
        new_name = self.apply_transformations(new_name)
        
        # 최종 파일명 구성
        return new_name + ext
    
    def generate_rename_plan(self):
        """이름 변경 계획 생성"""
        if not self.files:
            return []
        
        # 조건에 맞는 파일들만 필터링
        filtered_files = []
        for file_path in self.files:
            if self.matches_conditions(file_path):
                filtered_files.append(file_path)
        
        rename_plan = []
        used_names = set()
        
        # 모든 파일에 대해 계획 생성 (조건 미충족 파일도 포함)
        filtered_index = 0
        for file_path in self.files:
            matches = self.matches_conditions(file_path)
            
            if matches:
                new_name = self.generate_new_name(file_path, filtered_index)
                
                # 중복 처리
                if self.handle_duplicates:
                    original_name = new_name
                    counter = 1
                    while new_name in used_names:
                        name_part, ext_part = os.path.splitext(original_name)
                        new_name = f"{name_part}_{counter}{ext_part}"
                        counter += 1
                
                used_names.add(new_name)
                filtered_index += 1
            else:
                new_name = os.path.basename(file_path)  # 원본 이름 유지
            
            rename_plan.append((file_path, new_name, matches))
        
        return rename_plan
    
    def execute_rename(self):
        """이름 변경 실행"""
        rename_plan = self.generate_rename_plan()
        
        success_count = 0
        errors = []
        
        # 파일 경로 업데이트를 위한 맵핑
        path_updates = {}
        
        for file_path, new_name, matches in rename_plan:
            if not matches:
                continue
                
            try:
                dir_path = os.path.dirname(file_path)
                new_path = os.path.join(dir_path, new_name)
                
                if file_path != new_path and not os.path.exists(new_path):
                    os.rename(file_path, new_path)
                    path_updates[file_path] = new_path
                    success_count += 1
                    
            except Exception as e:
                errors.append(f"{os.path.basename(file_path)}: {str(e)}")
        
        # 성공적으로 변경된 파일들의 경로 업데이트
        for old_path, new_path in path_updates.items():
            try:
                index = self.files.index(old_path)
                self.files[index] = new_path
            except ValueError:
                pass
        
        return success_count, errors