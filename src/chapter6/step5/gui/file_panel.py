"""
파일 목록 관리 패널
"""

import tkinter as tk
from tkinter import ttk, filedialog
import os
from typing import Optional

from ..core.interfaces import FileEngineProtocol
from .interfaces import DataChangeNotifierProtocol, StatusReporterProtocol

# 드래그 앤 드롭 지원 (선택적)
try:
    from tkinterdnd2 import DND_FILES
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


class FilePanel:
    """
    파일 목록 관리 UI 컴포넌트
    완전히 모듈화된 구조
    """
    
    def __init__(self, 
                 parent: tk.Widget, 
                 engine: FileEngineProtocol,
                 notifier: DataChangeNotifierProtocol,
                 status_reporter: Optional[StatusReporterProtocol] = None):
        self.parent = parent
        self.engine = engine
        self.notifier = notifier
        self.status_reporter = status_reporter
        
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
        self.frame = ttk.LabelFrame(self.parent, text="파일 목록 [모듈화]", padding="10")
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
        self.notifier.on_data_changed()
    
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