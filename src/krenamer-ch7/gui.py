#!/usr/bin/env python3
"""
KRenamer GUI Module - Chapter 6
모듈화된 사용자 인터페이스
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

from .core import RenameEngine, RenameRule, RenameOperation
from .config import ConfigManager, RenameConfig
from .plugins import PluginManager, get_plugin_manager

logger = logging.getLogger(__name__)


class BaseWidget:
    """기본 위젯 클래스"""
    
    def __init__(self, parent, config_manager: ConfigManager):
        self.parent = parent
        self.config_manager = config_manager
        self.widgets = {}
        self.callbacks = {}
    
    def setup_ui(self):
        """UI 설정 (서브클래스에서 구현)"""
        pass
    
    def update_from_config(self, config: Any):
        """설정에서 UI 업데이트"""
        pass
    
    def update_to_config(self, config: Any):
        """UI에서 설정으로 업데이트"""
        pass
    
    def set_callback(self, event_name: str, callback: Callable):
        """콜백 설정"""
        self.callbacks[event_name] = callback
    
    def trigger_callback(self, event_name: str, *args, **kwargs):
        """콜백 실행"""
        if event_name in self.callbacks:
            self.callbacks[event_name](*args, **kwargs)


class FileListWidget(BaseWidget):
    """파일 목록 위젯"""
    
    def __init__(self, parent, config_manager: ConfigManager):
        super().__init__(parent, config_manager)
        self.setup_ui()
    
    def setup_ui(self):
        """파일 목록 UI 설정"""
        # 메인 프레임
        self.frame = ttk.LabelFrame(self.parent, text="파일 목록", padding="10")
        
        # 드롭 영역
        if DND_AVAILABLE:
            drop_text = "파일을 여기에 드래그 앤 드롭하거나 '파일 추가' 버튼을 사용하세요"
        else:
            drop_text = "tkinterdnd2가 설치되지 않음. '파일 추가' 버튼을 사용하세요"
        
        self.drop_label = ttk.Label(
            self.frame,
            text=drop_text,
            relief="solid",
            padding="20",
            anchor="center"
        )
        self.drop_label.pack(fill=tk.X, pady=(0, 10))
        
        # 파일 개수 및 통계
        stats_frame = ttk.Frame(self.frame)
        stats_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.count_var = tk.StringVar(value="파일: 0개")
        ttk.Label(stats_frame, textvariable=self.count_var).pack(side=tk.LEFT)
        
        self.size_var = tk.StringVar(value="")
        ttk.Label(stats_frame, textvariable=self.size_var).pack(side=tk.RIGHT)
        
        # 파일 목록 (Treeview 사용)
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Treeview 생성
        columns = ("이름", "크기", "경로")
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        
        # 컬럼 설정
        self.file_tree.heading("이름", text="파일명")
        self.file_tree.heading("크기", text="크기")
        self.file_tree.heading("경로", text="경로")
        
        self.file_tree.column("이름", width=200)
        self.file_tree.column("크기", width=80)
        self.file_tree.column("경로", width=300)
        
        # 스크롤바
        tree_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 버튼 프레임
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="파일 추가", command=self.add_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="선택 제거", command=self.remove_selected).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="모두 제거", command=self.clear_all).pack(side=tk.LEFT, padx=(0, 5))
        
        # 드래그 앤 드롭 설정
        if DND_AVAILABLE:
            self.drop_label.drop_target_register(DND_FILES)
            self.drop_label.dnd_bind('<<Drop>>', self.on_drop)
            self.file_tree.drop_target_register(DND_FILES)
            self.file_tree.dnd_bind('<<Drop>>', self.on_drop)
    
    def add_files(self):
        """파일 추가 다이얼로그"""
        files = filedialog.askopenfilenames(
            title="파일 선택",
            filetypes=[
                ("모든 파일", "*.*"),
                ("이미지 파일", "*.jpg *.jpeg *.png *.gif *.bmp"),
                ("문서 파일", "*.pdf *.doc *.docx *.txt"),
                ("음악 파일", "*.mp3 *.wav *.flac")
            ]
        )
        
        if files:
            self.trigger_callback('files_added', files)
    
    def on_drop(self, event):
        """드롭 이벤트 처리"""
        if DND_AVAILABLE:
            files = event.widget.tk.splitlist(event.data)
            self.trigger_callback('files_added', files)
    
    def remove_selected(self):
        """선택된 파일 제거"""
        selection = self.file_tree.selection()
        if selection:
            file_paths = []
            for item_id in selection:
                item = self.file_tree.item(item_id)
                file_path = item['values'][2]  # 경로 컬럼
                file_paths.append(file_path)
            
            self.trigger_callback('files_removed', file_paths)
    
    def clear_all(self):
        """모든 파일 제거"""
        if messagebox.askyesno("확인", "모든 파일을 제거하시겠습니까?"):
            self.trigger_callback('files_cleared')
    
    def update_file_list(self, files: List[Any], statistics: Dict[str, Any] = None):
        """파일 목록 업데이트"""
        # 기존 항목 제거
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # 새 항목 추가
        for file_info in files:
            file_size = self._format_size(file_info.size)
            self.file_tree.insert("", tk.END, values=(
                file_info.name,
                file_size,
                str(file_info.path.parent)
            ))
        
        # 통계 업데이트
        file_count = len(files)
        self.count_var.set(f"파일: {file_count}개")
        
        if statistics:
            total_size = statistics.get('total_size', 0)
            self.size_var.set(f"전체 크기: {self._format_size(total_size)}")
    
    def _format_size(self, size_bytes: int) -> str:
        """파일 크기 포맷팅"""
        if size_bytes == 0:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                if unit == 'B':
                    return f"{int(size_bytes)} {unit}"
                else:
                    return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.1f} TB"


class RenameOptionsWidget(BaseWidget):
    """리네임 옵션 위젯"""
    
    def __init__(self, parent, config_manager: ConfigManager):
        super().__init__(parent, config_manager)
        self.setup_ui()
    
    def setup_ui(self):
        """리네임 옵션 UI 설정"""
        self.frame = ttk.LabelFrame(self.parent, text="리네임 옵션", padding="10")
        
        # 기본 옵션
        basic_frame = ttk.Frame(self.frame)
        basic_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 접두사/접미사
        prefix_frame = ttk.Frame(basic_frame)
        prefix_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(prefix_frame, text="접두사:", width=10).pack(side=tk.LEFT)
        self.prefix_var = tk.StringVar()
        self.prefix_var.trace_add('write', self.on_option_change)
        ttk.Entry(prefix_frame, textvariable=self.prefix_var, width=15).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(prefix_frame, text="접미사:", width=10).pack(side=tk.LEFT)
        self.suffix_var = tk.StringVar()
        self.suffix_var.trace_add('write', self.on_option_change)
        ttk.Entry(prefix_frame, textvariable=self.suffix_var, width=15).pack(side=tk.LEFT, padx=5)
        
        # 찾기/바꾸기
        replace_frame = ttk.Frame(basic_frame)
        replace_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(replace_frame, text="찾기:", width=10).pack(side=tk.LEFT)
        self.find_var = tk.StringVar()
        self.find_var.trace_add('write', self.on_option_change)
        ttk.Entry(replace_frame, textvariable=self.find_var, width=15).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(replace_frame, text="바꾸기:", width=10).pack(side=tk.LEFT)
        self.replace_var = tk.StringVar()
        self.replace_var.trace_add('write', self.on_option_change)
        ttk.Entry(replace_frame, textvariable=self.replace_var, width=15).pack(side=tk.LEFT, padx=5)
        
        # 정규표현식 체크박스
        self.regex_var = tk.BooleanVar()
        self.regex_var.trace_add('write', self.on_option_change)
        ttk.Checkbutton(replace_frame, text="정규식", variable=self.regex_var).pack(side=tk.LEFT, padx=(10, 0))
        
        # 순번 매기기
        numbering_frame = ttk.Frame(basic_frame)
        numbering_frame.pack(fill=tk.X, pady=2)
        
        self.numbering_var = tk.BooleanVar()
        self.numbering_var.trace_add('write', self.on_option_change)
        ttk.Checkbutton(numbering_frame, text="순번", variable=self.numbering_var).pack(side=tk.LEFT)
        
        ttk.Label(numbering_frame, text="시작:", width=6).pack(side=tk.LEFT, padx=(10, 0))
        self.start_var = tk.StringVar(value="1")
        self.start_var.trace_add('write', self.on_option_change)
        ttk.Spinbox(numbering_frame, from_=1, to=9999, width=6, textvariable=self.start_var).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(numbering_frame, text="자릿수:", width=6).pack(side=tk.LEFT, padx=(5, 0))
        self.digits_var = tk.StringVar(value="3")
        self.digits_var.trace_add('write', self.on_option_change)
        ttk.Spinbox(numbering_frame, from_=1, to=10, width=6, textvariable=self.digits_var).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(numbering_frame, text="위치:").pack(side=tk.LEFT, padx=(5, 0))
        self.position_var = tk.StringVar(value="prefix")
        self.position_var.trace_add('write', self.on_option_change)
        position_combo = ttk.Combobox(numbering_frame, textvariable=self.position_var,
                                    values=["prefix", "suffix"], state="readonly", width=8)
        position_combo.pack(side=tk.LEFT, padx=2)
        
        # 대소문자 변환
        case_frame = ttk.Frame(basic_frame)
        case_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(case_frame, text="대소문자:", width=10).pack(side=tk.LEFT)
        self.case_var = tk.StringVar(value="none")
        self.case_var.trace_add('write', self.on_option_change)
        case_combo = ttk.Combobox(case_frame, textvariable=self.case_var,
                                values=["none", "upper", "lower", "title"], 
                                state="readonly", width=10)
        case_combo.pack(side=tk.LEFT, padx=5)
    
    def on_option_change(self, *args):
        """옵션 변경 시 콜백"""
        self.trigger_callback('options_changed')
    
    def get_rename_rules(self) -> List[RenameRule]:
        """현재 설정을 RenameRule 목록으로 변환"""
        rules = []
        
        # 찾기/바꾸기
        if self.find_var.get().strip():
            if self.regex_var.get():
                rules.append(RenameRule(
                    operation=RenameOperation.REGEX,
                    parameters={
                        'pattern': self.find_var.get(),
                        'replacement': self.replace_var.get(),
                        'flags': 0
                    },
                    priority=1
                ))
            else:
                rules.append(RenameRule(
                    operation=RenameOperation.REPLACE,
                    parameters={
                        'find': self.find_var.get(),
                        'replace': self.replace_var.get()
                    },
                    priority=1
                ))
        
        # 대소문자 변환
        if self.case_var.get() != "none":
            rules.append(RenameRule(
                operation=RenameOperation.CASE_CHANGE,
                parameters={'case_type': self.case_var.get()},
                priority=2
            ))
        
        # 접두사
        if self.prefix_var.get().strip():
            rules.append(RenameRule(
                operation=RenameOperation.PREFIX,
                parameters={'prefix': self.prefix_var.get()},
                priority=3
            ))
        
        # 접미사
        if self.suffix_var.get().strip():
            rules.append(RenameRule(
                operation=RenameOperation.SUFFIX,
                parameters={'suffix': self.suffix_var.get()},
                priority=4
            ))
        
        # 순번 매기기
        if self.numbering_var.get():
            try:
                start = int(self.start_var.get())
                digits = int(self.digits_var.get())
                rules.append(RenameRule(
                    operation=RenameOperation.NUMBERING,
                    parameters={
                        'start': start,
                        'digits': digits,
                        'position': self.position_var.get()
                    },
                    priority=5
                ))
            except ValueError:
                pass
        
        return rules
    
    def update_from_config(self, config: RenameConfig):
        """설정에서 UI 업데이트"""
        self.prefix_var.set(config.prefix)
        self.suffix_var.set(config.suffix)
        self.find_var.set(config.find_text)
        self.replace_var.set(config.replace_text)
        self.regex_var.set(config.use_regex)
        
        self.numbering_var.set(config.numbering_enabled)
        self.start_var.set(str(config.numbering_start))
        self.digits_var.set(str(config.numbering_digits))
        self.position_var.set(config.numbering_position)
        
        self.case_var.set(config.case_change)
    
    def update_to_config(self, config: RenameConfig):
        """UI에서 설정으로 업데이트"""
        config.prefix = self.prefix_var.get()
        config.suffix = self.suffix_var.get()
        config.find_text = self.find_var.get()
        config.replace_text = self.replace_var.get()
        config.use_regex = self.regex_var.get()
        
        config.numbering_enabled = self.numbering_var.get()
        try:
            config.numbering_start = int(self.start_var.get())
            config.numbering_digits = int(self.digits_var.get())
        except ValueError:
            pass
        config.numbering_position = self.position_var.get()
        
        config.case_change = self.case_var.get()


class PreviewWidget(BaseWidget):
    """미리보기 위젯"""
    
    def __init__(self, parent, config_manager: ConfigManager):
        super().__init__(parent, config_manager)
        self.setup_ui()
    
    def setup_ui(self):
        """미리보기 UI 설정"""
        self.frame = ttk.LabelFrame(self.parent, text="미리보기", padding="10")
        
        # 상태 정보
        status_frame = ttk.Frame(self.frame)
        status_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.status_var = tk.StringVar(value="미리보기를 생성하려면 옵션을 설정하세요")
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT)
        
        self.valid_count_var = tk.StringVar(value="")
        ttk.Label(status_frame, textvariable=self.valid_count_var).pack(side=tk.RIGHT)
        
        # 미리보기 테이블
        preview_frame = ttk.Frame(self.frame)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        columns = ("원본", "변경 후", "상태")
        self.preview_tree = ttk.Treeview(preview_frame, columns=columns, show="headings", height=10)
        
        # 컬럼 설정
        self.preview_tree.heading("원본", text="원본 파일명")
        self.preview_tree.heading("변경 후", text="변경 후 파일명")
        self.preview_tree.heading("상태", text="상태")
        
        self.preview_tree.column("원본", width=250)
        self.preview_tree.column("변경 후", width=250)
        self.preview_tree.column("상태", width=80)
        
        # 스크롤바
        preview_scroll = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.preview_tree.yview)
        self.preview_tree.configure(yscrollcommand=preview_scroll.set)
        
        self.preview_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 태그 설정 (색상)
        self.preview_tree.tag_configure('valid', foreground='green')
        self.preview_tree.tag_configure('invalid', foreground='red')
        self.preview_tree.tag_configure('unchanged', foreground='gray')
        
        # 실행 버튼
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="미리보기 새로고침", 
                  command=lambda: self.trigger_callback('preview_refresh')).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="이름 바꾸기 실행", 
                  command=lambda: self.trigger_callback('execute_rename')).pack(side=tk.LEFT)
    
    def update_preview(self, preview_data: List[tuple]):
        """미리보기 데이터 업데이트"""
        # 기존 항목 제거
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        valid_count = 0
        unchanged_count = 0
        
        for original, new_name, is_valid in preview_data:
            if original == new_name:
                status = "변경없음"
                tag = "unchanged"
                unchanged_count += 1
            elif is_valid:
                status = "유효"
                tag = "valid"
                valid_count += 1
            else:
                status = "오류"
                tag = "invalid"
            
            self.preview_tree.insert("", tk.END, 
                                   values=(original, new_name, status), 
                                   tags=(tag,))
        
        # 상태 업데이트
        total = len(preview_data)
        invalid_count = total - valid_count - unchanged_count
        
        if total == 0:
            self.status_var.set("파일이 없습니다")
            self.valid_count_var.set("")
        else:
            status_parts = []
            if valid_count > 0:
                status_parts.append(f"유효: {valid_count}")
            if invalid_count > 0:
                status_parts.append(f"오류: {invalid_count}")
            if unchanged_count > 0:
                status_parts.append(f"변경없음: {unchanged_count}")
            
            self.status_var.set(" | ".join(status_parts))
            self.valid_count_var.set(f"전체: {total}")


class MainWindow:
    """메인 윈도우"""
    
    def __init__(self):
        # 초기화
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
        
        self.config_manager = ConfigManager()
        self.plugin_manager = get_plugin_manager()
        self.rename_engine = RenameEngine()
        
        # UI 구성 요소
        self.file_list_widget = None
        self.options_widget = None
        self.preview_widget = None
        
        self.setup_window()
        self.setup_widgets()
        self.setup_callbacks()
        self.load_plugins()
        self.restore_window_state()
        
        logger.info("MainWindow initialized")
    
    def setup_window(self):
        """윈도우 기본 설정"""
        self.root.title("KRenamer - Chapter 6 (모듈화)")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)
        
        # 윈도우 닫기 이벤트
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_widgets(self):
        """위젯 설정"""
        # 패널 구성 (PanedWindow 사용)
        main_paned = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 상단: 파일 목록
        self.file_list_widget = FileListWidget(main_paned, self.config_manager)
        main_paned.add(self.file_list_widget.frame, weight=1)
        
        # 중단: 옵션
        self.options_widget = RenameOptionsWidget(main_paned, self.config_manager)
        main_paned.add(self.options_widget.frame)
        
        # 하단: 미리보기
        self.preview_widget = PreviewWidget(main_paned, self.config_manager)
        main_paned.add(self.preview_widget.frame, weight=2)
        
        # 메뉴바 설정
        self.setup_menubar()
        
        # 상태바 설정
        self.setup_statusbar()
    
    def setup_menubar(self):
        """메뉴바 설정"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 파일 메뉴
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="파일", menu=file_menu)
        file_menu.add_command(label="설정 저장", command=self.save_settings)
        file_menu.add_command(label="설정 로드", command=self.load_settings)
        file_menu.add_separator()
        file_menu.add_command(label="종료", command=self.on_closing)
        
        # 플러그인 메뉴
        plugin_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="플러그인", menu=plugin_menu)
        plugin_menu.add_command(label="플러그인 관리", command=self.show_plugin_manager)
        plugin_menu.add_command(label="플러그인 새로고침", command=self.reload_plugins)
        
        # 도움말 메뉴
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="도움말", menu=help_menu)
        help_menu.add_command(label="정보", command=self.show_about)
    
    def setup_statusbar(self):
        """상태바 설정"""
        self.statusbar = ttk.Frame(self.root)
        self.statusbar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="준비")
        ttk.Label(self.statusbar, textvariable=self.status_var).pack(side=tk.LEFT, padx=5)
        
        # 플러그인 개수 표시
        self.plugin_count_var = tk.StringVar()
        ttk.Label(self.statusbar, textvariable=self.plugin_count_var).pack(side=tk.RIGHT, padx=5)
    
    def setup_callbacks(self):
        """콜백 설정"""
        # 파일 목록 위젯 콜백
        self.file_list_widget.set_callback('files_added', self.on_files_added)
        self.file_list_widget.set_callback('files_removed', self.on_files_removed)
        self.file_list_widget.set_callback('files_cleared', self.on_files_cleared)
        
        # 옵션 위젯 콜백
        self.options_widget.set_callback('options_changed', self.on_options_changed)
        
        # 미리보기 위젯 콜백
        self.preview_widget.set_callback('preview_refresh', self.update_preview)
        self.preview_widget.set_callback('execute_rename', self.execute_rename)
    
    def load_plugins(self):
        """플러그인 로드"""
        try:
            results = self.plugin_manager.load_all_plugins()
            loaded_count = sum(results.values())
            total_count = len(results)
            
            self.plugin_count_var.set(f"플러그인: {loaded_count}/{total_count}")
            self.status_var.set(f"플러그인 {loaded_count}개 로드됨")
            
            logger.info(f"Loaded {loaded_count}/{total_count} plugins")
            
        except Exception as e:
            logger.error(f"Plugin loading failed: {e}")
            self.plugin_count_var.set("플러그인: 오류")
    
    def reload_plugins(self):
        """플러그인 재로드"""
        try:
            self.plugin_manager.unload_all_plugins()
            self.load_plugins()
            messagebox.showinfo("완료", "플러그인이 재로드되었습니다.")
            
        except Exception as e:
            logger.error(f"Plugin reload failed: {e}")
            messagebox.showerror("오류", f"플러그인 재로드 실패: {e}")
    
    # 이벤트 핸들러들
    def on_files_added(self, file_paths: List[str]):
        """파일 추가 이벤트"""
        added_count = 0
        for file_path in file_paths:
            if self.rename_engine.add_file(file_path):
                added_count += 1
        
        self.update_file_list()
        self.update_preview()
        
        if added_count > 0:
            self.status_var.set(f"{added_count}개 파일 추가됨")
    
    def on_files_removed(self, file_paths: List[str]):
        """파일 제거 이벤트"""
        removed_count = 0
        for file_path in file_paths:
            if self.rename_engine.remove_file(file_path):
                removed_count += 1
        
        self.update_file_list()
        self.update_preview()
        
        if removed_count > 0:
            self.status_var.set(f"{removed_count}개 파일 제거됨")
    
    def on_files_cleared(self):
        """파일 전체 제거 이벤트"""
        count = self.rename_engine.get_file_count()
        self.rename_engine.clear_files()
        
        self.update_file_list()
        self.update_preview()
        
        self.status_var.set(f"{count}개 파일 모두 제거됨")
    
    def on_options_changed(self):
        """옵션 변경 이벤트"""
        self.update_rename_engine_rules()
        self.update_preview()
        self.status_var.set("옵션이 변경되었습니다")
    
    def update_file_list(self):
        """파일 목록 업데이트"""
        files = self.rename_engine.files
        statistics = self.rename_engine.get_statistics()
        self.file_list_widget.update_file_list(files, statistics)
    
    def update_rename_engine_rules(self):
        """리네임 엔진 규칙 업데이트"""
        self.rename_engine.clear_rules()
        
        rules = self.options_widget.get_rename_rules()
        for rule in rules:
            self.rename_engine.add_rule(rule)
    
    def update_preview(self):
        """미리보기 업데이트"""
        if self.rename_engine.get_file_count() == 0:
            self.preview_widget.update_preview([])
            return
        
        try:
            preview_data = self.rename_engine.generate_preview()
            self.preview_widget.update_preview(preview_data)
            
        except Exception as e:
            logger.error(f"Preview generation failed: {e}")
            self.status_var.set(f"미리보기 생성 오류: {e}")
    
    def execute_rename(self):
        """리네임 실행"""
        if self.rename_engine.get_file_count() == 0:
            messagebox.showwarning("경고", "변경할 파일이 없습니다.")
            return
        
        # 확인
        preview = self.rename_engine.generate_preview()
        valid_files = [p for p in preview if p[2] and p[0] != p[1]]
        
        if not valid_files:
            messagebox.showwarning("경고", "변경 가능한 파일이 없습니다.")
            return
        
        result = messagebox.askyesno(
            "확인",
            f"{len(valid_files)}개 파일의 이름을 변경하시겠습니까?"
        )
        
        if not result:
            return
        
        # 실행
        try:
            results = self.rename_engine.execute_rename()
            
            # 결과 표시
            message = f"성공: {results['success']}개"
            if results['failed'] > 0:
                message += f", 실패: {results['failed']}개"
            
            if results['errors']:
                message += f"\n\n오류 목록:\n" + "\n".join(results['errors'][:5])
                if len(results['errors']) > 5:
                    message += f"\n... 외 {len(results['errors']) - 5}개"
            
            messagebox.showinfo("완료", message)
            
            # UI 업데이트
            self.update_file_list()
            self.update_preview()
            self.status_var.set(f"리네임 완료: {results['success']}개 성공")
            
        except Exception as e:
            logger.error(f"Rename execution failed: {e}")
            messagebox.showerror("오류", f"리네임 실행 오류: {e}")
    
    def save_settings(self):
        """설정 저장"""
        try:
            # 현재 윈도우 상태 저장
            self.config_manager.update_window_config(
                width=self.root.winfo_width(),
                height=self.root.winfo_height(),
                x=self.root.winfo_x(),
                y=self.root.winfo_y()
            )
            
            # 리네임 설정 저장
            rename_config = self.config_manager.get_rename_config()
            self.options_widget.update_to_config(rename_config)
            
            if self.config_manager.save_config():
                self.status_var.set("설정이 저장되었습니다")
            else:
                self.status_var.set("설정 저장 실패")
                
        except Exception as e:
            logger.error(f"Settings save failed: {e}")
            messagebox.showerror("오류", f"설정 저장 오류: {e}")
    
    def load_settings(self):
        """설정 로드"""
        try:
            # 설정 다시 로드
            self.config_manager = ConfigManager()
            
            # UI에 반영
            rename_config = self.config_manager.get_rename_config()
            self.options_widget.update_from_config(rename_config)
            
            self.restore_window_state()
            self.update_preview()
            
            self.status_var.set("설정이 로드되었습니다")
            
        except Exception as e:
            logger.error(f"Settings load failed: {e}")
            messagebox.showerror("오류", f"설정 로드 오류: {e}")
    
    def restore_window_state(self):
        """윈도우 상태 복원"""
        try:
            window_config = self.config_manager.get_window_config()
            
            self.root.geometry(f"{window_config.width}x{window_config.height}+"
                             f"{window_config.x}+{window_config.y}")
            
            if window_config.maximized:
                self.root.state('zoomed')
                
        except Exception as e:
            logger.error(f"Window state restore failed: {e}")
    
    def show_plugin_manager(self):
        """플러그인 관리자 다이얼로그"""
        # 간단한 플러그인 목록 표시
        plugins = self.plugin_manager.get_plugin_list()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("플러그인 관리")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 플러그인 목록
        frame = ttk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("이름", "버전", "설명", "저자")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        for plugin in plugins:
            tree.insert("", tk.END, values=(
                plugin['name'],
                plugin['version'], 
                plugin['description'],
                plugin['author']
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(dialog, text="닫기", command=dialog.destroy).pack(pady=10)
    
    def show_about(self):
        """정보 다이얼로그"""
        messagebox.showinfo(
            "KRenamer 정보",
            "KRenamer Chapter 6\n"
            "모듈화된 파일 리네이머\n\n"
            "- 확장 가능한 플러그인 시스템\n"
            "- 설정 관리 및 프리셋\n"
            "- 다양한 리네임 전략\n\n"
            "© 2024 KRenamer Team"
        )
    
    def on_closing(self):
        """윈도우 닫기 이벤트"""
        try:
            # 설정 저장
            self.save_settings()
            
            # 플러그인 정리
            self.plugin_manager.unload_all_plugins()
            
            logger.info("Application closing")
            
        except Exception as e:
            logger.error(f"Error during closing: {e}")
        
        finally:
            self.root.destroy()
    
    def run(self):
        """애플리케이션 실행"""
        logger.info("Starting GUI application")
        self.root.mainloop()


def main():
    """메인 함수"""
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        app = MainWindow()
        app.run()
        
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        messagebox.showerror("오류", f"애플리케이션 시작 실패: {e}")


if __name__ == "__main__":
    main()