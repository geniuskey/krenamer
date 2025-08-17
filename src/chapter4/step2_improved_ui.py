import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime

class ImprovedFileRenamer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("파일 리네이머 v2.0 - 향상된 UI")
        self.root.geometry("700x500")
        
        self.files = []
        self.create_widgets()
        
        # 실시간 미리보기를 위한 이벤트 바인딩
        self.prefix_var.trace('w', self.on_option_change)
        self.suffix_var.trace('w', self.on_option_change)
    
    def create_widgets(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # 제목과 상태 정보
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        ttk.Label(title_frame, text="파일 이름 변경 도구", 
                 font=("맑은 고딕", 16, "bold")).pack(side="left")
        
        # 현재 시간 표시
        self.time_var = tk.StringVar()
        self.update_time()
        ttk.Label(title_frame, textvariable=self.time_var, 
                 font=("맑은 고딕", 9)).pack(side="right")
        
        # 파일 관리 프레임
        file_frame = ttk.LabelFrame(main_frame, text="파일 관리", padding="5")
        file_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # 파일 추가/제거 버튼들
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill="x", pady=(0, 5))
        
        ttk.Button(btn_frame, text="📁 파일 추가", 
                  command=self.select_files).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="📂 폴더 추가", 
                  command=self.select_folder).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="🗑️ 전체 삭제", 
                  command=self.clear_files).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="❌ 선택 삭제", 
                  command=self.remove_selected).pack(side="left")
        
        # 파일 개수 정보
        self.file_count_var = tk.StringVar(value="파일 개수: 0")
        ttk.Label(btn_frame, textvariable=self.file_count_var).pack(side="right")
        
        # 파일 목록 (Treeview 사용)
        tree_frame = ttk.Frame(file_frame)
        tree_frame.pack(fill="both", expand=True)
        
        # Treeview 생성
        columns = ("파일명", "경로", "크기")
        self.file_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        
        # 컬럼 설정
        self.file_tree.heading("파일명", text="파일명")
        self.file_tree.heading("경로", text="경로")
        self.file_tree.heading("크기", text="크기")
        
        self.file_tree.column("파일명", width=200)
        self.file_tree.column("경로", width=300)
        self.file_tree.column("크기", width=80)
        
        # 스크롤바
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.file_tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")
        
        # 옵션 프레임
        option_frame = ttk.LabelFrame(main_frame, text="이름 변경 옵션", padding="10")
        option_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # 접두사
        ttk.Label(option_frame, text="접두사:").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.prefix_var = tk.StringVar()
        ttk.Entry(option_frame, textvariable=self.prefix_var, width=30).grid(row=0, column=1, sticky="w", padx=(0, 20))
        
        # 접미사  
        ttk.Label(option_frame, text="접미사:").grid(row=0, column=2, sticky="w", padx=(0, 5))
        self.suffix_var = tk.StringVar()
        ttk.Entry(option_frame, textvariable=self.suffix_var, width=30).grid(row=0, column=3, sticky="w")
        
        # 미리보기 프레임
        preview_frame = ttk.LabelFrame(main_frame, text="미리보기", padding="5")
        preview_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # 미리보기 텍스트
        self.preview_text = tk.Text(preview_frame, height=6, wrap="none")
        preview_scroll = ttk.Scrollbar(preview_frame, orient="vertical", command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scroll.set)
        
        self.preview_text.pack(side="left", fill="both", expand=True)
        preview_scroll.pack(side="right", fill="y")
        
        # 실행 버튼 프레임
        exec_frame = ttk.Frame(main_frame)
        exec_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(exec_frame, text="🔄 미리보기 새로고침", 
                  command=self.update_preview).pack(side="left", padx=(0, 10))
        ttk.Button(exec_frame, text="✅ 이름 변경 실행", 
                  command=self.execute_rename).pack(side="right")
        
        # 그리드 가중치 설정
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
    
    def update_time(self):
        """현재 시간 업데이트"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_var.set(current_time)
        self.root.after(1000, self.update_time)  # 1초마다 업데이트
    
    def select_files(self):
        """개별 파일 선택"""
        files = filedialog.askopenfilenames(
            title="이름을 변경할 파일들을 선택하세요",
            filetypes=[("모든 파일", "*.*"), ("이미지 파일", "*.jpg;*.png;*.gif"), 
                      ("문서 파일", "*.txt;*.doc;*.pdf")]
        )
        
        for file_path in files:
            if file_path not in self.files:
                self.files.append(file_path)
        
        self.update_file_display()
    
    def select_folder(self):
        """폴더 내 모든 파일 선택"""
        folder_path = filedialog.askdirectory(title="폴더를 선택하세요")
        if not folder_path:
            return
        
        try:
            for item in os.listdir(folder_path):
                file_path = os.path.join(folder_path, item)
                if os.path.isfile(file_path) and file_path not in self.files:
                    self.files.append(file_path)
            
            self.update_file_display()
            messagebox.showinfo("완료", f"{folder_path}의 파일들을 추가했습니다.")
            
        except Exception as e:
            messagebox.showerror("오류", f"폴더 읽기 실패: {str(e)}")
    
    def update_file_display(self):
        """파일 목록 화면 업데이트"""
        # 기존 항목 삭제
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # 새 파일 목록 추가
        for file_path in self.files:
            filename = os.path.basename(file_path)
            directory = os.path.dirname(file_path)
            
            # 파일 크기 계산
            try:
                size = os.path.getsize(file_path)
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024*1024:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/(1024*1024):.1f} MB"
            except:
                size_str = "?"
            
            self.file_tree.insert("", "end", values=(filename, directory, size_str))
        
        # 파일 개수 업데이트
        self.file_count_var.set(f"파일 개수: {len(self.files)}")
        
        # 미리보기 업데이트
        self.update_preview()
    
    def remove_selected(self):
        """선택된 파일 제거"""
        selected_items = self.file_tree.selection()
        if not selected_items:
            messagebox.showwarning("경고", "제거할 파일을 선택하세요.")
            return
        
        for item in selected_items:
            values = self.file_tree.item(item)['values']
            filename = values[0]
            directory = values[1]
            file_path = os.path.join(directory, filename)
            
            if file_path in self.files:
                self.files.remove(file_path)
        
        self.update_file_display()
    
    def clear_files(self):
        """모든 파일 제거"""
        self.files.clear()
        self.update_file_display()
        self.prefix_var.set("")
        self.suffix_var.set("")
    
    def on_option_change(self, *args):
        """옵션 변경 시 자동 미리보기 업데이트"""
        self.update_preview()
    
    def update_preview(self):
        """미리보기 업데이트"""
        self.preview_text.delete("1.0", tk.END)
        
        if not self.files:
            self.preview_text.insert("1.0", "파일이 선택되지 않았습니다.")
            return
        
        prefix = self.prefix_var.get()
        suffix = self.suffix_var.get()
        
        if not prefix and not suffix:
            self.preview_text.insert("1.0", "접두사나 접미사를 입력하세요.")
            return
        
        preview_content = "변경 미리보기:\n" + "="*60 + "\n"
        
        for file_path in self.files:
            old_name = os.path.basename(file_path)
            name, ext = os.path.splitext(old_name)
            new_name = f"{prefix}{name}{suffix}{ext}"
            
            preview_content += f"{old_name:30} → {new_name}\n"
        
        self.preview_text.insert("1.0", preview_content)
    
    def execute_rename(self):
        """이름 변경 실행"""
        if not self.files:
            messagebox.showwarning("경고", "선택된 파일이 없습니다.")
            return
        
        prefix = self.prefix_var.get()
        suffix = self.suffix_var.get()
        
        if not prefix and not suffix:
            messagebox.showwarning("경고", "접두사나 접미사를 입력하세요.")
            return
        
        # 확인 메시지
        if not messagebox.askyesno("확인", 
                                  f"{len(self.files)}개 파일의 이름을 변경하시겠습니까?"):
            return
        
        success_count = 0
        errors = []
        
        for file_path in self.files[:]:
            try:
                directory = os.path.dirname(file_path)
                old_name = os.path.basename(file_path)
                name, ext = os.path.splitext(old_name)
                new_name = f"{prefix}{name}{suffix}{ext}"
                new_path = os.path.join(directory, new_name)
                
                if old_name == new_name:
                    continue
                
                if os.path.exists(new_path):
                    errors.append(f"{old_name}: 대상 파일이 이미 존재")
                    continue
                
                os.rename(file_path, new_path)
                index = self.files.index(file_path)
                self.files[index] = new_path
                success_count += 1
                
            except Exception as e:
                errors.append(f"{os.path.basename(file_path)}: {str(e)}")
        
        # 결과 보고
        result_msg = f"✅ 성공: {success_count}개 파일 변경됨"
        if errors:
            result_msg += f"\n❌ 실패: {len(errors)}개"
            if len(errors) <= 5:
                result_msg += "\n\n세부 오류:\n" + "\n".join(errors)
        
        messagebox.showinfo("작업 완료", result_msg)
        self.update_file_display()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImprovedFileRenamer()
    app.run()