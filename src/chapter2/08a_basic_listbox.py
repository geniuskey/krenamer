import tkinter as tk

root = tk.Tk()
root.title("Listbox 기본 사용법")
root.geometry("400x300")

tk.Label(root, text="🗂️ 파일 목록:", font=("맑은 고딕", 12, "bold")).pack(pady=5)

# 기본 Listbox
listbox = tk.Listbox(root, height=10, font=("맑은 고딕", 11))
listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# 항목들 추가
files = [
    "문서1.txt",
    "이미지1.jpg", 
    "프레젠테이션.pdf",
    "스프레드시트.xlsx",
    "음악파일.mp3",
    "비디오.mp4",
    "README.md",
    "설정파일.json"
]

for file in files:
    listbox.insert(tk.END, file)

# 선택 이벤트 처리
def on_select(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        value = event.widget.get(index)
        result_label.config(text=f"선택된 파일: {value}")

listbox.bind('<<ListboxSelect>>', on_select)

result_label = tk.Label(root, text="파일을 선택해보세요", font=("맑은 고딕", 10), fg="blue")
result_label.pack(pady=5)

root.mainloop()