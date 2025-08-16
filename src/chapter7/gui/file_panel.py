"""
파일 목록 및 관리 패널
"""

import tkinter as tk
from tkinter import ttk, filedialog
import os


class FilePanel:
    """파일 목록 관리 패널"""
    
    def __init__(self, parent, engine, variables, status_callback=None):
        self.parent = parent
        self.engine = engine
        self.status_callback = status_callback
        
        # 변수들 참조
        self.display_filter = variables['display_filter']
        self.custom_extension = variables['custom_extension']
        self.count_var = variables['count_var']
        
        # UI 위젯들
        self.files_listbox = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """파일 패널 UI 설정"""
        # 파일 목록 프레임
        files_frame = ttk.LabelFrame(self.parent, text="파일 목록", padding="5")
        files_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 파일 필터
        filter_frame = ttk.Frame(files_frame)
        filter_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(filter_frame, text="파일 필터:").pack(side=tk.LEFT)
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.display_filter, width=13)
        filter_combo['values'] = ('모든 파일', '이미지 파일', '문서 파일', '텍스트 파일', '사용자 정의')
        filter_combo.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(filter_frame, text="확장자:").pack(side=tk.LEFT)
        custom_filter_entry = ttk.Entry(filter_frame, textvariable=self.custom_extension, width=10)
        custom_filter_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # 파일 개수
        count_label = ttk.Label(filter_frame, textvariable=self.count_var)
        count_label.pack(side=tk.RIGHT)
        
        # 파일 관리 버튼
        button_frame = ttk.Frame(files_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(button_frame, text="파일 추가", command=self.add_files_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="선택 제거", command=self.remove_selected_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="전체 지우기", command=self.clear_all_files).pack(side=tk.LEFT)
        
        # 리스트박스
        listbox_frame = ttk.Frame(files_frame)
        listbox_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.files_listbox = tk.Listbox(listbox_frame, height=6, selectmode=tk.EXTENDED)
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        self.files_listbox.config(yscrollcommand=scrollbar.set)
        
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 그리드 설정
        files_frame.columnconfigure(0, weight=1)
        files_frame.rowconfigure(2, weight=1)
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
    
    def add_files_dialog(self):
        """파일 선택 대화상자"""
        files = filedialog.askopenfilenames(title="파일 선택")
        if files:
            self.add_files(files)
    
    def add_files(self, file_paths):
        """파일 추가"""
        added_count = self.engine.add_files(file_paths)
        self.refresh_file_list()
        if added_count > 0 and self.status_callback:
            self.status_callback(f"{added_count}개 파일이 추가되었습니다")
    
    def remove_selected_files(self):
        """선택된 파일들 제거"""
        selection = self.files_listbox.curselection()
        if selection:
            indices = list(selection)
            self.engine.remove_files_by_indices(indices)
            self.refresh_file_list()
            if self.status_callback:
                self.status_callback(f"{len(selection)}개 파일이 제거되었습니다")
    
    def clear_all_files(self):
        """모든 파일 제거"""
        count = len(self.engine.files)
        self.engine.clear_files()
        self.refresh_file_list()
        if self.status_callback:
            self.status_callback(f"모든 파일({count}개)이 제거되었습니다")
    
    def refresh_file_list(self):
        """파일 목록 새로고침"""
        self.files_listbox.delete(0, tk.END)
        
        # 필터링된 파일 목록 표시
        filtered_files = self._get_filtered_files()
        
        for file_path in filtered_files:
            file_name = os.path.basename(file_path)
            self.files_listbox.insert(tk.END, file_name)
        
        # 파일 개수 업데이트
        self.count_var.set(f"파일: {len(filtered_files)}개")
    
    def _get_filtered_files(self):
        """필터에 따른 파일 목록 반환"""
        filter_type = self.display_filter.get()
        
        if filter_type == "모든 파일":
            return self.engine.files
        elif filter_type == "이미지 파일":
            image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
            return [f for f in self.engine.files if os.path.splitext(f)[1].lower() in image_exts]
        elif filter_type == "문서 파일":
            doc_exts = {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.hwp'}
            return [f for f in self.engine.files if os.path.splitext(f)[1].lower() in doc_exts]
        elif filter_type == "텍스트 파일":
            text_exts = {'.txt', '.log', '.csv', '.json', '.xml', '.html', '.css', '.js'}
            return [f for f in self.engine.files if os.path.splitext(f)[1].lower() in text_exts]
        elif filter_type == "사용자 정의":
            custom_exts = self.custom_extension.get().lower().split(',')
            custom_exts = [ext.strip() for ext in custom_exts if ext.strip()]
            if custom_exts:
                return [f for f in self.engine.files if os.path.splitext(f)[1].lower() in custom_exts]
        
        return self.engine.files