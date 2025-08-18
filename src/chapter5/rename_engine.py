import os
from typing import List, Tuple, Dict, Any
from pathlib import Path

class RenameEngine:
    """파일명 변경을 처리하는 엔진 클래스"""
    
    def __init__(self):
        # 파일 목록 관리
        self.files: List[str] = []
        
        # 이름 변경 옵션들
        self.prefix = ""
        self.suffix = ""
        self.find_text = ""
        self.replace_text = ""
        self.use_numbering = False
        self.number_start = 1
        self.number_digits = 3
        
        # 콜백 함수들 (선택적)
        self.on_files_changed = None
        self.on_options_changed = None
    
    # 파일 관리 메서드들
    def add_file(self, file_path: str) -> bool:
        """파일을 목록에 추가"""
        if os.path.isfile(file_path) and file_path not in self.files:
            self.files.append(file_path)
            self._notify_files_changed()
            return True
        return False
    
    def add_files(self, file_paths: List[str]) -> int:
        """여러 파일을 대량 추가"""
        added_count = 0
        for file_path in file_paths:
            if self.add_file(file_path):
                added_count += 1
        return added_count
    
    def remove_file(self, file_path: str) -> bool:
        """파일을 목록에서 제거"""
        if file_path in self.files:
            self.files.remove(file_path)
            self._notify_files_changed()
            return True
        return False
    
    def remove_files_by_indices(self, indices: List[int]) -> int:
        """인덱스로 여러 파일 제거"""
        # 역순으로 정렬해서 제거 (인덱스 꼬임 방지)
        removed_count = 0
        for index in sorted(indices, reverse=True):
            if 0 <= index < len(self.files):
                del self.files[index]
                removed_count += 1
        
        if removed_count > 0:
            self._notify_files_changed()
        return removed_count
    
    def clear_files(self):
        """모든 파일 제거"""
        self.files.clear()
        self._notify_files_changed()
    
    def get_file_count(self) -> int:
        """파일 개수 반환"""
        return len(self.files)
    
    # 옵션 설정 메서드들
    def set_prefix(self, prefix: str):
        """접두사 설정"""
        if self.prefix != prefix:
            self.prefix = prefix
            self._notify_options_changed()
    
    def set_suffix(self, suffix: str):
        """접미사 설정"""
        if self.suffix != suffix:
            self.suffix = suffix
            self._notify_options_changed()
    
    def set_find_replace(self, find_text: str, replace_text: str):
        """찾기/바꾸기 설정"""
        changed = self.find_text != find_text or self.replace_text != replace_text
        self.find_text = find_text
        self.replace_text = replace_text
        if changed:
            self._notify_options_changed()
    
    def set_numbering(self, use_numbering: bool, start: int = 1, digits: int = 3):
        """순번 매기기 설정"""
        changed = (self.use_numbering != use_numbering or 
                  self.number_start != start or 
                  self.number_digits != digits)
        
        self.use_numbering = use_numbering
        self.number_start = start
        self.number_digits = digits
        
        if changed:
            self._notify_options_changed()
    
    # 파일명 변경 로직
    def generate_new_name(self, original_filename: str, file_index: int = 0) -> str:
        """원본 파일명을 새로운 이름으로 변경"""
        name, ext = os.path.splitext(original_filename)
        
        # 1단계: 찾기/바꾸기 적용
        if self.find_text:
            name = name.replace(self.find_text, self.replace_text)
        
        # 2단계: 순번 매기기 적용
        if self.use_numbering:
            number = str(self.number_start + file_index).zfill(self.number_digits)
            name = f"{name}_{number}"
        
        # 3단계: 접두사/접미사 추가
        new_name = f"{self.prefix}{name}{self.suffix}{ext}"
        
        return new_name
    
    def is_valid_filename(self, filename: str, original_path: str) -> Tuple[bool, str]:
        """파일명 유효성 검사"""
        # 1. 빈 파일명 검사
        if not filename.strip():
            return False, "빈 파일명"
        
        # 2. Windows 금지 문자 검사
        forbidden_chars = '<>:"/\\|?*'
        for char in forbidden_chars:
            if char in filename:
                return False, f"금지된 문자 '{char}' 포함"
        
        # 3. 길이 검사
        if len(filename) > 255:
            return False, "파일명이 너무 김 (255자 초과)"
        
        # 4. 중복 파일명 검사
        directory = os.path.dirname(original_path)
        new_path = os.path.join(directory, filename)
        if os.path.exists(new_path) and new_path != original_path:
            return False, "동일한 이름의 파일이 이미 존재"
        
        return True, ""
    
    def generate_preview(self) -> List[Tuple[str, str, bool, str]]:
        """모든 파일의 미리보기 생성"""
        preview_list = []
        
        for i, file_path in enumerate(self.files):
            original_name = os.path.basename(file_path)
            new_name = self.generate_new_name(original_name, i)
            is_valid, error_msg = self.is_valid_filename(new_name, file_path)
            
            preview_list.append((original_name, new_name, is_valid, error_msg))
        
        return preview_list
    
    def execute_rename(self) -> Dict[str, Any]:
        """실제 파일명 변경 실행"""
        results = {
            'success': 0,
            'failed': 0,
            'errors': [],
            'renamed_files': []  # (원본경로, 새경로) 튜플 목록
        }
        
        preview = self.generate_preview()
        
        for i, (original_name, new_name, is_valid, error_msg) in enumerate(preview):
            original_path = self.files[i]
            
            if not is_valid:
                results['failed'] += 1
                results['errors'].append(f"{original_name}: {error_msg}")
                continue
            
            # 변경이 필요한지 확인
            if original_name == new_name:
                continue  # 변경 사항 없음
            
            directory = os.path.dirname(original_path)
            new_path = os.path.join(directory, new_name)
            
            try:
                os.rename(original_path, new_path)
                
                # 성공 시 내부 목록 업데이트
                self.files[i] = new_path
                results['success'] += 1
                results['renamed_files'].append((original_path, new_path))
                
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"{original_name}: {str(e)}")
        
        if results['success'] > 0:
            self._notify_files_changed()
        
        return results
    
    # 콜백 알림 메서드들
    def _notify_files_changed(self):
        """파일 목록 변경 알림"""
        if self.on_files_changed:
            self.on_files_changed()
    
    def _notify_options_changed(self):
        """옵션 변경 알림"""
        if self.on_options_changed:
            self.on_options_changed()
    
    # 유틸리티 메서드들
    def get_statistics(self) -> Dict[str, Any]:
        """파일 목록 통계 정보"""
        if not self.files:
            return {'total_files': 0, 'total_size': 0, 'file_types': {}}
        
        total_size = 0
        file_types = {}
        
        for file_path in self.files:
            try:
                # 파일 크기
                total_size += os.path.getsize(file_path)
                
                # 파일 형식
                ext = os.path.splitext(file_path)[1].lower()
                if not ext:
                    ext = '(확장자 없음)'
                file_types[ext] = file_types.get(ext, 0) + 1
                
            except OSError:
                continue  # 파일에 접근할 수 없음
        
        return {
            'total_files': len(self.files),
            'total_size': total_size,
            'file_types': file_types
        }
    
    def reset_options(self):
        """모든 옵션 초기화"""
        self.prefix = ""
        self.suffix = ""
        self.find_text = ""
        self.replace_text = ""
        self.use_numbering = False
        self.number_start = 1
        self.number_digits = 3
        self._notify_options_changed()