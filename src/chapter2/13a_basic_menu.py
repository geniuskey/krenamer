import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("기본 메뉴 예제")
root.geometry("500x300")

# 간단한 기능들
def new_document():
    messagebox.showinfo("새 문서", "새 문서를 만듭니다!")

def open_document():
    messagebox.showinfo("열기", "문서를 엽니다!")

def save_document():
    messagebox.showinfo("저장", "문서를 저장합니다!")

def show_about():
    messagebox.showinfo("프로그램 정보", "간단한 메뉴 예제\n버전 1.0")

# 메뉴바 생성 - 이것이 계층의 최상위!
menubar = tk.Menu(root)
root.config(menu=menubar)  # 루트 윈도우에 메뉴바 연결

# 파일 메뉴 만들기
file_menu = tk.Menu(menubar, tearoff=0)  # tearoff=0으로 띄어낼 수 없게 만들기
menubar.add_cascade(label="파일", menu=file_menu)  # 메뉴바에 추가

# 파일 메뉴 항목들
file_menu.add_command(label="새로 만들기", command=new_document)
file_menu.add_command(label="열기...", command=open_document)
file_menu.add_separator()  # 구분선 추가
file_menu.add_command(label="저장", command=save_document)
file_menu.add_separator()
file_menu.add_command(label="종료", command=root.quit)

# 도움말 메뉴
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="도움말", menu=help_menu)
help_menu.add_command(label="프로그램 정보", command=show_about)

# 메인 내용 영역
tk.Label(root, text="🎆 메뉴바가 생겼어요!", 
         font=("맑은 고딕", 16, "bold")).pack(expand=True)

root.mainloop()