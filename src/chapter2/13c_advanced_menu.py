import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("고급 메뉴 기능 예제")
root.geometry("600x450")

# 상태 변수들
dark_mode = tk.BooleanVar()
word_wrap = tk.BooleanVar(value=True)  # 기본값: 켜짐
show_status = tk.BooleanVar(value=True)
font_size = tk.IntVar(value=12)

# UI 요소들
text_widget = tk.Text(root, height=10, font=("맑은 고딕", font_size.get()), wrap=tk.WORD)
text_widget.pack(fill="both", expand=True, padx=5, pady=5)

status_frame = tk.Frame(root, height=25, bg="lightgray")
status_label = tk.Label(status_frame, text="준비 완료", bg="lightgray", anchor="w")
status_label.pack(side="left", padx=5)
status_frame.pack(fill="x", side="bottom")

# 기능 함수들
def toggle_dark_mode():
    if dark_mode.get():
        # 다크 모드 적용
        text_widget.config(bg="#2b2b2b", fg="white", insertbackground="white")
        root.configure(bg="#1e1e1e")
        status_frame.configure(bg="#1e1e1e")
        status_label.configure(bg="#1e1e1e", fg="white")
        status_label.config(text="다크 모드 활성화")
    else:
        # 라이트 모드 적용
        text_widget.config(bg="white", fg="black", insertbackground="black")
        root.configure(bg="white")
        status_frame.configure(bg="lightgray")
        status_label.configure(bg="lightgray", fg="black")
        status_label.config(text="라이트 모드 활성화")

def toggle_word_wrap():
    if word_wrap.get():
        text_widget.config(wrap=tk.WORD)
        status_label.config(text="줄바꿈 켜짐")
    else:
        text_widget.config(wrap=tk.NONE)
        status_label.config(text="줄바꿈 꺼짐")

def toggle_status_bar():
    if show_status.get():
        status_frame.pack(fill="x", side="bottom")
        status_label.config(text="상태바 표시")
    else:
        status_frame.pack_forget()

def change_font_size(size):
    font_size.set(size)
    text_widget.config(font=("맑은 고딕", size))
    status_label.config(text=f"글꼴 크기: {size}")

def show_preferences():
    messagebox.showinfo("환경설정", f"현재 설정:\n\n다크모드: {'켜짐' if dark_mode.get() else '꺼짐'}\n줄바꿈: {'켜짐' if word_wrap.get() else '꺼짐'}\n상태바: {'보이기' if show_status.get() else '숨기기'}\n글꼴 크기: {font_size.get()}")

# 메뉴바 생성
menubar = tk.Menu(root)
root.config(menu=menubar)

# 파일 메뉴
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="파일", menu=file_menu)
file_menu.add_command(label="새로 만들기", accelerator="Ctrl+N")
file_menu.add_command(label="열기...", accelerator="Ctrl+O")
file_menu.add_separator()

# 서브메뉴: 최근에 열었던 파일
recent_menu = tk.Menu(file_menu, tearoff=0)
file_menu.add_cascade(label="최근 파일", menu=recent_menu)
recent_files = ["document1.txt", "note.txt", "readme.md"]
for file in recent_files:
    recent_menu.add_command(label=file, command=lambda f=file: messagebox.showinfo("파일 열기", f"'{f}'를 엽니다"))

file_menu.add_separator()
file_menu.add_command(label="종료", command=root.quit)

# 보기 메뉴 (체크박스 있는 메뉴)
view_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="보기", menu=view_menu)

# 체크박스 메뉴 항목들
view_menu.add_checkbutton(label="다크 모드", variable=dark_mode, command=toggle_dark_mode)
view_menu.add_checkbutton(label="줄 바꿈", variable=word_wrap, command=toggle_word_wrap)
view_menu.add_checkbutton(label="상태바 보이기", variable=show_status, command=toggle_status_bar)
view_menu.add_separator()

# 서브메뉴: 글꼴 크기
font_menu = tk.Menu(view_menu, tearoff=0)
view_menu.add_cascade(label="글꼴 크기", menu=font_menu)
for size in [10, 12, 14, 16, 18, 20]:
    font_menu.add_radiobutton(label=f"{size}점", variable=font_size, value=size, 
                             command=lambda s=size: change_font_size(s))

# 도구 메뉴
tools_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="도구", menu=tools_menu)
tools_menu.add_command(label="환경설정...", command=show_preferences)
tools_menu.add_separator()
tools_menu.add_command(label="단어 수 세기", 
                      command=lambda: messagebox.showinfo("단어 수", f"현재 문서의 단어 수: {len(text_widget.get(1.0, tk.END).split())}개"))

# 도움말 메뉴
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="도움말", menu=help_menu)
help_menu.add_command(label="사용법", command=lambda: messagebox.showinfo("사용법", "이 프로그램은 고급 메뉴 기능을 시연합니다."))
help_menu.add_separator()
help_menu.add_command(label="프로그램 정보", command=lambda: messagebox.showinfo("정보", "고급 메뉴 예제\n버전 2.0\n\ntkinter 메뉴 시스템 데모"))

# 초기 텍스트
text_widget.insert(1.0, """🎆 고급 메뉴 기능 데모

이 예제에서 볼 수 있는 고급 메뉴 기능들:

🔹 체크박스 메뉴:
- 보기 > 다크 모드 (on/off 상태 체크)
- 보기 > 줄 바꿈 (on/off 상태 체크)
- 보기 > 상태바 보이기 (on/off 상태 체크)

🔹 라디오버튼 메뉴:
- 보기 > 글꼴 크기 (여러 선택지 중 하나만 선택)

🔹 서브메뉴:
- 파일 > 최근 파일 (하위 메뉴)
- 보기 > 글꼴 크기 (하위 메뉴)

🔹 다양한 기능:
- 도구 > 환경설정 (현재 상태 보기)
- 도구 > 단어 수 세기 (동적 계산)

메뉴를 클릭해서 다양한 기능들을 체험해보세요!
""")

root.mainloop()