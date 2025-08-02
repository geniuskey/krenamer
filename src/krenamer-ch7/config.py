#!/usr/bin/env python3
"""
KRenamer Configuration Manager - Chapter 6
설정 관리 및 프리셋 시스템
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class WindowConfig:
    """윈도우 설정"""
    width: int = 900
    height: int = 700
    x: int = 100
    y: int = 100
    maximized: bool = False
    theme: str = "default"


@dataclass
class RenameConfig:
    """리네임 설정"""
    prefix: str = ""
    suffix: str = ""
    find_text: str = ""
    replace_text: str = ""
    use_regex: bool = False
    
    # 순번 매기기
    numbering_enabled: bool = False
    numbering_start: int = 1
    numbering_digits: int = 3
    numbering_position: str = "prefix"
    
    # 대소문자
    case_change: str = "none"
    
    # 필터
    filter_by_size: bool = False
    min_size: int = 0
    max_size: int = 0
    filter_by_extension: bool = False
    allowed_extensions: List[str] = None
    
    def __post_init__(self):
        if self.allowed_extensions is None:
            self.allowed_extensions = []


@dataclass
class UIConfig:
    """UI 설정"""
    language: str = "ko"
    font_family: str = "맑은 고딕"
    font_size: int = 9
    auto_preview: bool = True
    confirm_operations: bool = True
    show_tooltips: bool = True
    recent_files_limit: int = 10


@dataclass
class AdvancedConfig:
    """고급 설정"""
    backup_enabled: bool = True
    backup_directory: str = ""
    log_operations: bool = True
    max_history: int = 100
    auto_update_check: bool = True
    plugin_directories: List[str] = None
    
    def __post_init__(self):
        if self.plugin_directories is None:
            self.plugin_directories = []


@dataclass
class AppConfig:
    """전체 애플리케이션 설정"""
    window: WindowConfig
    rename: RenameConfig
    ui: UIConfig
    advanced: AdvancedConfig
    version: str = "0.6.0"
    last_updated: str = ""
    
    def __post_init__(self):
        if not self.last_updated:
            self.last_updated = datetime.now().isoformat()


@dataclass
class Preset:
    """프리셋 정의"""
    name: str
    description: str
    rename_config: RenameConfig
    created_date: str
    modified_date: str
    author: str = "User"
    version: str = "1.0"
    
    def __post_init__(self):
        if not self.created_date:
            self.created_date = datetime.now().isoformat()
        if not self.modified_date:
            self.modified_date = self.created_date


class ConfigManager:
    """설정 관리자"""
    
    def __init__(self, app_name: str = "KRenamer"):
        self.app_name = app_name
        self.config_dir = self._get_config_directory()
        self.config_file = self.config_dir / "config.json"
        self.presets_file = self.config_dir / "presets.json"
        self.history_file = self.config_dir / "history.json"
        
        # 설정 디렉토리 생성
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # 현재 설정
        self.config = self._load_config()
        
        logger.info(f"ConfigManager initialized: {self.config_dir}")
    
    def _get_config_directory(self) -> Path:
        """OS별 설정 디렉토리 경로 반환"""
        if os.name == 'nt':  # Windows
            base_dir = Path.home() / "AppData" / "Local"
        elif os.name == 'posix':
            if os.uname().sysname == 'Darwin':  # macOS
                base_dir = Path.home() / "Library" / "Application Support"
            else:  # Linux
                base_dir = Path.home() / ".config"
        else:
            base_dir = Path.home()
        
        return base_dir / self.app_name
    
    def _create_default_config(self) -> AppConfig:
        """기본 설정 생성"""
        return AppConfig(
            window=WindowConfig(),
            rename=RenameConfig(),
            ui=UIConfig(),
            advanced=AdvancedConfig()
        )
    
    def _load_config(self) -> AppConfig:
        """설정 파일 로드"""
        if not self.config_file.exists():
            logger.info("Config file not found, creating default")
            return self._create_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 데이터를 AppConfig로 변환
            config = AppConfig(
                window=WindowConfig(**data.get('window', {})),
                rename=RenameConfig(**data.get('rename', {})),
                ui=UIConfig(**data.get('ui', {})),
                advanced=AdvancedConfig(**data.get('advanced', {})),
                version=data.get('version', '0.6.0'),
                last_updated=data.get('last_updated', '')
            )
            
            logger.info("Config loaded successfully")
            return config
            
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            logger.error(f"Failed to load config: {e}")
            logger.info("Using default config")
            return self._create_default_config()
    
    def save_config(self) -> bool:
        """설정 파일 저장"""
        try:
            # 마지막 업데이트 시간 갱신
            self.config.last_updated = datetime.now().isoformat()
            
            # dict로 변환
            data = asdict(self.config)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info("Config saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False
    
    def get_window_config(self) -> WindowConfig:
        """윈도우 설정 반환"""
        return self.config.window
    
    def get_rename_config(self) -> RenameConfig:
        """리네임 설정 반환"""
        return self.config.rename
    
    def get_ui_config(self) -> UIConfig:
        """UI 설정 반환"""
        return self.config.ui
    
    def get_advanced_config(self) -> AdvancedConfig:
        """고급 설정 반환"""
        return self.config.advanced
    
    def update_window_config(self, **kwargs) -> None:
        """윈도우 설정 업데이트"""
        for key, value in kwargs.items():
            if hasattr(self.config.window, key):
                setattr(self.config.window, key, value)
        logger.debug(f"Window config updated: {kwargs}")
    
    def update_rename_config(self, **kwargs) -> None:
        """리네임 설정 업데이트"""
        for key, value in kwargs.items():
            if hasattr(self.config.rename, key):
                setattr(self.config.rename, key, value)
        logger.debug(f"Rename config updated: {kwargs}")
    
    def update_ui_config(self, **kwargs) -> None:
        """UI 설정 업데이트"""
        for key, value in kwargs.items():
            if hasattr(self.config.ui, key):
                setattr(self.config.ui, key, value)
        logger.debug(f"UI config updated: {kwargs}")
    
    def update_advanced_config(self, **kwargs) -> None:
        """고급 설정 업데이트"""
        for key, value in kwargs.items():
            if hasattr(self.config.advanced, key):
                setattr(self.config.advanced, key, value)
        logger.debug(f"Advanced config updated: {kwargs}")
    
    def reset_to_defaults(self) -> None:
        """설정을 기본값으로 초기화"""
        self.config = self._create_default_config()
        logger.info("Config reset to defaults")
    
    # 프리셋 관리
    def load_presets(self) -> Dict[str, Preset]:
        """프리셋 목록 로드"""
        if not self.presets_file.exists():
            return {}
        
        try:
            with open(self.presets_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            presets = {}
            for name, preset_data in data.items():
                rename_data = preset_data.get('rename_config', {})
                preset = Preset(
                    name=preset_data.get('name', name),
                    description=preset_data.get('description', ''),
                    rename_config=RenameConfig(**rename_data),
                    created_date=preset_data.get('created_date', ''),
                    modified_date=preset_data.get('modified_date', ''),
                    author=preset_data.get('author', 'User'),
                    version=preset_data.get('version', '1.0')
                )
                presets[name] = preset
            
            logger.info(f"Loaded {len(presets)} presets")
            return presets
            
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            logger.error(f"Failed to load presets: {e}")
            return {}
    
    def save_presets(self, presets: Dict[str, Preset]) -> bool:
        """프리셋 목록 저장"""
        try:
            data = {}
            for name, preset in presets.items():
                data[name] = asdict(preset)
            
            with open(self.presets_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(presets)} presets")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save presets: {e}")
            return False
    
    def save_preset(self, name: str, description: str = "") -> bool:
        """현재 설정을 프리셋으로 저장"""
        presets = self.load_presets()
        
        preset = Preset(
            name=name,
            description=description,
            rename_config=self.config.rename,
            created_date=datetime.now().isoformat(),
            modified_date=datetime.now().isoformat()
        )
        
        presets[name] = preset
        return self.save_presets(presets)
    
    def load_preset(self, name: str) -> bool:
        """프리셋 로드"""
        presets = self.load_presets()
        
        if name not in presets:
            logger.warning(f"Preset not found: {name}")
            return False
        
        preset = presets[name]
        self.config.rename = preset.rename_config
        logger.info(f"Loaded preset: {name}")
        return True
    
    def delete_preset(self, name: str) -> bool:
        """프리셋 삭제"""
        presets = self.load_presets()
        
        if name not in presets:
            logger.warning(f"Preset not found: {name}")
            return False
        
        del presets[name]
        return self.save_presets(presets)
    
    def get_preset_list(self) -> List[Dict[str, str]]:
        """프리셋 목록 반환 (UI용)"""
        presets = self.load_presets()
        
        preset_list = []
        for preset in presets.values():
            preset_info = {
                'name': preset.name,
                'description': preset.description,
                'created_date': preset.created_date,
                'author': preset.author
            }
            preset_list.append(preset_info)
        
        # 생성일 기준 역순 정렬
        preset_list.sort(key=lambda x: x['created_date'], reverse=True)
        return preset_list
    
    # 최근 파일 관리
    def add_recent_file(self, file_path: str) -> None:
        """최근 파일 추가"""
        history = self.load_history()
        recent_files = history.get('recent_files', [])
        
        # 중복 제거
        if file_path in recent_files:
            recent_files.remove(file_path)
        
        # 맨 앞에 추가
        recent_files.insert(0, file_path)
        
        # 제한 수만큼 유지
        limit = self.config.ui.recent_files_limit
        recent_files = recent_files[:limit]
        
        history['recent_files'] = recent_files
        self.save_history(history)
    
    def get_recent_files(self) -> List[str]:
        """최근 파일 목록 반환"""
        history = self.load_history()
        recent_files = history.get('recent_files', [])
        
        # 존재하는 파일만 필터링
        existing_files = []
        for file_path in recent_files:
            if Path(file_path).exists():
                existing_files.append(file_path)
        
        return existing_files
    
    def clear_recent_files(self) -> None:
        """최근 파일 목록 삭제"""
        history = self.load_history()
        history['recent_files'] = []
        self.save_history(history)
    
    def load_history(self) -> Dict[str, Any]:
        """히스토리 로드"""
        if not self.history_file.exists():
            return {}
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    
    def save_history(self, history: Dict[str, Any]) -> bool:
        """히스토리 저장"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
            return False
    
    # 백업 및 복원
    def backup_config(self, backup_path: Optional[str] = None) -> str:
        """설정 백업"""
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.config_dir / f"backup_config_{timestamp}.json"
        
        backup_data = {
            'config': asdict(self.config),
            'presets': self.load_presets(),
            'history': self.load_history(),
            'backup_date': datetime.now().isoformat()
        }
        
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Config backed up to: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"Failed to backup config: {e}")
            raise
    
    def restore_config(self, backup_path: str) -> bool:
        """설정 복원"""
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # 설정 복원
            config_data = backup_data.get('config', {})
            self.config = AppConfig(
                window=WindowConfig(**config_data.get('window', {})),
                rename=RenameConfig(**config_data.get('rename', {})),
                ui=UIConfig(**config_data.get('ui', {})),
                advanced=AdvancedConfig(**config_data.get('advanced', {})),
                version=config_data.get('version', '0.6.0'),
                last_updated=config_data.get('last_updated', '')
            )
            
            # 프리셋 복원
            presets_data = backup_data.get('presets', {})
            if presets_data:
                presets = {}
                for name, preset_data in presets_data.items():
                    if isinstance(preset_data, dict):
                        rename_data = preset_data.get('rename_config', {})
                        preset = Preset(
                            name=preset_data.get('name', name),
                            description=preset_data.get('description', ''),
                            rename_config=RenameConfig(**rename_data),
                            created_date=preset_data.get('created_date', ''),
                            modified_date=preset_data.get('modified_date', ''),
                            author=preset_data.get('author', 'User'),
                            version=preset_data.get('version', '1.0')
                        )
                        presets[name] = preset
                
                self.save_presets(presets)
            
            # 히스토리 복원
            history_data = backup_data.get('history', {})
            if history_data:
                self.save_history(history_data)
            
            # 설정 저장
            self.save_config()
            
            logger.info(f"Config restored from: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restore config: {e}")
            return False
    
    def get_config_info(self) -> Dict[str, Any]:
        """설정 정보 반환"""
        return {
            'config_dir': str(self.config_dir),
            'config_file': str(self.config_file),
            'presets_file': str(self.presets_file),
            'history_file': str(self.history_file),
            'version': self.config.version,
            'last_updated': self.config.last_updated,
            'preset_count': len(self.load_presets()),
            'recent_files_count': len(self.get_recent_files())
        }