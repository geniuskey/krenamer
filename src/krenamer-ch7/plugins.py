#!/usr/bin/env python3
"""
KRenamer Plugin Manager - Chapter 6
플러그인 시스템과 확장성
"""

import os
import sys
import importlib
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional, Type, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class PluginInfo:
    """플러그인 정보"""
    name: str
    version: str
    description: str
    author: str
    website: str = ""
    license: str = "MIT"
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class PluginInterface(ABC):
    """플러그인 인터페이스"""
    
    @abstractmethod
    def get_info(self) -> PluginInfo:
        """플러그인 정보 반환"""
        pass
    
    @abstractmethod
    def initialize(self, context: Dict[str, Any]) -> bool:
        """플러그인 초기화"""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """플러그인 정리"""
        pass


class RenamePlugin(PluginInterface):
    """리네임 플러그인 기본 클래스"""
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """전략 이름 반환"""
        pass
    
    @abstractmethod
    def create_strategy(self):
        """전략 인스턴스 생성"""
        pass


class FilterPlugin(PluginInterface):
    """필터 플러그인 기본 클래스"""
    
    @abstractmethod
    def get_filter_name(self) -> str:
        """필터 이름 반환"""
        pass
    
    @abstractmethod
    def create_filter(self):
        """필터 인스턴스 생성"""
        pass


class UIPlugin(PluginInterface):
    """UI 플러그인 기본 클래스"""
    
    @abstractmethod
    def get_widget_info(self) -> Dict[str, Any]:
        """위젯 정보 반환"""
        pass
    
    @abstractmethod
    def create_widget(self, parent):
        """위젯 생성"""
        pass


