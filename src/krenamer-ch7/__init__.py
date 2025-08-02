"""
KRenamer Chapter 6: 모듈화된 아키텍처
확장 가능한 패키지 구조와 플러그인 시스템
"""

__version__ = "0.6.0"
__author__ = "KRenamer Team"

# 핵심 클래스들을 패키지 레벨에서 import 가능하게 설정
from .core import RenameEngine
from .gui import MainWindow
from .config import ConfigManager
from .plugins import PluginManager

__all__ = [
    'RenameEngine',
    'MainWindow', 
    'ConfigManager',
    'PluginManager'
]