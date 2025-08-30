"""
파일명 변경 엔진 구현
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any

try:
    from .interfaces import FileEngineProtocol
except ImportError:
    # 직접 실행 시 절대 import 사용
    from interfaces import FileEngineProtocol


class RenameEngineService:
    """
    파일명 변경 엔진 서비스
    완전히 독립적인 비즈니스 로직
    """
    
    def __init__(self):
        self.files: List[str] = []
        
        # 기본 리네임 설정
        self.method = "prefix"
        self.prefix_text = ""
        self.suffix_text = ""
        self.start_number = 1
        self.find_text = ""
        self.replace_text = ""
        
        # 고급 옵션
        self.case_sensitive = True
        self.use_regex = False
        
        # 일괄 변환 설정
        self.case_method = "none"
        self.remove_special_chars = False
        self.replace_spaces = False
        self.handle_duplicates = True
        
        # 필터 설정
        self.display_filter = "모든 파일"
        self.custom_extension = ""
    
    def add_files(self, file_paths: List[str]) -> int:
        """파일 추가"""
        added_count = 0
        for file_path in file_paths:
            if os.path.isfile(file_path) and file_path not in self.files:
                self.files.append(file_path)
                added_count += 1
        return added_count
    
    def remove_files_by_indices(self, indices: List[int]) -> int:
        """인덱스로 파일 제거"""
        removed_count = 0
        for index in sorted(indices, reverse=True):
            if 0 <= index < len(self.files):
                del self.files[index]
                removed_count += 1
        return removed_count
    
    def clear_files(self) -> int:
        """모든 파일 제거"""
        count = len(self.files)
        self.files.clear()
        return count
    
    def get_filtered_files(self) -> List[str]:
        """필터링된 파일 목록 반환"""
        if self.display_filter == "모든 파일":
            return self.files.copy()
        
        filtered = []
        for file_path in self.files:
            ext = Path(file_path).suffix.lower()
            
            if self.display_filter == "이미지 파일":
                if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
                    filtered.append(file_path)
            elif self.display_filter == "문서 파일":
                if ext in ['.pdf', '.doc', '.docx', '.txt', '.hwp']:
                    filtered.append(file_path)
            elif self.display_filter == "음악 파일":
                if ext in ['.mp3', '.wav', '.flac', '.m4a', '.ogg']:
                    filtered.append(file_path)
            elif self.display_filter == "사용자 정의":
                if self.custom_extension:
                    allowed_exts = [e.strip().lower() for e in self.custom_extension.split(',')]
                    if ext in allowed_exts:
                        filtered.append(file_path)
        
        return filtered
    
    def get_file_statistics(self) -> Dict[str, int]:
        """파일 통계 반환"""
        total = len(self.files)
        filtered = len(self.get_filtered_files())
        return {
            'total': total,
            'filtered': filtered,
            'hidden': total - filtered
        }
    
    def generate_new_name(self, file_path: str, index: int) -> str:
        """새로운 파일명 생성"""
        original_name = os.path.basename(file_path)
        name, ext = os.path.splitext(original_name)
        
        if self.method == "prefix":
            new_name = f"{self.prefix_text}{name}"
        elif self.method == "suffix":
            new_name = f"{name}{self.suffix_text}"
        elif self.method == "number":
            new_name = f"{self.start_number + index:03d}_{name}"
        elif self.method == "replace":
            new_name = self._apply_find_replace(name)
        else:
            new_name = name
        
        new_name = self._apply_transformations(new_name)
        return new_name + ext
    
    def _apply_find_replace(self, name: str) -> str:
        """찾기/바꾸기 적용"""
        if not self.find_text:
            return name
        
        if self.use_regex:
            try:
                flags = 0 if self.case_sensitive else re.IGNORECASE
                return re.sub(self.find_text, self.replace_text, name, flags=flags)
            except re.error:
                return name
        else:
            if self.case_sensitive:
                return name.replace(self.find_text, self.replace_text)
            else:
                pattern = re.compile(re.escape(self.find_text), re.IGNORECASE)
                return pattern.sub(self.replace_text, name)
    
    def _apply_transformations(self, name: str) -> str:
        """일괄 변환 규칙 적용"""
        if self.case_method == "upper":
            name = name.upper()
        elif self.case_method == "lower":
            name = name.lower()
        elif self.case_method == "title":
            name = name.title()
        
        if self.remove_special_chars:
            name = re.sub(r'[^\w\s.-]', '', name)
        
        if self.replace_spaces:
            name = name.replace(' ', '_')
        
        return name
    
    def generate_rename_plan(self) -> List[Dict[str, Any]]:
        """리네임 계획 생성"""
        filtered_files = self.get_filtered_files()
        plan = []
        used_names = set()
        
        for index, file_path in enumerate(filtered_files):
            original_name = os.path.basename(file_path)
            new_name = self.generate_new_name(file_path, index)
            
            if self.handle_duplicates:
                final_name = new_name
                counter = 1
                while final_name in used_names:
                    name_part, ext_part = os.path.splitext(new_name)
                    final_name = f"{name_part}_{counter}{ext_part}"
                    counter += 1
                new_name = final_name
            
            used_names.add(new_name)
            changed = original_name != new_name
            
            plan.append({
                'original': original_name,
                'new': new_name,
                'changed': changed,
                'path': file_path
            })
        
        return plan
    
    def execute_rename(self) -> Dict[str, Any]:
        """파일명 변경 실행"""
        plan = self.generate_rename_plan()
        success_count = 0
        errors = []
        
        for item in plan:
            if not item['changed']:
                continue
            
            file_path = item['path']
            new_name = item['new']
            original_name = item['original']
            
            try:
                dir_path = os.path.dirname(file_path)
                new_path = os.path.join(dir_path, new_name)
                
                if file_path == new_path:
                    continue
                
                if os.path.exists(new_path):
                    errors.append(f"{original_name}: 같은 이름의 파일이 이미 존재합니다")
                    continue
                
                os.rename(file_path, new_path)
                
                # 내부 파일 목록 업데이트
                file_index = self.files.index(file_path)
                self.files[file_index] = new_path
                success_count += 1
                
            except Exception as e:
                errors.append(f"{original_name}: {str(e)}")
        
        return {
            'success_count': success_count,
            'errors': errors
        }
    
    def validate_settings(self) -> List[str]:
        """설정 유효성 검사"""
        warnings = []
        
        if self.method == "replace" and not self.find_text:
            warnings.append("찾기/바꾸기 방식에서 '찾기' 텍스트가 비어있습니다")
        
        if self.method == "number" and self.start_number < 0:
            warnings.append("시작 번호는 0 이상이어야 합니다")
        
        if self.use_regex and self.find_text:
            try:
                re.compile(self.find_text)
            except re.error as e:
                warnings.append(f"정규식 패턴 오류: {str(e)}")
        
        if self.display_filter == "사용자 정의" and not self.custom_extension:
            warnings.append("사용자 정의 필터에서 확장자가 지정되지 않았습니다")
        
        return warnings