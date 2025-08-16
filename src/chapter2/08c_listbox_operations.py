import tkinter as tk

root = tk.Tk()
root.title("Listbox 조작 기능")
root.geometry("400x300")

# 상단 프레임 - 입력과 버튼
top_frame = tk.Frame(root)
top_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Label(top_frame, text="새 항목:", font=("맑은 고딕", 11)).pack(side=tk.LEFT)
entry = tk.Entry(top_frame, font=("맑은 고딕", 11), width=20)
entry.pack(side=tk.LEFT, padx=5)

# Listbox
listbox = tk.Listbox(root, height=6, font=("맑은 고딕", 11))
listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# 초기 항목들
initial_items = ["항목 1", "항목 2", "항목 3", "항목 4", "항목 5"]
for item in initial_items:
    listbox.insert(tk.END, item)

# 기능 함수들
def add_item():
    new_item = entry.get()
    if new_item:
        listbox.insert(tk.END, new_item)
        entry.delete(0, tk.END)

def delete_item():
    selection = listbox.curselection()
    if selection:
        listbox.delete(selection[0])

def clear_all():
    listbox.delete(0, tk.END)

def move_up():
    selection = listbox.curselection()
    if selection and selection[0] > 0:
        index = selection[0]
        item = listbox.get(index)
        listbox.delete(index)
        listbox.insert(index - 1, item)
        listbox.select_set(index - 1)

def move_down():
    selection = listbox.curselection()
    if selection and selection[0] < listbox.size() - 1:
        index = selection[0]
        item = listbox.get(index)
        listbox.delete(index)
        listbox.insert(index + 1, item)
        listbox.select_set(index + 1)

# 버튼 프레임
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

tk.Button(button_frame, text="추가", command=add_item, width=8).pack(side=tk.LEFT, padx=2)
tk.Button(button_frame, text="삭제", command=delete_item, width=8).pack(side=tk.LEFT, padx=2)
tk.Button(button_frame, text="모두 지우기", command=clear_all, width=8).pack(side=tk.LEFT, padx=2)
tk.Button(button_frame, text="↑", command=move_up, width=3).pack(side=tk.LEFT, padx=2)
tk.Button(button_frame, text="↓", command=move_down, width=3).pack(side=tk.LEFT, padx=2)

# Enter 키로 항목 추가
entry.bind('<Return>', lambda e: add_item())

root.mainloop()