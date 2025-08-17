import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re

# 드래그 앤 드롭 라이브러리 (선택적)
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

class FindReplaceFileRenamer:
    def __init__(self):
        # 드래그 앤 드롭 지원 여부에 따라 다른 방식으로 윈도우 생성
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
        
        self.root.title("파일 리네이머 v4.0 - 찾기/바꾸기")
        self.root.geometry("850x750")
        
        self.files = []
        self.create_widgets()
        self.setup_drag_drop()
        
        # 실시간 미리보기
        self.setup_preview_bindings()
    
    def create_widgets(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # 제목
        title_label = ttk.Label(main_frame, text="파일 이름 변경 도구 - 찾기/바꾸기", 
                               font=("맑은 고딕", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # 드래그 앤 드롭 영역
        self.create_drop_area(main_frame)
        
        # 파일 목록 영역
        self.create_file_list(main_frame)
        
        # 이름 변경 옵션 영역
        self.create_rename_options(main_frame)
        
        # 미리보기 영역
        self.create_preview_area(main_frame)
        
        # 실행 버튼
        self.create_action_buttons(main_frame)
        
        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)  # 파일 목록
        main_frame.rowconfigure(4, weight=1)  # 미리보기
    
    def create_drop_area(self, parent):
        """드래그 앤 드롭 영역 생성"""
        drop_frame = ttk.LabelFrame(parent, text="파일 추가", padding="10")
        drop_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # 드롭 라벨
        if DND_AVAILABLE:
            drop_text = "📁 파일을 여기에 드래그 앤 드롭하거나 버튼을 클릭하세요"
            bg_color = "#e8f4fd"
        else:
            drop_text = "⚠️ 드래그 앤 드롭 불가능 - 버튼을 사용하세요"
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
        ttk.Button(btn_frame, text="🗑️ 전체 삭제", 
                  command=self.clear_files).pack(side="right")
    
    def create_file_list(self, parent):
        """파일 목록 영역 생성"""
        list_frame = ttk.LabelFrame(parent, text="파일 목록", padding="5")
        list_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        
        # 파일 개수 표시
        self.file_count_var = tk.StringVar(value="파일 개수: 0")
        ttk.Label(list_frame, textvariable=self.file_count_var).pack(anchor="w", pady=(0, 5))
        
        # 파일 목록 (Treeview)
        columns = ("파일명", "경로", "크기")
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        
        self.file_tree.heading("파일명", text="파일명")
        self.file_tree.heading("경로", text="경로")  
        self.file_tree.heading("크기", text="크기")
        
        self.file_tree.column("파일명", width=200)
        self.file_tree.column("경로", width=300)
        self.file_tree.column("크기", width=80)
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
        self.file_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
    
    def create_rename_options(self, parent):
        """이름 변경 옵션 영역 생성"""
        options_frame = ttk.LabelFrame(parent, text="이름 변경 옵션", padding="10")
        options_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # 작업 모드 선택
        self.mode_var = tk.StringVar(value="prefix")
        
        mode_frame = ttk.Frame(options_frame)
        mode_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Radiobutton(mode_frame, text="접두사 추가", variable=self.mode_var, 
                       value="prefix").pack(side="left", padx=(0, 10))
        ttk.Radiobutton(mode_frame, text="접미사 추가", variable=self.mode_var, 
                       value="suffix").pack(side="left", padx=(0, 10))
        ttk.Radiobutton(mode_frame, text="찾기/바꾸기", variable=self.mode_var, 
                       value="find_replace").pack(side="left", padx=(0, 10))
        ttk.Radiobutton(mode_frame, text="연번 매기기", variable=self.mode_var, 
                       value="numbering").pack(side="left")
        
        # 옵션별 입력 영역
        self.create_option_inputs(options_frame)
    
    def create_option_inputs(self, parent):
        """각 모드별 입력 필드 생성"""
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill="x")
        
        # 접두사/접미사 입력
        prefix_suffix_frame = ttk.Frame(input_frame)
        prefix_suffix_frame.grid(row=0, column=0, sticky="ew", pady=2)
        
        ttk.Label(prefix_suffix_frame, text="텍스트:").pack(side="left")
        self.text_var = tk.StringVar()
        self.text_entry = ttk.Entry(prefix_suffix_frame, textvariable=self.text_var, width=20)
        self.text_entry.pack(side="left", padx=(5, 0))
        
        # 찾기/바꾸기 입력
        find_replace_frame = ttk.Frame(input_frame)
        find_replace_frame.grid(row=1, column=0, sticky="ew", pady=2)
        
        ttk.Label(find_replace_frame, text="찾기:").pack(side="left")
        self.find_var = tk.StringVar()
        self.find_entry = ttk.Entry(find_replace_frame, textvariable=self.find_var, width=15)
        self.find_entry.pack(side="left", padx=(5, 10))
        
        ttk.Label(find_replace_frame, text="바꾸기:").pack(side="left")
        self.replace_var = tk.StringVar()
        self.replace_entry = ttk.Entry(find_replace_frame, textvariable=self.replace_var, width=15)
        self.replace_entry.pack(side="left", padx=(5, 10))
        
        # 정규표현식 옵션
        self.regex_var = tk.BooleanVar()
        ttk.Checkbutton(find_replace_frame, text="정규표현식", 
                       variable=self.regex_var).pack(side="left", padx=(10, 0))
        
        # 연번 매기기 옵션
        numbering_frame = ttk.Frame(input_frame)
        numbering_frame.grid(row=2, column=0, sticky="ew", pady=2)
        
        ttk.Label(numbering_frame, text="시작번호:").pack(side="left")
        self.start_var = tk.StringVar(value="1")
        ttk.Entry(numbering_frame, textvariable=self.start_var, width=5).pack(side="left", padx=(5, 10))
        
        ttk.Label(numbering_frame, text="자릿수:").pack(side="left")
        self.digits_var = tk.StringVar(value="3")
        ttk.Entry(numbering_frame, textvariable=self.digits_var, width=5).pack(side="left", padx=(5, 10))
        
        ttk.Label(numbering_frame, text="형식:").pack(side="left")
        self.format_var = tk.StringVar(value="{number}_{name}")
        ttk.Entry(numbering_frame, textvariable=self.format_var, width=15).pack(side="left", padx=(5, 0))
        
        input_frame.columnconfigure(0, weight=1)
    
    def create_preview_area(self, parent):
        """미리보기 영역 생성"""
        preview_frame = ttk.LabelFrame(parent, text="미리보기", padding="5")
        preview_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        
        # 미리보기 목록
        columns = ("현재 이름", "새 이름")
        self.preview_tree = ttk.Treeview(preview_frame, columns=columns, show="headings", height=8)
        
        self.preview_tree.heading("현재 이름", text="현재 이름")
        self.preview_tree.heading("새 이름", text="새 이름")
        
        self.preview_tree.column("현재 이름", width=300)
        self.preview_tree.column("새 이름", width=300)
        
        # 스크롤바
        preview_scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", command=self.preview_tree.yview)
        self.preview_tree.configure(yscrollcommand=preview_scrollbar.set)
        
        self.preview_tree.pack(side="left", fill="both", expand=True)
        preview_scrollbar.pack(side="right", fill="y")
        
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
    
    def create_action_buttons(self, parent):
        """실행 버튼 영역 생성"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="🔄 미리보기 새로고침", 
                  command=self.update_preview).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="✅ 이름 변경 실행", 
                  command=self.execute_rename, 
                  style="Accent.TButton").pack(side="left")
    
    def setup_preview_bindings(self):
        """실시간 미리보기를 위한 이벤트 바인딩"""
        self.mode_var.trace('w', self.on_option_change)
        self.text_var.trace('w', self.on_option_change)
        self.find_var.trace('w', self.on_option_change)
        self.replace_var.trace('w', self.on_option_change)
        self.regex_var.trace('w', self.on_option_change)
        self.start_var.trace('w', self.on_option_change)
        self.digits_var.trace('w', self.on_option_change)
        self.format_var.trace('w', self.on_option_change)
    
    def setup_drag_drop(self):
        """드래그 앤 드롭 설정"""
        if DND_AVAILABLE:
            self.drop_label.drop_target_register(DND_FILES)
            self.drop_label.dnd_bind('<<Drop>>', self.on_drop)
            self.file_tree.drop_target_register(DND_FILES)
            self.file_tree.dnd_bind('<<Drop>>', self.on_drop)
    
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
    
    def add_files(self, file_paths):
        """파일 목록에 파일 추가"""
        added_count = 0
        
        for file_path in file_paths:
            if os.path.isfile(file_path) and file_path not in self.files:
                self.files.append(file_path)
                
                # Treeview에 추가
                filename = os.path.basename(file_path)
                size = self.get_file_size(file_path)
                self.file_tree.insert("", "end", values=(filename, file_path, size))
                added_count += 1
        
        self.update_file_count()
        self.update_preview()
        
        if added_count > 0:
            messagebox.showinfo("파일 추가", f"{added_count}개 파일이 추가되었습니다.")
    
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
    
    def clear_files(self):
        """모든 파일 제거"""
        if self.files:
            result = messagebox.askyesno("확인", "모든 파일을 제거하시겠습니까?")
            if result:
                self.files.clear()
                self.file_tree.delete(*self.file_tree.get_children())
                self.preview_tree.delete(*self.preview_tree.get_children())
                self.update_file_count()
    
    def update_file_count(self):
        """파일 개수 업데이트"""
        self.file_count_var.set(f"파일 개수: {len(self.files)}")
    
    def on_option_change(self, *args):
        """옵션 변경 시 미리보기 업데이트"""
        self.update_preview()
    
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
                    # 정규표현식 모드
                    try:
                        return re.sub(find_text, replace_text, filename)
                    except re.error:
                        return filename  # 정규식 오류 시 원본 반환
                else:
                    # 일반 찾기/바꾸기
                    return filename.replace(find_text, replace_text)
            
            elif mode == "numbering":
                try:
                    start = int(self.start_var.get())
                    digits = int(self.digits_var.get())
                    format_str = self.format_var.get()
                    
                    number = start + index
                    number_str = f"{number:0{digits}d}"
                    
                    # 형식 변수 치환
                    new_name = format_str.format(
                        number=number_str,
                        name=name,
                        ext=ext[1:] if ext else "",
                        filename=filename,
                        index=index
                    )
                    
                    # 확장자가 없으면 원본 확장자 추가
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
        # 기존 미리보기 삭제
        self.preview_tree.delete(*self.preview_tree.get_children())
        
        # 새 미리보기 생성
        for index, file_path in enumerate(self.files):
            current_name = os.path.basename(file_path)
            new_name = self.generate_new_name(file_path, index)
            
            # 변경사항이 있으면 하이라이트
            if current_name != new_name:
                tag = "changed"
            else:
                tag = "unchanged"
            
            item_id = self.preview_tree.insert("", "end", values=(current_name, new_name), tags=(tag,))
        
        # 태그 색상 설정
        self.preview_tree.tag_configure("changed", background="#e8f5e8")
        self.preview_tree.tag_configure("unchanged", background="#f5f5f5")
    
    def execute_rename(self):
        """실제 파일명 변경 실행"""
        if not self.files:
            messagebox.showwarning("경고", "변경할 파일이 없습니다.")
            return
        
        # 변경 계획 생성
        rename_plan = []
        for index, file_path in enumerate(self.files):
            current_name = os.path.basename(file_path)
            new_name = self.generate_new_name(file_path, index)
            
            if current_name != new_name:
                directory = os.path.dirname(file_path)
                new_path = os.path.join(directory, new_name)
                rename_plan.append((file_path, new_path))
        
        if not rename_plan:
            messagebox.showinfo("정보", "변경할 파일이 없습니다.")
            return
        
        # 확인 대화상자
        result = messagebox.askyesno(
            "확인", 
            f"{len(rename_plan)}개 파일의 이름을 변경하시겠습니까?"
        )
        
        if not result:
            return
        
        # 실행
        success_count = 0
        errors = []
        
        for old_path, new_path in rename_plan:
            try:
                # 동일한 이름의 파일이 이미 있는지 확인
                if os.path.exists(new_path):
                    errors.append(f"{os.path.basename(old_path)}: 대상 파일이 이미 존재함")
                    continue
                
                os.rename(old_path, new_path)
                success_count += 1
                
                # 내부 파일 목록 업데이트
                index = self.files.index(old_path)
                self.files[index] = new_path
                
            except Exception as e:
                errors.append(f"{os.path.basename(old_path)}: {str(e)}")
        
        # 결과 보고
        result_msg = f"성공: {success_count}개 파일 변경됨"
        if errors:
            result_msg += f"\n실패: {len(errors)}개"
            if len(errors) <= 5:
                result_msg += "\n" + "\n".join(errors)
        
        messagebox.showinfo("작업 완료", result_msg)
        
        # UI 업데이트
        self.refresh_file_list()
        self.update_preview()
    
    def refresh_file_list(self):
        """파일 목록 새로고침"""
        self.file_tree.delete(*self.file_tree.get_children())
        
        for file_path in self.files:
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                size = self.get_file_size(file_path)
                self.file_tree.insert("", "end", values=(filename, file_path, size))
            else:
                # 파일이 없으면 목록에서 제거
                self.files.remove(file_path)
        
        self.update_file_count()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FindReplaceFileRenamer()
    app.run()