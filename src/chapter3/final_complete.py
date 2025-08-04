# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

class KRenamer:
    """KRenamer 메인 애플리케이션 클래스"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.files = []  # 파일 목록
        
        # UI 구성 (단계별로 구성)
        self.setup_window()
        self.setup_title()
        self.setup_file_list()
        self.setup_buttons()
        self.setup_statusbar()
        
        print("🎉 KRenamer 기본 구조가 완성되었습니다!")
    
    def setup_window(self):
        """창 기본 설정"""
        self.root.title("KRenamer - 파일명 변경 도구")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        self.root.minsize(500, 400)
        self.center_window()
    
    def center_window(self):
        """창을 화면 중앙에 배치"""
        self.root.update_idletasks()
        width = 600
        height = 500
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_title(self):
        """제목 영역 구성"""
        # 메인 제목
        title_label = tk.Label(
            self.root,
            text="📁 KRenamer",
            font=("맑은 고딕", 20, "bold"),
            fg="darkblue",
            bg="lightblue",
            height=2
        )
        title_label.pack(fill=tk.X, padx=10, pady=10)
        
        # 설명
        desc_label = tk.Label(
            self.root,
            text="여러 파일의 이름을 한 번에 쉽게 바꿀 수 있는 도구입니다.",
            font=("맑은 고딕", 11),
            fg="gray"
        )
        desc_label.pack(pady=(0, 10))
    
    def setup_file_list(self):
        """파일 목록 영역 구성"""
        # 파일 목록 Frame
        file_frame = tk.LabelFrame(
            self.root,
            text="📂 파일 목록",
            font=("맑은 고딕", 12, "bold"),
            padx=10,
            pady=10
        )
        file_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # 파일 개수 표시
        self.file_count_var = tk.StringVar()
        self.update_file_count()
        
        count_label = tk.Label(
            file_frame,
            textvariable=self.file_count_var,
            font=("맑은 고딕", 10),
            fg="blue"
        )
        count_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Listbox와 Scrollbar
        listbox_frame = tk.Frame(file_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.file_listbox = tk.Listbox(
            listbox_frame,
            font=("맑은 고딕", 11),
            height=15,
            selectmode=tk.EXTENDED
        )
        
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.file_listbox.yview)
        
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 초기 안내 메시지
        self.show_empty_message()
    
    def setup_buttons(self):
        """버튼 영역 구성"""
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 파일 추가 버튼
        add_button = tk.Button(
            button_frame,
            text="📁 파일 추가",
            font=("맑은 고딕", 11),
            bg="lightgreen",
            width=12,
            command=self.add_files
        )
        add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 파일 제거 버튼
        self.remove_button = tk.Button(
            button_frame,
            text="🗑️ 파일 제거",
            font=("맑은 고딕", 11),
            bg="lightcoral",
            width=12,
            command=self.remove_files,
            state=tk.DISABLED
        )
        self.remove_button.pack(side=tk.LEFT, padx=5)
        
        # 전체 지우기 버튼
        self.clear_button = tk.Button(
            button_frame,
            text="🧹 모두 지우기",
            font=("맑은 고딕", 11),
            bg="orange",
            width=12,
            command=self.clear_files,
            state=tk.DISABLED
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # 이름 변경 버튼
        self.rename_button = tk.Button(
            button_frame,
            text="✨ 이름 변경",
            font=("맑은 고딕", 11, "bold"),
            bg="lightblue",
            width=12,
            command=self.rename_files,
            state=tk.DISABLED
        )
        self.rename_button.pack(side=tk.RIGHT)
    
    def setup_statusbar(self):
        """상태바 구성"""
        status_frame = tk.Frame(self.root, relief=tk.SUNKEN, bd=1)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 상태 메시지
        self.status_var = tk.StringVar()
        self.status_var.set("KRenamer에 오신 것을 환영합니다! 파일을 추가해보세요.")
        
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("맑은 고딕", 10),
            anchor=tk.W,
            padx=10
        )
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 파일 개수
        self.count_status_var = tk.StringVar()
        self.update_count_status()
        
        count_status_label = tk.Label(
            status_frame,
            textvariable=self.count_status_var,
            font=("맑은 고딕", 10),
            fg="blue",
            padx=10
        )
        count_status_label.pack(side=tk.RIGHT)
    
    def add_files(self):
        """파일 추가 기능"""
        example_files = [
            "📄 회의록_2024.txt",
            "📷 가족여행_제주도.jpg", 
            "🎵 좋아하는_팝송.mp3",
            "📊 월간보고서_3월.xlsx",
            "🎬 추억의_영화.mp4"
        ]
        
        # 처음 추가하는 경우 안내 메시지 지우기
        if not self.files:
            self.file_listbox.config(state=tk.NORMAL)
            self.file_listbox.delete(0, tk.END)
        
        # 중복되지 않은 파일들만 추가
        added_count = 0
        for file in example_files:
            if file not in self.files:
                self.files.append(file)
                self.file_listbox.insert(tk.END, file)
                added_count += 1
        
        # 상태 업데이트
        self.update_file_count()
        self.update_count_status()
        self.update_button_states()
        
        # 상태 메시지
        if added_count > 0:
            self.status_var.set(f"{added_count}개의 파일이 추가되었습니다!")
            messagebox.showinfo("파일 추가 완료", f"{added_count}개의 예시 파일이 추가되었습니다!")
    
    def remove_files(self):
        """선택된 파일 제거"""
        selection = self.file_listbox.curselection()
        
        if not selection:
            self.status_var.set("제거할 파일을 먼저 선택해주세요.")
            messagebox.showwarning("선택 필요", "제거할 파일을 선택해주세요!")
            return
        
        # 선택된 파일들 제거 (역순으로)
        removed_count = len(selection)
        for index in reversed(selection):
            file_name = self.file_listbox.get(index)
            self.files.remove(file_name)
            self.file_listbox.delete(index)
        
        # 모든 파일이 제거되면 안내 메시지 표시
        if not self.files:
            self.show_empty_message()
        
        # 상태 업데이트
        self.update_file_count()
        self.update_count_status()
        self.update_button_states()
        
        self.status_var.set(f"{removed_count}개의 파일이 제거되었습니다.")
    
    def clear_files(self):
        """모든 파일 제거"""
        if not self.files:
            return
        
        # 확인 대화상자
        result = messagebox.askyesno(
            "전체 삭제 확인", 
            f"정말로 모든 파일({len(self.files)}개)을 목록에서 제거하시겠습니까?"
        )
        
        if result:
            removed_count = len(self.files)
            self.files.clear()
            self.file_listbox.delete(0, tk.END)
            self.show_empty_message()
            
            # 상태 업데이트
            self.update_file_count()
            self.update_count_status()
            self.update_button_states()
            
            self.status_var.set("모든 파일이 목록에서 제거되었습니다.")
    
    def rename_files(self):
        """이름 변경 기능 (미래 구현)"""
        messagebox.showinfo(
            "준비 중", 
            "파일 이름 변경 기능은 다음 챕터에서 구현됩니다!"
        )
    
    def update_file_count(self):
        """파일 개수 표시 업데이트"""
        count = len(self.files)
        if count == 0:
            self.file_count_var.set("파일이 없습니다. 파일을 추가해보세요!")
        else:
            self.file_count_var.set(f"총 {count}개의 파일")
    
    def update_count_status(self):
        """상태바 파일 개수 업데이트"""
        count = len(self.files)
        if count == 0:
            self.count_status_var.set("파일 없음")
        else:
            self.count_status_var.set(f"파일 {count}개")
    
    def update_button_states(self):
        """파일 유무에 따른 버튼 상태 업데이트"""
        has_files = len(self.files) > 0
        state = tk.NORMAL if has_files else tk.DISABLED
        
        self.remove_button.config(state=state)
        self.clear_button.config(state=state)
        self.rename_button.config(state=state)
    
    def show_empty_message(self):
        """빈 목록일 때 안내 메시지 표시"""
        self.file_listbox.insert(tk.END, "")
        self.file_listbox.insert(tk.END, "    📁 파일을 추가해보세요!")
        self.file_listbox.insert(tk.END, "")
        self.file_listbox.insert(tk.END, "    '파일 추가' 버튼을 클릭하세요")
        self.file_listbox.insert(tk.END, "")
        
        # 안내 메시지는 선택되지 않도록
        self.file_listbox.config(state=tk.DISABLED)
    
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()

# 프로그램 실행
if __name__ == "__main__":
    app = KRenamer()
    app.run()