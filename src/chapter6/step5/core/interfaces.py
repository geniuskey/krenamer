"""
코어 인터페이스 정의
"""

from typing import List, Dict, Any, Protocol


class FileEngineProtocol(Protocol):
    """파일 엔진 인터페이스"""
    
    def add_files(self, file_paths: List[str]) -> int:
        """파일 추가"""
        ...
    
    def remove_files_by_indices(self, indices: List[int]) -> int:
        """인덱스로 파일 제거"""
        ...
    
    def clear_files(self) -> int:
        """모든 파일 제거"""
        ...
    
    def get_filtered_files(self) -> List[str]:
        """필터링된 파일 목록 반환"""
        ...
    
    def get_file_statistics(self) -> Dict[str, int]:
        """파일 통계 반환"""
        ...
    
    def generate_rename_plan(self) -> List[Dict[str, Any]]:
        """리네임 계획 생성"""
        ...
    
    def execute_rename(self) -> Dict[str, Any]:
        """파일명 변경 실행"""
        ...
    
    def validate_settings(self) -> List[str]:
        """설정 유효성 검사"""
        ...