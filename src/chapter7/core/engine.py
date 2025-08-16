#!/usr/bin/env python3
"""
KRenamer Chapter 7 - 리네임 엔진
완성된 파일명 변경 엔진
"""

import os
import re
from datetime import datetime
from pathlib import Path
from .conditions import FileConditionChecker


class RenameEngine:
    """파일명 변경 엔진"""
    
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
        
        # 배치 설정
        self.case_method = "none"
        self.remove_special_chars = False
        self.replace_spaces = False
        self.handle_duplicates = True
        
        # 조건 검사기
        self.condition_checker = FileConditionChecker()
    
    def add_files(self, file_paths):
        """파일 추가"""
        added_count = 0
        for file_path in file_paths:
            if os.path.isfile(file_path) and file_path not in self.files:
                self.files.append(file_path)
                added_count += 1
        return added_count
    
    def remove_files_by_indices(self, indices):
        """인덱스로 파일 제거"""
        for index in sorted(indices, reverse=True):
            if 0 <= index < len(self.files):
                del self.files[index]
    
    def clear_files(self):
        """모든 파일 제거"""
        self.files.clear()
    
    def matches_conditions(self, file_path):
        """파일이 설정된 조건들을 만족하는지 확인"""
        return self.condition_checker.matches_conditions(file_path)
    
    def apply_transformations(self, name):
        """일괄 변환 적용"""
        # 대소문자 변경
        if self.case_method == "upper":
            name = name.upper()
        elif self.case_method == "lower":
            name = name.lower()
        elif self.case_method == "title":
            name = name.title()
        
        # 특수문자 제거
        if self.remove_special_chars:
            name = re.sub(r'[^\w\s.-]', '', name)
        
        # 공백 처리
        if self.replace_spaces:
            name = name.replace(' ', '_')
        
        return name
    
    def generate_new_name(self, file_path, index):
        """새로운 파일명 생성"""
        original_name = os.path.basename(file_path)
        name, ext = os.path.splitext(original_name)
        
        # 기본 리네임 방식 적용
        if self.method == "prefix":
            new_name = f"{self.prefix_text}{name}"
        elif self.method == "suffix":
            new_name = f"{name}{self.suffix_text}"
        elif self.method == "number":
            new_name = f"{self.start_number + index:03d}_{name}"
        elif self.method == "replace":
            if self.find_text:
                new_name = name.replace(self.find_text, self.replace_text)
            else:
                new_name = name
        else:
            new_name = name
        
        # 패턴 기반 변경
        if self.use_regex and self.pattern:
            try:
                new_name = re.sub(self.pattern, self.replacement, new_name)
            except re.error:
                pass  # 정규식 오류 시 변경하지 않음
        
        # 일괄 변환 적용
        new_name = self.apply_transformations(new_name)
        
        return new_name + ext
    
    def generate_rename_plan(self):
        """리네임 계획 생성"""
        plan = []
        valid_files = []
        
        # 조건에 맞는 파일들만 필터링
        for file_path in self.files:
            matches = self.matches_conditions(file_path)
            if matches:
                valid_files.append(file_path)
        
        # 새 파일명 생성
        for index, file_path in enumerate(valid_files):
            new_name = self.generate_new_name(file_path, index)
            original_name = os.path.basename(file_path)
            matches = True
            plan.append((original_name, new_name, matches))
        
        # 조건에 맞지 않는 파일들도 추가 (변경되지 않음)
        for file_path in self.files:
            if not self.matches_conditions(file_path):
                original_name = os.path.basename(file_path)
                plan.append((original_name, original_name, False))
        
        return plan
    
    def execute_rename(self):
        """파일명 변경 실행"""
        success_count = 0
        errors = []
        valid_files = []
        
        # 조건에 맞는 파일들만 필터링
        for file_path in self.files:
            if self.matches_conditions(file_path):
                valid_files.append(file_path)
        
        # 실제 리네임 실행
        for index, file_path in enumerate(valid_files):
            try:
                new_name = self.generate_new_name(file_path, index)
                dir_path = os.path.dirname(file_path)
                new_path = os.path.join(dir_path, new_name)
                
                # 같은 이름인 경우 건너뛰기
                if file_path == new_path:
                    continue
                
                # 중복 파일명 처리
                if os.path.exists(new_path) and self.handle_duplicates:
                    base, ext = os.path.splitext(new_path)
                    counter = 1
                    while os.path.exists(f"{base}_{counter}{ext}"):
                        counter += 1
                    new_path = f"{base}_{counter}{ext}"
                
                # 파일명 변경
                os.rename(file_path, new_path)
                
                # 내부 리스트 업데이트
                file_index = self.files.index(file_path)
                self.files[file_index] = new_path
                
                success_count += 1
                
            except Exception as e:
                errors.append(f"{os.path.basename(file_path)}: {str(e)}")
        
        return success_count, errors