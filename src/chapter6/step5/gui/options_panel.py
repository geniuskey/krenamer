"""
옵션 설정 패널
"""

import tkinter as tk
from tkinter import ttk

from ..core.interfaces import FileEngineProtocol
from .interfaces import DataChangeNotifierProtocol


class OptionsPanel:
    """
    리네임 옵션 설정 UI 컴포넌트
    완전히 모듈화된 구조
    """
    
    def __init__(self, 
                 parent: tk.Widget, 
                 engine: FileEngineProtocol,
                 notifier: DataChangeNotifierProtocol):
        self.parent = parent
        self.engine = engine
        self.notifier = notifier
        
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
        basic_frame = ttk.LabelFrame(self.parent, text="기본 리네임 옵션 [모듈화]", padding="10")
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
        advanced_frame = ttk.LabelFrame(self.parent, text="고급 옵션 [모듈화]", padding="10")
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
        self.notifier.on_data_changed()
    
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