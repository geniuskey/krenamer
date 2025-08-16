"""
파일 필터링 조건 검사 로직
"""

import os
from datetime import datetime
from ..utils.file_utils import convert_size_to_bytes, get_file_modified_date


class FileConditionChecker:
    """파일 조건 검사 클래스"""
    
    def __init__(self):
        # 크기 조건
        self.use_size_condition = False
        self.size_operator = "<"
        self.size_value = 1.0
        self.size_unit = "MB"
        
        # 날짜 조건
        self.use_date_condition = False
        self.date_operator = "after"
        self.date_value = "2024-01-01"
        
        # 확장자 조건
        self.use_ext_condition = False
        self.allowed_extensions = ""
    
    def matches_conditions(self, file_path):
        """파일이 설정된 조건들을 만족하는지 확인"""
        try:
            # 파일 크기 조건
            if self.use_size_condition:
                if not self._check_size_condition(file_path):
                    return False
            
            # 날짜 조건
            if self.use_date_condition:
                if not self._check_date_condition(file_path):
                    return False
            
            # 확장자 조건
            if self.use_ext_condition:
                if not self._check_extension_condition(file_path):
                    return False
            
            return True
            
        except Exception:
            return False
    
    def _check_size_condition(self, file_path):
        """파일 크기 조건 검사"""
        try:
            file_size = os.path.getsize(file_path)
            target_size = convert_size_to_bytes(self.size_value, self.size_unit)
            
            if self.size_operator == "<":
                return file_size < target_size
            elif self.size_operator == "<=":
                return file_size <= target_size
            elif self.size_operator == "=":
                return file_size == target_size
            elif self.size_operator == ">=":
                return file_size >= target_size
            elif self.size_operator == ">":
                return file_size > target_size
            
            return True
        except:
            return False
    
    def _check_date_condition(self, file_path):
        """파일 날짜 조건 검사"""
        try:
            file_date = get_file_modified_date(file_path)
            if file_date is None:
                return False
            
            target_date = datetime.strptime(self.date_value, "%Y-%m-%d")
            
            if self.date_operator == "after":
                return file_date > target_date
            elif self.date_operator == "before":
                return file_date < target_date
            
            return True
        except:
            return False
    
    def _check_extension_condition(self, file_path):
        """파일 확장자 조건 검사"""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            allowed_exts = [ext.strip().lower() for ext in self.allowed_extensions.split(',')]
            return file_ext in allowed_exts
        except:
            return False