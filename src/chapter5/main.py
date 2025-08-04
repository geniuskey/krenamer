#!/usr/bin/env python3
"""
KRenamer Chapter 5: File Renaming Logic
파일명 변경 로직을 구현한 GUI

이 챕터에서는 다음 기능을 배웁니다:
- 다양한 리네임 방식 구현 (접두사, 접미사, 순번, 찾기/바꾸기)
- 동적 UI 필드 표시 (선택된 방식에 따라 필요한 입력 필드만 표시)
- 미리보기 기능
- 실제 파일명 변경 실행
- 오류 처리 및 결과 보고
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
from pathlib import Path

# tkinterdnd2 선택적 import
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


class RenameLogicKRenamerGUI:
    """
    KRenamer Chapter 5: 파일명 변경 로직
    
    Chapter 4의 드래그 앤 드롭 기능에 실제 파일명 변경 기능을 추가합니다:
    - 다양한 리네임 방식 (접두사, 접미사, 순번, 찾기/바꾸기)
    - 동적 UI 필드 표시
    - 미리보기 기능
    - 실제 파일명 변경 및 오류 처리
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
        self.rename_widgets = {}
        
        self.setup_window()
        self.setup_widgets()
        self.setup_drag_drop()
    
    def setup_window(self):
        """윈도우 기본 설정"""
        self.root.title("KRenamer - Chapter 5: 파일명 변경 로직")
        self.root.geometry("900x500")
        self.root.resizable(True, True)
        self.root.minsize(800, 500)
        
        self.center_window()
    
    def center_window(self):
        """윈도우를 화면 중앙에 배치"""
        self.root.update_idletasks()
        width = 900
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_widgets(self):
        """GUI 위젯들 설정 및 배치"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 섹션별 설정
        self.setup_file_list_section(main_frame)
        self.setup_rename_options_section(main_frame)
        self.setup_buttons_section(main_frame)
        self.setup_status_section(main_frame)
        
        # 그리드 가중치 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)  # 파일 목록 영역이 확장
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 초기 버튼 상태 및 필드 표시 설정
        self.update_button_states()
        self.update_rename_fields()
    
    def setup_file_list_section(self, parent):
        """파일 목록 섹션 설정"""
        # 파일 목록 프레임
        files_frame = ttk.LabelFrame(parent, text="파일 목록", padding="10")
        files_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # 헤더 프레임
        header_frame = ttk.Frame(files_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
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
        
        # 파일 리스트박스 (수평, 수직 스크롤 지원)
        self.files_listbox = tk.Listbox(
            listbox_frame, 
            height=12,
            font=("맑은 고딕", 9),
            selectmode=tk.EXTENDED
        )
        
        # 스크롤바들
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
    
    def setup_rename_options_section(self, parent):
        """이름 변경 옵션 섹션 설정"""
        # 이름 변경 옵션 프레임
        options_frame = ttk.LabelFrame(parent, text="이름 변경 옵션", padding="10")
        options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # 이름 변경 방식 선택
        self.rename_method = tk.StringVar(value="prefix")
        
        # 라디오 버튼 프레임
        method_frame = ttk.Frame(options_frame)
        method_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # 라디오 버튼들
        ttk.Radiobutton(
            method_frame, 
            text="접두사 추가", 
            variable=self.rename_method, 
            value="prefix", 
            command=self.update_rename_fields
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Radiobutton(
            method_frame, 
            text="접미사 추가", 
            variable=self.rename_method, 
            value="suffix", 
            command=self.update_rename_fields
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Radiobutton(
            method_frame, 
            text="순번 매기기", 
            variable=self.rename_method, 
            value="number", 
            command=self.update_rename_fields
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Radiobutton(
            method_frame, 
            text="찾기/바꾸기", 
            variable=self.rename_method, 
            value="replace", 
            command=self.update_rename_fields
        ).pack(side=tk.LEFT)
        
        # 입력 필드들 설정
        self.setup_rename_input_fields(options_frame)
        
        options_frame.columnconfigure(1, weight=1)
    
    def setup_rename_input_fields(self, parent):
        """이름 변경 입력 필드들 설정"""
        # 텍스트 입력 (접두사/접미사용)
        self.rename_widgets['text_label'] = ttk.Label(parent, text="텍스트:")
        self.rename_widgets['text_label'].grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.text_var = tk.StringVar()
        self.rename_widgets['text_entry'] = ttk.Entry(parent, textvariable=self.text_var, width=30)
        self.rename_widgets['text_entry'].grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 시작 번호 입력 (순번 매기기용)
        self.rename_widgets['number_label'] = ttk.Label(parent, text="시작 번호:")
        self.rename_widgets['number_label'].grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.start_number_var = tk.StringVar(value="1")
        self.rename_widgets['number_entry'] = ttk.Entry(parent, textvariable=self.start_number_var, width=10)
        self.rename_widgets['number_entry'].grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 자릿수 설정
        number_frame = ttk.Frame(parent)
        self.rename_widgets['number_frame'] = number_frame
        number_frame.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(number_frame, text="자릿수:").pack(side=tk.LEFT)
        self.digits_var = tk.StringVar(value="3")
        digits_combo = ttk.Combobox(number_frame, textvariable=self.digits_var, width=5, values=["1", "2", "3", "4", "5"])
        digits_combo.pack(side=tk.LEFT, padx=(5, 0))
        # digits_combo는 number_frame 내부에서 pack으로 관리되므로 rename_widgets에 추가하지 않음
        
        # 찾을 텍스트 입력 (찾기/바꾸기용)
        self.rename_widgets['find_label'] = ttk.Label(parent, text="찾을 텍스트:")
        self.rename_widgets['find_label'].grid(row=4, column=0, sticky=tk.W, pady=5)
        
        self.find_var = tk.StringVar()
        self.rename_widgets['find_entry'] = ttk.Entry(parent, textvariable=self.find_var, width=30)
        self.rename_widgets['find_entry'].grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 바꿀 텍스트 입력 (찾기/바꾸기용)
        self.rename_widgets['replace_label'] = ttk.Label(parent, text="바꿀 텍스트:")
        self.rename_widgets['replace_label'].grid(row=5, column=0, sticky=tk.W, pady=5)
        
        self.replace_var = tk.StringVar()
        self.rename_widgets['replace_entry'] = ttk.Entry(parent, textvariable=self.replace_var, width=30)
        self.rename_widgets['replace_entry'].grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 대소문자 구분 옵션
        replace_options_frame = ttk.Frame(parent)
        self.rename_widgets['replace_options_frame'] = replace_options_frame
        replace_options_frame.grid(row=6, column=1, sticky=tk.W, pady=5)
        
        self.case_sensitive = tk.BooleanVar(value=True)
        case_check = ttk.Checkbutton(replace_options_frame, text="대소문자 구분", variable=self.case_sensitive)
        case_check.pack(side=tk.LEFT)
        # case_check는 replace_options_frame 내부에서 pack으로 관리되므로 rename_widgets에 추가하지 않음
    
    def update_rename_fields(self):
        """선택된 이름 변경 방식에 따라 관련 필드만 표시"""
        method = self.rename_method.get()
        
        # 모든 필드 숨기기
        for widget in self.rename_widgets.values():
            widget.grid_remove()
        
        # 선택된 방식에 따라 해당 필드만 표시
        if method in ["prefix", "suffix"]:
            # 접두사/접미사: 텍스트 입력만 표시
            self.rename_widgets['text_label'].grid()
            self.rename_widgets['text_entry'].grid()
            
            if method == "prefix":
                self.rename_widgets['text_label'].config(text="접두사 텍스트:")
            else:
                self.rename_widgets['text_label'].config(text="접미사 텍스트:")
        
        elif method == "number":
            # 순번 매기기: 시작 번호와 자릿수 표시
            self.rename_widgets['number_label'].grid()
            self.rename_widgets['number_entry'].grid()
            self.rename_widgets['number_frame'].grid()
            # digits_combo는 number_frame 내부에서 pack으로 관리되므로 별도 grid 호출 불필요
        
        elif method == "replace":
            # 찾기/바꾸기: 찾을 텍스트, 바꿀 텍스트, 옵션 표시
            self.rename_widgets['find_label'].grid()
            self.rename_widgets['find_entry'].grid()
            self.rename_widgets['replace_label'].grid()
            self.rename_widgets['replace_entry'].grid()
            self.rename_widgets['replace_options_frame'].grid()
            # case_check는 replace_options_frame 내부에서 pack으로 관리되므로 별도 grid 호출 불필요
        
        # 상태 메시지 업데이트
        method_descriptions = {
            "prefix": "접두사 추가 - 파일명 앞에 텍스트를 추가합니다",
            "suffix": "접미사 추가 - 파일명 뒤(확장자 앞)에 텍스트를 추가합니다",
            "number": "순번 매기기 - 파일명에 순차적인 번호를 추가합니다",
            "replace": "찾기/바꾸기 - 특정 텍스트를 다른 텍스트로 바꿉니다"
        }
        self.status_var.set(method_descriptions.get(method, ""))
    
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
        
        # 이름 변경 버튼들
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
        self.status_var.set("파일을 추가하고 이름 변경 옵션을 선택하세요.")
        
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
                    ("텍스트 파일", "*.txt"),
                    ("이미지 파일", "*.jpg *.jpeg *.png *.gif *.bmp"),
                    ("문서 파일", "*.pdf *.doc *.docx")
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
        self.preview_button.config(state=state)
        self.execute_button.config(state=state)
    
    def generate_new_names(self):
        """새로운 파일명 생성"""
        if not self.files:
            return []
        
        method = self.rename_method.get()
        new_names = []
        
        for i, file_path in enumerate(self.files):
            file_name = os.path.basename(file_path)
            name, ext = os.path.splitext(file_name)
            
            if method == "prefix":
                prefix = self.text_var.get()
                new_name = f"{prefix}{name}{ext}"
            
            elif method == "suffix":
                suffix = self.text_var.get()
                new_name = f"{name}{suffix}{ext}"
            
            elif method == "number":
                try:
                    start_num = int(self.start_number_var.get())
                    digits = int(self.digits_var.get())
                    number = start_num + i
                    new_name = f"{number:0{digits}d}_{name}{ext}"
                except ValueError:
                    new_name = f"{i + 1:03d}_{name}{ext}"
            
            elif method == "replace":
                find_text = self.find_var.get()
                replace_text = self.replace_var.get()
                if find_text:
                    if self.case_sensitive.get():
                        new_name = name.replace(find_text, replace_text) + ext
                    else:
                        # 대소문자 구분 없이 바꾸기
                        pattern = re.compile(re.escape(find_text), re.IGNORECASE)
                        new_name = pattern.sub(replace_text, name) + ext
                else:
                    new_name = file_name
            
            else:
                new_name = file_name
            
            new_names.append(new_name)
        
        return new_names
    
    def preview_rename(self):
        """이름 변경 미리보기"""
        if not self.files:
            self.status_var.set("미리보기할 파일이 없습니다.")
            return
        
        new_names = self.generate_new_names()
        
        # 미리보기 창 생성
        preview_window = tk.Toplevel(self.root)
        preview_window.title("이름 변경 미리보기")
        preview_window.geometry("700x500")
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
            text="이름 변경 미리보기", 
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
            text=f"방식: {method_desc.get(self.rename_method.get(), '')}",
            font=("맑은 고딕", 10),
            foreground="blue"
        ).pack(side=tk.RIGHT)
        
        # 트리뷰로 변경 전/후 비교
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("original", "new")
        tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings", height=20)
        
        tree.heading("#0", text="순번")
        tree.heading("original", text="원본 파일명")
        tree.heading("new", text="새 파일명")
        
        tree.column("#0", width=60)
        tree.column("original", width=300)
        tree.column("new", width=300)
        
        # 데이터 추가
        for i, (original_path, new_name) in enumerate(zip(self.files, new_names)):
            original_name = os.path.basename(original_path)
            tree.insert("", tk.END, text=str(i+1), values=(original_name, new_name))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.config(yscrollcommand=scrollbar.set)
        
        # 버튼
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=(15, 0))
        
        ttk.Button(
            button_frame, 
            text="닫기", 
            command=preview_window.destroy,
            width=12
        ).pack(side=tk.RIGHT)
        
        self.status_var.set(f"{len(self.files)}개 파일의 미리보기를 확인하세요.")
    
    def execute_rename(self):
        """이름 변경 실행"""
        if not self.files:
            self.status_var.set("이름을 변경할 파일이 없습니다.")
            return
        
        new_names = self.generate_new_names()
        
        # 확인 대화상자
        if not messagebox.askyesno(
            "확인", 
            f"{len(self.files)}개 파일의 이름을 변경하시겠습니까?\\n\\n"
            f"변경 방식: {self.rename_method.get()}"
        ):
            return
        
        success_count = 0
        errors = []
        updated_files = []
        
        for file_path, new_name in zip(self.files, new_names):
            try:
                dir_path = os.path.dirname(file_path)
                new_path = os.path.join(dir_path, new_name)
                
                # 파일명이 실제로 변경되는 경우에만 수행
                if file_path != new_path:
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
    print("KRenamer Chapter 5: 파일명 변경 로직")
    print("=" * 40)
    print("이 예제에서 배우는 내용:")
    print("- 다양한 리네임 방식 구현")
    print("- 동적 UI 필드 표시")
    print("- 미리보기 기능")
    print("- 실제 파일명 변경 실행")
    print("- 오류 처리 및 결과 보고")
    
    if not DND_AVAILABLE:
        print()
        print("WARNING: tkinterdnd2가 설치되지 않았습니다.")
        print("드래그 앤 드롭 기능을 사용하려면 다음 명령어로 설치하세요:")
        print("pip install tkinterdnd2")
        print()
    
    print("GUI 윈도우를 시작합니다...")
    
    try:
        app = RenameLogicKRenamerGUI()
        app.run()
    except Exception as e:
        print(f"애플리케이션 시작 중 오류 발생: {e}")
        return 1
    
    print("KRenamer Chapter 5 완료!")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())