import tkinter as tk

def button_clicked():
    """버튼이 클릭되었을 때 실행되는 함수"""
    print("🎉 버튼이 클릭되었어요!")
    # 라벨의 텍스트를 바꿔봅시다
    status_label.config(text="버튼이 클릭되었습니다!")

def reset_button_clicked():
    """리셋 버튼이 클릭되었을 때 실행되는 함수"""
    print("🔄 리셋 버튼이 클릭되었어요!")
    status_label.config(text="초기 상태로 돌아왔습니다.")

# 메인 창 설정
root = tk.Tk()
root.title("버튼 클릭 연습")
root.geometry("500x400")
root.configure(bg="lightblue")  # 배경색 설정

# 제목 라벨
title_label = tk.Label(
    root, 
    text="버튼 클릭 연습 프로그램", 
    font=("맑은 고딕", 16, "bold"),
    bg="lightblue"
)
title_label.pack(pady=20)

# 설명 라벨
info_label = tk.Label(
    root,
    text="아래 버튼들을 클릭해보세요!",
    font=("맑은 고딕", 12),
    bg="lightblue"
)
info_label.pack(pady=10)

# 클릭 버튼
click_button = tk.Button(
    root,
    text="클릭하세요!",
    command=button_clicked,  # 버튼이 클릭되면 button_clicked 함수 실행
    font=("맑은 고딕", 14),
    bg="lightgreen",
    fg="black",
    width=15,
    height=2
)
click_button.pack(pady=10)

# 리셋 버튼
reset_button = tk.Button(
    root,
    text="리셋",
    command=reset_button_clicked,
    font=("맑은 고딕", 12),
    bg="lightcoral",
    fg="black",
    width=10
)
reset_button.pack(pady=5)

# 상태 표시 라벨
status_label = tk.Label(
    root,
    text="버튼을 기다리고 있어요...",
    font=("맑은 고딕", 12),
    bg="lightblue",
    fg="darkblue"
)
status_label.pack(pady=20)

# 프로그램 실행
print("버튼 연습 프로그램이 시작됩니다!")
root.mainloop()