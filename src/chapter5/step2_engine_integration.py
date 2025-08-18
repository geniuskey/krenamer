import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from rename_engine import RenameEngine

class TwoPanelRenamer:
    """2-패널 레이아웃 기본 구조"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KRenamer v5.0 - 2-패널 레이아웃")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # 엔진 초기화
        self.engine = RenameEngine()
        self.engine.on_files_changed = self.on_files_changed
        self.engine.on_options_changed = self.on_options_changed
        
        self.create_widgets()
        self.create_variables()
        self.bind_events()
    
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
        
        # 작업 버튼들
        ttk.Button(toolbar, text="🔄 미리보기 새로고침", 
                  command=self.refresh_preview).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="✅ 이름 변경 실행", 
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
        paned.add(left_panel, weight=1)
        
        # 오른쪽 패널 (미리보기)
        right_panel = ttk.Frame(paned)
        paned.add(right_panel, weight=1)
        
        self.create_left_panel(left_panel)
        self.create_right_panel(right_panel)
    
    def create_left_panel(self, parent):
        """왼쪽 패널 - 파일 관리와 옵션"""
        # 파일 목록 섹션
        files_group = ttk.LabelFrame(parent, text="파일 목록", padding="10")
        files_group.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
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
        
        # 미리보기 테이블
        tree_frame = ttk.Frame(preview_group)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
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
        self.preview_tree.column("상태", width=80, anchor=tk.CENTER)
        
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
    
    def create_variables(self):
        """변수 초기화"""
        # 초기 상태 설정
        self.update_file_list()
        self.update_preview()
    
    def bind_events(self):
        """이벤트 바인딩"""
        # 옵션 변경 감지
        self.prefix_var.trace('w', self.on_option_change)
        self.suffix_var.trace('w', self.on_option_change)
        self.find_var.trace('w', self.on_option_change)
        self.replace_var.trace('w', self.on_option_change)
        self.use_numbering_var.trace('w', self.on_option_change)
        self.number_start_var.trace('w', self.on_option_change)
        self.number_digits_var.trace('w', self.on_option_change)
        
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
        self.engine.set_prefix(self.prefix_var.get())
        self.engine.set_suffix(self.suffix_var.get())
        self.engine.set_find_replace(self.find_var.get(), self.replace_var.get())
        self.engine.set_numbering(
            self.use_numbering_var.get(),
            self.number_start_var.get(),
            self.number_digits_var.get()
        )
    
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
            file_num = int(item['values'][0]) - 1
            if 0 <= file_num < len(self.engine.files):
                file_path = self.engine.files[file_num]
                os.startfile(os.path.dirname(file_path))
    
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
        
        # 단순 구현: 첫 번째 선택된 파일만 이동
        index = selected[0]
        file_path = self.engine.files.pop(index)
        self.engine.files.insert(index - 1, file_path)
        
        self.engine._notify_files_changed()
        # 선택 상태 유지
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
        # 선택 상태 유지
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
        self.use_numbering_var.set(False)
        self.number_start_var.set(1)
        self.number_digits_var.set(3)
        
        self.status_var.set("옵션이 초기화되었습니다")
    
    # 미리보기 및 UI 업데이트
    def update_file_list(self):
        """파일 목록 업데이트"""
        self.files_listbox.delete(0, tk.END)
        
        for file_path in self.engine.files:
            filename = os.path.basename(file_path)
            self.files_listbox.insert(tk.END, filename)
        
        self.file_count_var.set(f"파일 개수: {self.engine.get_file_count()}")
    
    def update_preview(self):
        """미리보기 업데이트"""
        # 기존 항목 제거
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        if self.engine.get_file_count() == 0:
            self.preview_tree.insert("", tk.END, values=(
                "", "파일을 추가하세요", "", ""
            ))
            self.preview_stats_var.set("변경 예정: 0개, 오류: 0개")
            return
        
        preview = self.engine.generate_preview()
        valid_count = 0
        error_count = 0
        
        for i, (original, new, is_valid, error_msg) in enumerate(preview):
            if is_valid:
                status = "✅ 유효"
                valid_count += 1
                # 색상 태그 (나중에 추가)
                tags = ("valid",)
            else:
                status = f"❌ {error_msg}"
                error_count += 1
                tags = ("error",)
            
            self.preview_tree.insert("", tk.END, values=(
                i + 1, original, new, status
            ), tags=tags)
        
        # 색상 설정
        self.preview_tree.tag_configure("valid", foreground="darkgreen")
        self.preview_tree.tag_configure("error", foreground="red")
        
        self.preview_stats_var.set(f"변경 예정: {valid_count}개, 오류: {error_count}개")
    
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
        
        # 미리보기에서 유효한 변경사항 확인
        preview = self.engine.generate_preview()
        valid_changes = sum(1 for _, _, is_valid, _ in preview if is_valid)
        
        if valid_changes == 0:
            messagebox.showwarning("경고", "변경할 수 있는 파일이 없습니다.")
            return
        
        # 확인 대화상자
        if not messagebox.askyesno("확인", 
                                  f"{valid_changes}개 파일의 이름을 변경하시겠습니까?"):
            return
        
        # 실행
        self.status_var.set("파일명 변경 중...")
        self.root.update()  # UI 즉시 업데이트
        
        try:
            results = self.engine.execute_rename()
            
            # 결과 메시지
            message = f"✅ 성공: {results['success']}개 파일 변경됨"
            if results['failed'] > 0:
                message += f"\n❌ 실패: {results['failed']}개 파일"
                if results['errors']:
                    message += f"\n\n첫 번째 오류: {results['errors'][0]}"
            
            messagebox.showinfo("작업 완료", message)
            self.status_var.set(f"완료: {results['success']}개 파일 변경됨")
            
        except Exception as e:
            messagebox.showerror("오류", f"파일명 변경 중 오류 발생: {str(e)}")
            self.status_var.set("오류 발생")
    
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()

if __name__ == "__main__":
    app = TwoPanelRenamer()
    app.run()