import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
from rename_engine import RenameEngine

# 드래그 앤 드롭 라이브러리 (선택적)
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

class RealTimePreviewRenamer:
    """실시간 미리보기와 고급 기능이 포함된 리네이머"""
    
    def __init__(self):
        # 드래그 앤 드롭 지원 여부에 따라 다른 방식으로 윈도우 생성
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
        
        self.root.title("KRenamer v5.0 - 실시간 미리보기")
        self.root.geometry("1100x750")
        self.root.minsize(900, 650)
        
        # 엔진 초기화
        self.engine = RenameEngine()
        self.engine.on_files_changed = self.on_files_changed
        self.engine.on_options_changed = self.on_options_changed
        
        # 필터링 상태
        self.search_text = ""
        self.filter_status = "all"  # all, valid, error, changed
        
        self.create_widgets()
        self.create_variables()
        self.bind_events()
        self.setup_drag_drop()
    
    def create_widgets(self):
        """위젯 생성"""
        # 메인 컨테이너
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 상단 툴바
        self.create_toolbar(main_frame)
        
        # 2-패널 메인 영역
        self.create_main_panels(main_frame)
        
        # 하단 상태바
        self.create_statusbar(main_frame)
    
    def create_toolbar(self, parent):
        """상단 툴바"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        # 파일 관리 버튼들
        ttk.Button(toolbar, text="📁 파일 추가", 
                  command=self.add_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="📂 폴더 추가", 
                  command=self.add_folder).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # 검색 기능
        ttk.Label(toolbar, text="검색:").pack(side=tk.LEFT, padx=(5, 2))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=15)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(toolbar, text="🔍", command=self.apply_search, 
                  width=3).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="❌", command=self.clear_search, 
                  width=3).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # 작업 버튼들
        ttk.Button(toolbar, text="🔄 새로고침", 
                  command=self.refresh_preview).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="✅ 실행", 
                  command=self.execute_rename).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # 초기화 버튼들
        ttk.Button(toolbar, text="🗑️ 전체 삭제", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="⚙️ 옵션 초기화", 
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
            drop_text = "📁 파일을 여기에 드래그 앤 드롭하세요"
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
    
    def create_rename_options(self, parent):
        """이름 변경 옵션 위젯들"""
        # 접두사/접미사
        prefix_frame = ttk.Frame(parent)
        prefix_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(prefix_frame, text="접두사:", width=8).pack(side=tk.LEFT)
        self.prefix_var = tk.StringVar()
        ttk.Entry(prefix_frame, textvariable=self.prefix_var, width=20).pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(prefix_frame, text="접미사:", width=8).pack(side=tk.LEFT)
        self.suffix_var = tk.StringVar()
        ttk.Entry(prefix_frame, textvariable=self.suffix_var, width=20).pack(side=tk.LEFT, padx=(5, 0))
        
        # 찾기/바꾸기
        replace_frame = ttk.Frame(parent)
        replace_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(replace_frame, text="찾기:", width=8).pack(side=tk.LEFT)
        self.find_var = tk.StringVar()
        ttk.Entry(replace_frame, textvariable=self.find_var, width=20).pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(replace_frame, text="바꾸기:", width=8).pack(side=tk.LEFT)
        self.replace_var = tk.StringVar()
        ttk.Entry(replace_frame, textvariable=self.replace_var, width=20).pack(side=tk.LEFT, padx=(5, 0))
        
        # 정규표현식 옵션
        self.use_regex_var = tk.BooleanVar()
        ttk.Checkbutton(replace_frame, text="정규식", 
                       variable=self.use_regex_var).pack(side=tk.RIGHT)
        
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
        sort_combo.pack(side=tk.LEFT, padx=(5, 0))
        sort_combo.bind('<<ComboboxSelected>>', self.on_sort_change)
        
        # 미리보기 테이블
        tree_frame = ttk.Frame(preview_group)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        columns = ("순번", "원본 파일명", "새 파일명", "상태")
        self.preview_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        # 컬럼 설정
        self.preview_tree.heading("순번", text="#")
        self.preview_tree.heading("원본 파일명", text="원본 파일명")
        self.preview_tree.heading("새 파일명", text="새 파일명")
        self.preview_tree.heading("상태", text="상태")
        
        self.preview_tree.column("순번", width=50, anchor=tk.CENTER)
        self.preview_tree.column("원본 파일명", width=200)
        self.preview_tree.column("새 파일명", width=200)
        self.preview_tree.column("상태", width=100, anchor=tk.CENTER)
        
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
        
        # 파일 통계
        self.file_stats_var = tk.StringVar(value="")
        ttk.Label(statusbar, textvariable=self.file_stats_var).pack(side=tk.RIGHT)
    
    def setup_drag_drop(self):
        """드래그 앤 드롭 설정"""
        if DND_AVAILABLE:
            self.drop_label.drop_target_register(DND_FILES)
            self.drop_label.dnd_bind('<<Drop>>', self.on_drop)
            
            # 메인 윈도우에도 드롭 기능 추가
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_drop)
    
    def on_drop(self, event):
        """드롭 이벤트 처리"""
        try:
            files = self.parse_drop_files(event.data)
            if files:
                added = self.engine.add_files(files)
                self.status_var.set(f"{added}개 파일이 추가되었습니다")
        except Exception as e:
            self.status_var.set(f"드롭 오류: {str(e)}")
    
    def parse_drop_files(self, data):
        """드롭된 파일 데이터 파싱"""
        files = []
        try:
            # tkinterdnd2 데이터 파싱
            raw_files = self.root.tk.splitlist(data)
            for file_path in raw_files:
                # 중괄호 제거
                if file_path.startswith('{') and file_path.endswith('}'):
                    file_path = file_path[1:-1]
                
                if os.path.exists(file_path):
                    if os.path.isfile(file_path):
                        files.append(file_path)
                    elif os.path.isdir(file_path):
                        # 폴더인 경우 내부 파일들 추가
                        for item in os.listdir(file_path):
                            item_path = os.path.join(file_path, item)
                            if os.path.isfile(item_path):
                                files.append(item_path)
        except Exception:
            pass
        
        return files
    
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
        self.use_regex_var.trace('w', self.on_option_change)
        self.use_numbering_var.trace('w', self.on_option_change)
        self.number_start_var.trace('w', self.on_option_change)
        self.number_digits_var.trace('w', self.on_option_change)
        
        # 검색 이벤트
        self.search_var.trace('w', self.on_search_change)
        
        # 리스트박스 선택 변경
        self.files_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        # 더블클릭으로 파일 열기
        self.preview_tree.bind('<Double-1>', self.on_preview_double_click)
    
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
        # 정규표현식 모드에서는 특별 처리
        if self.use_regex_var.get():
            # 정규표현식은 엔진에서 직접 처리하지 않고 여기서 처리
            pass
        else:
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
        # 실시간 검색 적용
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
    
    def on_preview_double_click(self, event):
        """미리보기 더블클릭 시 파일 탐색기에서 열기"""
        selection = self.preview_tree.selection()
        if selection:
            item = self.preview_tree.item(selection[0])
            values = item['values']
            if values and len(values) > 0 and values[0]:
                try:
                    file_num = int(values[0]) - 1
                    if 0 <= file_num < len(self.engine.files):
                        file_path = self.engine.files[file_num]
                        os.startfile(os.path.dirname(file_path))
                except (ValueError, IndexError):
                    pass
    
    def on_preview_filter_change(self, event=None):
        """미리보기 필터 변경"""
        self.update_preview()
    
    def on_sort_change(self, event=None):
        """정렬 변경"""
        self.update_preview()
    
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
            else:
                messagebox.showinfo("정보", "선택한 폴더에 파일이 없습니다.")
                
        except Exception as e:
            messagebox.showerror("오류", f"폴더 읽기 실패: {str(e)}")
    
    def remove_selected(self):
        """선택된 파일들 제거"""
        selected = self.files_listbox.curselection()
        if not selected:
            messagebox.showwarning("경고", "제거할 파일을 선택하세요.")
            return
        
        removed = self.engine.remove_files_by_indices(list(selected))
        self.status_var.set(f"{removed}개 파일이 제거되었습니다")
    
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
    
    def clear_all(self):
        """모든 파일 삭제"""
        if self.engine.get_file_count() > 0:
            if messagebox.askyesno("확인", "모든 파일을 목록에서 제거하시겠습니까?"):
                self.engine.clear_files()
                self.status_var.set("모든 파일이 제거되었습니다")
    
    def reset_options(self):
        """옵션 초기화"""
        self.engine.reset_options()
        # GUI 변수들도 초기화
        self.prefix_var.set("")
        self.suffix_var.set("")
        self.find_var.set("")
        self.replace_var.set("")
        self.use_regex_var.set(False)
        self.use_numbering_var.set(False)
        self.number_start_var.set(1)
        self.number_digits_var.set(3)
        
        self.status_var.set("옵션이 초기화되었습니다")
    
    # 고급 파일명 생성 (정규표현식 지원)
    def generate_new_name_advanced(self, original_filename: str, file_index: int = 0) -> str:
        """고급 파일명 생성 (정규표현식 지원)"""
        name, ext = os.path.splitext(original_filename)
        
        # 1단계: 찾기/바꾸기 적용 (정규표현식 지원)
        find_text = self.find_var.get()
        replace_text = self.replace_var.get()
        
        if find_text:
            try:
                if self.use_regex_var.get():
                    # 정규표현식 모드
                    name = re.sub(find_text, replace_text, name)
                else:
                    # 일반 텍스트 모드
                    name = name.replace(find_text, replace_text)
            except re.error:
                # 정규표현식 오류 시 원본 유지
                pass
        
        # 2단계: 순번 매기기 적용
        if self.use_numbering_var.get():
            number = str(self.number_start_var.get() + file_index).zfill(self.number_digits_var.get())
            name = f"{name}_{number}"
        
        # 3단계: 접두사/접미사 추가
        prefix = self.prefix_var.get()
        suffix = self.suffix_var.get()
        new_name = f"{prefix}{name}{suffix}{ext}"
        
        return new_name
    
    # 미리보기 및 UI 업데이트
    def update_file_list(self):
        """파일 목록 업데이트 (검색 필터 적용)"""
        self.files_listbox.delete(0, tk.END)
        
        displayed_count = 0
        for file_path in self.engine.files:
            filename = os.path.basename(file_path)
            
            # 검색 필터 적용
            if self.search_text and self.search_text not in filename.lower():
                continue
            
            self.files_listbox.insert(tk.END, filename)
            displayed_count += 1
        
        total_count = self.engine.get_file_count()
        if self.search_text:
            self.file_count_var.set(f"파일 개수: {displayed_count}/{total_count} (검색 결과)")
        else:
            self.file_count_var.set(f"파일 개수: {total_count}")
    
    def update_preview(self):
        """미리보기 업데이트 (고급 필터링 및 정렬 지원)"""
        # 기존 항목 제거
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        if self.engine.get_file_count() == 0:
            self.preview_tree.insert("", tk.END, values=(
                "", "파일을 추가하세요", "", ""
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
        # "순서"는 기본 순서 유지
        
        # 테이블에 추가
        for item in preview_data:
            self.preview_tree.insert("", tk.END, values=(
                item['index'], item['original'], item['new'], item['status']
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
    
    def execute_rename(self):
        """파일명 변경 실행"""
        if self.engine.get_file_count() == 0:
            messagebox.showwarning("경고", "변경할 파일이 없습니다.")
            return
        
        # 변경 계획 생성 (고급 모드 사용)
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
        
        # 실행
        self.status_var.set("파일명 변경 중...")
        self.root.update()
        
        try:
            success_count = 0
            errors = []
            
            for old_path, new_path in rename_plan:
                try:
                    os.rename(old_path, new_path)
                    
                    # 내부 파일 목록 업데이트
                    index = self.engine.files.index(old_path)
                    self.engine.files[index] = new_path
                    success_count += 1
                    
                except Exception as e:
                    errors.append(f"{os.path.basename(old_path)}: {str(e)}")
            
            # 결과 메시지
            message = f"✅ 성공: {success_count}개 파일 변경됨"
            if errors:
                message += f"\n❌ 실패: {len(errors)}개 파일"
                if len(errors) <= 3:
                    message += "\n" + "\n".join(errors)
            
            messagebox.showinfo("작업 완료", message)
            self.status_var.set(f"완료: {success_count}개 파일 변경됨")
            
            # UI 업데이트
            self.engine._notify_files_changed()
            
        except Exception as e:
            messagebox.showerror("오류", f"파일명 변경 중 오류 발생: {str(e)}")
            self.status_var.set("오류 발생")
    
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()

if __name__ == "__main__":
    app = RealTimePreviewRenamer()
    app.run()