class PluginManager:
    """플러그인 관리자"""
    
    def __init__(self):
        self.plugins: Dict[str, PluginInterface] = {}
        self.plugin_directories: List[Path] = []
        self.loaded_modules: Dict[str, Any] = {}
        
        # 기본 플러그인 디렉토리
        self.add_plugin_directory(Path(__file__).parent / "plugins")
        
        logger.info("PluginManager initialized")
    
    def add_plugin_directory(self, directory: Path) -> None:
        """플러그인 디렉토리 추가"""
        if directory.exists() and directory.is_dir():
            self.plugin_directories.append(directory)
            logger.info(f"Added plugin directory: {directory}")
        else:
            logger.warning(f"Plugin directory not found: {directory}")
    
    def discover_plugins(self) -> List[str]:
        """플러그인 자동 발견"""
        discovered = []
        
        for plugin_dir in self.plugin_directories:
            if not plugin_dir.exists():
                continue
            
            # Python 파일 검색
            for py_file in plugin_dir.glob("*.py"):
                if py_file.name.startswith("_"):
                    continue
                
                try:
                    plugin_name = py_file.stem
                    discovered.append(str(py_file))
                    logger.debug(f"Discovered plugin: {plugin_name}")
                    
                except Exception as e:
                    logger.error(f"Error discovering plugin {py_file}: {e}")
        
        return discovered
    
    def load_plugin(self, plugin_path: str) -> bool:
        """플러그인 로드"""
        try:
            plugin_path = Path(plugin_path)
            plugin_name = plugin_path.stem
            
            # 모듈 로드
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if spec is None or spec.loader is None:
                logger.error(f"Cannot load plugin spec: {plugin_path}")
                return False
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # 플러그인 클래스 찾기
            plugin_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, PluginInterface) and 
                    attr != PluginInterface):
                    plugin_class = attr
                    break
            
            if plugin_class is None:
                logger.error(f"No plugin class found in: {plugin_path}")
                return False
            
            # 플러그인 인스턴스 생성
            plugin_instance = plugin_class()
            plugin_info = plugin_instance.get_info()
            
            # 의존성 확인
            if not self._check_dependencies(plugin_info.dependencies):
                logger.error(f"Plugin dependencies not met: {plugin_info.name}")
                return False
            
            # 플러그인 초기화
            context = {
                'plugin_manager': self,
                'plugin_directory': plugin_path.parent
            }
            
            if not plugin_instance.initialize(context):
                logger.error(f"Plugin initialization failed: {plugin_info.name}")
                return False
            
            # 등록
            self.plugins[plugin_info.name] = plugin_instance
            self.loaded_modules[plugin_info.name] = module
            
            logger.info(f"Plugin loaded: {plugin_info.name} v{plugin_info.version}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_path}: {e}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """플러그인 언로드"""
        if plugin_name not in self.plugins:
            logger.warning(f"Plugin not found: {plugin_name}")
            return False
        
        try:
            plugin = self.plugins[plugin_name]
            plugin.cleanup()
            
            del self.plugins[plugin_name]
            if plugin_name in self.loaded_modules:
                del self.loaded_modules[plugin_name]
            
            logger.info(f"Plugin unloaded: {plugin_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unload plugin {plugin_name}: {e}")
            return False
    
    def reload_plugin(self, plugin_name: str) -> bool:
        """플러그인 재로드"""
        if plugin_name not in self.loaded_modules:
            logger.warning(f"Plugin not loaded: {plugin_name}")
            return False
        
        try:
            # 플러그인 정보 저장
            plugin = self.plugins[plugin_name]
            plugin_info = plugin.get_info()
            
            # 언로드
            self.unload_plugin(plugin_name)
            
            # 모듈 재로드
            module = self.loaded_modules.get(plugin_name)
            if module:
                importlib.reload(module)
            
            # 다시 로드 (원본 경로 찾기 필요)
            # 실제 구현에서는 플러그인 경로를 따로 저장해야 함
            
            logger.info(f"Plugin reloaded: {plugin_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to reload plugin {plugin_name}: {e}")
            return False
    
    def get_plugin(self, plugin_name: str) -> Optional[PluginInterface]:
        """플러그인 인스턴스 반환"""
        return self.plugins.get(plugin_name)
    
    def get_plugins_by_type(self, plugin_type: Type[PluginInterface]) -> List[PluginInterface]:
        """타입별 플러그인 목록 반환"""
        matching_plugins = []
        
        for plugin in self.plugins.values():
            if isinstance(plugin, plugin_type):
                matching_plugins.append(plugin)
        
        return matching_plugins
    
    def get_plugin_list(self) -> List[Dict[str, Any]]:
        """플러그인 목록 반환 (UI용)"""
        plugin_list = []
        
        for plugin in self.plugins.values():
            info = plugin.get_info()
            plugin_data = {
                'name': info.name,
                'version': info.version,
                'description': info.description,
                'author': info.author,
                'website': info.website,
                'license': info.license,
                'type': type(plugin).__name__
            }
            plugin_list.append(plugin_data)
        
        return plugin_list
    
    def _check_dependencies(self, dependencies: List[str]) -> bool:
        """의존성 확인"""
        for dependency in dependencies:
            try:
                importlib.import_module(dependency)
            except ImportError:
                logger.error(f"Missing dependency: {dependency}")
                return False
        
        return True
    
    def load_all_plugins(self) -> Dict[str, bool]:
        """모든 플러그인 로드"""
        results = {}
        discovered_plugins = self.discover_plugins()
        
        for plugin_path in discovered_plugins:
            plugin_name = Path(plugin_path).stem
            results[plugin_name] = self.load_plugin(plugin_path)
        
        loaded_count = sum(results.values())
        logger.info(f"Loaded {loaded_count}/{len(results)} plugins")
        
        return results
    
    def unload_all_plugins(self) -> None:
        """모든 플러그인 언로드"""
        plugin_names = list(self.plugins.keys())
        
        for plugin_name in plugin_names:
            self.unload_plugin(plugin_name)
        
        logger.info("All plugins unloaded")


# 예제 플러그인들

class TimestampRenamePlugin(RenamePlugin):
    """타임스탬프 리네임 플러그인 예제"""
    
    def get_info(self) -> PluginInfo:
        return PluginInfo(
            name="timestamp_rename",
            version="1.0.0",
            description="타임스탬프 기반 파일명 변경",
            author="KRenamer Team",
            dependencies=["datetime"]
        )
    
    def initialize(self, context: Dict[str, Any]) -> bool:
        logger.info("TimestampRenamePlugin initialized")
        return True
    
    def cleanup(self) -> None:
        logger.info("TimestampRenamePlugin cleanup")
    
    def get_strategy_name(self) -> str:
        return "timestamp"
    
    def create_strategy(self):
        from datetime import datetime
        from ..core import RenameStrategy, FileInfo
        
        class TimestampStrategy(RenameStrategy):
            def apply(self, file_info: FileInfo, parameters: Dict[str, Any]) -> str:
                timestamp_format = parameters.get('format', '%Y%m%d_%H%M%S')
                position = parameters.get('position', 'prefix')
                
                timestamp = datetime.now().strftime(timestamp_format)
                
                if position == 'prefix':
                    return f"{timestamp}_{file_info.name}"
                else:
                    return f"{file_info.stem}_{timestamp}{file_info.suffix}"
            
            def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
                try:
                    format_str = parameters.get('format', '%Y%m%d_%H%M%S')
                    datetime.now().strftime(format_str)
                    return True
                except ValueError:
                    return False
        
        return TimestampStrategy()


class HashRenamePlugin(RenamePlugin):
    """해시 기반 리네임 플러그인 예제"""
    
    def get_info(self) -> PluginInfo:
        return PluginInfo(
            name="hash_rename",
            version="1.0.0",
            description="파일 해시값 기반 리네임",
            author="KRenamer Team",
            dependencies=["hashlib"]
        )
    
    def initialize(self, context: Dict[str, Any]) -> bool:
        logger.info("HashRenamePlugin initialized")
        return True
    
    def cleanup(self) -> None:
        logger.info("HashRenamePlugin cleanup")
    
    def get_strategy_name(self) -> str:
        return "hash"
    
    def create_strategy(self):
        import hashlib
        from ..core import RenameStrategy, FileInfo
        
        class HashStrategy(RenameStrategy):
            def apply(self, file_info: FileInfo, parameters: Dict[str, Any]) -> str:
                algorithm = parameters.get('algorithm', 'md5')
                length = parameters.get('length', 8)
                position = parameters.get('position', 'suffix')
                
                try:
                    # 파일 해시 계산
                    hasher = hashlib.new(algorithm)
                    with open(file_info.path, 'rb') as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            hasher.update(chunk)
                    
                    file_hash = hasher.hexdigest()[:length]
                    
                    if position == 'prefix':
                        return f"{file_hash}_{file_info.name}"
                    else:
                        return f"{file_info.stem}_{file_hash}{file_info.suffix}"
                        
                except Exception as e:
                    logger.error(f"Hash calculation failed: {e}")
                    return file_info.name
            
            def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
                algorithm = parameters.get('algorithm', 'md5')
                try:
                    hashlib.new(algorithm)
                    return True
                except ValueError:
                    return False
        
        return HashStrategy()


class SizeFilterPlugin(FilterPlugin):
    """파일 크기 필터 플러그인 예제"""
    
    def get_info(self) -> PluginInfo:
        return PluginInfo(
            name="size_filter",
            version="1.0.0",
            description="고급 파일 크기 필터링",
            author="KRenamer Team"
        )
    
    def initialize(self, context: Dict[str, Any]) -> bool:
        logger.info("SizeFilterPlugin initialized")
        return True
    
    def cleanup(self) -> None:
        logger.info("SizeFilterPlugin cleanup")
    
    def get_filter_name(self) -> str:
        return "advanced_size"
    
    def create_filter(self):
        from ..core import FileInfo
        
        class AdvancedSizeFilter:
            def __init__(self, min_size: int = 0, max_size: int = 0, 
                         size_unit: str = "B", comparison: str = "range"):
                self.min_size = min_size
                self.max_size = max_size
                self.size_unit = size_unit
                self.comparison = comparison
                
                # 단위 변환
                multipliers = {
                    "B": 1,
                    "KB": 1024,
                    "MB": 1024**2,
                    "GB": 1024**3,
                    "TB": 1024**4
                }
                
                self.multiplier = multipliers.get(size_unit, 1)
            
            def matches(self, file_info: FileInfo) -> bool:
                file_size = file_info.size
                min_bytes = self.min_size * self.multiplier
                max_bytes = self.max_size * self.multiplier
                
                if self.comparison == "range":
                    return min_bytes <= file_size <= max_bytes
                elif self.comparison == "greater":
                    return file_size > min_bytes
                elif self.comparison == "less":
                    return file_size < max_bytes
                elif self.comparison == "equal":
                    return min_bytes <= file_size <= min_bytes + (1024 * self.multiplier)
                
                return True
        
        return AdvancedSizeFilter


# 플러그인 레지스트리
class PluginRegistry:
    """플러그인 레지스트리 (글로벌 인스턴스)"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.manager = PluginManager()
        return cls._instance
    
    @property
    def plugin_manager(self) -> PluginManager:
        return self.manager


# 편의 함수들
def get_plugin_manager() -> PluginManager:
    """글로벌 플러그인 매니저 반환"""
    registry = PluginRegistry()
    return registry.plugin_manager


def register_rename_strategy(strategy_name: str, strategy_class):
    """리네임 전략 등록 (편의 함수)"""
    # 실제 구현에서는 RenameEngine과 연동
    pass


def register_filter(filter_name: str, filter_class):
    """필터 등록 (편의 함수)"""
    # 실제 구현에서는 FilterManager와 연동
    pass