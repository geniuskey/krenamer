import tkinter as tk

root = tk.Tk()
root.title("다중 선택 Listbox")
root.geometry("400x350")

tk.Label(root, text="📁 다중 선택 가능한 파일 목록:", font=("맑은 고딕", 12, "bold")).pack(pady=5)

# 다중 선택 가능한 Listbox
listbox = tk.Listbox(root, height=12, font=("맑은 고딕", 11), selectmode=tk.EXTENDED)
listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# 더 많은 항목들 추가
files = [
    "document1.pdf", "image1.jpg", "music1.mp3", "video1.mp4",
    "document2.docx", "image2.png", "music2.wav", "video2.avi",
    "spreadsheet.xlsx", "presentation.pptx", "archive.zip", "data.csv",
    "script.py", "style.css", "index.html", "config.json"
]

for file in files:
    listbox.insert(tk.END, file)

def show_selection():
    selected_indices = listbox.curselection()
    selected_files = [listbox.get(i) for i in selected_indices]
    
    if selected_files:
        result = f"선택된 파일 ({len(selected_files)}개):\n"
        result += "\n".join(f"• {file}" for file in selected_files)
        result_label.config(text=result)
    else:
        result_label.config(text="선택된 파일이 없습니다")

tk.Button(root, text="선택 항목 보기", command=show_selection, 
          font=("맑은 고딕", 11)).pack(pady=5)

result_label = tk.Label(root, text="Ctrl 또는 Shift 키로 여러 파일을 선택해보세요", 
                       font=("맑은 고딕", 10), fg="gray", anchor="w", justify="left")
result_label.pack(padx=10, pady=5, fill=tk.X)

root.mainloop()