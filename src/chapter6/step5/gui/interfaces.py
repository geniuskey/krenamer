"""
GUI 인터페이스 정의
"""

from typing import Protocol


class DataChangeNotifierProtocol(Protocol):
    """데이터 변경 알림 인터페이스"""
    
    def on_data_changed(self) -> None:
        """데이터 변경 시 호출"""
        ...


class StatusReporterProtocol(Protocol):
    """상태 보고 인터페이스"""
    
    def report_status(self, message: str) -> None:
        """상태 메시지 보고"""
        ...