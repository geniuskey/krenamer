import tkinter as tk
from tkinter import messagebox

class FileListManager:
    """파일 목록을 관리하는 클래스"""
    
    def __init__(self):
        self.files = []  # 파일 목록 저장
        
    def add_file(self, filename):
        """파일 추가"""
        if filename and filename not in self.files:
            self.files.append(filename)
            return True
        return False
    
    def remove_file(self, filename):
        """파일 제거"""
        if filename in self.files:
            self.files.remove(filename)
            return True
        return False
    
    def get_file_count(self):
        """총 파일 개수 반환"""
        return len(self.files)

# 전역 변수
file_manager = FileListManager()

def add_file_to_list():
    """파일을 목록에 추가하는 함수"""
    filename = file_entry.get().strip()
    
    if not filename:
        messagebox.showwarning("입력 오류", "파일명을 입력해주세요!")
        return
    
    if file_manager.add_file(filename):
        # 리스트박스에 추가
        file_listbox.insert(tk.END, filename)
        file_entry.delete(0, tk.END)  # 입력창 초기화
        update_status()
        print(f"✅ '{filename}' 파일이 추가되었습니다.")
    else:
        messagebox.showinfo("중복 파일", "이미 존재하는 파일명입니다!")

def remove_selected_file():
    """선택된 파일을 목록에서 제거"""
    try:
        selected_index = file_listbox.curselection()[0]  # 선택된 항목의 인덱스
        selected_file = file_listbox.get(selected_index)  # 선택된 파일명
        
        # 파일 매니저에서 제거
        if file_manager.remove_file(selected_file):
            file_listbox.delete(selected_index)  # 리스트박스에서 제거
            update_status()
            print(f"🗑️ '{selected_file}' 파일이 제거되었습니다.")
        
    except IndexError:
        messagebox.showwarning("선택 오류", "제거할 파일을 선택해주세요!")

def clear_all_files():
    """모든 파일 제거"""
    if file_manager.get_file_count() == 0:
        messagebox.showinfo("알림", "제거할 파일이 없습니다!")
        return
    
    # 확인 대화상자
    result = messagebox.askyesno("확인", "정말로 모든 파일을 제거하시겠습니까?")
    if result:
        file_manager.files.clear()
        file_listbox.delete(0, tk.END)
        update_status()
        print("🧹 모든 파일이 제거되었습니다.")

def update_status():
    """상태 표시줄 업데이트"""
    count = file_manager.get_file_count()
    status_label.config(text=f"총 {count}개의 파일이 관리되고 있습니다.")

def show_file_info():
    """선택된 파일의 정보 표시"""
    try:
        selected_index = file_listbox.curselection()[0]
        selected_file = file_listbox.get(selected_index)
        
        from pathlib import Path
        file_path = Path(selected_file)
        
        info = f"""📁 파일 정보:

📄 파일명: {selected_file}
📝 이름: {file_path.stem}
📎 확장자: {file_path.suffix}
📏 길이: {len(selected_file)}글자
📍 목록 위치: {selected_index + 1}번째
"""
        messagebox.showinfo("파일 정보", info)
        
    except IndexError:
        messagebox.showwarning("선택 오류", "정보를 볼 파일을 선택해주세요!")

# 메인 창 설정
root = tk.Tk()
root.title("파일 목록 관리자")
root.geometry("700x600")
root.configure(bg="white")

# 제목
title_label = tk.Label(
    root,
    text="📋 파일 목록 관리자",
    font=("맑은 고딕", 18, "bold"),
    bg="white",
    fg="darkgreen"
)
title_label.pack(pady=15)

# 파일 추가 섹션
add_frame = tk.Frame(root, bg="white")
add_frame.pack(pady=10)

tk.Label(
    add_frame,
    text="추가할 파일명:",
    font=("맑은 고딕", 12),
    bg="white"
).pack(side=tk.LEFT)

file_entry = tk.Entry(
    add_frame,
    font=("맑은 고딕", 12),
    width=30
)
file_entry.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(
    add_frame,
    text="추가 ➕",
    command=add_file_to_list,
    font=("맑은 고딕", 11),
    bg="lightgreen"
)
add_button.pack(side=tk.LEFT, padx=5)

# 파일 목록 표시 섹션
list_frame = tk.Frame(root, bg="white")
list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

tk.Label(
    list_frame,
    text="📂 파일 목록:",
    font=("맑은 고딕", 12, "bold"),
    bg="white"
).pack(anchor=tk.W)

# 스크롤바가 있는 리스트박스
scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

file_listbox = tk.Listbox(
    list_frame,
    font=("맑은 고딕", 11),
    height=15,
    yscrollcommand=scrollbar.set
)
file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=file_listbox.yview)

# 버튼 섹션
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=10)

remove_button = tk.Button(
    button_frame,
    text="선택 제거 🗑️",
    command=remove_selected_file,
    font=("맑은 고딕", 11),
    bg="lightcoral"
)
remove_button.pack(side=tk.LEFT, padx=5)

info_button = tk.Button(
    button_frame,
    text="파일 정보 ℹ️",
    command=show_file_info,
    font=("맑은 고딕", 11),
    bg="lightblue"
)
info_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(
    button_frame,
    text="전체 삭제 🧹",
    command=clear_all_files,
    font=("맑은 고딕", 11),
    bg="orange"
)
clear_button.pack(side=tk.LEFT, padx=5)

# 상태 표시줄
status_label = tk.Label(
    root,
    text="파일을 추가해보세요!",
    font=("맑은 고딕", 10),
    bg="lightgray",
    relief=tk.SUNKEN,
    anchor=tk.W
)
status_label.pack(side=tk.BOTTOM, fill=tk.X)

# Enter 키로 파일 추가
file_entry.bind('<Return>', lambda event: add_file_to_list())

print("파일 목록 관리자가 시작됩니다!")
root.mainloop()