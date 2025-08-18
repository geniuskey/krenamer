import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
import re
import threading
import logging
import shutil
import datetime
import time
from pathlib import Path
from typing import Dict, List, Callable, Any
from rename_engine import RenameEngine

# 드래그 앤 드롭 라이브러리 (선택적)
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

class BackupManager:
    """백업 관리 시스템"""
    
    def __init__(self, backup_dir: str):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = self.backup_dir / "backup_history.json"
        self.load_history()
    
    def load_history(self):
        """백업 히스토리 로드"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            else:
                self.history = []
        except Exception:
            self.history = []
    
    def save_history(self):
        """백업 히스토리 저장"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"백업 히스토리 저장 실패: {e}")
    
    def create_backup(self, files: List[tuple], operation_name: str = "rename") -> str:
        """백업 생성"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_id = f"{operation_name}_{timestamp}"
        backup_path = self.backup_dir / backup_id
        backup_path.mkdir(exist_ok=True)
        
        backup_info = {
            'id': backup_id,
            'timestamp': timestamp,
            'operation': operation_name,
            'files': [],
            'metadata_file': str(backup_path / "metadata.json")
        }
        
        try:
            for old_path, new_path in files:
                if os.path.exists(old_path):
                    backup_file_path = backup_path / os.path.basename(old_path)
                    shutil.copy2(old_path, backup_file_path)
                    
                    backup_info['files'].append({
                        'original_path': old_path,
                        'new_path': new_path,
                        'backup_path': str(backup_file_path),
                        'size': os.path.getsize(old_path),
                        'modified': os.path.getmtime(old_path)
                    })
            
            # 메타데이터 저장
            with open(backup_info['metadata_file'], 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, indent=2, ensure_ascii=False)
            
            self.history.append(backup_info)
            self.save_history()
            
            logging.info(f"백업 생성 완료: {backup_id}")
            return backup_id
            
        except Exception as e:
            logging.error(f"백업 생성 실패: {e}")
            return None
    
    def get_backup_list(self) -> List[Dict]:
        """백업 목록 반환"""
        return sorted(self.history, key=lambda x: x['timestamp'], reverse=True)

class ProgressDialog:
    """진행률 표시 대화상자"""
    
    def __init__(self, parent, title="작업 진행 중"):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x150")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 중앙에 위치
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # 위젯 생성
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_var = tk.StringVar(value="작업 준비 중...")
        ttk.Label(main_frame, textvariable=self.status_var).pack(pady=(0, 10))
        
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        self.cancel_button = ttk.Button(main_frame, text="취소", command=self.cancel)
        self.cancel_button.pack()
        
        self.cancelled = False
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel)
    
    def update(self, current: int, total: int, status: str):
        """진행률 업데이트"""
        if not self.cancelled:
            self.progress['maximum'] = total
            self.progress['value'] = current
            self.status_var.set(f"{status} ({current}/{total})")
            self.dialog.update()
    
    def cancel(self):
        """작업 취소"""
        self.cancelled = True
        self.dialog.destroy()
    
    def close(self):
        """대화상자 닫기"""
        try:
            self.dialog.destroy()
        except:
            pass

class ProfessionalRenamer:
    """전문가급 파일 리네이머"""
    
    def __init__(self):
        # 드래그 앤 드롭 지원 여부에 따라 다른 방식으로 윈도우 생성
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
        
        self.root.title("KRenamer Pro v5.0 - 전문가급")
        self.root.geometry("1300x900")
        self.root.minsize(1100, 750)
        
        # 로깅 설정
        self.setup_logging()
        
        # 엔진 초기화
        self.engine = RenameEngine()
        self.engine.on_files_changed = self.on_files_changed
        self.engine.on_options_changed = self.on_options_changed
        
        # 백업 매니저 초기화
        self.backup_dir = os.path.expanduser("~/.krenamer/backups")
        self.backup_manager = BackupManager(self.backup_dir)
        
        # 설정 파일 경로
        self.settings_dir = os.path.expanduser("~/.krenamer")
        self.settings_file = os.path.join(self.settings_dir, "settings.json")
        self.presets_file = os.path.join(self.settings_dir, "presets.json")
        
        # 필터링 상태
        self.search_text = ""
        self.filter_status = "all"
        
        # 스레딩 관련
        self.current_operation = None
        self.operation_cancelled = False
        
        # 설정 로드
        self.settings = self.load_settings()
        self.presets = self.load_presets()
        
        self.create_widgets()
        self.create_variables()
        self.bind_events()
        self.setup_drag_drop()
        self.setup_keyboard_shortcuts()
        
        # 설정 적용
        self.apply_settings()
        
        logging.info("KRenamer Pro 시작")
    
    def setup_logging(self):
        """로깅 시스템 설정"""
        log_dir = os.path.expanduser("~/.krenamer/logs")
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"krenamer_{datetime.date.today().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    def create_widgets(self):
        """위젯 생성"""
        # 메뉴바
        self.create_menubar()
        
        # 메인 컨테이너
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 상단 툴바
        self.create_toolbar(main_frame)
        
        # 2-패널 메인 영역
        self.create_main_panels(main_frame)
        
        # 하단 상태바
        self.create_statusbar(main_frame)
    
    def create_menubar(self):
        """메뉴바 생성"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 파일 메뉴
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="파일", menu=file_menu)
        file_menu.add_command(label="파일 추가...", command=self.add_files)
        file_menu.add_command(label="폴더 추가...", command=self.add_folder)
        file_menu.add_command(label="재귀적 폴더 추가...", command=self.add_folder_recursive)
        file_menu.add_separator()
        file_menu.add_command(label="종료", command=self.quit_app)
        
        # 작업 메뉴
        action_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="작업", menu=action_menu)
        action_menu.add_command(label="미리보기 새로고침", command=self.refresh_preview)
        action_menu.add_command(label="이름 변경 실행", command=self.execute_rename_threaded)
        action_menu.add_separator()
        action_menu.add_command(label="파일 검증", command=self.validate_files)
        
        # 백업 메뉴
        backup_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="백업", menu=backup_menu)
        backup_menu.add_command(label="백업 관리...", command=self.show_backup_manager)
        
        # 도구 메뉴
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="도구", menu=tools_menu)
        tools_menu.add_command(label="중복 파일 찾기", command=self.find_duplicates)
        tools_menu.add_command(label="배치 처리기...", command=self.show_batch_processor)
        
        # 도움말 메뉴
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="도움말", menu=help_menu)
        help_menu.add_command(label="정보", command=self.show_about)
    
    def create_toolbar(self, parent):
        """상단 툴바"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        # 파일 관리 버튼들
        ttk.Button(toolbar, text="📁 파일 추가", 
                  command=self.add_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="📂 폴더 추가", 
                  command=self.add_folder).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="🔄 재귀 추가", 
                  command=self.add_folder_recursive).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # 검색 기능
        ttk.Label(toolbar, text="검색:").pack(side=tk.LEFT, padx=(5, 2))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=15)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(toolbar, text="🔍", command=self.apply_search, 
                  width=3).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="❌", command=self.clear_search, 
                  width=3).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # 작업 버튼들
        ttk.Button(toolbar, text="🔄 새로고침", 
                  command=self.refresh_preview).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="✅ 실행", 
                  command=self.execute_rename_threaded).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="💾 백업", 
                  command=self.show_backup_manager).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # 초기화
        ttk.Button(toolbar, text="🗑️ 전체 삭제", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="⚙️ 초기화", 
                  command=self.reset_options).pack(side=tk.LEFT)
    
    def create_main_panels(self, parent):
        """메인 2-패널 영역"""
        # PanedWindow로 좌우 분할
        paned = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # 왼쪽 패널 (파일 관리 + 옵션)
        left_panel = ttk.Frame(paned)
        paned.add(left_panel, weight=2)
        
        # 오른쪽 패널 (미리보기)
        right_panel = ttk.Frame(paned)
        paned.add(right_panel, weight=3)
        
        self.create_left_panel(left_panel)
        self.create_right_panel(right_panel)
    
    def create_left_panel(self, parent):
        """왼쪽 패널 - 파일 관리와 옵션"""
        # 드래그 앤 드롭 영역
        self.create_drop_area(parent)
        
        # 파일 목록 섹션
        files_group = ttk.LabelFrame(parent, text="파일 목록", padding="10")
        files_group.pack(fill=tk.BOTH, expand=True, pady=(10, 10))
        
        # 파일 필터와 통계
        filter_frame = ttk.Frame(files_group)
        filter_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(filter_frame, text="필터:").pack(side=tk.LEFT)
        
        self.filter_var = tk.StringVar(value="모든 파일")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                   values=["모든 파일", "이미지 파일", "문서 파일", "비디오 파일"],
                                   width=12, state="readonly")
        filter_combo.pack(side=tk.LEFT, padx=(5, 15))
        filter_combo.bind('<<ComboboxSelected>>', self.on_file_filter_change)
        
        self.file_count_var = tk.StringVar(value="파일 개수: 0")
        ttk.Label(filter_frame, textvariable=self.file_count_var,
                 foreground="blue").pack(side=tk.RIGHT)
        
        # 파일 목록 (Listbox)
        list_frame = ttk.Frame(files_group)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.files_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED,
                                       font=("맑은 고딕", 9))
        
        list_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL,
                                   command=self.files_listbox.yview)
        self.files_listbox.configure(yscrollcommand=list_scroll.set)
        
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 파일 조작 버튼들
        file_buttons = ttk.Frame(files_group)
        file_buttons.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(file_buttons, text="❌ 선택 삭제",
                  command=self.remove_selected).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(file_buttons, text="🔺 위로",
                  command=self.move_up).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(file_buttons, text="🔻 아래로",
                  command=self.move_down).pack(side=tk.LEFT)
        
        # 이름 변경 옵션 섹션
        options_group = ttk.LabelFrame(parent, text="이름 변경 옵션", padding="10")
        options_group.pack(fill=tk.X)
        
        self.create_rename_options(options_group)
    
    def create_drop_area(self, parent):
        """드래그 앤 드롭 영역 생성"""
        drop_frame = ttk.LabelFrame(parent, text="파일 추가", padding="10")
        drop_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 드롭 라벨
        if DND_AVAILABLE:
            drop_text = "📁 파일/폴더를 드래그 앤 드롭하세요\n[Shift]: 재귀적 추가"
            bg_color = "#e8f4fd"
        else:
            drop_text = "⚠️ 드래그 앤 드롭 불가능 - 버튼을 사용하세요"
            bg_color = "#fff2cc"
        
        self.drop_label = tk.Label(
            drop_frame, 
            text=drop_text,
            font=("맑은 고딕", 10),
            bg=bg_color,
            relief="ridge",
            bd=2,
            height=3
        )
        self.drop_label.pack(fill="x")
    
    def create_rename_options(self, parent):
        """이름 변경 옵션 위젯들"""
        # 접두사/접미사
        prefix_frame = ttk.Frame(parent)
        prefix_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(prefix_frame, text="접두사:", width=8).pack(side=tk.LEFT)
        self.prefix_var = tk.StringVar()
        ttk.Entry(prefix_frame, textvariable=self.prefix_var, width=15).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(prefix_frame, text="접미사:", width=8).pack(side=tk.LEFT)
        self.suffix_var = tk.StringVar()
        ttk.Entry(prefix_frame, textvariable=self.suffix_var, width=15).pack(side=tk.LEFT, padx=(5, 0))
        
        # 찾기/바꾸기
        replace_frame = ttk.Frame(parent)
        replace_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(replace_frame, text="찾기:", width=8).pack(side=tk.LEFT)
        self.find_var = tk.StringVar()
        ttk.Entry(replace_frame, textvariable=self.find_var, width=15).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(replace_frame, text="바꾸기:", width=8).pack(side=tk.LEFT)
        self.replace_var = tk.StringVar()
        ttk.Entry(replace_frame, textvariable=self.replace_var, width=15).pack(side=tk.LEFT, padx=(5, 0))
        
        # 순번 매기기
        number_frame = ttk.Frame(parent)
        number_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.use_numbering_var = tk.BooleanVar()
        ttk.Checkbutton(number_frame, text="순번 매기기", 
                       variable=self.use_numbering_var).pack(side=tk.LEFT)
        
        ttk.Label(number_frame, text="시작:").pack(side=tk.LEFT, padx=(15, 5))
        self.number_start_var = tk.IntVar(value=1)
        ttk.Spinbox(number_frame, from_=1, to=999, width=5,
                   textvariable=self.number_start_var).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(number_frame, text="자릿수:").pack(side=tk.LEFT, padx=(0, 5))
        self.number_digits_var = tk.IntVar(value=3)
        ttk.Spinbox(number_frame, from_=1, to=5, width=5,
                   textvariable=self.number_digits_var).pack(side=tk.LEFT)
    
    def create_right_panel(self, parent):
        """오른쪽 패널 - 미리보기"""
        preview_group = ttk.LabelFrame(parent, text="실시간 미리보기", padding="10")
        preview_group.pack(fill=tk.BOTH, expand=True)
        
        # 미리보기 필터
        filter_frame = ttk.Frame(preview_group)
        filter_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(filter_frame, text="표시:").pack(side=tk.LEFT)
        
        self.preview_filter_var = tk.StringVar(value="모두")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.preview_filter_var,
                                   values=["모두", "변경될 파일", "유효한 파일", "오류 파일"],
                                   width=12, state="readonly")
        filter_combo.pack(side=tk.LEFT, padx=(5, 15))
        filter_combo.bind('<<ComboboxSelected>>', self.on_preview_filter_change)
        
        # 정렬 옵션
        ttk.Label(filter_frame, text="정렬:").pack(side=tk.LEFT)
        
        self.sort_var = tk.StringVar(value="순서")
        sort_combo = ttk.Combobox(filter_frame, textvariable=self.sort_var,
                                 values=["순서", "파일명", "새파일명", "상태"],
                                 width=10, state="readonly")
        sort_combo.pack(side=tk.LEFT, padx=(5, 15))
        sort_combo.bind('<<ComboboxSelected>>', self.on_sort_change)
        
        # 미리보기 테이블
        tree_frame = ttk.Frame(preview_group)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        columns = ("순번", "원본 파일명", "새 파일명", "상태", "크기")
        self.preview_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        # 컬럼 설정
        self.preview_tree.heading("순번", text="#")
        self.preview_tree.heading("원본 파일명", text="원본 파일명")
        self.preview_tree.heading("새 파일명", text="새 파일명")
        self.preview_tree.heading("상태", text="상태")
        self.preview_tree.heading("크기", text="크기")
        
        self.preview_tree.column("순번", width=50, anchor=tk.CENTER)
        self.preview_tree.column("원본 파일명", width=200)
        self.preview_tree.column("새 파일명", width=200)
        self.preview_tree.column("상태", width=100, anchor=tk.CENTER)
        self.preview_tree.column("크기", width=80, anchor=tk.E)
        
        # 스크롤바
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL,
                                   command=self.preview_tree.yview)
        self.preview_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.preview_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 미리보기 통계
        stats_frame = ttk.Frame(preview_group)
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.preview_stats_var = tk.StringVar(value="변경 예정: 0개, 오류: 0개")
        ttk.Label(stats_frame, textvariable=self.preview_stats_var,
                 foreground="darkgreen").pack(side=tk.LEFT)
    
    def create_statusbar(self, parent):
        """하단 상태바"""
        statusbar = ttk.Frame(parent)
        statusbar.pack(fill=tk.X, pady=(5, 0))
        
        self.status_var = tk.StringVar(value="준비")
        ttk.Label(statusbar, textvariable=self.status_var).pack(side=tk.LEFT)
        
        # 진행률 표시
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(statusbar, variable=self.progress_var, length=200)
        self.progress_bar.pack(side=tk.RIGHT, padx=(10, 5))
        
        # 파일 통계
        self.file_stats_var = tk.StringVar(value="")
        ttk.Label(statusbar, textvariable=self.file_stats_var).pack(side=tk.RIGHT, padx=(0, 10))
    
    def setup_drag_drop(self):
        """드래그 앤 드롭 설정"""
        if DND_AVAILABLE:
            self.drop_label.drop_target_register(DND_FILES)
            self.drop_label.dnd_bind('<<Drop>>', self.on_drop)
            
            # 메인 윈도우에도 드롭 기능 추가
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_drop)
    
    def setup_keyboard_shortcuts(self):
        """키보드 단축키 설정"""
        # 파일 관련
        self.root.bind('<Control-o>', lambda e: self.add_files())
        self.root.bind('<Control-q>', lambda e: self.quit_app())
        
        # 편집 관련
        self.root.bind('<Control-a>', lambda e: self.select_all())
        self.root.bind('<Delete>', lambda e: self.remove_selected())
        
        # 작업 관련
        self.root.bind('<F5>', lambda e: self.refresh_preview())
        self.root.bind('<Control-Return>', lambda e: self.execute_rename_threaded())
    
    def create_variables(self):
        """변수 초기화"""
        # 초기 상태 설정
        self.update_file_list()
        self.update_preview()
    
    def bind_events(self):
        """이벤트 바인딩"""
        # 옵션 변경 감지 (실시간 미리보기)
        self.prefix_var.trace('w', self.on_option_change)
        self.suffix_var.trace('w', self.on_option_change)
        self.find_var.trace('w', self.on_option_change)
        self.replace_var.trace('w', self.on_option_change)
        self.use_numbering_var.trace('w', self.on_option_change)
        self.number_start_var.trace('w', self.on_option_change)
        self.number_digits_var.trace('w', self.on_option_change)
        
        # 검색 이벤트
        self.search_var.trace('w', self.on_search_change)
        
        # 리스트박스 선택 변경
        self.files_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        # 윈도우 닫기 이벤트
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
    
    # 설정 관리
    def load_settings(self):
        """설정 불러오기"""
        default_settings = {
            "window_geometry": "1300x900",
            "auto_backup": True,
            "backup_days": 30,
            "thread_count": 4
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    default_settings.update(settings)
            return default_settings
        except Exception:
            return default_settings
    
    def save_settings(self):
        """설정 저장"""
        try:
            os.makedirs(self.settings_dir, exist_ok=True)
            self.settings["window_geometry"] = self.root.geometry()
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"설정 저장 실패: {e}")
    
    def apply_settings(self):
        """설정 적용"""
        try:
            if "window_geometry" in self.settings:
                self.root.geometry(self.settings["window_geometry"])
        except Exception:
            pass
    
    def load_presets(self):
        """프리셋 불러오기"""
        try:
            if os.path.exists(self.presets_file):
                with open(self.presets_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception:
            return {}
    
    def save_presets(self):
        """프리셋 저장"""
        try:
            os.makedirs(self.settings_dir, exist_ok=True)
            with open(self.presets_file, 'w', encoding='utf-8') as f:
                json.dump(self.presets, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"프리셋 저장 실패: {e}")
    
    # 이벤트 핸들러들
    def on_files_changed(self):
        """파일 목록 변경 시 호출"""
        self.update_file_list()
        self.update_preview()
        self.update_statistics()
    
    def on_options_changed(self):
        """옵션 변경 시 호출"""
        self.update_preview()
    
    def on_option_change(self, *args):
        """GUI 옵션 변경 시 엔진에 반영"""
        self.engine.set_prefix(self.prefix_var.get())
        self.engine.set_suffix(self.suffix_var.get())
        self.engine.set_find_replace(self.find_var.get(), self.replace_var.get())
        self.engine.set_numbering(
            self.use_numbering_var.get(),
            self.number_start_var.get(),
            self.number_digits_var.get()
        )
    
    def on_search_change(self, *args):
        """검색어 변경 시"""
        search_text = self.search_var.get().lower()
        if len(search_text) >= 2 or search_text == "":
            self.apply_search()
    
    def on_file_select(self, event):
        """파일 선택 변경 시"""
        selected = self.files_listbox.curselection()
        if selected:
            self.status_var.set(f"{len(selected)}개 파일 선택됨")
        else:
            self.status_var.set("준비")
    
    def on_file_filter_change(self, event=None):
        """파일 필터 변경"""
        self.update_file_list()
    
    def on_preview_filter_change(self, event=None):
        """미리보기 필터 변경"""
        self.update_preview()
    
    def on_sort_change(self, event=None):
        """정렬 변경"""
        self.update_preview()
    
    def on_drop(self, event):
        """드롭 이벤트 처리"""
        try:
            files = self.parse_drop_files(event.data)
            if files:
                added = self.engine.add_files(files)
                self.status_var.set(f"{added}개 파일이 추가되었습니다")
        except Exception as e:
            self.status_var.set(f"드롭 오류: {str(e)}")
            logging.error(f"드롭 오류: {e}")
    
    def parse_drop_files(self, data):
        """드롭된 파일 데이터 파싱"""
        files = []
        try:
            raw_files = self.root.tk.splitlist(data)
            for file_path in raw_files:
                if file_path.startswith('{') and file_path.endswith('}'):
                    file_path = file_path[1:-1]
                
                if os.path.exists(file_path):
                    if os.path.isfile(file_path):
                        files.append(file_path)
                    elif os.path.isdir(file_path):
                        for item in os.listdir(file_path):
                            item_path = os.path.join(file_path, item)
                            if os.path.isfile(item_path):
                                files.append(item_path)
        except Exception:
            pass
        
        return files
    
    # 검색 및 필터링
    def apply_search(self):
        """검색 적용"""
        self.search_text = self.search_var.get().lower()
        self.update_file_list()
        self.status_var.set(f"검색: '{self.search_text}'" if self.search_text else "검색 해제")
    
    def clear_search(self):
        """검색 해제"""
        self.search_var.set("")
        self.search_text = ""
        self.update_file_list()
        self.status_var.set("검색 해제")
    
    # 파일 관리 메서드들
    def add_files(self):
        """파일 추가"""
        files = filedialog.askopenfilenames(
            title="추가할 파일을 선택하세요",
            filetypes=[
                ("모든 파일", "*.*"),
                ("이미지 파일", "*.jpg;*.jpeg;*.png;*.gif;*.bmp"),
                ("문서 파일", "*.txt;*.doc;*.docx;*.pdf"),
                ("비디오 파일", "*.mp4;*.avi;*.mkv;*.mov")
            ]
        )
        
        if files:
            added = self.engine.add_files(list(files))
            self.status_var.set(f"{added}개 파일이 추가되었습니다")
            logging.info(f"파일 추가: {added}개")
    
    def add_folder(self):
        """폴더의 모든 파일 추가"""
        folder = filedialog.askdirectory(title="폴더를 선택하세요")
        if not folder:
            return
        
        try:
            files = []
            for item in os.listdir(folder):
                item_path = os.path.join(folder, item)
                if os.path.isfile(item_path):
                    files.append(item_path)
            
            if files:
                added = self.engine.add_files(files)
                self.status_var.set(f"폴더에서 {added}개 파일이 추가되었습니다")
                logging.info(f"폴더 추가: {folder} ({added}개 파일)")
            else:
                messagebox.showinfo("정보", "선택한 폴더에 파일이 없습니다.")
                
        except Exception as e:
            messagebox.showerror("오류", f"폴더 읽기 실패: {str(e)}")
            logging.error(f"폴더 추가 실패: {e}")
    
    def add_folder_recursive(self):
        """재귀적 폴더 추가"""
        folder = filedialog.askdirectory(title="재귀적으로 추가할 폴더를 선택하세요")
        if not folder:
            return
        
        try:
            files = []
            for root, dirs, filenames in os.walk(folder):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    files.append(file_path)
            
            if files:
                added = self.engine.add_files(files)
                self.status_var.set(f"재귀적으로 {added}개 파일이 추가되었습니다")
                logging.info(f"재귀적 폴더 추가: {folder} ({added}개 파일)")
            else:
                messagebox.showinfo("정보", "선택한 폴더에 파일이 없습니다.")
                
        except Exception as e:
            messagebox.showerror("오류", f"폴더 읽기 실패: {str(e)}")
            logging.error(f"재귀적 폴더 추가 실패: {e}")
    
    def remove_selected(self):
        """선택된 파일들 제거"""
        selected = self.files_listbox.curselection()
        if not selected:
            messagebox.showwarning("경고", "제거할 파일을 선택하세요.")
            return
        
        removed = self.engine.remove_files_by_indices(list(selected))
        self.status_var.set(f"{removed}개 파일이 제거되었습니다")
        logging.info(f"파일 제거: {removed}개")
    
    def move_up(self):
        """선택된 파일을 위로 이동"""
        selected = self.files_listbox.curselection()
        if not selected or selected[0] == 0:
            return
        
        index = selected[0]
        file_path = self.engine.files.pop(index)
        self.engine.files.insert(index - 1, file_path)
        
        self.engine._notify_files_changed()
        self.files_listbox.selection_set(index - 1)
    
    def move_down(self):
        """선택된 파일을 아래로 이동"""
        selected = self.files_listbox.curselection()
        if not selected or selected[0] >= len(self.engine.files) - 1:
            return
        
        index = selected[0]
        file_path = self.engine.files.pop(index)
        self.engine.files.insert(index + 1, file_path)
        
        self.engine._notify_files_changed()
        self.files_listbox.selection_set(index + 1)
    
    def select_all(self):
        """모든 파일 선택"""
        self.files_listbox.selection_set(0, tk.END)
    
    def clear_all(self):
        """모든 파일 삭제"""
        if self.engine.get_file_count() > 0:
            if messagebox.askyesno("확인", "모든 파일을 목록에서 제거하시겠습니까?"):
                count = self.engine.get_file_count()
                self.engine.clear_files()
                self.status_var.set("모든 파일이 제거되었습니다")
                logging.info(f"모든 파일 제거: {count}개")
    
    def reset_options(self):
        """옵션 초기화"""
        self.engine.reset_options()
        # GUI 변수들도 초기화
        self.prefix_var.set("")
        self.suffix_var.set("")
        self.find_var.set("")
        self.replace_var.set("")
        self.use_numbering_var.set(False)
        self.number_start_var.set(1)
        self.number_digits_var.set(3)
        
        self.status_var.set("옵션이 초기화되었습니다")
        logging.info("옵션 초기화")
    
    # 고급 파일명 생성
    def generate_new_name_advanced(self, original_filename: str, file_index: int = 0) -> str:
        """고급 파일명 생성"""
        name, ext = os.path.splitext(original_filename)
        
        # 1단계: 찾기/바꾸기 적용
        find_text = self.find_var.get()
        replace_text = self.replace_var.get()
        
        if find_text:
            name = name.replace(find_text, replace_text)
        
        # 2단계: 순번 매기기 적용
        if self.use_numbering_var.get():
            number = str(self.number_start_var.get() + file_index).zfill(self.number_digits_var.get())
            name = f"{name}_{number}"
        
        # 3단계: 접두사/접미사 추가
        prefix = self.prefix_var.get()
        suffix = self.suffix_var.get()
        new_name = f"{prefix}{name}{suffix}{ext}"
        
        return new_name
    
    # 전문가급 기능들
    def execute_rename_threaded(self):
        """멀티스레딩으로 파일명 변경 실행"""
        if self.engine.get_file_count() == 0:
            messagebox.showwarning("경고", "변경할 파일이 없습니다.")
            return
        
        # 변경 계획 생성
        rename_plan = []
        for i, file_path in enumerate(self.engine.files):
            original_name = os.path.basename(file_path)
            new_name = self.generate_new_name_advanced(original_name, i)
            
            if original_name != new_name:
                is_valid, error_msg = self.engine.is_valid_filename(new_name, file_path)
                if is_valid:
                    directory = os.path.dirname(file_path)
                    new_path = os.path.join(directory, new_name)
                    rename_plan.append((file_path, new_path))
        
        if not rename_plan:
            messagebox.showwarning("경고", "변경할 수 있는 파일이 없습니다.")
            return
        
        # 확인 대화상자
        if not messagebox.askyesno("확인", 
                                  f"{len(rename_plan)}개 파일의 이름을 변경하시겠습니까?"):
            return
        
        # 백업 생성 (설정에 따라)
        backup_id = None
        if self.settings.get('auto_backup', True):
            backup_id = self.backup_manager.create_backup(rename_plan, "rename")
            if backup_id:
                logging.info(f"자동 백업 생성: {backup_id}")
        
        # 진행률 대화상자 표시
        progress_dialog = ProgressDialog(self.root, "파일명 변경 중")
        
        # 별도 스레드에서 실행
        def rename_worker():
            try:
                success_count = 0
                errors = []
                total = len(rename_plan)
                
                for i, (old_path, new_path) in enumerate(rename_plan):
                    if progress_dialog.cancelled:
                        break
                    
                    try:
                        progress_dialog.update(i + 1, total, f"변경 중: {os.path.basename(old_path)}")
                        time.sleep(0.01)  # UI 업데이트를 위한 짧은 대기
                        
                        os.rename(old_path, new_path)
                        
                        # 내부 파일 목록 업데이트 (메인 스레드에서)
                        self.root.after(0, lambda op=old_path, np=new_path: self.update_file_path(op, np))
                        success_count += 1
                        
                        logging.info(f"파일명 변경: {old_path} -> {new_path}")
                        
                    except Exception as e:
                        error_msg = f"{os.path.basename(old_path)}: {str(e)}"
                        errors.append(error_msg)
                        logging.error(f"파일명 변경 실패: {error_msg}")
                
                # 결과 표시 (메인 스레드에서)
                def show_result():
                    progress_dialog.close()
                    
                    if progress_dialog.cancelled:
                        message = f"작업 취소됨\n✅ 성공: {success_count}개 파일"
                    else:
                        message = f"✅ 성공: {success_count}개 파일 변경됨"
                    
                    if errors:
                        message += f"\n❌ 실패: {len(errors)}개 파일"
                        if len(errors) <= 5:
                            message += "\n\n" + "\n".join(errors[:5])
                    
                    messagebox.showinfo("작업 완료", message)
                    self.status_var.set(f"완료: {success_count}개 파일 변경됨")
                    
                    # UI 업데이트
                    self.engine._notify_files_changed()
                    
                    logging.info(f"파일명 변경 작업 완료: 성공 {success_count}개, 실패 {len(errors)}개")
                
                self.root.after(0, show_result)
                
            except Exception as e:
                def show_error():
                    progress_dialog.close()
                    messagebox.showerror("오류", f"파일명 변경 중 오류 발생: {str(e)}")
                    logging.error(f"파일명 변경 중 오류: {e}")
                
                self.root.after(0, show_error)
        
        # 스레드 시작
        self.current_operation = threading.Thread(target=rename_worker)
        self.current_operation.daemon = True
        self.current_operation.start()
        
        logging.info(f"파일명 변경 작업 시작: {len(rename_plan)}개 파일")
    
    def update_file_path(self, old_path, new_path):
        """파일 경로 업데이트 (메인 스레드에서 호출)"""
        try:
            index = self.engine.files.index(old_path)
            self.engine.files[index] = new_path
        except ValueError:
            pass
    
    def show_backup_manager(self):
        """백업 관리자 창"""
        backup_window = tk.Toplevel(self.root)
        backup_window.title("백업 관리")
        backup_window.geometry("600x400")
        backup_window.transient(self.root)
        backup_window.grab_set()
        
        main_frame = ttk.Frame(backup_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 백업 목록
        ttk.Label(main_frame, text="백업 목록:").pack(anchor="w")
        
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        columns = ("ID", "날짜", "작업", "파일 수")
        backup_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            backup_tree.heading(col, text=col)
            backup_tree.column(col, width=120)
        
        backup_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=backup_tree.yview)
        backup_tree.configure(yscrollcommand=backup_scroll.set)
        
        backup_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        backup_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 백업 목록 로드
        for backup_info in self.backup_manager.get_backup_list():
            backup_tree.insert("", tk.END, values=(
                backup_info['id'][:20] + "..." if len(backup_info['id']) > 20 else backup_info['id'],
                backup_info['timestamp'],
                backup_info['operation'],
                len(backup_info['files'])
            ))
        
        # 버튼들
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="새로고침", 
                  command=lambda: None).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="닫기", 
                  command=backup_window.destroy).pack(side=tk.RIGHT)
    
    def show_batch_processor(self):
        """배치 처리기 창"""
        batch_window = tk.Toplevel(self.root)
        batch_window.title("배치 처리기")
        batch_window.geometry("500x400")
        batch_window.transient(self.root)
        
        # 배치 처리 로직 구현
        main_frame = ttk.Frame(batch_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="배치 처리 기능", 
                 font=("맑은 고딕", 14, "bold")).pack(pady=(0, 10))
        ttk.Label(main_frame, text="여러 폴더에 대해 일괄 처리를 수행합니다.").pack()
        
        # 폴더 선택
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=(20, 10))
        
        ttk.Label(folder_frame, text="처리할 폴더들:").pack(anchor="w")
        
        self.batch_folders = tk.Listbox(folder_frame, height=6)
        self.batch_folders.pack(fill=tk.BOTH, expand=True, pady=(5, 5))
        
        batch_buttons = ttk.Frame(folder_frame)
        batch_buttons.pack(fill=tk.X)
        
        ttk.Button(batch_buttons, text="폴더 추가", 
                  command=self.add_batch_folder).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(batch_buttons, text="제거", 
                  command=self.remove_batch_folder).pack(side=tk.LEFT)
        
        # 실행 버튼
        ttk.Button(main_frame, text="배치 처리 실행", 
                  command=self.execute_batch_processing).pack(pady=(20, 0))
    
    def add_batch_folder(self):
        """배치 처리할 폴더 추가"""
        folder = filedialog.askdirectory(title="배치 처리할 폴더 선택")
        if folder:
            self.batch_folders.insert(tk.END, folder)
    
    def remove_batch_folder(self):
        """배치 처리 폴더 제거"""
        selection = self.batch_folders.curselection()
        if selection:
            self.batch_folders.delete(selection[0])
    
    def execute_batch_processing(self):
        """배치 처리 실행"""
        folders = [self.batch_folders.get(i) for i in range(self.batch_folders.size())]
        if not folders:
            messagebox.showwarning("경고", "처리할 폴더를 선택하세요.")
            return
        
        messagebox.showinfo("정보", f"{len(folders)}개 폴더에 대한 배치 처리를 시작합니다.")
        logging.info(f"배치 처리 시작: {folders}")
    
    def find_duplicates(self):
        """중복 파일 찾기"""
        if not self.engine.files:
            messagebox.showinfo("정보", "파일을 먼저 추가하세요.")
            return
        
        # 파일명 기준 중복 검사
        filename_counts = {}
        duplicates = []
        
        for file_path in self.engine.files:
            filename = os.path.basename(file_path)
            if filename in filename_counts:
                filename_counts[filename].append(file_path)
            else:
                filename_counts[filename] = [file_path]
        
        for filename, paths in filename_counts.items():
            if len(paths) > 1:
                duplicates.extend(paths[1:])  # 첫 번째를 제외한 나머지
        
        if duplicates:
            message = f"{len(duplicates)}개의 중복 파일을 발견했습니다.\n제거하시겠습니까?"
            if messagebox.askyesno("중복 파일", message):
                removed = 0
                for dup_path in duplicates:
                    if self.engine.remove_file(dup_path):
                        removed += 1
                
                self.status_var.set(f"{removed}개 중복 파일이 제거되었습니다")
                logging.info(f"중복 파일 제거: {removed}개")
        else:
            messagebox.showinfo("중복 파일", "중복 파일이 없습니다.")
    
    def validate_files(self):
        """파일 유효성 검사"""
        if not self.engine.files:
            messagebox.showinfo("정보", "파일을 먼저 추가하세요.")
            return
        
        invalid_files = []
        for file_path in self.engine.files:
            if not os.path.exists(file_path):
                invalid_files.append(file_path)
        
        if invalid_files:
            message = f"{len(invalid_files)}개의 유효하지 않은 파일을 발견했습니다.\n제거하시겠습니까?"
            if messagebox.askyesno("파일 검증", message):
                for invalid_path in invalid_files:
                    self.engine.remove_file(invalid_path)
                
                self.status_var.set(f"{len(invalid_files)}개 유효하지 않은 파일이 제거되었습니다")
                logging.info(f"유효하지 않은 파일 제거: {len(invalid_files)}개")
        else:
            messagebox.showinfo("파일 검증", "모든 파일이 유효합니다.")
    
    # UI 업데이트 메서드들
    def update_file_list(self):
        """파일 목록 업데이트 (필터 적용)"""
        self.files_listbox.delete(0, tk.END)
        
        file_filter = self.filter_var.get()
        displayed_count = 0
        
        for file_path in self.engine.files:
            filename = os.path.basename(file_path)
            
            # 검색 필터 적용
            if self.search_text and self.search_text not in filename.lower():
                continue
            
            # 파일 타입 필터 적용
            if file_filter != "모든 파일":
                ext = os.path.splitext(filename)[1].lower()
                if file_filter == "이미지 파일" and ext not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                    continue
                elif file_filter == "문서 파일" and ext not in ['.txt', '.doc', '.docx', '.pdf']:
                    continue
                elif file_filter == "비디오 파일" and ext not in ['.mp4', '.avi', '.mkv', '.mov']:
                    continue
            
            self.files_listbox.insert(tk.END, filename)
            displayed_count += 1
        
        total_count = self.engine.get_file_count()
        if self.search_text or file_filter != "모든 파일":
            self.file_count_var.set(f"파일 개수: {displayed_count}/{total_count} (필터 적용)")
        else:
            self.file_count_var.set(f"파일 개수: {total_count}")
    
    def update_preview(self):
        """미리보기 업데이트"""
        # 기존 항목 제거
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        if self.engine.get_file_count() == 0:
            self.preview_tree.insert("", tk.END, values=(
                "", "파일을 추가하세요", "", "", ""
            ))
            self.preview_stats_var.set("변경 예정: 0개, 오류: 0개")
            return
        
        # 미리보기 데이터 생성
        preview_data = []
        valid_count = 0
        error_count = 0
        changed_count = 0
        
        for i, file_path in enumerate(self.engine.files):
            original_name = os.path.basename(file_path)
            new_name = self.generate_new_name_advanced(original_name, i)
            
            # 파일 크기
            try:
                size = os.path.getsize(file_path)
                size_str = f"{size / 1024:.1f} KB" if size < 1024*1024 else f"{size / (1024*1024):.1f} MB"
            except:
                size_str = "N/A"
            
            # 유효성 검사
            is_valid, error_msg = self.engine.is_valid_filename(new_name, file_path)
            
            if is_valid:
                status = "✅ 유효"
                valid_count += 1
                tags = ("valid",)
            else:
                status = f"❌ {error_msg}"
                error_count += 1
                tags = ("error",)
            
            # 변경 여부 확인
            is_changed = original_name != new_name
            if is_changed:
                changed_count += 1
                if is_valid:
                    status = "🔄 변경예정"
                    tags = ("changed",)
            
            preview_data.append({
                'index': i + 1,
                'original': original_name,
                'new': new_name,
                'status': status,
                'size': size_str,
                'tags': tags,
                'is_valid': is_valid,
                'is_changed': is_changed
            })
        
        # 필터링
        filter_type = self.preview_filter_var.get()
        if filter_type == "변경될 파일":
            preview_data = [item for item in preview_data if item['is_changed']]
        elif filter_type == "유효한 파일":
            preview_data = [item for item in preview_data if item['is_valid']]
        elif filter_type == "오류 파일":
            preview_data = [item for item in preview_data if not item['is_valid']]
        
        # 정렬
        sort_type = self.sort_var.get()
        if sort_type == "파일명":
            preview_data.sort(key=lambda x: x['original'].lower())
        elif sort_type == "새파일명":
            preview_data.sort(key=lambda x: x['new'].lower())
        elif sort_type == "상태":
            preview_data.sort(key=lambda x: x['status'])
        
        # 테이블에 추가
        for item in preview_data:
            self.preview_tree.insert("", tk.END, values=(
                item['index'], item['original'], item['new'], item['status'], item['size']
            ), tags=item['tags'])
        
        # 색상 설정
        self.preview_tree.tag_configure("valid", foreground="darkgreen")
        self.preview_tree.tag_configure("changed", foreground="blue")
        self.preview_tree.tag_configure("error", foreground="red")
        
        self.preview_stats_var.set(f"변경 예정: {changed_count}개, 유효: {valid_count}개, 오류: {error_count}개")
    
    def update_statistics(self):
        """통계 정보 업데이트"""
        stats = self.engine.get_statistics()
        if stats['total_files'] > 0:
            size_mb = stats['total_size'] / (1024 * 1024)
            self.file_stats_var.set(
                f"총 {stats['total_files']}개 파일, {size_mb:.1f}MB"
            )
        else:
            self.file_stats_var.set("")
    
    def refresh_preview(self):
        """미리보기 강제 새로고침"""
        self.update_preview()
        self.status_var.set("미리보기가 새로고침되었습니다")
        logging.info("미리보기 새로고침")
    
    def show_about(self):
        """프로그램 정보"""
        about_text = """KRenamer Pro v5.0
전문가급 파일 이름 변경 도구

주요 기능:
• 멀티스레딩 처리
• 자동 백업 시스템
• 실시간 미리보기
• 드래그 앤 드롭
• 배치 처리
• 로깅 시스템
• 중복 파일 관리

Python tkinter로 개발"""
        
        messagebox.showinfo("KRenamer Pro 정보", about_text)
    
    def quit_app(self):
        """애플리케이션 종료"""
        # 실행 중인 작업이 있으면 확인
        if self.current_operation and self.current_operation.is_alive():
            if not messagebox.askyesno("확인", "실행 중인 작업이 있습니다. 종료하시겠습니까?"):
                return
        
        self.save_settings()
        logging.info("KRenamer Pro 종료")
        self.root.quit()
    
    def run(self):
        """애플리케이션 실행"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            logging.info("사용자에 의해 종료됨")
        finally:
            self.save_settings()
            logging.info("KRenamer Pro 종료")

if __name__ == "__main__":
    app = ProfessionalRenamer()
    app.run()