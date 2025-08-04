# -*- coding: utf-8 -*-
import tkinter as tk

root = tk.Tk()
root.title("Label 연습")
root.geometry("500x400")
root.configure(bg="white")

# 기본 라벨
basic_label = tk.Label(root, text="안녕하세요! 이것은 기본 라벨입니다.")
basic_label.pack(pady=10)

# 스타일이 적용된 라벨
styled_label = tk.Label(
    root,
    text="🎨 예쁘게 꾸민 라벨",
    font=("맑은 고딕", 16, "bold"),    # 폰트 설정
    fg="blue",                         # 글자색
    bg="lightyellow",                  # 배경색
    width=20,                          # 너비 (글자 수)
    height=2                           # 높이 (줄 수)
)
styled_label.pack(pady=10)

# 여러 줄 라벨
multiline_label = tk.Label(
    root,
    text="여러 줄로 된 라벨입니다.\n두 번째 줄\n세 번째 줄",
    font=("맑은 고딕", 12),
    justify=tk.LEFT,                   # 텍스트 정렬
    bg="lightgreen"
)
multiline_label.pack(pady=10)

# 동적으로 변하는 라벨
dynamic_var = tk.StringVar()
dynamic_var.set("변경 가능한 텍스트")

dynamic_label = tk.Label(
    root,
    textvariable=dynamic_var,          # StringVar 사용
    font=("맑은 고딕", 14),
    fg="red"
)
dynamic_label.pack(pady=10)

# 텍스트를 변경하는 버튼
def change_text():
    import random
    texts = ["안녕하세요!", "Hello!", "こんにちは!", "Bonjour!", "¡Hola!"]
    dynamic_var.set(random.choice(texts))

change_button = tk.Button(root, text="텍스트 변경", command=change_text)
change_button.pack(pady=10)

root.mainloop()