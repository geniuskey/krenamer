#!/usr/bin/env python3
"""
KRenamer Chapter 6: Advanced Conditions and Features
고급 조건부 파일명 변경 기능

이 챕터에서는 다음 고급 기능들을 배웁니다:
- 조건부 필터링 (파일 크기, 날짜, 확장자)
- 정규식 패턴 매칭
- 동적 UI 필드 표시 (선택된 방식에 따라 필요한 입력 필드만 표시)
- 일괄 변환 규칙 (대소문자, 특수문자 처리)
- 중복 파일명 처리
- 실시간 미리보기 기능
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
from datetime import datetime
from pathlib import Path

# tkinterdnd2 선택적 import
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


class AdvancedKRenamerGUI:
    """
    KRenamer Chapter 6: 고급 조건부 파일명 변경
    
    Chapter 5의 기본 리네임 기능에 고급 조건과 필터링 기능을 추가합니다:
    - 조건부 필터링 (파일 크기, 날짜, 확장자)
    - 정규식 패턴 매칭
    - 동적 UI 필드 표시
    - 일괄 변환 규칙
    - 실시간 미리보기
    """
    
    def __init__(self):
        # tkinterdnd2가 사용 가능하면 DnD 윈도우 생성
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
        
        # 파일 경로를 저장할 리스트
        self.files = []
        
        # UI 위젯 참조 저장용 딕셔너리
        self.basic_widgets = {}
        
        self.setup_window()
        self.setup_widgets()
        self.setup_drag_drop()
    
    def setup_window(self):
        """윈도우 기본 설정"""
        self.root.title("KRenamer - Chapter 6: 고급 조건과 기능")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        self.root.minsize(900, 500)
        
        self.center_window()
    
    def center_window(self):
        """윈도우를 화면 중앙에 배치"""
        self.root.update_idletasks()
        width = 1000
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_widgets(self):
        """GUI 위젯들 설정 및 배치"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 상단: 파일 목록
        self.setup_file_list_section(main_frame)
        
        # 중간: 고급 옵션 탭
        self.setup_advanced_options_section(main_frame)
        
        # 하단: 버튼 및 상태바
        self.setup_buttons_section(main_frame)
        self.setup_status_section(main_frame)
        
        # 그리드 가중치 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)  # 파일 목록 영역이 확장
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 초기 설정
        self.update_button_states()
        self.update_basic_fields()
    
    def setup_file_list_section(self, parent):
        """파일 목록 섹션 설정"""
        # 파일 목록 프레임
        files_frame = ttk.LabelFrame(parent, text="파일 목록", padding="10")
        files_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # 파일 필터 및 정보 헤더
        header_frame = ttk.Frame(files_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 파일 필터
        ttk.Label(header_frame, text="파일 필터:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar()
        filter_combo = ttk.Combobox(header_frame, textvariable=self.filter_var, width=15)
        filter_combo['values'] = ('모든 파일', '이미지 파일', '문서 파일', '텍스트 파일', '사용자 정의')
        filter_combo.set('모든 파일')
        filter_combo.pack(side=tk.LEFT, padx=(5, 15))
        
        # 사용자 정의 확장자
        self.custom_filter_var = tk.StringVar()
        ttk.Label(header_frame, text="확장자:").pack(side=tk.LEFT)
        self.custom_filter_entry = ttk.Entry(header_frame, textvariable=self.custom_filter_var, width=12)
        self.custom_filter_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        # 파일 개수 표시
        self.count_var = tk.StringVar()
        self.count_var.set("파일: 0개")
        count_label = ttk.Label(
            header_frame, 
            textvariable=self.count_var,
            font=("맑은 고딕", 9),
            foreground="blue"
        )
        count_label.pack(side=tk.RIGHT)
        
        # 리스트박스 프레임
        listbox_frame = ttk.Frame(files_frame)
        listbox_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 파일 리스트박스
        self.files_listbox = tk.Listbox(
            listbox_frame, 
            height=8,
            font=("맑은 고딕", 9),
            selectmode=tk.EXTENDED
        )
        
        # 스크롤바
        scrollbar_y = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        scrollbar_x = ttk.Scrollbar(listbox_frame, orient=tk.HORIZONTAL, command=self.files_listbox.xview)
        
        self.files_listbox.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # 그리드 배치
        self.files_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 그리드 설정
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        files_frame.columnconfigure(0, weight=1)
        files_frame.rowconfigure(1, weight=1)
    
    def setup_advanced_options_section(self, parent):
        """고급 옵션 탭 섹션 설정"""
        # 노트북 위젯으로 탭 구성
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # 탭들 설정
        self.setup_basic_tab()
        self.setup_pattern_tab()
        self.setup_conditional_tab()
        self.setup_batch_tab()
    
    def setup_basic_tab(self):
        """기본 이름 변경 탭"""
        basic_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(basic_frame, text="기본 변경")
        
        # 기본 이름 변경 방식 선택
        self.basic_method = tk.StringVar(value="prefix")
        
        # 라디오 버튼 프레임
        method_frame = ttk.Frame(basic_frame)
        method_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Radiobutton(
            method_frame, 
            text="접두사 추가", 
            variable=self.basic_method, 
            value="prefix", 
            command=self.update_basic_fields
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Radiobutton(
            method_frame, 
            text="접미사 추가", 
            variable=self.basic_method, 
            value="suffix", 
            command=self.update_basic_fields
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Radiobutton(
            method_frame, 
            text="순번 매기기", 
            variable=self.basic_method, 
            value="number", 
            command=self.update_basic_fields
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Radiobutton(
            method_frame, 
            text="찾기/바꾸기", 
            variable=self.basic_method, 
            value="replace", 
            command=self.update_basic_fields
        ).pack(side=tk.LEFT)
        
        # 동적 입력 필드들 설정
        self.setup_basic_input_fields(basic_frame)
        
        basic_frame.columnconfigure(1, weight=1)
    
    def setup_basic_input_fields(self, parent):
        """기본 변경 입력 필드들 설정"""
        # 텍스트 입력 (접두사/접미사용)
        self.basic_widgets['text_label'] = ttk.Label(parent, text="텍스트:")
        self.basic_widgets['text_label'].grid(row=1, column=0, sticky=tk.W, pady=8)
        
        self.basic_text_var = tk.StringVar()
        self.basic_widgets['text_entry'] = ttk.Entry(parent, textvariable=self.basic_text_var, width=40)
        self.basic_widgets['text_entry'].grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8)
        
        # 시작 번호 입력 (순번 매기기용)
        self.basic_widgets['number_label'] = ttk.Label(parent, text="시작 번호:")
        self.basic_widgets['number_label'].grid(row=2, column=0, sticky=tk.W, pady=8)
        
        self.basic_start_var = tk.StringVar(value="1")
        self.basic_widgets['number_entry'] = ttk.Entry(parent, textvariable=self.basic_start_var, width=10)
        self.basic_widgets['number_entry'].grid(row=2, column=1, sticky=tk.W, pady=8)
        
        # 자릿수 설정 (순번 매기기용)
        number_options_frame = ttk.Frame(parent)
        self.basic_widgets['number_options_frame'] = number_options_frame
        number_options_frame.grid(row=3, column=1, sticky=tk.W, pady=8)
        
        ttk.Label(number_options_frame, text="자릿수:").pack(side=tk.LEFT)
        self.digits_var = tk.StringVar(value="3")
        digits_combo = ttk.Combobox(number_options_frame, textvariable=self.digits_var, width=5, values=["1", "2", "3", "4", "5"])
        digits_combo.pack(side=tk.LEFT, padx=(5, 15))
        # digits_combo는 number_options_frame 내부에서 pack으로 관리되므로 basic_widgets에 추가하지 않음
        
        ttk.Label(number_options_frame, text="접두사:").pack(side=tk.LEFT)
        self.number_prefix_var = tk.StringVar()
        prefix_entry = ttk.Entry(number_options_frame, textvariable=self.number_prefix_var, width=10)
        prefix_entry.pack(side=tk.LEFT, padx=(5, 0))
        # prefix_entry는 number_options_frame 내부에서 pack으로 관리되므로 basic_widgets에 추가하지 않음
        
        # 찾을 텍스트 입력 (찾기/바꾸기용)
        self.basic_widgets['find_label'] = ttk.Label(parent, text="찾을 텍스트:")
        self.basic_widgets['find_label'].grid(row=4, column=0, sticky=tk.W, pady=8)
        
        self.basic_find_var = tk.StringVar()
        self.basic_widgets['find_entry'] = ttk.Entry(parent, textvariable=self.basic_find_var, width=40)
        self.basic_widgets['find_entry'].grid(row=4, column=1, sticky=(tk.W, tk.E), pady=8)
        
        # 바꿀 텍스트 입력 (찾기/바꾸기용)
        self.basic_widgets['replace_label'] = ttk.Label(parent, text="바꿀 텍스트:")
        self.basic_widgets['replace_label'].grid(row=5, column=0, sticky=tk.W, pady=8)
        
        self.basic_replace_var = tk.StringVar()
        self.basic_widgets['replace_entry'] = ttk.Entry(parent, textvariable=self.basic_replace_var, width=40)
        self.basic_widgets['replace_entry'].grid(row=5, column=1, sticky=(tk.W, tk.E), pady=8)
        
        # 찾기/바꾸기 옵션 (찾기/바꾸기용)
        replace_options_frame = ttk.Frame(parent)
        self.basic_widgets['replace_options_frame'] = replace_options_frame
        replace_options_frame.grid(row=6, column=1, sticky=tk.W, pady=8)
        
        self.case_sensitive = tk.BooleanVar(value=True)
        case_check = ttk.Checkbutton(replace_options_frame, text="대소문자 구분", variable=self.case_sensitive)
        case_check.pack(side=tk.LEFT, padx=(0, 15))
        # case_check는 replace_options_frame 내부에서 pack으로 관리되므로 basic_widgets에 추가하지 않음
        
        self.use_regex_basic = tk.BooleanVar()
        regex_check = ttk.Checkbutton(replace_options_frame, text="정규식 사용", variable=self.use_regex_basic)
        regex_check.pack(side=tk.LEFT)
        # regex_check는 replace_options_frame 내부에서 pack으로 관리되므로 basic_widgets에 추가하지 않음
    
    def update_basic_fields(self):
        """선택된 기본 변경 방식에 따라 관련 필드만 표시"""
        method = self.basic_method.get()
        
        # 모든 필드 숨기기
        for widget in self.basic_widgets.values():
            widget.grid_remove()
        
        # 선택된 방식에 따라 해당 필드만 표시
        if method in ["prefix", "suffix"]:
            # 접두사/접미사: 텍스트 입력만 표시
            self.basic_widgets['text_label'].grid()
            self.basic_widgets['text_entry'].grid()
            
            if method == "prefix":
                self.basic_widgets['text_label'].config(text="접두사 텍스트:")
            else:
                self.basic_widgets['text_label'].config(text="접미사 텍스트:")
        
        elif method == "number":
            # 순번 매기기: 시작 번호, 자릿수, 접두사 표시
            self.basic_widgets['number_label'].grid()
            self.basic_widgets['number_entry'].grid()
            self.basic_widgets['number_options_frame'].grid()
            # digits_combo와 prefix_entry는 number_options_frame 내부에서 pack으로 관리되므로 별도 grid 호출 불필요
        
        elif method == "replace":
            # 찾기/바꾸기: 찾을 텍스트, 바꿀 텍스트, 옵션 표시
            self.basic_widgets['find_label'].grid()
            self.basic_widgets['find_entry'].grid()
            self.basic_widgets['replace_label'].grid()
            self.basic_widgets['replace_entry'].grid()
            self.basic_widgets['replace_options_frame'].grid()
            # case_check와 regex_check는 replace_options_frame 내부에서 pack으로 관리되므로 별도 grid 호출 불필요
    
    def setup_pattern_tab(self):
        """패턴 기반 탭"""
        pattern_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(pattern_frame, text="패턴 기반")
        
        # 정규식 사용 여부
        self.use_regex = tk.BooleanVar()
        ttk.Checkbutton(pattern_frame, text="정규식 사용", variable=self.use_regex).grid(row=0, column=0, sticky=tk.W, pady=(0, 15))
        
        # 패턴 입력
        ttk.Label(pattern_frame, text="검색 패턴:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.pattern_var = tk.StringVar()
        ttk.Entry(pattern_frame, textvariable=self.pattern_var, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8)
        
        ttk.Label(pattern_frame, text="치환 패턴:").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.replacement_var = tk.StringVar()
        ttk.Entry(pattern_frame, textvariable=self.replacement_var, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8)
        
        # 패턴 예제
        example_frame = ttk.LabelFrame(pattern_frame, text="정규식 패턴 예제", padding="10")
        example_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(15, 0))
        
        examples = [
            "• 숫자 제거: [0-9]+ → (공백)",
            "• 공백을 언더스코어로: \\s+ → _",
            "• 날짜 형식 변경: (\\d{4})(\\d{2})(\\d{2}) → \\1-\\2-\\3",
            "• 확장자 변경: \\.txt$ → .bak",
            "• 특수문자 제거: [^\\w\\s.-] → (공백)",
            "• 연속 공백 정리: \\s+ → (단일 공백)"
        ]
        
        for i, example in enumerate(examples):
            ttk.Label(example_frame, text=example, font=("Consolas", 9)).grid(row=i//2, column=i%2, sticky=tk.W, padx=(0, 20), pady=2)
        
        pattern_frame.columnconfigure(1, weight=1)
    
    def setup_conditional_tab(self):
        """조건부 변경 탭"""
        conditional_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(conditional_frame, text="조건부 변경")
        
        # 파일 크기 조건
        size_frame = ttk.LabelFrame(conditional_frame, text="파일 크기 조건", padding="10")
        size_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.use_size_condition = tk.BooleanVar()
        ttk.Checkbutton(size_frame, text="파일 크기 조건 사용", variable=self.use_size_condition).grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 10))
        
        size_input_frame = ttk.Frame(size_frame)
        size_input_frame.grid(row=1, column=0, columnspan=4, sticky=tk.W, padx=(20, 0))
        
        self.size_operator = tk.StringVar(value=">")
        ttk.Combobox(size_input_frame, textvariable=self.size_operator, values=["<", "<=", "=", ">=", ">"], width=5).pack(side=tk.LEFT, padx=(0, 5))
        
        self.size_value = tk.StringVar(value="1")
        ttk.Entry(size_input_frame, textvariable=self.size_value, width=10).pack(side=tk.LEFT, padx=(0, 5))
        
        self.size_unit = tk.StringVar(value="MB")
        ttk.Combobox(size_input_frame, textvariable=self.size_unit, values=["Bytes", "KB", "MB", "GB"], width=8).pack(side=tk.LEFT)
        
        # 날짜 조건
        date_frame = ttk.LabelFrame(conditional_frame, text="수정 날짜 조건", padding="10")
        date_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.use_date_condition = tk.BooleanVar()
        ttk.Checkbutton(date_frame, text="수정 날짜 조건 사용", variable=self.use_date_condition).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        date_input_frame = ttk.Frame(date_frame)
        date_input_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=(20, 0))
        
        self.date_operator = tk.StringVar(value="after")
        ttk.Radiobutton(date_input_frame, text="이후", variable=self.date_operator, value="after").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(date_input_frame, text="이전", variable=self.date_operator, value="before").pack(side=tk.LEFT)
        
        date_entry_frame = ttk.Frame(date_frame)
        date_entry_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=(20, 0), pady=(10, 0))
        
        self.date_value = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(date_entry_frame, textvariable=self.date_value, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(date_entry_frame, text="(YYYY-MM-DD 형식)", font=("맑은 고딕", 8), foreground="gray").pack(side=tk.LEFT)
        
        # 확장자 조건
        ext_frame = ttk.LabelFrame(conditional_frame, text="확장자 조건", padding="10")
        ext_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.use_ext_condition = tk.BooleanVar()
        ttk.Checkbutton(ext_frame, text="특정 확장자만 대상", variable=self.use_ext_condition).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        ext_input_frame = ttk.Frame(ext_frame)
        ext_input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(20, 0))
        
        self.ext_list = tk.StringVar(value=".jpg,.png,.gif,.bmp")
        ttk.Entry(ext_input_frame, textvariable=self.ext_list, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(ext_frame, text="(쉼표로 구분, 예: .jpg,.png,.txt)", font=("맑은 고딕", 8), foreground="gray").grid(row=2, column=0, padx=(20, 0), sticky=tk.W, pady=(5, 0))
        
        conditional_frame.columnconfigure(0, weight=1)
        ext_input_frame.columnconfigure(0, weight=1)
    
    def setup_batch_tab(self):
        """일괄 작업 탭"""
        batch_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(batch_frame, text="일괄 작업")
        
        # 대소문자 변환
        case_frame = ttk.LabelFrame(batch_frame, text="대소문자 변환", padding="10")
        case_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.case_method = tk.StringVar(value="none")
        
        case_radio_frame = ttk.Frame(case_frame)
        case_radio_frame.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Radiobutton(case_radio_frame, text="변경 안함", variable=self.case_method, value="none").grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        ttk.Radiobutton(case_radio_frame, text="모두 대문자", variable=self.case_method, value="upper").grid(row=0, column=1, sticky=tk.W, padx=(0, 15))
        ttk.Radiobutton(case_radio_frame, text="모두 소문자", variable=self.case_method, value="lower").grid(row=0, column=2, sticky=tk.W, padx=(0, 15))
        ttk.Radiobutton(case_radio_frame, text="첫글자만 대문자", variable=self.case_method, value="title").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # 특수문자 처리
        special_frame = ttk.LabelFrame(batch_frame, text="특수문자 및 공백 처리", padding="10")
        special_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        special_options_frame = ttk.Frame(special_frame)
        special_options_frame.grid(row=0, column=0, sticky=tk.W)
        
        self.remove_special = tk.BooleanVar()
        ttk.Checkbutton(special_options_frame, text="특수문자 제거", variable=self.remove_special).grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        
        self.replace_space = tk.BooleanVar()
        ttk.Checkbutton(special_options_frame, text="공백을 언더스코어로", variable=self.replace_space).grid(row=0, column=1, sticky=tk.W, padx=(0, 15))
        
        self.remove_consecutive = tk.BooleanVar()
        ttk.Checkbutton(special_options_frame, text="연속 공백 정리", variable=self.remove_consecutive).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # 중복 및 안전 처리
        safety_frame = ttk.LabelFrame(batch_frame, text="중복 및 안전 처리", padding="10")
        safety_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        safety_options_frame = ttk.Frame(safety_frame)
        safety_options_frame.grid(row=0, column=0, sticky=tk.W)
        
        self.handle_duplicate = tk.BooleanVar(value=True)
        ttk.Checkbutton(safety_options_frame, text="중복 파일명에 번호 추가", variable=self.handle_duplicate).grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        
        self.backup_enabled = tk.BooleanVar()
        ttk.Checkbutton(safety_options_frame, text="변경 전 백업 생성", variable=self.backup_enabled).grid(row=0, column=1, sticky=tk.W)
        
        batch_frame.columnconfigure(0, weight=1)
    
    def setup_buttons_section(self, parent):
        """버튼 섹션 설정"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, pady=(0, 15))
        
        # 파일 관리 버튼들
        self.add_button = ttk.Button(
            button_frame, 
            text="파일 추가", 
            command=self.add_files_dialog,
            width=12
        )
        self.add_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.add_folder_button = ttk.Button(
            button_frame, 
            text="폴더 추가", 
            command=self.add_folder_dialog,
            width=12
        )
        self.add_folder_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.remove_button = ttk.Button(
            button_frame, 
            text="선택 제거", 
            command=self.remove_selected_files,
            width=12
        )
        self.remove_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(
            button_frame, 
            text="전체 지우기", 
            command=self.clear_all_files,
            width=12
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 20))
        
        # 고급 기능 버튼들
        self.test_button = ttk.Button(
            button_frame, 
            text="조건 테스트", 
            command=self.test_conditions,
            width=12
        )
        self.test_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.preview_button = ttk.Button(
            button_frame, 
            text="미리보기", 
            command=self.preview_rename,
            width=12
        )
        self.preview_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.execute_button = ttk.Button(
            button_frame, 
            text="이름 변경 실행", 
            command=self.execute_rename,
            width=15
        )
        self.execute_button.pack(side=tk.LEFT)
    
    def setup_status_section(self, parent):
        """상태바 섹션 설정"""
        # 상태바 프레임
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 상태 메시지
        self.status_var = tk.StringVar()
        self.status_var.set("파일을 추가하고 고급 이름 변경 옵션을 설정하세요.")
        
        status_label = ttk.Label(
            status_frame, 
            textvariable=self.status_var,
            font=("맑은 고딕", 9),
            foreground="gray"
        )
        status_label.pack(side=tk.LEFT)
        
        # DnD 상태 표시
        dnd_status = "DnD: 사용가능" if DND_AVAILABLE else "DnD: 사용불가"
        dnd_label = ttk.Label(
            status_frame,
            text=dnd_status,
            font=("맑은 고딕", 9),
            foreground="green" if DND_AVAILABLE else "red"
        )
        dnd_label.pack(side=tk.RIGHT)
    
    def setup_drag_drop(self):
        """드래그 앤 드롭 설정"""
        if DND_AVAILABLE:
            # 리스트박스에 드래그 앤 드롭 등록
            self.files_listbox.drop_target_register(DND_FILES)
            self.files_listbox.dnd_bind('<<Drop>>', self.on_drop)
            
            # 메인 윈도우에도 드래그 앤 드롭 등록
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_drop)
    
    def on_drop(self, event):
        """드래그 앤 드롭 이벤트 처리"""
        try:
            files = self.parse_drop_data(event.data)
            if files:
                self.add_files(files)
        except Exception as e:
            self.status_var.set(f"드래그 앤 드롭 처리 중 오류: {e}")
    
    def parse_drop_data(self, data):
        """드롭 데이터 파싱"""
        files = []
        try:
            raw_files = self.root.tk.splitlist(data)
            for file_path in raw_files:
                if file_path.startswith('{') and file_path.endswith('}'):
                    file_path = file_path[1:-1]
                if os.path.exists(file_path):
                    files.append(file_path)
        except Exception:
            if isinstance(data, str):
                file_path = data.strip('{}')
                if os.path.exists(file_path):
                    files.append(file_path)
        return files
    
    def add_files_dialog(self):
        """파일 선택 대화상자"""
        try:
            files = filedialog.askopenfilenames(
                title="파일 선택",
                filetypes=[
                    ("모든 파일", "*.*"),
                    ("이미지 파일", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff"),
                    ("문서 파일", "*.pdf *.doc *.docx *.txt *.hwp"),
                    ("음악 파일", "*.mp3 *.wav *.flac *.m4a"),
                    ("비디오 파일", "*.mp4 *.avi *.mkv *.mov *.wmv")
                ]
            )
            if files:
                self.add_files(files)
        except Exception as e:
            messagebox.showerror("오류", f"파일 선택 중 오류가 발생했습니다: {e}")
    
    def add_folder_dialog(self):
        """폴더 선택 대화상자"""
        try:
            folder = filedialog.askdirectory(title="폴더 선택")
            if folder:
                folder_files = []
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        folder_files.append(file_path)
                
                if folder_files:
                    self.add_files(folder_files)
                else:
                    self.status_var.set("선택한 폴더에 파일이 없습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"폴더 선택 중 오류가 발생했습니다: {e}")
    
    def add_files(self, file_paths):
        """파일 추가 처리"""
        added_count = 0
        skipped_count = 0
        
        for file_path in file_paths:
            try:
                if os.path.isfile(file_path) and file_path not in self.files:
                    self.files.append(file_path)
                    file_name = os.path.basename(file_path)
                    self.files_listbox.insert(tk.END, file_name)
                    added_count += 1
                else:
                    skipped_count += 1
            except Exception:
                skipped_count += 1
        
        self.update_file_count()
        self.update_button_states()
        
        if added_count > 0:
            message = f"{added_count}개 파일이 추가되었습니다."
            if skipped_count > 0:
                message += f" ({skipped_count}개 건너뜀)"
            self.status_var.set(message)
        else:
            self.status_var.set("추가할 새로운 파일이 없습니다.")
    
    def remove_selected_files(self):
        """선택된 파일들 제거"""
        selection = self.files_listbox.curselection()
        if selection:
            removed_count = len(selection)
            for index in reversed(selection):
                self.files_listbox.delete(index)
                del self.files[index]
            
            self.update_file_count()
            self.update_button_states()
            self.status_var.set(f"{removed_count}개 파일이 제거되었습니다.")
        else:
            self.status_var.set("제거할 파일을 선택해주세요.")
    
    def clear_all_files(self):
        """모든 파일 제거"""
        if self.files:
            count = len(self.files)
            self.files.clear()
            self.files_listbox.delete(0, tk.END)
            
            self.update_file_count()
            self.update_button_states()
            self.status_var.set(f"모든 파일({count}개)이 제거되었습니다.")
        else:
            self.status_var.set("제거할 파일이 없습니다.")
    
    def update_file_count(self):
        """파일 개수 업데이트"""
        count = len(self.files)
        self.count_var.set(f"파일: {count}개")
    
    def update_button_states(self):
        """버튼 상태 업데이트"""
        has_files = len(self.files) > 0
        
        state = tk.NORMAL if has_files else tk.DISABLED
        self.remove_button.config(state=state)
        self.clear_button.config(state=state)
        self.test_button.config(state=state)
        self.preview_button.config(state=state)
        self.execute_button.config(state=state)
    
    def matches_conditions(self, file_path):
        """파일이 설정된 조건들을 만족하는지 확인"""
        # 파일 크기 조건
        if self.use_size_condition.get():
            try:
                file_size = os.path.getsize(file_path)
                target_size = float(self.size_value.get())
                
                unit = self.size_unit.get()
                if unit == "KB":
                    target_size *= 1024
                elif unit == "MB":
                    target_size *= 1024 * 1024
                elif unit == "GB":
                    target_size *= 1024 * 1024 * 1024
                
                operator = self.size_operator.get()
                if operator == "<" and not (file_size < target_size):
                    return False
                elif operator == "<=" and not (file_size <= target_size):
                    return False
                elif operator == "=" and not (abs(file_size - target_size) < 1024):  # 1KB 오차 허용
                    return False
                elif operator == ">=" and not (file_size >= target_size):
                    return False
                elif operator == ">" and not (file_size > target_size):
                    return False
            except (ValueError, OSError):
                return False
        
        # 날짜 조건
        if self.use_date_condition.get():
            try:
                file_mtime = os.path.getmtime(file_path)
                file_date = datetime.fromtimestamp(file_mtime).date()
                target_date = datetime.strptime(self.date_value.get(), "%Y-%m-%d").date()
                
                if self.date_operator.get() == "after" and file_date <= target_date:
                    return False
                elif self.date_operator.get() == "before" and file_date >= target_date:
                    return False
            except (ValueError, OSError):
                return False
        
        # 확장자 조건
        if self.use_ext_condition.get():
            file_ext = os.path.splitext(file_path)[1].lower()
            allowed_exts = [ext.strip().lower() for ext in self.ext_list.get().split(',') if ext.strip()]
            if file_ext not in allowed_exts:
                return False
        
        return True
    
    def apply_transformations(self, name):
        """파일명에 변환 규칙 적용"""
        # 대소문자 변환
        case_method = self.case_method.get()
        if case_method == "upper":
            name = name.upper()
        elif case_method == "lower":
            name = name.lower()
        elif case_method == "title":
            name = name.title()
        
        # 특수문자 제거
        if self.remove_special.get():
            name = re.sub(r'[^\w\s.-]', '', name)
        
        # 연속 공백 정리
        if self.remove_consecutive.get():
            name = re.sub(r'\s+', ' ', name).strip()
        
        # 공백을 언더스코어로
        if self.replace_space.get():
            name = re.sub(r'\s+', '_', name)
        
        return name
    
    def generate_new_names(self):
        """조건에 맞는 파일들의 새 이름 생성"""
        if not self.files:
            return []
        
        # 조건에 맞는 파일들만 필터링
        filtered_files = []
        for file_path in self.files:
            if self.matches_conditions(file_path):
                filtered_files.append(file_path)
        
        new_names = []
        used_names = set()
        
        for i, file_path in enumerate(filtered_files):
            file_name = os.path.basename(file_path)
            name, ext = os.path.splitext(file_name)
            
            # 기본 이름 변경 적용
            method = self.basic_method.get()
            if method == "prefix":
                new_name = f"{self.basic_text_var.get()}{name}"
            elif method == "suffix":
                new_name = f"{name}{self.basic_text_var.get()}"
            elif method == "number":
                try:
                    start_num = int(self.basic_start_var.get())
                    digits = int(self.digits_var.get())
                    prefix = self.number_prefix_var.get()
                    number = start_num + i
                    new_name = f"{prefix}{number:0{digits}d}_{name}" if prefix else f"{number:0{digits}d}_{name}"
                except ValueError:
                    new_name = f"{i + 1:03d}_{name}"
            elif method == "replace":
                find_text = self.basic_find_var.get()
                replace_text = self.basic_replace_var.get()
                if find_text:
                    if self.use_regex_basic.get():
                        try:
                            flags = 0 if self.case_sensitive.get() else re.IGNORECASE
                            new_name = re.sub(find_text, replace_text, name, flags=flags)
                        except re.error:
                            new_name = name  # 정규식 오류 시 원본 유지
                    else:
                        if self.case_sensitive.get():
                            new_name = name.replace(find_text, replace_text)
                        else:
                            # 대소문자 구분 없이 바꾸기
                            pattern = re.compile(re.escape(find_text), re.IGNORECASE)
                            new_name = pattern.sub(replace_text, name)
                else:
                    new_name = name
            else:
                new_name = name
            
            # 패턴 기반 변경 적용
            if self.pattern_var.get():
                pattern = self.pattern_var.get()
                replacement = self.replacement_var.get()
                
                if self.use_regex.get():
                    try:
                        new_name = re.sub(pattern, replacement, new_name)
                    except re.error:
                        pass  # 정규식 오류 시 변경하지 않음
                else:
                    new_name = new_name.replace(pattern, replacement)
            
            # 변환 규칙 적용
            new_name = self.apply_transformations(new_name)
            
            # 최종 파일명 구성
            full_new_name = new_name + ext
            
            # 중복 처리
            if self.handle_duplicate.get():
                original_name = full_new_name
                counter = 1
                while full_new_name in used_names:
                    name_part, ext_part = os.path.splitext(original_name)
                    full_new_name = f"{name_part}_{counter}{ext_part}"
                    counter += 1
            
            used_names.add(full_new_name)
            new_names.append((file_path, full_new_name))
        
        return new_names
    
    def test_conditions(self):
        """설정된 조건들을 테스트"""
        if not self.files:
            self.status_var.set("테스트할 파일이 없습니다.")
            return
        
        matching_files = []
        condition_details = []
        
        for file_path in self.files:
            if self.matches_conditions(file_path):
                matching_files.append(os.path.basename(file_path))
                
                # 어떤 조건들이 적용되었는지 확인
                details = []
                if self.use_size_condition.get():
                    size = os.path.getsize(file_path)
                    unit = self.size_unit.get()
                    if unit == "KB":
                        size_display = f"{size/1024:.1f}KB"
                    elif unit == "MB":
                        size_display = f"{size/(1024*1024):.1f}MB"
                    elif unit == "GB":
                        size_display = f"{size/(1024*1024*1024):.1f}GB"
                    else:
                        size_display = f"{size}B"
                    details.append(f"크기: {size_display}")
                
                if self.use_date_condition.get():
                    mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    details.append(f"날짜: {mtime.strftime('%Y-%m-%d')}")
                
                if self.use_ext_condition.get():
                    ext = os.path.splitext(file_path)[1]
                    details.append(f"확장자: {ext}")
                
                condition_details.append(" | ".join(details))
        
        total_files = len(self.files)
        matching_count = len(matching_files)
        
        result_msg = f"전체 {total_files}개 파일 중 {matching_count}개가 조건에 일치합니다\\n\\n"
        
        if matching_count > 0:
            result_msg += "일치하는 파일:\\n"
            display_count = min(matching_count, 8)  # 최대 8개까지만 표시
            
            for i in range(display_count):
                file_info = matching_files[i]
                if i < len(condition_details) and condition_details[i]:
                    file_info += f" ({condition_details[i]})"
                result_msg += f"• {file_info}\\n"
            
            if matching_count > display_count:
                result_msg += f"... 외 {matching_count - display_count}개"
        
        messagebox.showinfo("조건 테스트 결과", result_msg)
        self.status_var.set(f"조건 테스트 완료: {matching_count}/{total_files} 파일 일치")
    
    def preview_rename(self):
        """이름 변경 미리보기"""
        new_names = self.generate_new_names()
        
        if not new_names:
            self.status_var.set("조건에 맞는 파일이 없습니다.")
            return
        
        # 미리보기 창 생성
        preview_window = tk.Toplevel(self.root)
        preview_window.title("고급 이름 변경 미리보기")
        preview_window.geometry("800x600")
        preview_window.transient(self.root)
        preview_window.grab_set()
        
        # 미리보기 내용
        frame = ttk.Frame(preview_window, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 제목
        title_frame = ttk.Frame(frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            title_frame, 
            text="고급 이름 변경 미리보기", 
            font=("맑은 고딕", 12, "bold")
        ).pack(side=tk.LEFT)
        
        method_desc = {
            "prefix": "접두사 추가",
            "suffix": "접미사 추가", 
            "number": "순번 매기기",
            "replace": "찾기/바꾸기"
        }
        ttk.Label(
            title_frame,
            text=f"방식: {method_desc.get(self.basic_method.get(), '')}",
            font=("맑은 고딕", 10),
            foreground="blue"
        ).pack(side=tk.RIGHT)
        
        # 트리뷰로 변경 전/후 비교
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("original", "new", "conditions")
        tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings", height=22)
        
        tree.heading("#0", text="순번")
        tree.heading("original", text="원본 파일명")
        tree.heading("new", text="새 파일명")
        tree.heading("conditions", text="적용 조건")
        
        tree.column("#0", width=60)
        tree.column("original", width=250)
        tree.column("new", width=250)
        tree.column("conditions", width=200)
        
        # 데이터 추가
        for i, (file_path, new_name) in enumerate(new_names):
            original_name = os.path.basename(file_path)
            
            # 적용된 조건들 표시
            conditions = []
            if self.use_size_condition.get():
                conditions.append("크기")
            if self.use_date_condition.get():
                conditions.append("날짜")
            if self.use_ext_condition.get():
                conditions.append("확장자")
            if self.pattern_var.get():
                conditions.append("패턴")
            if self.case_method.get() != "none":
                conditions.append("대소문자")
            if self.remove_special.get():
                conditions.append("특수문자")
            
            condition_text = ", ".join(conditions) if conditions else "기본"
            
            tree.insert("", tk.END, text=str(i+1), values=(original_name, new_name, condition_text))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.config(yscrollcommand=scrollbar.set)
        
        # 요약 정보
        summary_frame = ttk.Frame(frame)
        summary_frame.pack(fill=tk.X, pady=(15, 0))
        
        summary_text = f"총 {len(self.files)}개 파일 중 {len(new_names)}개 파일이 변경 예정"
        ttk.Label(summary_frame, text=summary_text, font=("맑은 고딕", 10, "bold")).pack(side=tk.LEFT)
        
        # 버튼
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=(10, 0))
        
        ttk.Button(
            button_frame, 
            text="닫기", 
            command=preview_window.destroy,
            width=12
        ).pack(side=tk.RIGHT)
        
        self.status_var.set(f"미리보기: {len(new_names)}개 파일 변경 예정")
    
    def execute_rename(self):
        """이름 변경 실행"""
        new_names = self.generate_new_names()
        
        if not new_names:
            self.status_var.set("조건에 맞는 파일이 없습니다.")
            return
        
        # 확인 대화상자
        confirm_msg = f"{len(new_names)}개 파일의 이름을 변경하시겠습니까?\\n\\n"
        confirm_msg += f"변경 방식: {self.basic_method.get()}\\n"
        if self.use_size_condition.get() or self.use_date_condition.get() or self.use_ext_condition.get():
            confirm_msg += "조건부 필터링 적용됨"
        
        if not messagebox.askyesno("확인", confirm_msg):
            return
        
        success_count = 0
        errors = []
        updated_files = []
        
        for file_path, new_name in new_names:
            try:
                dir_path = os.path.dirname(file_path)
                new_path = os.path.join(dir_path, new_name)
                
                # 파일명이 실제로 변경되는 경우에만 수행
                if file_path != new_path:
                    # 백업 생성 (옵션)
                    if self.backup_enabled.get():
                        backup_path = f"{file_path}.backup"
                        try:
                            import shutil
                            shutil.copy2(file_path, backup_path)
                        except Exception:
                            pass  # 백업 실패해도 계속 진행
                    
                    if os.path.exists(new_path):
                        errors.append(f"{os.path.basename(file_path)}: 같은 이름의 파일이 이미 존재")
                        updated_files.append(file_path)  # 원본 경로 유지
                    else:
                        os.rename(file_path, new_path)
                        updated_files.append(new_path)  # 새 경로로 업데이트
                        success_count += 1
                else:
                    updated_files.append(file_path)  # 변경 없음
                
            except Exception as e:
                errors.append(f"{os.path.basename(file_path)}: {str(e)}")
                updated_files.append(file_path)  # 원본 경로 유지
        
        # 파일 목록 업데이트
        self.files = updated_files
        self.refresh_file_list()
        
        # 결과 메시지
        if errors:
            error_msg = f"{success_count}개 파일 변경 완료.\\n오류 발생:\\n" + "\\n".join(errors[:5])
            if len(errors) > 5:
                error_msg += f"\\n... 외 {len(errors)-5}개"
            messagebox.showwarning("완료", error_msg)
            self.status_var.set(f"이름 변경 완료: {success_count}개 성공, {len(errors)}개 오류")
        else:
            messagebox.showinfo("완료", f"{success_count}개 파일의 이름이 성공적으로 변경되었습니다.")
            self.status_var.set(f"이름 변경 완료: {success_count}개 파일 성공")
    
    def refresh_file_list(self):
        """파일 목록 새로고침"""
        self.files_listbox.delete(0, tk.END)
        
        for file_path in self.files:
            if os.path.exists(file_path):
                file_name = os.path.basename(file_path)
                self.files_listbox.insert(tk.END, file_name)
        
        self.update_file_count()
    
    def run(self):
        """애플리케이션 실행"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\\n프로그램이 사용자에 의해 종료되었습니다.")
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")


def main():
    """메인 함수"""
    print("KRenamer Chapter 6: 고급 조건과 기능")
    print("=" * 40)
    print("이 예제에서 배우는 내용:")
    print("• 조건부 필터링 (파일 크기, 날짜, 확장자)")
    print("• 정규식 패턴 매칭")
    print("• 동적 UI 필드 표시")
    print("• 일괄 변환 규칙")
    print("• 중복 파일명 처리")
    print("• 실시간 미리보기")
    
    if not DND_AVAILABLE:
        print()
        print("⚠️  tkinterdnd2가 설치되지 않았습니다.")
        print("드래그 앤 드롭 기능을 사용하려면 다음 명령어로 설치하세요:")
        print("pip install tkinterdnd2")
        print()
    
    print("GUI 윈도우를 시작합니다...")
    
    try:
        app = AdvancedKRenamerGUI()
        app.run()
    except Exception as e:
        print(f"애플리케이션 시작 중 오류 발생: {e}")
        return 1
    
    print("KRenamer Chapter 6 완료!")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())