import tkinter as tk

root = tk.Tk()
root.title("Entry 기본 사용법")
root.geometry("400x200")

# 기본 입력창
tk.Label(root, text="이름을 입력하세요:", font=("맑은 고딕", 12)).pack(pady=10)
name_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30)
name_entry.pack(pady=5)

# 입력값 가져오기
def show_input():
    user_input = name_entry.get()  # Entry에서 텍스트 가져오기
    result_label.config(text=f"입력하신 내용: {user_input}")

tk.Button(root, text="입력값 확인", command=show_input).pack(pady=10)

result_label = tk.Label(root, text="", font=("맑은 고딕", 11), fg="blue")
result_label.pack()

root.mainloop()