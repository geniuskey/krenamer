# -*- coding: utf-8 -*-
import tkinter as tk
import math

root = tk.Tk()
root.title("Canvas 그리기 연습")
root.geometry("800x600")

# 캔버스 생성
canvas = tk.Canvas(root, width=600, height=400, bg="white", bd=2, relief="sunken")
canvas.pack(pady=10)

# 그리기 함수들
def draw_shapes():
    """기본 도형들 그리기"""
    canvas.delete("all")  # 캔버스 초기화
    
    # 직사각형
    canvas.create_rectangle(50, 50, 150, 100, fill="lightblue", outline="blue", width=2)
    canvas.create_text(100, 110, text="직사각형", font=("맑은 고딕", 10))
    
    # 원
    canvas.create_oval(200, 50, 300, 150, fill="lightgreen", outline="green", width=2)
    canvas.create_text(250, 160, text="원", font=("맑은 고딕", 10))
    
    # 선
    canvas.create_line(350, 50, 450, 150, fill="red", width=3)
    canvas.create_line(450, 50, 350, 150, fill="red", width=3)
    canvas.create_text(400, 160, text="선", font=("맑은 고딕", 10))
    
    # 다각형
    points = [500, 50, 550, 100, 520, 150, 480, 150, 450, 100]
    canvas.create_polygon(points, fill="lightyellow", outline="orange", width=2)
    canvas.create_text(500, 160, text="다각형", font=("맑은 고딕", 10))

def draw_pattern():
    """패턴 그리기"""
    canvas.delete("all")
    
    # 격자 패턴
    for i in range(0, 600, 20):
        canvas.create_line(i, 0, i, 400, fill="lightgray")
    for i in range(0, 400, 20):
        canvas.create_line(0, i, 600, i, fill="lightgray")
    
    # 원형 패턴
    center_x, center_y = 300, 200
    for i in range(12):
        angle = i * 30 * math.pi / 180
        x = center_x + 80 * math.cos(angle)
        y = center_y + 80 * math.sin(angle)
        canvas.create_oval(x-10, y-10, x+10, y+10, fill="blue")

# 버튼 영역
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="기본 도형", command=draw_shapes,
          font=("맑은 고딕", 11)).pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="패턴", command=draw_pattern,
          font=("맑은 고딕", 11)).pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="지우기", command=lambda: canvas.delete("all"),
          font=("맑은 고딕", 11), bg="orange").pack(side=tk.LEFT, padx=5)

# 초기 도형 그리기
draw_shapes()

root.mainloop()