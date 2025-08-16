import tkinter as tk
from tkinter import messagebox, filedialog

root = tk.Tk()
root.title("텍스트 에디터 - 메뉴 예제")
root.geometry("600x400")

# 텍스트 위젯 생성
text_widget = tk.Text(root, font=("맑은 고딕", 12), wrap=tk.WORD)
text_widget.pack(fill="both", expand=True, padx=10, pady=10)

# 파일 관련 기능들
def new_file():
    if text_widget.get(1.0, tk.END).strip():  # 내용이 있는지 확인
        if messagebox.askyesno("새 파일", "현재 내용을 지우고 새 파일을 만들까요?"):
            text_widget.delete(1.0, tk.END)
    else:
        text_widget.delete(1.0, tk.END)

def open_file():
    filename = filedialog.askopenfilename(
        title="파일 열기",
        filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")]
    )
    if filename:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                text_widget.delete(1.0, tk.END)
                text_widget.insert(1.0, content)
                root.title(f"텍스트 에디터 - {filename.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("오류", f"파일을 열 수 없습니다: {e}")

def save_file():
    filename = filedialog.asksaveasfilename(
        title="파일 저장",
        defaultextension=".txt",
        filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")]
    )
    if filename:
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                content = text_widget.get(1.0, tk.END)
                file.write(content)
            messagebox.showinfo("저장 완료", f"파일이 저장되었습니다!\n{filename}")
            root.title(f"텍스트 에디터 - {filename.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("오류", f"파일을 저장할 수 없습니다: {e}")

# 편집 기능들
def cut_text():
    text_widget.event_generate("<<Cut>>")

def copy_text():
    text_widget.event_generate("<<Copy>>")

def paste_text():
    text_widget.event_generate("<<Paste>>")

def select_all():
    text_widget.tag_add(tk.SEL, "1.0", tk.END)
    text_widget.mark_set(tk.INSERT, "1.0")
    text_widget.see(tk.INSERT)

# 메뉴바 생성
menubar = tk.Menu(root)
root.config(menu=menubar)

# 파일 메뉴
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="파일", menu=file_menu)
file_menu.add_command(label="새로 만들기", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="열기...", command=open_file, accelerator="Ctrl+O")
file_menu.add_separator()
file_menu.add_command(label="저장...", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="종료", command=root.quit, accelerator="Ctrl+Q")

# 편집 메뉴
edit_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="편집", menu=edit_menu)
edit_menu.add_command(label="잘라내기", command=cut_text, accelerator="Ctrl+X")
edit_menu.add_command(label="복사", command=copy_text, accelerator="Ctrl+C")
edit_menu.add_command(label="붙여넣기", command=paste_text, accelerator="Ctrl+V")
edit_menu.add_separator()
edit_menu.add_command(label="모두 선택", command=select_all, accelerator="Ctrl+A")

# 키보드 단축키 바인딩
root.bind('<Control-n>', lambda e: new_file())
root.bind('<Control-o>', lambda e: open_file())
root.bind('<Control-s>', lambda e: save_file())
root.bind('<Control-q>', lambda e: root.quit())

# 초기 텍스트
text_widget.insert(1.0, """📝 텍스트 에디터 예제

이 간단한 텍스트 에디터로 다음 기능들을 체험해보세요:

📁 파일 메뉴:
- 새로 만들기 (Ctrl+N)
- 열기 (Ctrl+O)
- 저장 (Ctrl+S)
- 종료 (Ctrl+Q)

✂️ 편집 메뉴:
- 잘라내기 (Ctrl+X)
- 복사 (Ctrl+C)
- 붙여넣기 (Ctrl+V)
- 모두 선택 (Ctrl+A)

⌨️ 키보드 단축키도 지원합니다!

이 내용을 수정해보고, 파일로 저장해보세요.
""")

root.mainloop()