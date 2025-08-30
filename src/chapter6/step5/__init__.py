"""
KRenamer Chapter 6 Step 5: 완전한 모듈 구조
Chapter 7 스타일의 패키지 구조를 사전 체험하는 모듈
"""

__version__ = "6.5.0"
__author__ = "KRenamer Development Team"

# 주요 클래스 임포트
from .core.engine import RenameEngineService
from .gui.main_window import MainApplication

__all__ = ['RenameEngineService', 'MainApplication']