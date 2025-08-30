#!/usr/bin/env python3
"""
KRenamer Chapter 6 Step 2: UI와 로직 완전 분리
Step 1의 클래스들을 더 명확하게 분리하여 UI와 비즈니스 로직 완전 분리

변경 사항:
- RenameEngine을 완전히 독립적인 클래스로 분리 (GUI 의존성 제거)
- GUI는 사용자 입력과 화면 표시만 담당
- Engine은 순수한 파일명 변경 로직만 담당
- 의존성 방향: GUI → Engine (Engine은 GUI를 전혀 알지 못함)

핵심 개념:
- 관심사의 분리 (Separation of Concerns)
- MVC 패턴의 기초
- 단방향 의존성
- 테스트 가능한 구조
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any

# 드래그 앤 드롭 지원 (선택적)
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


class RenameEngine:
    """
    완전히 독립적인 파일명 변경 엔진
    
    특징:
    - GUI나 tkinter에 대한 의존성 없음
    - 순수한 파이썬 로직만 사용
    - 설정은 속성으로 관리
    - 테스트하기 쉬운 구조
    """
    
    def __init__(self):
        # 파일 목록
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
        self.case_method = "none"  # none, upper, lower, title
        self.remove_special_chars = False
        self.replace_spaces = False
        self.handle_duplicates = True
        
        # 필터 설정
        self.display_filter = "모든 파일"
        self.custom_extension = ""
    
    def add_files(self, file_paths: List[str]) -> int:
        """파일 추가 - 순수 로직만"""
        added_count = 0
        for file_path in file_paths:
            if os.path.isfile(file_path) and file_path not in self.files:
                self.files.append(file_path)
                added_count += 1
        return added_count
    
    def remove_files_by_indices(self, indices: List[int]) -> int:
        """인덱스로 파일 제거 - 순수 로직만"""
        removed_count = 0
        for index in sorted(indices, reverse=True):
            if 0 <= index < len(self.files):
                del self.files[index]
                removed_count += 1
        return removed_count
    
    def clear_files(self) -> int:
        """모든 파일 제거 - 순수 로직만"""
        count = len(self.files)
        self.files.clear()
        return count
    
    def get_filtered_files(self) -> List[str]:
        """필터링된 파일 목록 반환 - 순수 로직만"""
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
        """파일 통계 반환 - 순수 로직만"""
        total = len(self.files)
        filtered = len(self.get_filtered_files())
        return {
            'total': total,
            'filtered': filtered,
            'hidden': total - filtered
        }
    
    def generate_new_name(self, file_path: str, index: int) -> str:
        """새로운 파일명 생성 - 순수 로직만"""
        original_name = os.path.basename(file_path)
        name, ext = os.path.splitext(original_name)
        
        # 기본 리네임 방식 적용
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
        
        # 일괄 변환 적용
        new_name = self._apply_transformations(new_name)
        
        return new_name + ext
    
    def _apply_find_replace(self, name: str) -> str:
        """찾기/바꾸기 적용 - 순수 로직만"""
        if not self.find_text:
            return name
        
        if self.use_regex:
            try:
                flags = 0 if self.case_sensitive else re.IGNORECASE
                return re.sub(self.find_text, self.replace_text, name, flags=flags)
            except re.error:
                return name  # 정규식 오류 시 원본 유지
        else:
            if self.case_sensitive:
                return name.replace(self.find_text, self.replace_text)
            else:
                # 대소문자 구분 없이 바꾸기
                pattern = re.compile(re.escape(self.find_text), re.IGNORECASE)
                return pattern.sub(self.replace_text, name)
    
    def _apply_transformations(self, name: str) -> str:
        """일괄 변환 규칙 적용 - 순수 로직만"""
        # 대소문자 변환
        if self.case_method == "upper":
            name = name.upper()
        elif self.case_method == "lower":
            name = name.lower()
        elif self.case_method == "title":
            name = name.title()
        
        # 특수문자 제거
        if self.remove_special_chars:
            name = re.sub(r'[^\w\s.-]', '', name)
        
        # 공백 처리
        if self.replace_spaces:
            name = name.replace(' ', '_')
        
        return name
    
    def generate_rename_plan(self) -> List[Dict[str, Any]]:
        """
        리네임 계획 생성 - 순수 로직만
        반환: [{'original': str, 'new': str, 'changed': bool, 'path': str}, ...]
        """
        filtered_files = self.get_filtered_files()
        plan = []
        used_names = set()
        
        for index, file_path in enumerate(filtered_files):
            original_name = os.path.basename(file_path)
            new_name = self.generate_new_name(file_path, index)
            
            # 중복 처리
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
        """
        파일명 변경 실행 - 순수 로직만
        반환: {'success_count': int, 'errors': List[str], 'updated_files': List[str]}
        """
        plan = self.generate_rename_plan()
        success_count = 0
        errors = []
        updated_files = []
        
        for item in plan:
            if not item['changed']:
                updated_files.append(item['path'])
                continue
            
            file_path = item['path']
            new_name = item['new']
            original_name = item['original']
            
            try:
                dir_path = os.path.dirname(file_path)
                new_path = os.path.join(dir_path, new_name)
                
                # 같은 이름인 경우 건너뛰기
                if file_path == new_path:
                    updated_files.append(file_path)
                    continue
                
                # 대상 파일이 이미 존재하는 경우
                if os.path.exists(new_path):
                    errors.append(f"{original_name}: 같은 이름의 파일이 이미 존재합니다")
                    updated_files.append(file_path)
                    continue
                
                # 파일명 변경 실행
                os.rename(file_path, new_path)
                updated_files.append(new_path)
                success_count += 1
                
            except Exception as e:
                errors.append(f"{original_name}: {str(e)}")
                updated_files.append(file_path)
        
        # 성공한 경우 내부 파일 목록 업데이트
        if success_count > 0:
            # 원본 파일 목록에서 업데이트된 경로로 교체
            for i, original_path in enumerate(self.files):
                for item in plan:
                    if item['path'] == original_path and item['changed']:
                        # 성공적으로 변경된 경우만 업데이트
                        dir_path = os.path.dirname(original_path)
                        new_path = os.path.join(dir_path, item['new'])
                        if os.path.exists(new_path):
                            self.files[i] = new_path
                        break
        
        return {
            'success_count': success_count,
            'errors': errors,
            'updated_files': updated_files
        }
    
    def validate_settings(self) -> List[str]:
        """설정 유효성 검사 - 순수 로직만"""
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


class Step2GUI:
    """
    순수한 GUI 클래스 - UI 관리만 담당
    
    특징:
    - 비즈니스 로직 없음 (모두 Engine에 위임)
    - 사용자 입력 처리와 화면 표시만 담당
    - Engine의 결과를 받아서 UI 업데이트
    - Engine과 단방향 통신 (GUI → Engine)
    """
    
    def __init__(self):
        # 윈도우 초기화
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
        
        # 엔진 생성 (의존성 주입 스타일)
        self.engine = RenameEngine()
        
        # UI 변수들
        self.setup_variables()
        
        # UI 구성
        self.setup_window()
        self.setup_widgets()
        self.setup_drag_drop()
        self.setup_bindings()
        
        # 초기 상태 업데이트
        self.refresh_ui()
    
    def setup_window(self):
        """윈도우 기본 설정"""
        self.root.title("Chapter 6 Step 2: UI와 로직 완전 분리")
        self.root.geometry("1000x650")
        self.root.resizable(True, True)
        self.center_window()
    
    def center_window(self):
        """윈도우 중앙 배치"""
        self.root.update_idletasks()
        width, height = 1000, 650
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_variables(self):
        """tkinter 변수 설정"""
        # 파일 관리 변수
        self.display_filter_var = tk.StringVar(value="모든 파일")
        self.custom_extension_var = tk.StringVar()
        self.count_var = tk.StringVar(value="파일: 0개")
        
        # 리네임 설정 변수
        self.method_var = tk.StringVar(value="prefix")
        self.text_var = tk.StringVar()
        self.start_num_var = tk.StringVar(value="1")
        self.find_var = tk.StringVar()
        self.replace_var = tk.StringVar()
        
        # 고급 옵션 변수
        self.case_sensitive_var = tk.BooleanVar(value=True)
        self.use_regex_var = tk.BooleanVar()
        self.case_method_var = tk.StringVar(value="none")
        self.remove_special_var = tk.BooleanVar()
        self.replace_spaces_var = tk.BooleanVar()
        self.handle_duplicates_var = tk.BooleanVar(value=True)
        
        # 상태 변수
        self.status_var = tk.StringVar(value="파일을 추가하고 리네임 옵션을 설정하세요")
        self.warning_var = tk.StringVar()
    
    def setup_widgets(self):
        """위젯 구성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 상단: 설명
        info_frame = ttk.LabelFrame(main_frame, text="Step 2: UI와 로직 완전 분리", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_text = (
            "이 단계에서는 GUI와 비즈니스 로직을 완전히 분리합니다:\n"
            "• RenameEngine: GUI 의존성 없는 순수한 로직\n"
            "• Step2GUI: 사용자 입력과 화면 표시만 담당\n"
            "• 의존성 방향: GUI → Engine (Engine은 GUI를 모름)"
        )
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)
        
        # 경고 표시
        self.warning_label = ttk.Label(info_frame, textvariable=self.warning_var, foreground="red")
        self.warning_label.pack(anchor=tk.W, pady=(5, 0))
        
        # 좌우 패널 분할
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 왼쪽 패널: 파일 관리 + 옵션
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # 오른쪽 패널: 미리보기
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)
        
        # 왼쪽 패널 구성
        self.setup_file_section(left_frame)
        self.setup_options_section(left_frame)
        self.setup_advanced_section(left_frame)
        self.setup_buttons_section(left_frame)
        
        # 오른쪽 패널 구성
        self.setup_preview_section(right_frame)
        
        # 상태바
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X)
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT)
    
    def setup_file_section(self, parent):
        """파일 목록 섹션"""
        file_frame = ttk.LabelFrame(parent, text="파일 목록", padding="10")
        file_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 필터와 개수 표시
        header_frame = ttk.Frame(file_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="필터:").pack(side=tk.LEFT)
        
        filter_combo = ttk.Combobox(
            header_frame, 
            textvariable=self.display_filter_var,
            values=["모든 파일", "이미지 파일", "문서 파일", "음악 파일", "사용자 정의"],
            width=12
        )
        filter_combo.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(header_frame, text="확장자:").pack(side=tk.LEFT)
        ttk.Entry(header_frame, textvariable=self.custom_extension_var, width=15).pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(header_frame, textvariable=self.count_var, foreground="blue").pack(side=tk.RIGHT)
        
        # 파일 리스트박스
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.files_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        
        # 스크롤바
        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        scrollbar_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.files_listbox.xview)
        self.files_listbox.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # 그리드 배치
        self.files_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
    
    def setup_options_section(self, parent):
        """기본 옵션 섹션"""
        options_frame = ttk.LabelFrame(parent, text="기본 리네임 옵션", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 방식 선택
        method_frame = ttk.Frame(options_frame)
        method_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Radiobutton(method_frame, text="접두사", variable=self.method_var, value="prefix").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(method_frame, text="접미사", variable=self.method_var, value="suffix").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(method_frame, text="순번", variable=self.method_var, value="number").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(method_frame, text="찾기/바꾸기", variable=self.method_var, value="replace").pack(side=tk.LEFT)
        
        # 텍스트 입력
        text_frame = ttk.Frame(options_frame)
        text_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(text_frame, text="텍스트:", width=10).pack(side=tk.LEFT)
        ttk.Entry(text_frame, textvariable=self.text_var, width=30).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(text_frame, text="시작번호:").pack(side=tk.LEFT, padx=(10, 5))
        ttk.Entry(text_frame, textvariable=self.start_num_var, width=8).pack(side=tk.LEFT)
        
        # 찾기/바꾸기 입력
        replace_frame = ttk.Frame(options_frame)
        replace_frame.pack(fill=tk.X)
        
        ttk.Label(replace_frame, text="찾기:", width=10).pack(side=tk.LEFT)
        ttk.Entry(replace_frame, textvariable=self.find_var, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(replace_frame, text="바꾸기:").pack(side=tk.LEFT)
        ttk.Entry(replace_frame, textvariable=self.replace_var, width=15).pack(side=tk.LEFT, padx=(5, 0))
    
    def setup_advanced_section(self, parent):
        """고급 옵션 섹션"""
        advanced_frame = ttk.LabelFrame(parent, text="고급 옵션", padding="10")
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 첫 번째 행
        row1_frame = ttk.Frame(advanced_frame)
        row1_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Checkbutton(row1_frame, text="대소문자 구분", variable=self.case_sensitive_var).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(row1_frame, text="정규식 사용", variable=self.use_regex_var).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(row1_frame, text="중복 처리", variable=self.handle_duplicates_var).pack(side=tk.LEFT)
        
        # 두 번째 행 - 대소문자 변환
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
    
    def setup_buttons_section(self, parent):
        """버튼 섹션"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=(10, 0))
        
        # 파일 관리 버튼
        file_buttons = ttk.Frame(button_frame)
        file_buttons.pack(pady=(0, 5))
        
        ttk.Button(file_buttons, text="파일 추가", command=self.add_files_dialog).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(file_buttons, text="폴더 추가", command=self.add_folder_dialog).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(file_buttons, text="선택 제거", command=self.remove_selected_files).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(file_buttons, text="전체 지우기", command=self.clear_all_files).pack(side=tk.LEFT)
        
        # 실행 버튼
        action_buttons = ttk.Frame(button_frame)
        action_buttons.pack()
        
        ttk.Button(action_buttons, text="설정 검증", command=self.validate_settings).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_buttons, text="미리보기", command=self.update_preview).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_buttons, text="이름 변경 실행", command=self.execute_rename).pack(side=tk.LEFT)
    
    def setup_preview_section(self, parent):
        """미리보기 섹션"""
        preview_frame = ttk.LabelFrame(parent, text="미리보기", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # 상단 정보
        info_frame = ttk.Frame(preview_frame)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_var = tk.StringVar()
        ttk.Label(info_frame, textvariable=self.stats_var, font=("맑은 고딕", 9), foreground="blue").pack(side=tk.LEFT)
        
        # 트리뷰로 미리보기 표시
        tree_frame = ttk.Frame(preview_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("original", "new", "status")
        self.preview_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        self.preview_tree.heading("original", text="원본 파일명")
        self.preview_tree.heading("new", text="새 파일명")
        self.preview_tree.heading("status", text="상태")
        
        self.preview_tree.column("original", width=200)
        self.preview_tree.column("new", width=200)
        self.preview_tree.column("status", width=80)
        
        # 스크롤바
        preview_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.preview_tree.yview)
        self.preview_tree.config(yscrollcommand=preview_scrollbar.set)
        
        self.preview_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_drag_drop(self):
        """드래그 앤 드롭 설정"""
        if DND_AVAILABLE:
            self.files_listbox.drop_target_register(DND_FILES)
            self.files_listbox.dnd_bind('<<Drop>>', self.on_drop)
    
    def setup_bindings(self):
        """이벤트 바인딩"""
        # 변수 변경 감지
        variables_to_trace = [
            self.display_filter_var, self.custom_extension_var,
            self.method_var, self.text_var, self.start_num_var, self.find_var, self.replace_var,
            self.case_sensitive_var, self.use_regex_var, self.case_method_var,
            self.remove_special_var, self.replace_spaces_var, self.handle_duplicates_var
        ]
        
        for var in variables_to_trace:
            var.trace('w', self.on_settings_changed)
    
    def on_drop(self, event):
        """드래그 앤 드롭 이벤트 처리 - UI 이벤트만"""
        files = self.root.tk.splitlist(event.data)
        self.add_files(files)
    
    def on_settings_changed(self, *args):
        """설정 변경 시 호출 - UI 이벤트만"""
        self.sync_ui_to_engine()
        self.refresh_ui()
    
    def sync_ui_to_engine(self):
        """UI 설정을 Engine에 동기화 - 단방향 통신"""
        # 필터 설정
        self.engine.display_filter = self.display_filter_var.get()
        self.engine.custom_extension = self.custom_extension_var.get()
        
        # 기본 리네임 설정
        self.engine.method = self.method_var.get()
        self.engine.prefix_text = self.text_var.get()
        self.engine.suffix_text = self.text_var.get()
        
        try:
            self.engine.start_number = int(self.start_num_var.get())
        except:
            self.engine.start_number = 1
        
        self.engine.find_text = self.find_var.get()
        self.engine.replace_text = self.replace_var.get()
        
        # 고급 옵션
        self.engine.case_sensitive = self.case_sensitive_var.get()
        self.engine.use_regex = self.use_regex_var.get()
        self.engine.case_method = self.case_method_var.get()
        self.engine.remove_special_chars = self.remove_special_var.get()
        self.engine.replace_spaces = self.replace_spaces_var.get()
        self.engine.handle_duplicates = self.handle_duplicates_var.get()
    
    def refresh_ui(self):
        """UI 전체 새로고침 - UI 업데이트만"""
        self.refresh_file_list()
        self.update_file_count()
        self.update_preview()
        self.validate_settings()
    
    def refresh_file_list(self):
        """파일 리스트박스 새로고침 - UI 업데이트만"""
        self.files_listbox.delete(0, tk.END)
        
        filtered_files = self.engine.get_filtered_files()
        for file_path in filtered_files:
            filename = os.path.basename(file_path)
            self.files_listbox.insert(tk.END, filename)
    
    def update_file_count(self):
        """파일 개수 표시 업데이트 - UI 업데이트만"""
        stats = self.engine.get_file_statistics()
        self.count_var.set(f"파일: {stats['total']}개 (필터: {stats['filtered']}개)")
    
    def update_preview(self):
        """미리보기 업데이트 - UI 업데이트만"""
        # 기존 항목 제거
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        # Engine에서 계획 받아오기
        self.sync_ui_to_engine()
        plan = self.engine.generate_rename_plan()
        
        if not plan:
            self.stats_var.set("변경할 파일이 없습니다")
            return
        
        # 통계 계산
        changed_count = sum(1 for item in plan if item['changed'])
        self.stats_var.set(f"총 {len(plan)}개 파일 중 {changed_count}개 변경 예정")
        
        # 미리보기 표시
        for item in plan:
            if item['changed']:
                status = "변경됨"
                tags = ("changed",)
            else:
                status = "동일"
                tags = ("same",)
            
            self.preview_tree.insert("", tk.END, values=(
                item['original'], 
                item['new'], 
                status
            ), tags=tags)
        
        # 색상 설정
        self.preview_tree.tag_configure("changed", foreground="blue")
        self.preview_tree.tag_configure("same", foreground="gray")
    
    def validate_settings(self):
        """설정 검증 - UI 표시만"""
        self.sync_ui_to_engine()
        warnings = self.engine.validate_settings()
        
        if warnings:
            self.warning_var.set("⚠️ " + warnings[0])
        else:
            self.warning_var.set("")
    
    def add_files_dialog(self):
        """파일 추가 대화상자 - UI 이벤트만"""
        files = filedialog.askopenfilenames(title="파일 선택")
        if files:
            self.add_files(files)
    
    def add_folder_dialog(self):
        """폴더 추가 대화상자 - UI 이벤트만"""
        folder = filedialog.askdirectory(title="폴더 선택")
        if folder:
            files = []
            for root, dirs, filenames in os.walk(folder):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
            self.add_files(files)
    
    def add_files(self, files):
        """파일 추가 - Engine에 위임"""
        added_count = self.engine.add_files(files)
        if added_count > 0:
            self.status_var.set(f"{added_count}개 파일이 추가되었습니다")
            self.refresh_ui()
        else:
            self.status_var.set("추가할 새로운 파일이 없습니다")
    
    def remove_selected_files(self):
        """선택된 파일 제거 - Engine에 위임"""
        selection = self.files_listbox.curselection()
        if selection:
            # 필터링된 인덱스를 원본 인덱스로 변환
            filtered_files = self.engine.get_filtered_files()
            original_indices = []
            
            for sel_index in selection:
                if sel_index < len(filtered_files):
                    file_path = filtered_files[sel_index]
                    if file_path in self.engine.files:
                        original_index = self.engine.files.index(file_path)
                        original_indices.append(original_index)
            
            removed_count = self.engine.remove_files_by_indices(original_indices)
            self.status_var.set(f"{removed_count}개 파일이 제거되었습니다")
            self.refresh_ui()
        else:
            self.status_var.set("제거할 파일을 선택해주세요")
    
    def clear_all_files(self):
        """모든 파일 제거 - Engine에 위임"""
        removed_count = self.engine.clear_files()
        if removed_count > 0:
            self.status_var.set(f"모든 파일({removed_count}개)이 제거되었습니다")
            self.refresh_ui()
    
    def execute_rename(self):
        """파일명 변경 실행 - Engine에 위임"""
        if not self.engine.files:
            self.status_var.set("변경할 파일이 없습니다")
            return
        
        self.sync_ui_to_engine()
        
        # 미리 검증
        warnings = self.engine.validate_settings()
        if warnings:
            if not messagebox.askyesno("경고", f"다음 경고가 있습니다:\n{warnings[0]}\n\n계속 진행하시겠습니까?"):
                return
        
        # 변경 계획 확인
        plan = self.engine.generate_rename_plan()
        change_count = sum(1 for item in plan if item['changed'])
        
        if change_count == 0:
            self.status_var.set("변경될 파일이 없습니다")
            return
        
        # 확인 대화상자
        if not messagebox.askyesno("확인", f"{change_count}개 파일의 이름을 변경하시겠습니까?"):
            return
        
        # Engine에 실행 위임
        result = self.engine.execute_rename()
        
        # 결과 처리 (UI만)
        success_count = result['success_count']
        errors = result['errors']
        
        if errors:
            error_msg = f"{success_count}개 파일 변경 완료.\n오류:\n" + "\n".join(errors[:5])
            if len(errors) > 5:
                error_msg += f"\n... 외 {len(errors)-5}개"
            messagebox.showwarning("완료", error_msg)
        else:
            messagebox.showinfo("완료", f"{success_count}개 파일의 이름이 변경되었습니다")
        
        self.status_var.set(f"변경 완료: {success_count}개 성공, {len(errors)}개 오류")
        self.refresh_ui()
    
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()


def main():
    """메인 함수"""
    print("KRenamer Chapter 6 Step 2: UI와 로직 완전 분리")
    print("=" * 50)
    print("학습 내용:")
    print("• GUI와 비즈니스 로직의 완전한 분리")
    print("• RenameEngine: GUI 의존성 없는 순수한 로직")
    print("• Step2GUI: 사용자 입력과 화면 표시만 담당")
    print("• 의존성 방향: GUI → Engine (Engine은 GUI를 모름)")
    print()
    print("핵심 개념:")
    print("• 관심사의 분리 (Separation of Concerns)")
    print("• MVC 패턴의 기초")
    print("• 단방향 의존성")
    print("• 테스트 가능한 구조")
    print()
    
    if not DND_AVAILABLE:
        print("⚠️  tkinterdnd2가 설치되지 않았습니다.")
        print("드래그 앤 드롭 기능을 사용하려면 다음 명령어로 설치하세요:")
        print("pip install tkinterdnd2")
        print()
    
    try:
        app = Step2GUI()
        app.run()
        return 0
    except Exception as e:
        print(f"애플리케이션 실행 중 오류: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())