# -*- coding: utf-8 -*-
import tkinter as tk

# 1단계: 기본 창 만들기
root = tk.Tk()  # 새로운 창을 만듭니다
root.title("내 첫 번째 GUI 프로그램")  # 창 제목 설정
root.geometry("300x200")  # 창 크기 설정 (가로x세로)

# 2단계: 창 보여주기 (이것이 없으면 창이 안 보여요!)
root.mainloop()