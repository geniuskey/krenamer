"""
옵션 탭들 - 기본, 패턴, 조건부, 일괄 작업 탭
"""

import tkinter as tk
from tkinter import ttk


class OptionsTabs:
    """옵션 탭들을 관리하는 클래스"""
    
    def __init__(self, parent, variables, update_callback=None):
        self.parent = parent
        self.update_callback = update_callback
        
        # 변수들 참조
        self.basic_method = variables['basic_method']
        self.basic_text = variables['basic_text']
        self.basic_start_num = variables['basic_start_num']
        self.basic_find = variables['basic_find']
        self.basic_replace = variables['basic_replace']
        
        self.use_regex = variables['use_regex']
        self.pattern_text = variables['pattern_text']
        self.replacement_text = variables['replacement_text']
        
        self.use_size_condition = variables['use_size_condition']
        self.size_operator = variables['size_operator']
        self.size_value = variables['size_value']
        self.size_unit = variables['size_unit']
        self.use_date_condition = variables['use_date_condition']
        self.date_operator = variables['date_operator']
        self.date_value = variables['date_value']
        self.use_ext_condition = variables['use_ext_condition']
        self.allowed_extensions = variables['allowed_extensions']
        
        self.case_method = variables['case_method']
        self.remove_special_chars = variables['remove_special_chars']
        self.replace_spaces = variables['replace_spaces']
        self.handle_duplicates = variables['handle_duplicates']
        
        # UI 위젯들
        self.notebook = None
        self.basic_widgets = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """옵션 탭들 UI 설정"""
        # 노트북 위젯으로 탭 구성
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 각 탭 설정
        self.setup_basic_tab()
        self.setup_pattern_tab()
        self.setup_conditional_tab()
        self.setup_batch_tab()
    
    def setup_basic_tab(self):
        """기본 변경 탭"""
        basic_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(basic_frame, text="기본 변경")
        
        # 기본 이름 변경 방식
        method_frame = ttk.Frame(basic_frame)
        method_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(method_frame, text="접두사", variable=self.basic_method, value="prefix", 
                       command=self.update_basic_fields).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(method_frame, text="접미사", variable=self.basic_method, value="suffix",
                       command=self.update_basic_fields).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(method_frame, text="순번", variable=self.basic_method, value="number",
                       command=self.update_basic_fields).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(method_frame, text="찾기/바꾸기", variable=self.basic_method, value="replace",
                       command=self.update_basic_fields).pack(side=tk.LEFT)
        
        # 입력 필드들
        self.basic_widgets['text_label'] = ttk.Label(basic_frame, text="텍스트:")
        self.basic_widgets['text_label'].grid(row=1, column=0, sticky=tk.W, pady=2)
        self.basic_widgets['text_entry'] = ttk.Entry(basic_frame, textvariable=self.basic_text, width=30)
        self.basic_widgets['text_entry'].grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        self.basic_widgets['number_label'] = ttk.Label(basic_frame, text="시작 번호:")
        self.basic_widgets['number_label'].grid(row=2, column=0, sticky=tk.W, pady=2)
        self.basic_widgets['number_entry'] = ttk.Entry(basic_frame, textvariable=self.basic_start_num, width=10)
        self.basic_widgets['number_entry'].grid(row=2, column=1, sticky=tk.W, pady=2)
        
        self.basic_widgets['find_label'] = ttk.Label(basic_frame, text="찾을 텍스트:")
        self.basic_widgets['find_label'].grid(row=3, column=0, sticky=tk.W, pady=2)
        self.basic_widgets['find_entry'] = ttk.Entry(basic_frame, textvariable=self.basic_find, width=30)
        self.basic_widgets['find_entry'].grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        
        self.basic_widgets['replace_label'] = ttk.Label(basic_frame, text="바꿀 텍스트:")
        self.basic_widgets['replace_label'].grid(row=4, column=0, sticky=tk.W, pady=2)
        self.basic_widgets['replace_entry'] = ttk.Entry(basic_frame, textvariable=self.basic_replace, width=30)
        self.basic_widgets['replace_entry'].grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)
        
        basic_frame.columnconfigure(1, weight=1)
        self.update_basic_fields()
    
    def setup_pattern_tab(self):
        """패턴 기반 탭"""
        pattern_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(pattern_frame, text="패턴 기반")
        
        ttk.Checkbutton(pattern_frame, text="정규식 사용", variable=self.use_regex).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(pattern_frame, text="검색 패턴:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(pattern_frame, textvariable=self.pattern_text, width=40).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(pattern_frame, text="바꿀 내용:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(pattern_frame, textvariable=self.replacement_text, width=40).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        
        pattern_frame.columnconfigure(1, weight=1)
    
    def setup_conditional_tab(self):
        """조건부 변경 탭"""
        cond_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(cond_frame, text="조건부 변경")
        
        # 파일 크기 조건
        size_frame = ttk.LabelFrame(cond_frame, text="파일 크기 조건", padding="5")
        size_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(size_frame, text="크기 조건 사용", variable=self.use_size_condition).grid(row=0, column=0, columnspan=3, sticky=tk.W)
        
        size_input_frame = ttk.Frame(size_frame)
        size_input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Label(size_input_frame, text="파일 크기가").pack(side=tk.LEFT)
        size_op_combo = ttk.Combobox(size_input_frame, textvariable=self.size_operator, width=5, values=["<", "<=", "=", ">=", ">"])
        size_op_combo.pack(side=tk.LEFT, padx=5)
        ttk.Entry(size_input_frame, textvariable=self.size_value, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Combobox(size_input_frame, textvariable=self.size_unit, width=5, values=["B", "KB", "MB", "GB"]).pack(side=tk.LEFT)
        
        # 날짜 조건
        date_frame = ttk.LabelFrame(cond_frame, text="날짜 조건", padding="5")
        date_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(date_frame, text="날짜 조건 사용", variable=self.use_date_condition).grid(row=0, column=0, columnspan=3, sticky=tk.W)
        
        date_input_frame = ttk.Frame(date_frame)
        date_input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Combobox(date_input_frame, textvariable=self.date_operator, width=8, values=["after", "before"]).pack(side=tk.LEFT)
        ttk.Entry(date_input_frame, textvariable=self.date_value, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Label(date_input_frame, text="(YYYY-MM-DD)").pack(side=tk.LEFT)
        
        # 확장자 조건
        ext_frame = ttk.LabelFrame(cond_frame, text="확장자 조건", padding="5")
        ext_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        ttk.Checkbutton(ext_frame, text="확장자 조건 사용", variable=self.use_ext_condition).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(ext_frame, text="허용할 확장자:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        ttk.Entry(ext_frame, textvariable=self.allowed_extensions, width=30).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(2, 0))
        
        cond_frame.columnconfigure(0, weight=1)
        size_frame.columnconfigure(0, weight=1)
        date_frame.columnconfigure(0, weight=1)
        ext_frame.columnconfigure(0, weight=1)
    
    def setup_batch_tab(self):
        """일괄 작업 탭"""
        batch_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(batch_frame, text="일괄 작업")
        
        # 대소문자 변경
        case_frame = ttk.LabelFrame(batch_frame, text="대소문자 변경", padding="5")
        case_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(case_frame, text="변경 안함", variable=self.case_method, value="none").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(case_frame, text="소문자", variable=self.case_method, value="lower").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(case_frame, text="대문자", variable=self.case_method, value="upper").grid(row=0, column=2, sticky=tk.W)
        ttk.Radiobutton(case_frame, text="첫글자만 대문자", variable=self.case_method, value="title").grid(row=1, column=0, sticky=tk.W)
        
        # 기타 옵션
        other_frame = ttk.LabelFrame(batch_frame, text="기타 옵션", padding="5")
        other_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(other_frame, text="특수문자 제거", variable=self.remove_special_chars).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(other_frame, text="공백을 언더스코어로", variable=self.replace_spaces).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(other_frame, text="중복 파일명 처리", variable=self.handle_duplicates).grid(row=2, column=0, sticky=tk.W)
        
        batch_frame.columnconfigure(0, weight=1)
        case_frame.columnconfigure(2, weight=1)
        other_frame.columnconfigure(0, weight=1)
    
    def update_basic_fields(self):
        """선택된 기본 변경 방식에 따라 관련 필드만 표시"""
        method = self.basic_method.get()
        
        # 모든 필드 숨기기
        for widget in self.basic_widgets.values():
            widget.grid_remove()
        
        # 선택된 방식에 따라 해당 필드만 표시
        if method == "prefix":
            self.basic_widgets['text_label'].grid()
            self.basic_widgets['text_entry'].grid()
            self.basic_widgets['text_label'].config(text="접두사 텍스트:")
        elif method == "suffix":
            self.basic_widgets['text_label'].grid()
            self.basic_widgets['text_entry'].grid()
            self.basic_widgets['text_label'].config(text="접미사 텍스트:")
        elif method == "number":
            self.basic_widgets['number_label'].grid()
            self.basic_widgets['number_entry'].grid()
        elif method == "replace":
            self.basic_widgets['find_label'].grid()
            self.basic_widgets['find_entry'].grid()
            self.basic_widgets['replace_label'].grid()
            self.basic_widgets['replace_entry'].grid()
        
        # 콜백 호출
        if self.update_callback:
            self.update_callback()