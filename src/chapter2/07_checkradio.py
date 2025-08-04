# -*- coding: utf-8 -*-
import tkinter as tk

root = tk.Tk()
root.title("체크박스와 라디오버튼")
root.geometry("500x500")

# 체크박스 섹션
check_frame = tk.LabelFrame(root, text="🔲 체크박스 (여러 개 선택 가능)", 
                           font=("맑은 고딕", 12, "bold"), padx=10, pady=10)
check_frame.pack(pady=10, padx=20, fill="x")

# 체크박스 변수들
pizza_var = tk.BooleanVar()
burger_var = tk.BooleanVar()
chicken_var = tk.BooleanVar()
noodle_var = tk.BooleanVar()

tk.Label(check_frame, text="좋아하는 음식을 모두 선택하세요:", 
         font=("맑은 고딕", 11)).pack(anchor="w")

tk.Checkbutton(check_frame, text="🍕 피자", variable=pizza_var,
               font=("맑은 고딕", 11)).pack(anchor="w")
tk.Checkbutton(check_frame, text="🍔 햄버거", variable=burger_var,
               font=("맑은 고딕", 11)).pack(anchor="w")
tk.Checkbutton(check_frame, text="🍗 치킨", variable=chicken_var,
               font=("맑은 고딕", 11)).pack(anchor="w")
tk.Checkbutton(check_frame, text="🍜 라면", variable=noodle_var,
               font=("맑은 고딕", 11)).pack(anchor="w")

# 라디오버튼 섹션
radio_frame = tk.LabelFrame(root, text="🔘 라디오버튼 (하나만 선택 가능)", 
                           font=("맑은 고딕", 12, "bold"), padx=10, pady=10)
radio_frame.pack(pady=10, padx=20, fill="x")

# 라디오버튼 변수
color_var = tk.StringVar()
color_var.set("red")  # 기본값 설정

tk.Label(radio_frame, text="좋아하는 색깔을 하나 선택하세요:", 
         font=("맑은 고딕", 11)).pack(anchor="w")

colors = [("🔴 빨강", "red"), ("🔵 파랑", "blue"), ("🟢 초록", "green"), ("🟡 노랑", "yellow")]

for text, value in colors:
    tk.Radiobutton(radio_frame, text=text, variable=color_var, value=value,
                   font=("맑은 고딕", 11)).pack(anchor="w")

# 결과 표시 함수
def show_selections():
    # 체크박스 결과
    foods = []
    if pizza_var.get(): foods.append("피자")
    if burger_var.get(): foods.append("햄버거")
    if chicken_var.get(): foods.append("치킨")
    if noodle_var.get(): foods.append("라면")
    
    # 라디오버튼 결과
    selected_color = color_var.get()
    color_names = {"red": "빨강", "blue": "파랑", "green": "초록", "yellow": "노랑"}
    
    # 결과 메시지
    result = "📋 선택 결과:\n\n"
    
    if foods:
        result += f"좋아하는 음식: {', '.join(foods)}\n"
    else:
        result += "선택된 음식이 없습니다.\n"
    
    result += f"좋아하는 색깔: {color_names[selected_color]}"
    
    result_label.config(text=result)

# 버튼과 결과 표시 영역
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="선택 결과 보기", command=show_selections,
          font=("맑은 고딕", 12), bg="lightgreen").pack(side=tk.LEFT, padx=5)

# 결과 표시 라벨
result_label = tk.Label(root, text="위에서 선택을 하고 '선택 결과 보기'를 클릭하세요.",
                       font=("맑은 고딕", 11), fg="blue", justify="left")
result_label.pack(pady=20)

root.mainloop()