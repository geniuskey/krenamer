"""
메인 윈도우 - RenamerGUI 메인 클래스
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

try:
    from ..core import RenameEngine
except ImportError:
    from core import RenameEngine  # noqa
from .file_panel import FilePanel
from .options_tabs import OptionsTabs
from .preview_panel import PreviewPanel


class RenamerGUI:
    """메인 리네이머 GUI 클래스"""
    
    def __init__(self):
        # 윈도우 초기화
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
        
        # 엔진 초기화
        self.engine = RenameEngine()
        
        # 변수들 초기화
        self.setup_variables()
        
        # UI 설정
        self.setup_window()
        self.setup_widgets()
        self.setup_drag_drop()
        self.setup_bindings()
    
    def setup_window(self):
        """윈도우 설정"""
        self.root.title("KRenamer Chapter 7 - 완성된 한국어 파일 리네이머")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        self.center_window()
    
    def center_window(self):
        """윈도우 중앙 배치"""
        self.root.update_idletasks()
        width = 1000
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_variables(self):
        """tkinter 변수들 설정"""
        # 파일 관리 변수
        self.display_filter = tk.StringVar(value="모든 파일")
        self.custom_extension = tk.StringVar()
        self.count_var = tk.StringVar(value="파일: 0개")
        self.status_var = tk.StringVar(value="파일을 추가하고 이름 변경 옵션을 선택하세요")
        
        # 기본 변경 변수
        self.basic_method = tk.StringVar(value="prefix")
        self.basic_text = tk.StringVar()
        self.basic_start_num = tk.StringVar(value="1")
        self.basic_find = tk.StringVar()
        self.basic_replace = tk.StringVar()
        
        # 패턴 변수
        self.use_regex = tk.BooleanVar()
        self.pattern_text = tk.StringVar()
        self.replacement_text = tk.StringVar()
        
        # 조건 변수
        self.use_size_condition = tk.BooleanVar()
        self.size_operator = tk.StringVar(value=">")
        self.size_value = tk.DoubleVar(value=1.0)
        self.size_unit = tk.StringVar(value="MB")
        self.use_date_condition = tk.BooleanVar()
        self.date_operator = tk.StringVar(value="after")
        self.date_value = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.use_ext_condition = tk.BooleanVar()
        self.allowed_extensions = tk.StringVar(value=".jpg,.png,.gif")
        
        # 일괄 작업 변수
        self.case_method = tk.StringVar(value="none")
        self.remove_special_chars = tk.BooleanVar()
        self.replace_spaces = tk.BooleanVar()
        self.handle_duplicates = tk.BooleanVar(value=True)
    
    def setup_widgets(self):
        """위젯들 설정"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 좌측: 파일 리스트 및 옵션
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # 우측: 미리보기
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # 각 패널 생성
        variables = {
            'display_filter': self.display_filter,
            'custom_extension': self.custom_extension,
            'count_var': self.count_var,
            'basic_method': self.basic_method,
            'basic_text': self.basic_text,
            'basic_start_num': self.basic_start_num,
            'basic_find': self.basic_find,
            'basic_replace': self.basic_replace,
            'use_regex': self.use_regex,
            'pattern_text': self.pattern_text,
            'replacement_text': self.replacement_text,
            'use_size_condition': self.use_size_condition,
            'size_operator': self.size_operator,
            'size_value': self.size_value,
            'size_unit': self.size_unit,
            'use_date_condition': self.use_date_condition,
            'date_operator': self.date_operator,
            'date_value': self.date_value,
            'use_ext_condition': self.use_ext_condition,
            'allowed_extensions': self.allowed_extensions,
            'case_method': self.case_method,
            'remove_special_chars': self.remove_special_chars,
            'replace_spaces': self.replace_spaces,
            'handle_duplicates': self.handle_duplicates
        }
        
        self.file_panel = FilePanel(left_frame, self.engine, variables, self.set_status)
        self.preview_panel = PreviewPanel(right_frame, self.engine)
        self.options_tabs = OptionsTabs(left_frame, variables, self.update_preview)
        
        # 버튼 섹션
        self.setup_buttons_section(left_frame)
        
        # 상태바
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # 그리드 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=0)
        left_frame.rowconfigure(1, weight=1)
        left_frame.rowconfigure(2, weight=0)
        left_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
    
    def setup_buttons_section(self, parent):
        """버튼 섹션 설정"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, pady=(10, 0))
        
        ttk.Button(button_frame, text="미리보기", command=self.update_preview).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="이름 변경 실행", command=self.execute_rename).pack(side=tk.LEFT)
    
    def setup_drag_drop(self):
        """드래그 앤 드롭 설정"""
        if DND_AVAILABLE:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_drop)
            
            self.file_panel.files_listbox.drop_target_register(DND_FILES)
            self.file_panel.files_listbox.dnd_bind('<<Drop>>', self.on_drop)
    
    def setup_bindings(self):
        """이벤트 바인딩"""
        # 변수 변경 감지
        variables_to_trace = [
            self.basic_method, self.basic_text, self.basic_start_num, self.basic_find, self.basic_replace,
            self.use_regex, self.pattern_text, self.replacement_text,
            self.use_size_condition, self.size_operator, self.size_value, self.size_unit,
            self.use_date_condition, self.date_operator, self.date_value,
            self.use_ext_condition, self.allowed_extensions,
            self.case_method, self.remove_special_chars, self.replace_spaces, self.handle_duplicates,
            self.display_filter, self.custom_extension
        ]
        
        for var in variables_to_trace:
            var.trace('w', self.update_preview)
    
    def on_drop(self, event):
        """드래그 앤 드롭 이벤트 처리"""
        files = self.root.tk.splitlist(event.data)
        self.file_panel.add_files(files)
        self.update_preview()
    
    def apply_settings_to_engine(self):
        """GUI 설정을 엔진에 적용"""
        # 기본 설정
        self.engine.method = self.basic_method.get()
        self.engine.prefix_text = self.basic_text.get()
        self.engine.suffix_text = self.basic_text.get()
        try:
            self.engine.start_number = int(self.basic_start_num.get())
        except:
            self.engine.start_number = 1
        self.engine.find_text = self.basic_find.get()
        self.engine.replace_text = self.basic_replace.get()
        
        # 패턴 설정
        self.engine.use_regex = self.use_regex.get()
        self.engine.pattern = self.pattern_text.get()
        self.engine.replacement = self.replacement_text.get()
        
        # 조건 설정 (condition_checker에 적용)
        self.engine.condition_checker.use_size_condition = self.use_size_condition.get()
        self.engine.condition_checker.size_operator = self.size_operator.get()
        self.engine.condition_checker.size_value = self.size_value.get()
        self.engine.condition_checker.size_unit = self.size_unit.get()
        self.engine.condition_checker.use_date_condition = self.use_date_condition.get()
        self.engine.condition_checker.date_operator = self.date_operator.get()
        self.engine.condition_checker.date_value = self.date_value.get()
        self.engine.condition_checker.use_ext_condition = self.use_ext_condition.get()
        self.engine.condition_checker.allowed_extensions = self.allowed_extensions.get()
        
        # 일괄 작업 설정
        self.engine.case_method = self.case_method.get()
        self.engine.remove_special_chars = self.remove_special_chars.get()
        self.engine.replace_spaces = self.replace_spaces.get()
        self.engine.handle_duplicates = self.handle_duplicates.get()
    
    def update_preview(self, *args):
        """미리보기 업데이트"""
        self.apply_settings_to_engine()
        self.preview_panel.update_preview()
        self.file_panel.refresh_file_list()
    
    def execute_rename(self):
        """이름 변경 실행"""
        if not self.engine.files:
            self.set_status("변경할 파일이 없습니다")
            return
        
        self.apply_settings_to_engine()
        rename_plan = self.engine.generate_rename_plan()
        
        # 실제 변경될 파일 수 계산
        change_count = sum(1 for _, _, matches in rename_plan if matches)
        
        if change_count == 0:
            self.set_status("조건에 맞는 파일이 없습니다")
            return
        
        if not messagebox.askyesno("확인", f"{change_count}개 파일의 이름을 변경하시겠습니까?"):
            return
        
        # 실행
        success_count, errors = self.engine.execute_rename()
        
        # 결과 처리
        if errors:
            error_msg = f"{success_count}개 파일 변경 완료.\n오류:\n" + "\n".join(errors[:3])
            if len(errors) > 3:
                error_msg += f"\n... 외 {len(errors)-3}개"
            messagebox.showwarning("완료", error_msg)
        else:
            messagebox.showinfo("완료", f"{success_count}개 파일의 이름이 변경되었습니다")
        
        self.set_status(f"변경 완료: {success_count}개 성공, {len(errors)}개 오류")
        self.file_panel.refresh_file_list()
        self.update_preview()
    
    def set_status(self, message):
        """상태 메시지 설정"""
        self.status_var.set(message)
    
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()