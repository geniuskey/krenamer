import tkinter as tk

root = tk.Tk()
root.title("Text 기본 사용법")
root.geometry("500x300")

tk.Label(root, text="📝 여러 줄 텍스트 입력:", font=("맑은 고딕", 12, "bold")).pack(pady=5)

# 기본 Text 위젯
text_widget = tk.Text(
    root,
    height=10,
    width=50,
    font=("맑은 고딕", 11),
    wrap=tk.WORD,              # 단어 단위로 줄바꿈
    bg="lightyellow"
)
text_widget.pack(pady=10)

# 초기 텍스트 넣기
text_widget.insert(tk.END, "여기에 여러 줄의 텍스트를 입력할 수 있습니다.\n")
text_widget.insert(tk.END, "Enter를 눌러서 줄을 바꿀 수 있습니다.\n")
text_widget.insert(tk.END, "Text 위젯은 긴 문서 작성에 적합합니다.")

root.mainloop()