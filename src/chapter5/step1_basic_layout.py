#!/usr/bin/env python3
"""
KRenamer Chapter 5 - Step 1: 기본 2-패널 레이아웃
최종 KRenamer GUI와 유사한 레이아웃으로 구성
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

# tkinterdnd2 선택적 import
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


class KRenamerStep1:
    """Step 1: 기본 2-패널 레이아웃"""
    
    def __init__(self):
        # tkinterdnd2가 사용 가능하면 DnD 윈도우 생성
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
        
        self.files = []
        
        self.setup_window()
        self.setup_widgets()
        self.setup_drag_drop()
    
    def setup_window(self):
        """윈도우 기본 설정"""
        self.root.title("KRenamer - Step 1: 기본 2-패널 레이아웃")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.root.minsize(700, 500)
        
        # 한글 폰트 설정
        try:
            self.root.option_add("*Font", "맑은고딕 9")
        except:
            pass
    
    def setup_widgets(self):
        """GUI 위젯들 설정 및 배치"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 수평 패널 나누기 (왼쪽: 컨트롤, 오른쪽: 미리보기)
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 왼쪽 패널 (컨트롤)
        left_frame = ttk.Frame(paned_window, padding="5")
        paned_window.add(left_frame, weight=1)
        
        # 오른쪽 패널 (미리보기)
        right_frame = ttk.Frame(paned_window, padding="5")
        paned_window.add(right_frame, weight=1)
        
        self.setup_left_panel(left_frame)
        self.setup_right_panel(right_frame)
        self.setup_bottom_buttons(main_frame)
        self.setup_status_bar(main_frame)
        
        self.update_button_states()
    
    def setup_left_panel(self, parent):
        """왼쪽 컨트롤 패널"""
        # 파일 목록 섹션
        files_frame = ttk.LabelFrame(parent, text="파일 목록", padding="10")
        files_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 파일 필터 및 개수
        header_frame = ttk.Frame(files_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="파일 필터:").pack(side=tk.LEFT)
        
        self.filter_var = tk.StringVar(value="모든 파일")
        filter_combo = ttk.Combobox(header_frame, textvariable=self.filter_var, 
                                   values=["모든 파일", "이미지 파일", "문서 파일", "텍스트 파일"], 
                                   width=12, state="readonly")
        filter_combo.pack(side=tk.LEFT, padx=(5, 15))
        
        self.count_var = tk.StringVar(value="파일 개수: 0")
        ttk.Label(header_frame, textvariable=self.count_var, foreground="blue").pack(side=tk.RIGHT)
        
        # 파일 리스트박스
        listbox_frame = ttk.Frame(files_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.files_listbox = tk.Listbox(listbox_frame, height=12, font=("맑은고딕", 9),
                                       selectmode=tk.EXTENDED)
        
        scrollbar_y = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        self.files_listbox.config(yscrollcommand=scrollbar_y.set)
        
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 기본 변경 옵션 섹션
        options_frame = ttk.LabelFrame(parent, text="기본 변경 파일 기법 조건 설정 적용", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 라디오 버튼들
        self.rename_method = tk.StringVar(value="prefix")
        
        radio_frame = ttk.Frame(options_frame)
        radio_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Radiobutton(radio_frame, text="접두사", variable=self.rename_method, 
                       value="prefix", command=self.update_input_fields).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(radio_frame, text="접미사", variable=self.rename_method, 
                       value="suffix", command=self.update_input_fields).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(radio_frame, text="순번", variable=self.rename_method, 
                       value="number", command=self.update_input_fields).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(radio_frame, text="찾기/바꾸기", variable=self.rename_method, 
                       value="replace", command=self.update_input_fields).pack(side=tk.LEFT)
        
        # 동적 입력 필드
        self.input_frame = ttk.Frame(options_frame)
        self.input_frame.pack(fill=tk.X)
        
        self.text_var = tk.StringVar()
        self.find_var = tk.StringVar()
        self.replace_var = tk.StringVar()
        self.start_number_var = tk.StringVar(value="1")
        
        self.setup_input_fields()
        self.update_input_fields()
    
    def setup_input_fields(self):
        """입력 필드 위젯 생성"""
        # 텍스트 입력 (접두사/접미사용)
        self.text_label = ttk.Label(self.input_frame, text="텍스트:")
        self.text_entry = ttk.Entry(self.input_frame, textvariable=self.text_var, width=25)
        
        # 찾기/바꾸기 입력
        self.find_label = ttk.Label(self.input_frame, text="찾을 텍스트:")
        self.find_entry = ttk.Entry(self.input_frame, textvariable=self.find_var, width=25)
        self.replace_label = ttk.Label(self.input_frame, text="바꿀 텍스트:")
        self.replace_entry = ttk.Entry(self.input_frame, textvariable=self.replace_var, width=25)
        
        # 순번 입력
        self.number_label = ttk.Label(self.input_frame, text="시작 번호:")
        self.number_entry = ttk.Entry(self.input_frame, textvariable=self.start_number_var, width=10)
    
    def update_input_fields(self):
        """선택된 방식에 따라 입력 필드 표시"""
        # 모든 위젯 숨기기
        for widget in self.input_frame.winfo_children():
            widget.grid_remove()
        
        method = self.rename_method.get()
        
        if method in ["prefix", "suffix"]:
            self.text_label.grid(row=0, column=0, sticky=tk.W, pady=5)
            self.text_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
            if method == "prefix":
                self.text_label.config(text="접두사 텍스트:")
            else:
                self.text_label.config(text="접미사 텍스트:")
        
        elif method == "number":
            self.number_label.grid(row=0, column=0, sticky=tk.W, pady=5)
            self.number_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        elif method == "replace":
            self.find_label.grid(row=0, column=0, sticky=tk.W, pady=2)
            self.find_entry.grid(row=0, column=1, sticky=tk.W, pady=2, padx=(10, 0))
            self.replace_label.grid(row=1, column=0, sticky=tk.W, pady=2)
            self.replace_entry.grid(row=1, column=1, sticky=tk.W, pady=2, padx=(10, 0))
    
    def setup_right_panel(self, parent):
        """오른쪽 미리보기 패널"""
        preview_frame = ttk.LabelFrame(parent, text="실시간 미리보기", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # 미리보기 테이블
        tree_frame = ttk.Frame(preview_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("number", "original", "new", "status")
        self.preview_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        self.preview_tree.heading("number", text="순번")
        self.preview_tree.heading("original", text="원본 파일명")
        self.preview_tree.heading("new", text="새 파일명")
        self.preview_tree.heading("status", text="상태")
        
        self.preview_tree.column("number", width=50)
        self.preview_tree.column("original", width=200)
        self.preview_tree.column("new", width=200)
        self.preview_tree.column("status", width=60)
        
        # 스크롤바
        preview_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.preview_tree.yview)
        self.preview_tree.config(yscrollcommand=preview_scrollbar.set)
        
        self.preview_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 초기 메시지
        self.preview_tree.insert("", tk.END, values=("", "파일을 추가하고 옵션을 설정하세요", "", ""))
    
    def setup_bottom_buttons(self, parent):
        """하단 버튼들"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(5, 5))
        
        # 파일 관리 버튼들
        self.add_button = ttk.Button(button_frame, text="파일 추가", command=self.add_files, width=12)
        self.add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.remove_button = ttk.Button(button_frame, text="선택 제거", command=self.remove_files, 
                                       width=12, state=tk.DISABLED)
        self.remove_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_button = ttk.Button(button_frame, text="모두 제거", command=self.clear_files, 
                                      width=12, state=tk.DISABLED)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 20))
        
        # 실행 버튼
        self.execute_button = ttk.Button(button_frame, text="실행", command=self.execute_rename, 
                                        width=12, state=tk.DISABLED)
        self.execute_button.pack(side=tk.RIGHT)
    
    def setup_status_bar(self, parent):
        """상태바"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.status_var = tk.StringVar(value="파일을 추가하고 옵션을 설정하세요")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                font=("맑은고딕", 9), foreground="gray")
        status_label.pack(side=tk.LEFT)
    
    def setup_drag_drop(self):
        """드래그 앤 드롭 설정"""
        if DND_AVAILABLE:
            self.files_listbox.drop_target_register(DND_FILES)
            self.files_listbox.dnd_bind('<<Drop>>', self.on_drop)
    
    def on_drop(self, event):
        """드래그 앤 드롭 이벤트 처리"""
        try:
            files = self.parse_drop_data(event.data)
            if files:
                self.add_file_paths(files)
        except Exception as e:
            self.status_var.set(f"드래그 앤 드롭 오류: {e}")
    
    def parse_drop_data(self, data):
        """드롭 데이터 파싱"""
        files = []
        try:
            raw_files = self.root.tk.splitlist(data)
            for file_path in raw_files:
                if file_path.startswith('{') and file_path.endswith('}'):
                    file_path = file_path[1:-1]
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    files.append(file_path)
        except:
            pass
        return files
    
    def add_files(self):
        """파일 선택 대화상자"""
        files = filedialog.askopenfilenames(
            title="파일 선택",
            filetypes=[("모든 파일", "*.*")]
        )
        if files:
            self.add_file_paths(files)
    
    def add_file_paths(self, file_paths):
        """파일 경로 목록 추가"""
        added_count = 0
        for file_path in file_paths:
            if file_path not in self.files:
                self.files.append(file_path)
                filename = os.path.basename(file_path)
                self.files_listbox.insert(tk.END, filename)
                added_count += 1
        
        if added_count > 0:
            self.update_file_count()
            self.update_button_states()
            self.update_preview()
            self.status_var.set(f"{added_count}개 파일이 추가되었습니다")
    
    def remove_files(self):
        """선택된 파일 제거"""
        selection = self.files_listbox.curselection()
        if selection:
            for index in reversed(selection):
                self.files_listbox.delete(index)
                del self.files[index]
            self.update_file_count()
            self.update_button_states()
            self.update_preview()
            self.status_var.set(f"{len(selection)}개 파일이 제거되었습니다")
    
    def clear_files(self):
        """모든 파일 제거"""
        if self.files:
            count = len(self.files)
            self.files.clear()
            self.files_listbox.delete(0, tk.END)
            self.update_file_count()
            self.update_button_states()
            self.update_preview()
            self.status_var.set(f"{count}개 파일이 모두 제거되었습니다")
    
    def update_file_count(self):
        """파일 개수 업데이트"""
        self.count_var.set(f"파일 개수: {len(self.files)}")
    
    def update_button_states(self):
        """버튼 상태 업데이트"""
        has_files = len(self.files) > 0
        state = tk.NORMAL if has_files else tk.DISABLED
        
        self.remove_button.config(state=state)
        self.clear_button.config(state=state)
        self.execute_button.config(state=state)
    
    def generate_new_names(self):
        """새로운 파일명 생성"""
        if not self.files:
            return []
        
        method = self.rename_method.get()
        new_names = []
        
        for i, file_path in enumerate(self.files):
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            
            if method == "prefix":
                prefix = self.text_var.get()
                new_name = f"{prefix}{name}{ext}"
            elif method == "suffix":
                suffix = self.text_var.get()
                new_name = f"{name}{suffix}{ext}"
            elif method == "number":
                try:
                    start_num = int(self.start_number_var.get())
                    number = start_num + i
                    new_name = f"{number:03d}_{name}{ext}"
                except ValueError:
                    new_name = f"{i+1:03d}_{name}{ext}"
            elif method == "replace":
                find_text = self.find_var.get()
                replace_text = self.replace_var.get()
                if find_text:
                    new_name = name.replace(find_text, replace_text) + ext
                else:
                    new_name = filename
            else:
                new_name = filename
            
            new_names.append(new_name)
        
        return new_names
    
    def update_preview(self):
        """미리보기 업데이트"""
        # 기존 항목 제거
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        if not self.files:
            self.preview_tree.insert("", tk.END, values=("", "파일을 추가하고 옵션을 설정하세요", "", ""))
            return
        
        new_names = self.generate_new_names()
        
        for i, (file_path, new_name) in enumerate(zip(self.files, new_names)):
            original_name = os.path.basename(file_path)
            status = "변경" if original_name != new_name else "변경없음"
            
            self.preview_tree.insert("", tk.END, values=(str(i+1), original_name, new_name, status))
    
    def execute_rename(self):
        """파일명 변경 실행"""
        if not self.files:
            return
        
        if not messagebox.askyesno("확인", f"{len(self.files)}개 파일의 이름을 변경하시겠습니까?"):
            return
        
        new_names = self.generate_new_names()
        success_count = 0
        errors = []
        
        for file_path, new_name in zip(self.files, new_names):
            try:
                dir_path = os.path.dirname(file_path)
                new_path = os.path.join(dir_path, new_name)
                
                if file_path != new_path and not os.path.exists(new_path):
                    os.rename(file_path, new_path)
                    success_count += 1
                
            except Exception as e:
                errors.append(f"{os.path.basename(file_path)}: {str(e)}")
        
        if errors:
            messagebox.showwarning("완료", f"{success_count}개 성공, {len(errors)}개 오류")
        else:
            messagebox.showinfo("완료", f"{success_count}개 파일 이름 변경 완료")
        
        # 파일 목록 새로고침
        self.files.clear()
        self.files_listbox.delete(0, tk.END)
        self.update_file_count()
        self.update_button_states()
        self.update_preview()
        
        self.status_var.set(f"이름 변경 완료: {success_count}개 성공")
    
    def run(self):
        """애플리케이션 실행"""
        # 입력 필드 변경시 미리보기 업데이트
        self.text_var.trace_add('write', lambda *args: self.update_preview())
        self.find_var.trace_add('write', lambda *args: self.update_preview())
        self.replace_var.trace_add('write', lambda *args: self.update_preview())
        self.start_number_var.trace_add('write', lambda *args: self.update_preview())
        
        self.root.mainloop()


def main():
    app = KRenamerStep1()
    app.run()


if __name__ == "__main__":
    main()