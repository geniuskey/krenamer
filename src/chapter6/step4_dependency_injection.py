#!/usr/bin/env python3
"""
KRenamer Chapter 6 Step 4: 의존성 주입 패턴 적용
Step 3의 컴포넌트들에 의존성 주입 패턴을 적용하여 느슨한 결합 구현

변경 사항:
- 강한 결합 → 느슨한 결합
- 생성자를 통한 의존성 주입
- 콜백 인터페이스 정의
- 서비스 로케이터 패턴 도입
- 설정 가능한 컴포넌트 구조

핵심 개념:
- 의존성 주입 (Dependency Injection)
- 제어의 역전 (Inversion of Control)
- 느슨한 결합 vs 강한 결합
- 인터페이스 기반 설계
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any, Callable, Protocol
from abc import ABC, abstractmethod

# 드래그 앤 드롭 지원 (선택적)
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


# 인터페이스 정의 (Protocol 사용)
class FileEngineProtocol(Protocol):
    """파일 엔진 인터페이스"""
    def add_files(self, file_paths: List[str]) -> int: ...
    def remove_files_by_indices(self, indices: List[int]) -> int: ...
    def clear_files(self) -> int: ...
    def get_filtered_files(self) -> List[str]: ...
    def get_file_statistics(self) -> Dict[str, int]: ...
    def generate_rename_plan(self) -> List[Dict[str, Any]]: ...
    def execute_rename(self) -> Dict[str, Any]: ...
    def validate_settings(self) -> List[str]: ...


class StatusReporterProtocol(Protocol):
    """상태 보고 인터페이스"""
    def report_status(self, message: str) -> None: ...


class DataChangeNotifierProtocol(Protocol):
    """데이터 변경 알림 인터페이스"""  
    def on_data_changed(self) -> None: ...


# 서비스 클래스들
class RenameEngineService:
    """파일명 변경 엔진 서비스 (Step 3와 동일한 로직, 인터페이스 준수)"""
    
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


class ServiceContainer:
    """서비스 컨테이너 - 의존성 관리"""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
    
    def register(self, name: str, service: Any):
        """서비스 등록"""
        self._services[name] = service
    
    def get(self, name: str) -> Any:
        """서비스 조회"""
        if name not in self._services:
            raise KeyError(f"Service '{name}' not registered")
        return self._services[name]
    
    def create_engine(self) -> FileEngineProtocol:
        """엔진 생성 팩토리 메서드"""
        return RenameEngineService()


# 의존성 주입이 적용된 컴포넌트들
class FilePanel:
    """
    파일 목록 관리 UI 컴포넌트 (의존성 주입 적용)
    
    의존성:
    - FileEngineProtocol: 파일 엔진 (생성자 주입)
    - DataChangeNotifierProtocol: 데이터 변경 알림 (생성자 주입)
    - StatusReporterProtocol: 상태 보고 (생성자 주입, 선택적)
    """
    
    def __init__(self, 
                 parent: tk.Widget, 
                 engine: FileEngineProtocol,
                 notifier: DataChangeNotifierProtocol,
                 status_reporter: Optional[StatusReporterProtocol] = None):
        self.parent = parent
        self.engine = engine  # 의존성 주입
        self.notifier = notifier  # 의존성 주입  
        self.status_reporter = status_reporter  # 의존성 주입 (선택적)
        
        # UI 변수들
        self.display_filter_var = tk.StringVar(value="모든 파일")
        self.custom_extension_var = tk.StringVar()
        self.count_var = tk.StringVar(value="파일: 0개")
        
        # 위젯 생성
        self.create_widgets()
        self.setup_bindings()
        self.setup_drag_drop()
        
        # 초기 새로고침
        self.refresh()
    
    def create_widgets(self):
        """위젯 생성"""
        self.frame = ttk.LabelFrame(self.parent, text="파일 목록 (DI)", padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 상단: 필터 및 정보
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="필터:").pack(side=tk.LEFT)
        
        self.filter_combo = ttk.Combobox(
            header_frame, 
            textvariable=self.display_filter_var,
            values=["모든 파일", "이미지 파일", "문서 파일", "음악 파일", "사용자 정의"],
            width=12
        )
        self.filter_combo.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(header_frame, text="확장자:").pack(side=tk.LEFT)
        self.ext_entry = ttk.Entry(header_frame, textvariable=self.custom_extension_var, width=15)
        self.ext_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(header_frame, textvariable=self.count_var, foreground="blue").pack(side=tk.RIGHT)
        
        # 파일 리스트
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.files_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        
        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        scrollbar_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.files_listbox.xview)
        self.files_listbox.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.files_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 버튼들
        button_frame = ttk.Frame(self.frame)
        button_frame.pack()
        
        ttk.Button(button_frame, text="파일 추가", command=self.add_files_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="폴더 추가", command=self.add_folder_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="선택 제거", command=self.remove_selected).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="전체 지우기", command=self.clear_all).pack(side=tk.LEFT)
    
    def setup_bindings(self):
        """이벤트 바인딩"""
        self.display_filter_var.trace('w', self.on_filter_changed)
        self.custom_extension_var.trace('w', self.on_filter_changed)
    
    def setup_drag_drop(self):
        """드래그 앤 드롭 설정"""
        if DND_AVAILABLE:
            self.files_listbox.drop_target_register(DND_FILES)
            self.files_listbox.dnd_bind('<<Drop>>', self.on_drop)
    
    def on_drop(self, event):
        """드래그 앤 드롭 이벤트"""
        files = self.parent.tk.splitlist(event.data)
        self.add_files(files)
    
    def on_filter_changed(self, *args):
        """필터 변경 이벤트"""
        self.sync_filter_to_engine()
        self.refresh()
        self.notifier.on_data_changed()  # 의존성 주입된 알림자 사용
    
    def sync_filter_to_engine(self):
        """필터 설정을 엔진에 동기화"""
        self.engine.display_filter = self.display_filter_var.get()
        self.engine.custom_extension = self.custom_extension_var.get()
    
    def refresh(self):
        """파일 목록 새로고침"""
        self.files_listbox.delete(0, tk.END)
        filtered_files = self.engine.get_filtered_files()
        
        for file_path in filtered_files:
            filename = os.path.basename(file_path)
            self.files_listbox.insert(tk.END, filename)
        
        stats = self.engine.get_file_statistics()
        self.count_var.set(f"파일: {stats['total']}개 (필터: {stats['filtered']}개)")
    
    def add_files_dialog(self):
        """파일 추가 대화상자"""
        files = filedialog.askopenfilenames(title="파일 선택")
        if files:
            self.add_files(files)
    
    def add_folder_dialog(self):
        """폴더 추가 대화상자"""
        folder = filedialog.askdirectory(title="폴더 선택")
        if folder:
            files = []
            for root, dirs, filenames in os.walk(folder):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
            self.add_files(files)
    
    def add_files(self, files):
        """파일 추가"""
        added_count = self.engine.add_files(files)
        self.refresh()
        self.notifier.on_data_changed()
        
        # 상태 보고 (의존성 주입된 리포터 사용)
        if self.status_reporter:
            if added_count > 0:
                self.status_reporter.report_status(f"{added_count}개 파일이 추가되었습니다")
            else:
                self.status_reporter.report_status("추가할 새로운 파일이 없습니다")
        
        return added_count
    
    def remove_selected(self):
        """선택된 파일 제거"""
        selection = self.files_listbox.curselection()
        if not selection:
            if self.status_reporter:
                self.status_reporter.report_status("제거할 파일을 선택해주세요")
            return 0
        
        filtered_files = self.engine.get_filtered_files()
        original_indices = []
        
        for sel_index in selection:
            if sel_index < len(filtered_files):
                file_path = filtered_files[sel_index]
                if hasattr(self.engine, 'files') and file_path in self.engine.files:
                    original_index = self.engine.files.index(file_path)
                    original_indices.append(original_index)
        
        removed_count = self.engine.remove_files_by_indices(original_indices)
        self.refresh()
        self.notifier.on_data_changed()
        
        if self.status_reporter:
            self.status_reporter.report_status(f"{removed_count}개 파일이 제거되었습니다")
        
        return removed_count
    
    def clear_all(self):
        """모든 파일 제거"""
        removed_count = self.engine.clear_files()
        self.refresh()
        self.notifier.on_data_changed()
        
        if self.status_reporter:
            if removed_count > 0:
                self.status_reporter.report_status(f"모든 파일({removed_count}개)이 제거되었습니다")
        
        return removed_count


class OptionsPanel:
    """
    리네임 옵션 설정 UI 컴포넌트 (의존성 주입 적용)
    
    의존성:
    - FileEngineProtocol: 파일 엔진 (생성자 주입)
    - DataChangeNotifierProtocol: 데이터 변경 알림 (생성자 주입)
    """
    
    def __init__(self, 
                 parent: tk.Widget, 
                 engine: FileEngineProtocol,
                 notifier: DataChangeNotifierProtocol):
        self.parent = parent
        self.engine = engine  # 의존성 주입
        self.notifier = notifier  # 의존성 주입
        
        # UI 변수들
        self.setup_variables()
        
        # 위젯 생성
        self.create_widgets()
        self.setup_bindings()
        
        # 초기 동기화
        self.sync_to_engine()
    
    def setup_variables(self):
        """tkinter 변수 설정"""
        self.method_var = tk.StringVar(value="prefix")
        self.text_var = tk.StringVar()
        self.start_num_var = tk.StringVar(value="1")
        self.find_var = tk.StringVar()
        self.replace_var = tk.StringVar()
        
        self.case_sensitive_var = tk.BooleanVar(value=True)
        self.use_regex_var = tk.BooleanVar()
        self.case_method_var = tk.StringVar(value="none")
        self.remove_special_var = tk.BooleanVar()
        self.replace_spaces_var = tk.BooleanVar()
        self.handle_duplicates_var = tk.BooleanVar(value=True)
        
        self.warning_var = tk.StringVar()
    
    def create_widgets(self):
        """위젯 생성"""
        # 기본 옵션 프레임
        basic_frame = ttk.LabelFrame(self.parent, text="기본 리네임 옵션 (DI)", padding="10")
        basic_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 방식 선택
        method_frame = ttk.Frame(basic_frame)
        method_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Radiobutton(method_frame, text="접두사", variable=self.method_var, value="prefix").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(method_frame, text="접미사", variable=self.method_var, value="suffix").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(method_frame, text="순번", variable=self.method_var, value="number").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(method_frame, text="찾기/바꾸기", variable=self.method_var, value="replace").pack(side=tk.LEFT)
        
        # 입력 필드들
        input_frame = ttk.Frame(basic_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="텍스트:", width=10).pack(side=tk.LEFT)
        ttk.Entry(input_frame, textvariable=self.text_var, width=20).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(input_frame, text="시작번호:").pack(side=tk.LEFT, padx=(10, 5))
        ttk.Entry(input_frame, textvariable=self.start_num_var, width=8).pack(side=tk.LEFT)
        
        replace_frame = ttk.Frame(basic_frame)
        replace_frame.pack(fill=tk.X)
        
        ttk.Label(replace_frame, text="찾기:", width=10).pack(side=tk.LEFT)
        ttk.Entry(replace_frame, textvariable=self.find_var, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(replace_frame, text="바꾸기:").pack(side=tk.LEFT)
        ttk.Entry(replace_frame, textvariable=self.replace_var, width=15).pack(side=tk.LEFT, padx=(5, 0))
        
        # 고급 옵션 프레임
        advanced_frame = ttk.LabelFrame(self.parent, text="고급 옵션 (DI)", padding="10")
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        row1_frame = ttk.Frame(advanced_frame)
        row1_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Checkbutton(row1_frame, text="대소문자 구분", variable=self.case_sensitive_var).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(row1_frame, text="정규식 사용", variable=self.use_regex_var).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(row1_frame, text="중복 처리", variable=self.handle_duplicates_var).pack(side=tk.LEFT)
        
        row2_frame = ttk.Frame(advanced_frame)
        row2_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(row2_frame, text="대소문자:").pack(side=tk.LEFT, padx=(0, 5))
        case_combo = ttk.Combobox(
            row2_frame,
            textvariable=self.case_method_var,
            values=["none", "upper", "lower", "title"],
            width=10
        )
        case_combo.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Checkbutton(row2_frame, text="특수문자 제거", variable=self.remove_special_var).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(row2_frame, text="공백 → _", variable=self.replace_spaces_var).pack(side=tk.LEFT)
        
        # 검증 프레임
        validation_frame = ttk.Frame(self.parent)
        validation_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(validation_frame, text="설정 검증", command=self.validate_settings).pack(side=tk.LEFT)
        
        self.warning_label = ttk.Label(validation_frame, textvariable=self.warning_var, foreground="red")
        self.warning_label.pack(side=tk.LEFT, padx=(15, 0))
    
    def setup_bindings(self):
        """이벤트 바인딩"""
        variables = [
            self.method_var, self.text_var, self.start_num_var, self.find_var, self.replace_var,
            self.case_sensitive_var, self.use_regex_var, self.case_method_var,
            self.remove_special_var, self.replace_spaces_var, self.handle_duplicates_var
        ]
        
        for var in variables:
            var.trace('w', self.on_settings_changed)
    
    def on_settings_changed(self, *args):
        """설정 변경 이벤트"""
        self.sync_to_engine()
        self.validate_settings()
        self.notifier.on_data_changed()  # 의존성 주입된 알림자 사용
    
    def sync_to_engine(self):
        """설정을 엔진에 동기화"""
        self.engine.method = self.method_var.get()
        self.engine.prefix_text = self.text_var.get()
        self.engine.suffix_text = self.text_var.get()
        
        try:
            self.engine.start_number = int(self.start_num_var.get())
        except:
            self.engine.start_number = 1
        
        self.engine.find_text = self.find_var.get()
        self.engine.replace_text = self.replace_var.get()
        self.engine.case_sensitive = self.case_sensitive_var.get()
        self.engine.use_regex = self.use_regex_var.get()
        self.engine.case_method = self.case_method_var.get()
        self.engine.remove_special_chars = self.remove_special_var.get()
        self.engine.replace_spaces = self.replace_spaces_var.get()
        self.engine.handle_duplicates = self.handle_duplicates_var.get()
    
    def validate_settings(self):
        """설정 검증"""
        warnings = self.engine.validate_settings()
        if warnings:
            self.warning_var.set("⚠️ " + warnings[0])
        else:
            self.warning_var.set("")


class PreviewPanel:
    """
    미리보기 표시 UI 컴포넌트 (의존성 주입 적용)
    
    의존성:
    - FileEngineProtocol: 파일 엔진 (생성자 주입)
    """
    
    def __init__(self, parent: tk.Widget, engine: FileEngineProtocol):
        self.parent = parent
        self.engine = engine  # 의존성 주입
        
        # UI 변수들
        self.stats_var = tk.StringVar()
        
        # 위젯 생성
        self.create_widgets()
    
    def create_widgets(self):
        """위젯 생성"""
        self.frame = ttk.LabelFrame(self.parent, text="미리보기 (DI)", padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        info_frame = ttk.Frame(self.frame)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(info_frame, textvariable=self.stats_var, font=("맑은 고딕", 9), foreground="blue").pack(side=tk.LEFT)
        
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("index", "original", "new", "status")
        self.preview_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        self.preview_tree.heading("index", text="순번")
        self.preview_tree.heading("original", text="원본 파일명")
        self.preview_tree.heading("new", text="새 파일명")
        self.preview_tree.heading("status", text="상태")
        
        self.preview_tree.column("index", width=50)
        self.preview_tree.column("original", width=200)
        self.preview_tree.column("new", width=200)
        self.preview_tree.column("status", width=80)
        
        preview_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.preview_tree.yview)
        self.preview_tree.config(yscrollcommand=preview_scrollbar.set)
        
        self.preview_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def refresh(self):
        """미리보기 새로고침"""
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        plan = self.engine.generate_rename_plan()
        
        if not plan:
            self.stats_var.set("변경할 파일이 없습니다")
            return
        
        changed_count = sum(1 for item in plan if item['changed'])
        self.stats_var.set(f"총 {len(plan)}개 파일 중 {changed_count}개 변경 예정")
        
        for i, item in enumerate(plan):
            if item['changed']:
                status = "변경됨"
                tags = ("changed",)
            else:
                status = "동일"
                tags = ("same",)
            
            self.preview_tree.insert("", tk.END, values=(
                i + 1,
                item['original'], 
                item['new'], 
                status
            ), tags=tags)
        
        self.preview_tree.tag_configure("changed", foreground="blue")
        self.preview_tree.tag_configure("same", foreground="gray")


class Step4MainGUI:
    """
    의존성 주입이 적용된 메인 GUI 클래스
    
    역할:
    - 서비스 컨테이너 관리
    - 의존성 주입을 통한 컴포넌트 생성
    - 인터페이스를 통한 컴포넌트 간 통신
    """
    
    def __init__(self):
        # 윈도우 초기화
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
        
        # 서비스 컨테이너 설정
        self.container = ServiceContainer()
        self.setup_services()
        
        # 상태 변수
        self.status_var = tk.StringVar(value="의존성 주입이 적용된 컴포넌트들이 준비되었습니다")
        
        # UI 구성
        self.setup_window()
        self.setup_widgets()
        
        # 초기 상태
        self.on_data_changed()
    
    def setup_services(self):
        """서비스 컨테이너 설정"""
        # 엔진 서비스 생성 및 등록
        engine = self.container.create_engine()
        self.container.register('engine', engine)
    
    def setup_window(self):
        """윈도우 기본 설정"""
        self.root.title("Chapter 6 Step 4: 의존성 주입 패턴 적용")
        self.root.geometry("1200x750")
        self.root.resizable(True, True)
        self.center_window()
    
    def center_window(self):
        """윈도우 중앙 배치"""
        self.root.update_idletasks()
        width, height = 1200, 750
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_widgets(self):
        """위젯 구성 - 의존성 주입을 통한 컴포넌트 생성"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 상단: 설명
        info_frame = ttk.LabelFrame(main_frame, text="Step 4: 의존성 주입 패턴 적용", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_text = (
            "이 단계에서는 컴포넌트들에 의존성 주입 패턴을 적용합니다:\n"
            "• 생성자를 통한 의존성 주입\n"
            "• 인터페이스 기반 설계 (Protocol 사용)\n"  
            "• 서비스 컨테이너를 통한 의존성 관리\n"
            "• 느슨한 결합 구조 구현"
        )
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)
        
        # 메인 레이아웃
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        left_panel = ttk.Frame(paned)
        paned.add(left_panel, weight=1)
        
        right_panel = ttk.Frame(paned)
        paned.add(right_panel, weight=1)
        
        # 의존성 주입을 통한 컴포넌트 생성
        engine = self.container.get('engine')
        
        # 인터페이스를 통한 의존성 주입
        self.file_panel = FilePanel(
            parent=left_panel,
            engine=engine,  # FileEngineProtocol 주입
            notifier=self,  # DataChangeNotifierProtocol 주입
            status_reporter=self  # StatusReporterProtocol 주입 (선택적)
        )
        
        self.options_panel = OptionsPanel(
            parent=left_panel,
            engine=engine,  # FileEngineProtocol 주입
            notifier=self   # DataChangeNotifierProtocol 주입
        )
        
        self.preview_panel = PreviewPanel(
            parent=right_panel,
            engine=engine   # FileEngineProtocol 주입
        )
        
        # 실행 버튼
        button_frame = ttk.Frame(left_panel)
        button_frame.pack(pady=(10, 0))
        
        ttk.Button(button_frame, text="미리보기 새로고침", command=self.refresh_preview).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="이름 변경 실행", command=self.execute_rename).pack(side=tk.LEFT)
        
        # 상태바
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X)
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT)
    
    # DataChangeNotifierProtocol 구현
    def on_data_changed(self):
        """데이터 변경 알림 처리"""
        self.refresh_preview()
    
    # StatusReporterProtocol 구현
    def report_status(self, message: str):
        """상태 보고 처리"""
        self.status_var.set(message)
    
    def refresh_preview(self):
        """미리보기 새로고침"""
        self.preview_panel.refresh()
    
    def execute_rename(self):
        """파일명 변경 실행"""
        engine = self.container.get('engine')
        
        if not hasattr(engine, 'files') or not engine.files:
            self.report_status("변경할 파일이 없습니다")
            messagebox.showwarning("경고", "변경할 파일이 없습니다")
            return
        
        warnings = engine.validate_settings()
        if warnings:
            if not messagebox.askyesno("경고", f"다음 경고가 있습니다:\n{warnings[0]}\n\n계속 진행하시겠습니까?"):
                return
        
        plan = engine.generate_rename_plan()
        change_count = sum(1 for item in plan if item['changed'])
        
        if change_count == 0:
            self.report_status("변경될 파일이 없습니다")
            messagebox.showinfo("정보", "변경될 파일이 없습니다")
            return
        
        if not messagebox.askyesno("확인", f"{change_count}개 파일의 이름을 변경하시겠습니까?"):
            return
        
        result = engine.execute_rename()
        success_count = result['success_count']
        errors = result['errors']
        
        if errors:
            error_msg = f"{success_count}개 파일 변경 완료.\n오류:\n" + "\n".join(errors[:5])
            if len(errors) > 5:
                error_msg += f"\n... 외 {len(errors)-5}개"
            messagebox.showwarning("완료", error_msg)
        else:
            messagebox.showinfo("완료", f"{success_count}개 파일의 이름이 변경되었습니다")
        
        self.report_status(f"변경 완료: {success_count}개 성공, {len(errors)}개 오류")
        
        # UI 새로고침
        self.file_panel.refresh()
        self.refresh_preview()
    
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()


def main():
    """메인 함수"""
    print("KRenamer Chapter 6 Step 4: 의존성 주입 패턴 적용")
    print("=" * 50)
    print("학습 내용:")
    print("• 강한 결합 → 느슨한 결합")
    print("• 생성자를 통한 의존성 주입")
    print("• 인터페이스 기반 설계 (Protocol)")
    print("• 서비스 컨테이너를 통한 의존성 관리")
    print("• 설정 가능한 컴포넌트 구조")
    print()
    print("핵심 개념:")
    print("• 의존성 주입 (Dependency Injection)")
    print("• 제어의 역전 (Inversion of Control)")
    print("• 느슨한 결합 vs 강한 결합")
    print("• 인터페이스 기반 설계")
    print()
    
    if not DND_AVAILABLE:
        print("⚠️  tkinterdnd2가 설치되지 않았습니다.")
        print("드래그 앤 드롭 기능을 사용하려면 다음 명령어로 설치하세요:")
        print("pip install tkinterdnd2")
        print()
    
    try:
        app = Step4MainGUI()
        app.run()
        return 0
    except Exception as e:
        print(f"애플리케이션 실행 중 오류: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())