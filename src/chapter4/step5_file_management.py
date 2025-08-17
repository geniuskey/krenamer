import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
import shutil
import json
from datetime import datetime
from pathlib import Path

# 드래그 앤 드롭 라이브러리 (선택적)
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

class FileManagementRenamer:
    def __init__(self):
        # 드래그 앤 드롭 지원 여부에 따라 다른 방식으로 윈도우 생성
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
        
        self.root.title("파일 리네이머 v5.0 - 완성된 파일 관리")
        self.root.geometry("900x800")
        
        self.files = []
        self.backup_history = []  # 백업 히스토리
        self.filter_enabled = False
        
        self.create_widgets()
        self.setup_drag_drop()
        self.setup_preview_bindings()
        self.setup_menu()
        
        # 설정 로드
        self.load_settings()
    
    def create_widgets(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # 제목
        title_label = ttk.Label(main_frame, text="완성된 파일 관리 도구", 
                               font=("맑은 고딕", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # 좌측 패널 (파일 관리)
        self.create_left_panel(main_frame)
        
        # 우측 패널 (옵션 및 미리보기)
        self.create_right_panel(main_frame)
        
        # 하단 상태바
        self.create_status_bar(main_frame)
        
        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
    
    def create_left_panel(self, parent):
        """좌측 패널 - 파일 관리"""
        left_frame = ttk.Frame(parent)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        
        # 드래그 앤 드롭 영역
        self.create_drop_area(left_frame)
        
        # 파일 목록 영역
        self.create_file_list(left_frame)
        
        # 파일 관리 버튼
        self.create_file_management_buttons(left_frame)
        
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
    
    def create_right_panel(self, parent):
        """우측 패널 - 옵션 및 미리보기"""
        right_frame = ttk.Frame(parent)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
        
        # 필터 옵션
        self.create_filter_options(right_frame)
        
        # 이름 변경 옵션
        self.create_rename_options(right_frame)
        
        # 미리보기 영역
        self.create_preview_area(right_frame)
        
        # 실행 버튼들
        self.create_action_buttons(right_frame)
        
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(2, weight=1)
    
    def create_drop_area(self, parent):
        """드래그 앤 드롭 영역"""
        drop_frame = ttk.LabelFrame(parent, text="파일 추가", padding="10")
        drop_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        if DND_AVAILABLE:
            drop_text = "📁 파일을 드래그 앤 드롭하세요"
            bg_color = "#e8f4fd"
        else:
            drop_text = "⚠️ 드래그 앤 드롭 불가능"
            bg_color = "#fff2cc"
        
        self.drop_label = tk.Label(
            drop_frame, 
            text=drop_text,
            font=("맑은 고딕", 11),
            bg=bg_color,
            relief="ridge",
            bd=2,
            height=2
        )
        self.drop_label.pack(fill="x", pady=(0, 10))
        
        # 파일 추가 버튼들
        btn_frame = ttk.Frame(drop_frame)
        btn_frame.pack(fill="x")
        
        ttk.Button(btn_frame, text="📄 파일 선택", 
                  command=self.select_files).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="📂 폴더 선택", 
                  command=self.select_folder).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="📂 재귀 폴더", 
                  command=self.select_folder_recursive).pack(side="left")
    
    def create_file_list(self, parent):
        """파일 목록 영역"""
        list_frame = ttk.LabelFrame(parent, text="파일 목록", padding="5")
        list_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        # 파일 카운터와 필터 정보
        info_frame = ttk.Frame(list_frame)
        info_frame.pack(fill="x", pady=(0, 5))
        
        self.file_count_var = tk.StringVar(value="파일 개수: 0")
        ttk.Label(info_frame, textvariable=self.file_count_var).pack(side="left")
        
        self.filter_info_var = tk.StringVar(value="")
        ttk.Label(info_frame, textvariable=self.filter_info_var, 
                 foreground="blue").pack(side="left", padx=(10, 0))
        
        # 파일 목록 (Treeview with 더 많은 정보)
        columns = ("파일명", "크기", "수정일", "확장자", "경로")
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        # 컬럼 설정
        self.file_tree.heading("파일명", text="파일명")
        self.file_tree.heading("크기", text="크기")
        self.file_tree.heading("수정일", text="수정일")
        self.file_tree.heading("확장자", text="확장자")
        self.file_tree.heading("경로", text="경로")
        
        self.file_tree.column("파일명", width=150)
        self.file_tree.column("크기", width=80)
        self.file_tree.column("수정일", width=100)
        self.file_tree.column("확장자", width=60)
        self.file_tree.column("경로", width=200)
        
        # 스크롤바
        tree_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.file_tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")
        
        # 더블클릭으로 파일 열기
        self.file_tree.bind("<Double-1>", self.open_file_location)
        
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
    
    def create_file_management_buttons(self, parent):
        """파일 관리 버튼들"""
        mgmt_frame = ttk.Frame(parent)
        mgmt_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Button(mgmt_frame, text="🗑️ 선택 제거", 
                  command=self.remove_selected).pack(side="left", padx=(0, 5))
        ttk.Button(mgmt_frame, text="🗑️ 전체 제거", 
                  command=self.clear_files).pack(side="left", padx=(0, 5))
        ttk.Button(mgmt_frame, text="↕️ 정렬", 
                  command=self.sort_files).pack(side="left", padx=(0, 5))
        ttk.Button(mgmt_frame, text="🔄 새로고침", 
                  command=self.refresh_files).pack(side="left")
    
    def create_filter_options(self, parent):
        """필터 옵션"""
        filter_frame = ttk.LabelFrame(parent, text="파일 필터", padding="10")
        filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # 필터 활성화
        self.filter_enabled_var = tk.BooleanVar()
        filter_check = ttk.Checkbutton(filter_frame, text="필터 사용", 
                                      variable=self.filter_enabled_var,
                                      command=self.on_filter_change)
        filter_check.pack(anchor="w", pady=(0, 5))
        
        # 필터 옵션들
        filter_options = ttk.Frame(filter_frame)
        filter_options.pack(fill="x")
        
        # 확장자 필터
        ttk.Label(filter_options, text="확장자:").grid(row=0, column=0, sticky="w", pady=2)
        self.ext_filter_var = tk.StringVar()
        ttk.Entry(filter_options, textvariable=self.ext_filter_var, 
                 width=20).grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=2)
        
        # 크기 필터
        ttk.Label(filter_options, text="최소 크기:").grid(row=1, column=0, sticky="w", pady=2)
        self.min_size_var = tk.StringVar()
        ttk.Entry(filter_options, textvariable=self.min_size_var, 
                 width=20).grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=2)
        
        ttk.Label(filter_options, text="최대 크기:").grid(row=2, column=0, sticky="w", pady=2)
        self.max_size_var = tk.StringVar()
        ttk.Entry(filter_options, textvariable=self.max_size_var, 
                 width=20).grid(row=2, column=1, sticky="ew", padx=(5, 0), pady=2)
        
        # 파일명 패턴 필터
        ttk.Label(filter_options, text="파일명 패턴:").grid(row=3, column=0, sticky="w", pady=2)
        self.pattern_var = tk.StringVar()
        ttk.Entry(filter_options, textvariable=self.pattern_var, 
                 width=20).grid(row=3, column=1, sticky="ew", padx=(5, 0), pady=2)
        
        filter_options.columnconfigure(1, weight=1)
        
        # 필터 이벤트 바인딩
        self.ext_filter_var.trace('w', self.on_filter_change)
        self.min_size_var.trace('w', self.on_filter_change)
        self.max_size_var.trace('w', self.on_filter_change)
        self.pattern_var.trace('w', self.on_filter_change)
    
    def create_rename_options(self, parent):
        """이름 변경 옵션"""
        options_frame = ttk.LabelFrame(parent, text="이름 변경 옵션", padding="10")
        options_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # 모드 선택
        self.mode_var = tk.StringVar(value="prefix")
        
        mode_frame = ttk.Frame(options_frame)
        mode_frame.pack(fill="x", pady=(0, 10))
        
        modes = [
            ("접두사", "prefix"),
            ("접미사", "suffix"),
            ("찾기/바꾸기", "find_replace"),
            ("연번", "numbering"),
            ("템플릿", "template")
        ]
        
        for i, (text, value) in enumerate(modes):
            ttk.Radiobutton(mode_frame, text=text, variable=self.mode_var, 
                           value=value).grid(row=0, column=i, padx=(0, 10))
        
        # 입력 영역
        self.create_option_inputs(options_frame)
        
        # 고급 옵션
        advanced_frame = ttk.Frame(options_frame)
        advanced_frame.pack(fill="x", pady=(10, 0))
        
        self.preserve_case_var = tk.BooleanVar()
        ttk.Checkbutton(advanced_frame, text="대소문자 보존", 
                       variable=self.preserve_case_var).pack(side="left", padx=(0, 10))
        
        self.backup_enabled_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(advanced_frame, text="백업 생성", 
                       variable=self.backup_enabled_var).pack(side="left")
    
    def create_option_inputs(self, parent):
        """옵션 입력 필드들"""
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill="x")
        
        # 기본 텍스트 입력
        basic_frame = ttk.Frame(input_frame)
        basic_frame.grid(row=0, column=0, sticky="ew", pady=2)
        
        ttk.Label(basic_frame, text="텍스트:").pack(side="left")
        self.text_var = tk.StringVar()
        ttk.Entry(basic_frame, textvariable=self.text_var, width=20).pack(side="left", padx=(5, 0))
        
        # 찾기/바꾸기
        find_frame = ttk.Frame(input_frame)
        find_frame.grid(row=1, column=0, sticky="ew", pady=2)
        
        ttk.Label(find_frame, text="찾기:").pack(side="left")
        self.find_var = tk.StringVar()
        ttk.Entry(find_frame, textvariable=self.find_var, width=12).pack(side="left", padx=(5, 10))
        
        ttk.Label(find_frame, text="바꾸기:").pack(side="left")
        self.replace_var = tk.StringVar()
        ttk.Entry(find_frame, textvariable=self.replace_var, width=12).pack(side="left", padx=(5, 0))
        
        # 정규식 및 대소문자 옵션
        options_subframe = ttk.Frame(find_frame)
        options_subframe.pack(side="right", padx=(10, 0))
        
        self.regex_var = tk.BooleanVar()
        ttk.Checkbutton(options_subframe, text="정규식", 
                       variable=self.regex_var).pack(side="left")
        
        self.ignore_case_var = tk.BooleanVar()
        ttk.Checkbutton(options_subframe, text="대소문자 무시", 
                       variable=self.ignore_case_var).pack(side="left", padx=(5, 0))
        
        # 연번 매기기
        number_frame = ttk.Frame(input_frame)
        number_frame.grid(row=2, column=0, sticky="ew", pady=2)
        
        ttk.Label(number_frame, text="시작:").pack(side="left")
        self.start_var = tk.StringVar(value="1")
        ttk.Entry(number_frame, textvariable=self.start_var, width=5).pack(side="left", padx=(5, 10))
        
        ttk.Label(number_frame, text="자릿수:").pack(side="left")
        self.digits_var = tk.StringVar(value="3")
        ttk.Entry(number_frame, textvariable=self.digits_var, width=5).pack(side="left", padx=(5, 10))
        
        ttk.Label(number_frame, text="증가값:").pack(side="left")
        self.step_var = tk.StringVar(value="1")
        ttk.Entry(number_frame, textvariable=self.step_var, width=5).pack(side="left", padx=(5, 0))
        
        # 템플릿
        template_frame = ttk.Frame(input_frame)
        template_frame.grid(row=3, column=0, sticky="ew", pady=2)
        
        ttk.Label(template_frame, text="템플릿:").pack(side="left")
        self.template_var = tk.StringVar(value="{number:03d}_{name}")
        ttk.Entry(template_frame, textvariable=self.template_var, width=30).pack(side="left", padx=(5, 0))
        
        input_frame.columnconfigure(0, weight=1)
    
    def create_preview_area(self, parent):
        """미리보기 영역"""
        preview_frame = ttk.LabelFrame(parent, text="미리보기", padding="5")
        preview_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        
        # 미리보기 설정
        preview_settings = ttk.Frame(preview_frame)
        preview_settings.pack(fill="x", pady=(0, 5))
        
        self.preview_auto_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(preview_settings, text="자동 미리보기", 
                       variable=self.preview_auto_var).pack(side="left")
        
        ttk.Button(preview_settings, text="🔄 새로고침", 
                  command=self.update_preview).pack(side="right")
        
        # 미리보기 목록
        columns = ("현재 이름", "새 이름", "상태")
        self.preview_tree = ttk.Treeview(preview_frame, columns=columns, show="headings", height=10)
        
        self.preview_tree.heading("현재 이름", text="현재 이름")
        self.preview_tree.heading("새 이름", text="새 이름")
        self.preview_tree.heading("상태", text="상태")
        
        self.preview_tree.column("현재 이름", width=150)
        self.preview_tree.column("새 이름", width=150)
        self.preview_tree.column("상태", width=80)
        
        # 스크롤바
        preview_scroll = ttk.Scrollbar(preview_frame, orient="vertical", command=self.preview_tree.yview)
        self.preview_tree.configure(yscrollcommand=preview_scroll.set)
        
        self.preview_tree.pack(side="left", fill="both", expand=True)
        preview_scroll.pack(side="right", fill="y")
        
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(1, weight=1)
    
    def create_action_buttons(self, parent):
        """실행 버튼들"""
        action_frame = ttk.Frame(parent)
        action_frame.grid(row=3, column=0, sticky="ew", pady=10)
        
        # 첫 번째 줄
        top_buttons = ttk.Frame(action_frame)
        top_buttons.pack(fill="x", pady=(0, 5))
        
        ttk.Button(top_buttons, text="💾 설정 저장", 
                  command=self.save_settings).pack(side="left", padx=(0, 5))
        ttk.Button(top_buttons, text="📂 설정 불러오기", 
                  command=self.load_settings_dialog).pack(side="left", padx=(0, 5))
        ttk.Button(top_buttons, text="↩️ 실행 취소", 
                  command=self.undo_last_operation).pack(side="right")
        
        # 두 번째 줄
        bottom_buttons = ttk.Frame(action_frame)
        bottom_buttons.pack(fill="x")
        
        ttk.Button(bottom_buttons, text="🧪 테스트 실행", 
                  command=self.test_execution).pack(side="left", padx=(0, 10))
        
        ttk.Button(bottom_buttons, text="✅ 실행", 
                  command=self.execute_rename,
                  style="Accent.TButton").pack(side="right", padx=(10, 0))
        
        ttk.Button(bottom_buttons, text="⚡ 일괄 실행", 
                  command=self.batch_execute).pack(side="right")
    
    def create_status_bar(self, parent):
        """상태바"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        
        self.status_var = tk.StringVar(value="준비")
        ttk.Label(status_frame, textvariable=self.status_var).pack(side="left")
        
        # 진행률 표시
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                           length=200, mode='determinate')
        self.progress_bar.pack(side="right", padx=(10, 0))
        
        self.progress_text_var = tk.StringVar()
        ttk.Label(status_frame, textvariable=self.progress_text_var).pack(side="right", padx=(0, 10))
    
    def setup_menu(self):
        """메뉴바 설정"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 파일 메뉴
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="파일", menu=file_menu)
        file_menu.add_command(label="프로젝트 저장", command=self.save_project)
        file_menu.add_command(label="프로젝트 열기", command=self.load_project)
        file_menu.add_separator()
        file_menu.add_command(label="설정", command=self.show_preferences)
        file_menu.add_separator()
        file_menu.add_command(label="종료", command=self.root.quit)
        
        # 편집 메뉴
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="편집", menu=edit_menu)
        edit_menu.add_command(label="모두 선택", command=self.select_all_files)
        edit_menu.add_command(label="선택 해제", command=self.deselect_all_files)
        edit_menu.add_separator()
        edit_menu.add_command(label="실행 취소", command=self.undo_last_operation)
        
        # 도구 메뉴
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="도구", menu=tools_menu)
        tools_menu.add_command(label="중복 파일 찾기", command=self.find_duplicates)
        tools_menu.add_command(label="파일 검증", command=self.validate_files)
        tools_menu.add_command(label="통계 보기", command=self.show_statistics)
        
        # 도움말 메뉴
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="도움말", menu=help_menu)
        help_menu.add_command(label="사용법", command=self.show_help)
        help_menu.add_command(label="정보", command=self.show_about)
    
    def setup_drag_drop(self):
        """드래그 앤 드롭 설정"""
        if DND_AVAILABLE:
            self.drop_label.drop_target_register(DND_FILES)
            self.drop_label.dnd_bind('<<Drop>>', self.on_drop)
            self.file_tree.drop_target_register(DND_FILES)
            self.file_tree.dnd_bind('<<Drop>>', self.on_drop)
    
    def setup_preview_bindings(self):
        """미리보기 이벤트 바인딩"""
        vars_to_trace = [
            self.mode_var, self.text_var, self.find_var, self.replace_var,
            self.regex_var, self.ignore_case_var, self.start_var, self.digits_var,
            self.step_var, self.template_var, self.preserve_case_var
        ]
        
        for var in vars_to_trace:
            var.trace('w', self.on_option_change)
    
    # 주요 기능 메서드들
    def on_drop(self, event):
        """드롭 이벤트 처리"""
        files = self.root.tk.splitlist(event.data)
        self.add_files(files)
    
    def select_files(self):
        """파일 선택 다이얼로그"""
        files = filedialog.askopenfilenames(
            title="파일 선택",
            filetypes=[
                ("모든 파일", "*.*"),
                ("이미지 파일", "*.jpg *.jpeg *.png *.gif *.bmp"),
                ("문서 파일", "*.txt *.pdf *.doc *.docx"),
                ("동영상 파일", "*.mp4 *.avi *.mkv *.mov")
            ]
        )
        if files:
            self.add_files(files)
    
    def select_folder(self):
        """폴더 선택 및 파일 추가"""
        folder = filedialog.askdirectory(title="폴더 선택")
        if folder:
            files = [os.path.join(folder, f) for f in os.listdir(folder) 
                    if os.path.isfile(os.path.join(folder, f))]
            self.add_files(files)
    
    def select_folder_recursive(self):
        """재귀적 폴더 선택"""
        folder = filedialog.askdirectory(title="폴더 선택 (하위 폴더 포함)")
        if folder:
            files = []
            for root, dirs, filenames in os.walk(folder):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
            self.add_files(files)
    
    def add_files(self, file_paths):
        """파일 목록에 파일 추가"""
        added_count = 0
        
        for file_path in file_paths:
            if os.path.isfile(file_path) and file_path not in self.files:
                self.files.append(file_path)
                added_count += 1
        
        self.refresh_file_tree()
        self.update_preview()
        
        if added_count > 0:
            self.status_var.set(f"{added_count}개 파일이 추가되었습니다.")
    
    def refresh_file_tree(self):
        """파일 트리 새로고침"""
        self.file_tree.delete(*self.file_tree.get_children())
        
        filtered_files = self.get_filtered_files()
        
        for file_path in filtered_files:
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                size = self.get_file_size(file_path)
                modified = self.get_file_modified_date(file_path)
                ext = os.path.splitext(filename)[1]
                
                self.file_tree.insert("", "end", values=(filename, size, modified, ext, file_path))
        
        self.update_file_count()
    
    def get_filtered_files(self):
        """필터링된 파일 목록 반환"""
        if not self.filter_enabled_var.get():
            return self.files
        
        filtered = []
        for file_path in self.files:
            if self.matches_filter(file_path):
                filtered.append(file_path)
        
        return filtered
    
    def matches_filter(self, file_path):
        """파일이 필터 조건에 맞는지 확인"""
        try:
            filename = os.path.basename(file_path)
            
            # 확장자 필터
            if self.ext_filter_var.get():
                ext_filter = self.ext_filter_var.get().lower()
                file_ext = os.path.splitext(filename)[1].lower()
                if ext_filter not in file_ext:
                    return False
            
            # 크기 필터
            file_size = os.path.getsize(file_path)
            
            if self.min_size_var.get():
                min_size = self.parse_size(self.min_size_var.get())
                if file_size < min_size:
                    return False
            
            if self.max_size_var.get():
                max_size = self.parse_size(self.max_size_var.get())
                if file_size > max_size:
                    return False
            
            # 패턴 필터
            if self.pattern_var.get():
                pattern = self.pattern_var.get()
                if pattern not in filename:
                    return False
            
            return True
            
        except Exception:
            return False
    
    def parse_size(self, size_str):
        """크기 문자열을 바이트로 변환"""
        if not size_str:
            return 0
        
        size_str = size_str.upper()
        multipliers = {
            'B': 1, 'K': 1024, 'KB': 1024,
            'M': 1024**2, 'MB': 1024**2,
            'G': 1024**3, 'GB': 1024**3
        }
        
        for suffix, multiplier in multipliers.items():
            if size_str.endswith(suffix):
                try:
                    number = float(size_str[:-len(suffix)])
                    return int(number * multiplier)
                except ValueError:
                    break
        
        try:
            return int(size_str)
        except ValueError:
            return 0
    
    def get_file_size(self, file_path):
        """파일 크기를 읽기 쉬운 형태로 반환"""
        try:
            size = os.path.getsize(file_path)
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size/1024:.1f} KB"
            else:
                return f"{size/(1024*1024):.1f} MB"
        except OSError:
            return "알 수 없음"
    
    def get_file_modified_date(self, file_path):
        """파일 수정일 반환"""
        try:
            mtime = os.path.getmtime(file_path)
            return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        except OSError:
            return "알 수 없음"
    
    def generate_new_name(self, file_path, index):
        """새로운 파일명 생성"""
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        mode = self.mode_var.get()
        
        try:
            if mode == "prefix":
                text = self.text_var.get()
                return f"{text}{filename}"
            
            elif mode == "suffix":
                text = self.text_var.get()
                return f"{name}{text}{ext}"
            
            elif mode == "find_replace":
                find_text = self.find_var.get()
                replace_text = self.replace_var.get()
                
                if not find_text:
                    return filename
                
                if self.regex_var.get():
                    try:
                        flags = re.IGNORECASE if self.ignore_case_var.get() else 0
                        return re.sub(find_text, replace_text, filename, flags=flags)
                    except re.error:
                        return filename
                else:
                    if self.ignore_case_var.get():
                        return re.sub(re.escape(find_text), replace_text, filename, flags=re.IGNORECASE)
                    else:
                        return filename.replace(find_text, replace_text)
            
            elif mode == "numbering":
                try:
                    start = int(self.start_var.get())
                    digits = int(self.digits_var.get())
                    step = int(self.step_var.get())
                    
                    number = start + (index * step)
                    number_str = f"{number:0{digits}d}"
                    return f"{number_str}_{filename}"
                    
                except ValueError:
                    return filename
            
            elif mode == "template":
                try:
                    template = self.template_var.get()
                    start = int(self.start_var.get())
                    digits = int(self.digits_var.get())
                    step = int(self.step_var.get())
                    
                    number = start + (index * step)
                    number_str = f"{number:0{digits}d}"
                    
                    new_name = template.format(
                        number=number_str,
                        name=name,
                        ext=ext[1:] if ext else "",
                        filename=filename,
                        index=index,
                        date=datetime.now().strftime("%Y%m%d"),
                        time=datetime.now().strftime("%H%M%S")
                    )
                    
                    if not new_name.endswith(ext) and ext:
                        new_name += ext
                    
                    return new_name
                    
                except (ValueError, KeyError):
                    return filename
            
        except Exception:
            return filename
        
        return filename
    
    def update_preview(self):
        """미리보기 업데이트"""
        if not self.preview_auto_var.get():
            return
        
        self.preview_tree.delete(*self.preview_tree.get_children())
        
        filtered_files = self.get_filtered_files()
        
        for index, file_path in enumerate(filtered_files):
            current_name = os.path.basename(file_path)
            new_name = self.generate_new_name(file_path, index)
            
            if current_name != new_name:
                status = "변경"
                tag = "changed"
            else:
                status = "동일"
                tag = "unchanged"
            
            self.preview_tree.insert("", "end", values=(current_name, new_name, status), tags=(tag,))
        
        self.preview_tree.tag_configure("changed", background="#e8f5e8")
        self.preview_tree.tag_configure("unchanged", background="#f5f5f5")
    
    def execute_rename(self):
        """실제 파일명 변경 실행"""
        filtered_files = self.get_filtered_files()
        
        if not filtered_files:
            messagebox.showwarning("경고", "변경할 파일이 없습니다.")
            return
        
        # 변경 계획 생성
        rename_plan = []
        for index, file_path in enumerate(filtered_files):
            current_name = os.path.basename(file_path)
            new_name = self.generate_new_name(file_path, index)
            
            if current_name != new_name:
                directory = os.path.dirname(file_path)
                new_path = os.path.join(directory, new_name)
                rename_plan.append((file_path, new_path))
        
        if not rename_plan:
            messagebox.showinfo("정보", "변경할 파일이 없습니다.")
            return
        
        # 백업 생성 확인
        if self.backup_enabled_var.get():
            backup_result = self.create_backup(rename_plan)
            if not backup_result:
                return
        
        # 실행 확인
        result = messagebox.askyesno(
            "확인", 
            f"{len(rename_plan)}개 파일의 이름을 변경하시겠습니까?\n"
            f"{'백업이 생성됩니다.' if self.backup_enabled_var.get() else '백업이 생성되지 않습니다.'}"
        )
        
        if not result:
            return
        
        # 진행률 초기화
        self.progress_var.set(0)
        self.progress_text_var.set("0%")
        self.root.update()
        
        # 실행
        success_count = 0
        errors = []
        total = len(rename_plan)
        
        for i, (old_path, new_path) in enumerate(rename_plan):
            try:
                # 진행률 업데이트
                progress = (i + 1) / total * 100
                self.progress_var.set(progress)
                self.progress_text_var.set(f"{progress:.1f}%")
                self.status_var.set(f"처리 중: {os.path.basename(old_path)}")
                self.root.update()
                
                # 중복 파일명 확인
                if os.path.exists(new_path):
                    errors.append(f"{os.path.basename(old_path)}: 대상 파일이 이미 존재함")
                    continue
                
                # 파일명 변경
                os.rename(old_path, new_path)
                success_count += 1
                
                # 내부 목록 업데이트
                index = self.files.index(old_path)
                self.files[index] = new_path
                
            except Exception as e:
                errors.append(f"{os.path.basename(old_path)}: {str(e)}")
        
        # 진행률 완료
        self.progress_var.set(100)
        self.progress_text_var.set("완료")
        self.status_var.set("작업 완료")
        
        # 결과 보고
        result_msg = f"성공: {success_count}개 파일 변경됨"
        if errors:
            result_msg += f"\n실패: {len(errors)}개"
            if len(errors) <= 5:
                result_msg += "\n" + "\n".join(errors)
        
        messagebox.showinfo("작업 완료", result_msg)
        
        # UI 새로고침
        self.refresh_file_tree()
        self.update_preview()
    
    def create_backup(self, rename_plan):
        """백업 생성"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = Path.home() / ".file_renamer_backups" / timestamp
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # 백업 정보 저장
            backup_info = {
                "timestamp": timestamp,
                "original_files": len(rename_plan),
                "changes": []
            }
            
            for old_path, new_path in rename_plan:
                if old_path != new_path:
                    # 파일 복사
                    backup_file = backup_dir / os.path.basename(old_path)
                    shutil.copy2(old_path, backup_file)
                    
                    backup_info["changes"].append({
                        "old_path": old_path,
                        "new_path": new_path,
                        "backup_file": str(backup_file)
                    })
            
            # 백업 정보 파일 저장
            info_file = backup_dir / "backup_info.json"
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, ensure_ascii=False, indent=2)
            
            # 백업 히스토리에 추가
            self.backup_history.append(str(backup_dir))
            
            self.status_var.set(f"백업 생성: {backup_dir}")
            return True
            
        except Exception as e:
            messagebox.showerror("백업 오류", f"백업 생성 실패: {e}")
            return False
    
    # 스텁 메서드들 (기본 구현)
    def on_filter_change(self, *args):
        """필터 변경 시 호출"""
        self.refresh_file_tree()
        self.update_preview()
    
    def on_option_change(self, *args):
        """옵션 변경 시 호출"""
        self.update_preview()
    
    def update_file_count(self):
        """파일 개수 업데이트"""
        total = len(self.files)
        filtered = len(self.get_filtered_files())
        
        if self.filter_enabled_var.get() and total != filtered:
            self.file_count_var.set(f"파일 개수: {filtered}/{total}")
            self.filter_info_var.set("(필터링됨)")
        else:
            self.file_count_var.set(f"파일 개수: {total}")
            self.filter_info_var.set("")
    
    def open_file_location(self, event):
        """파일 위치 열기"""
        selection = self.file_tree.selection()
        if selection:
            item = self.file_tree.item(selection[0])
            file_path = item['values'][4]  # 경로 컬럼
            try:
                os.startfile(os.path.dirname(file_path))
            except:
                pass
    
    def clear_files(self):
        """모든 파일 제거"""
        if self.files:
            result = messagebox.askyesno("확인", "모든 파일을 제거하시겠습니까?")
            if result:
                self.files.clear()
                self.refresh_file_tree()
                self.update_preview()
    
    def remove_selected(self):
        """선택된 파일 제거"""
        selection = self.file_tree.selection()
        if selection:
            for item in selection:
                values = self.file_tree.item(item)['values']
                file_path = values[4]  # 경로 컬럼
                if file_path in self.files:
                    self.files.remove(file_path)
            
            self.refresh_file_tree()
            self.update_preview()
    
    def sort_files(self):
        """파일 정렬"""
        self.files.sort(key=lambda x: os.path.basename(x).lower())
        self.refresh_file_tree()
        self.update_preview()
    
    def refresh_files(self):
        """파일 새로고침"""
        # 존재하지 않는 파일 제거
        existing_files = [f for f in self.files if os.path.exists(f)]
        self.files = existing_files
        self.refresh_file_tree()
        self.update_preview()
    
    # 스텁 메서드들 (메뉴 기능)
    def save_settings(self):
        messagebox.showinfo("정보", "설정 저장 기능은 구현 예정입니다.")
    
    def load_settings(self):
        pass  # 실제 설정 로드 로직
    
    def load_settings_dialog(self):
        messagebox.showinfo("정보", "설정 불러오기 기능은 구현 예정입니다.")
    
    def save_project(self):
        messagebox.showinfo("정보", "프로젝트 저장 기능은 구현 예정입니다.")
    
    def load_project(self):
        messagebox.showinfo("정보", "프로젝트 불러오기 기능은 구현 예정입니다.")
    
    def show_preferences(self):
        messagebox.showinfo("정보", "환경설정 기능은 구현 예정입니다.")
    
    def select_all_files(self):
        for item in self.file_tree.get_children():
            self.file_tree.selection_add(item)
    
    def deselect_all_files(self):
        self.file_tree.selection_remove(self.file_tree.selection())
    
    def undo_last_operation(self):
        messagebox.showinfo("정보", "실행 취소 기능은 구현 예정입니다.")
    
    def find_duplicates(self):
        messagebox.showinfo("정보", "중복 파일 찾기 기능은 구현 예정입니다.")
    
    def validate_files(self):
        messagebox.showinfo("정보", "파일 검증 기능은 구현 예정입니다.")
    
    def show_statistics(self):
        messagebox.showinfo("정보", "통계 보기 기능은 구현 예정입니다.")
    
    def show_help(self):
        messagebox.showinfo("도움말", "파일 리네이머 v5.0\n\n완성된 파일 관리 도구입니다.")
    
    def show_about(self):
        messagebox.showinfo("정보", "파일 리네이머 v5.0\nChapter 4 Step 5 완성 버전")
    
    def test_execution(self):
        messagebox.showinfo("정보", "테스트 실행 기능은 구현 예정입니다.")
    
    def batch_execute(self):
        messagebox.showinfo("정보", "일괄 실행 기능은 구현 예정입니다.")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FileManagementRenamer()
    app.run()