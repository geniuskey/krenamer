import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
root.title("스크롤 가능한 Text")
root.geometry("500x400")

tk.Label(root, text="📋 스크롤 가능한 텍스트:", font=("맑은 고딕", 12, "bold")).pack(pady=5)

# 스크롤바가 있는 Text 위젯
text_area = scrolledtext.ScrolledText(
    root,
    height=15,
    width=60,
    font=("맑은 고딕", 11),
    wrap=tk.WORD
)
text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# 많은 양의 텍스트 추가
for i in range(50):
    text_area.insert(tk.END, f"이것은 {i+1}번째 줄입니다. 스크롤해서 아래 내용을 확인해보세요!\n")

root.mainloop()