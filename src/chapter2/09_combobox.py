import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Combobox 사용법")
root.geometry("450x300")

tk.Label(root, text="🔽 Combobox 예제", font=("맑은 고딕", 14, "bold")).pack(pady=10)

# 기본 Combobox
tk.Label(root, text="선호하는 프로그래밍 언어:", font=("맑은 고딕", 12)).pack(pady=5)
languages = ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "Swift"]
language_combo = ttk.Combobox(root, values=languages, font=("맑은 고딕", 11), state="readonly")
language_combo.pack(pady=5)
language_combo.set("Python")  # 기본값 설정

# 편집 가능한 Combobox
tk.Label(root, text="좋아하는 색상 (직접 입력 가능):", font=("맑은 고딕", 12)).pack(pady=(20, 5))
colors = ["빨강", "파랑", "초록", "노랑", "보라", "주황"]
color_combo = ttk.Combobox(root, values=colors, font=("맑은 고딕", 11))
color_combo.pack(pady=5)

# 선택 이벤트 처리
def on_language_select(event):
    selected = event.widget.get()
    result_label.config(text=f"선택된 언어: {selected}")

def on_color_select(event):
    selected = event.widget.get()
    color_label.config(text=f"선택/입력된 색상: {selected}")

language_combo.bind('<<ComboboxSelected>>', on_language_select)
color_combo.bind('<<ComboboxSelected>>', on_color_select)

# 결과 표시
result_label = tk.Label(root, text="언어를 선택해보세요", font=("맑은 고딕", 10), fg="blue")
result_label.pack(pady=10)

color_label = tk.Label(root, text="색상을 선택하거나 직접 입력해보세요", font=("맑은 고딕", 10), fg="green")
color_label.pack(pady=5)

# 현재 값 확인 버튼
def show_values():
    lang = language_combo.get()
    color = color_combo.get()
    info = f"언어: {lang}, 색상: {color}"
    info_label.config(text=info)

tk.Button(root, text="선택 내용 확인", command=show_values, 
          font=("맑은 고딕", 11), bg="lightgray").pack(pady=15)

info_label = tk.Label(root, text="", font=("맑은 고딕", 10), fg="darkblue")
info_label.pack()

root.mainloop()