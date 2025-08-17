import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class BasicFileRenamer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("파일 리네이머 v1.0")
        self.root.geometry("600x400")
        
        # Chapter 3에서 사용한 변수들
        self.files = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # 제목
        title_label = ttk.Label(self.root, text="파일 이름 변경 도구", 
                               font=("맑은 고딕", 16, "bold"))
        title_label.pack(pady=10)
        
        # 파일 추가 버튼
        ttk.Button(self.root, text="파일 선택", 
                  command=self.select_files).pack(pady=5)
        
        # 파일 목록 표시 (간단한 리스트박스)
        self.file_listbox = tk.Listbox(self.root, height=8)
        self.file_listbox.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 옵션 프레임
        option_frame = ttk.Frame(self.root)
        option_frame.pack(fill="x", padx=20, pady=5)
        
        # 접두사 입력
        ttk.Label(option_frame, text="접두사:").grid(row=0, column=0, sticky="w")
        self.prefix_var = tk.StringVar()
        self.prefix_entry = ttk.Entry(option_frame, textvariable=self.prefix_var, width=20)
        self.prefix_entry.grid(row=0, column=1, padx=5)
        
        # 버튼 프레임
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="미리보기", 
                  command=self.preview_changes).pack(side="left", padx=5)
        ttk.Button(button_frame, text="실행", 
                  command=self.execute_rename).pack(side="left", padx=5)
        ttk.Button(button_frame, text="초기화", 
                  command=self.clear_files).pack(side="left", padx=5)
    
    def select_files(self):
        """파일 선택 다이얼로그"""
        files = filedialog.askopenfilenames(
            title="이름을 변경할 파일들을 선택하세요",
            filetypes=[("모든 파일", "*.*")]
        )
        
        for file_path in files:
            if file_path not in self.files:
                self.files.append(file_path)
        
        self.update_file_list()
    
    def update_file_list(self):
        """파일 목록 업데이트"""
        self.file_listbox.delete(0, tk.END)
        for file_path in self.files:
            filename = os.path.basename(file_path)
            self.file_listbox.insert(tk.END, filename)
    
    def preview_changes(self):
        """Chapter 3의 미리보기 기능을 GUI로"""
        if not self.files:
            messagebox.showwarning("경고", "선택된 파일이 없습니다.")
            return
        
        prefix = self.prefix_var.get().strip()
        if not prefix:
            messagebox.showwarning("경고", "접두사를 입력하세요.")
            return
        
        # 미리보기 창 생성
        preview_window = tk.Toplevel(self.root)
        preview_window.title("미리보기")
        preview_window.geometry("500x400")
        
        # 미리보기 텍스트 표시
        text_widget = tk.Text(preview_window, wrap="none")
        scrollbar = ttk.Scrollbar(preview_window, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        preview_content = "변경 예정:\n" + "="*50 + "\n"
        
        for file_path in self.files:
            old_name = os.path.basename(file_path)
            name, ext = os.path.splitext(old_name)
            new_name = f"{prefix}{name}{ext}"
            preview_content += f"{old_name} → {new_name}\n"
        
        text_widget.insert("1.0", preview_content)
        text_widget.configure(state="disabled")
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def execute_rename(self):
        """Chapter 3의 실행 로직을 GUI로"""
        if not self.files:
            messagebox.showwarning("경고", "선택된 파일이 없습니다.")
            return
        
        prefix = self.prefix_var.get().strip()
        if not prefix:
            messagebox.showwarning("경고", "접두사를 입력하세요.")
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
                new_name = f"{prefix}{name}{ext}"
                new_path = os.path.join(directory, new_name)
                
                if old_name == new_name:
                    continue  # 변경할 필요 없음
                
                if os.path.exists(new_path):
                    errors.append(f"{old_name}: 대상 파일이 이미 존재")
                    continue
                
                os.rename(file_path, new_path)
                # 목록에서 경로 업데이트
                index = self.files.index(file_path)
                self.files[index] = new_path
                success_count += 1
                
            except Exception as e:
                errors.append(f"{os.path.basename(file_path)}: {str(e)}")
        
        # 결과 보고
        result_msg = f"성공: {success_count}개 파일 변경됨"
        if errors:
            result_msg += f"\n실패: {len(errors)}개"
            if len(errors) <= 5:  # 오류가 적으면 모두 표시
                result_msg += "\n" + "\n".join(errors)
        
        messagebox.showinfo("작업 완료", result_msg)
        self.update_file_list()
    
    def clear_files(self):
        """파일 목록 초기화"""
        self.files.clear()
        self.update_file_list()
        self.prefix_var.set("")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BasicFileRenamer()
    app.run()