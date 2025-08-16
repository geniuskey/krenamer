import tkinter as tk

root = tk.Tk()
root.title("Entry 다양한 스타일")
root.geometry("500x300")

# 일반 텍스트 입력창
tk.Label(root, text="이름:", font=("맑은 고딕", 12)).pack(pady=5)
name_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30)
name_entry.pack(pady=5)

# 비밀번호 입력창 (별표로 숨김)
tk.Label(root, text="비밀번호:", font=("맑은 고딕", 12)).pack(pady=5)
password_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30, show="*")
password_entry.pack(pady=5)

# 읽기 전용 입력창
tk.Label(root, text="읽기 전용:", font=("맑은 고딕", 12)).pack(pady=5)
readonly_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30, state="readonly")
readonly_entry.insert(0, "이 텍스트는 수정할 수 없습니다")
readonly_entry.pack(pady=5)

root.mainloop()