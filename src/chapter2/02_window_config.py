import tkinter as tk

root = tk.Tk()

# 창 설정 옵션들
root.title("창 설정 연습")                  # 제목
root.geometry("300x200")                  # 크기
root.resizable(True, False)               # 가로만 크기 조절 가능
root.minsize(200, 100)                    # 최소 크기
root.maxsize(800, 600)                    # 최대 크기
root.configure(bg="lightblue")            # 배경색

root.mainloop()