import tkinter as tk

root = tk.Tk()
root.title("Canvas 기본 도형")
root.geometry("540x420")

# 캔버스 생성
canvas = tk.Canvas(root, width=500, height=330, bg="white", bd=2, relief="sunken")
canvas.pack(anchor="center", pady=10)


# 기본 도형들 그리기
def draw_basic_shapes():
    # 직사각형
    canvas.create_rectangle(50, 50, 150, 100, fill="lightblue", outline="blue", width=2)
    canvas.create_text(100, 110, text="직사각형", font=("맑은 고딕", 10))

    # 원 (타원)
    canvas.create_oval(200, 50, 300, 150, fill="lightgreen", outline="green", width=2)
    canvas.create_text(250, 160, text="원", font=("맑은 고딕", 10))

    # 직선
    canvas.create_line(350, 50, 450, 150, fill="red", width=3)
    canvas.create_text(400, 160, text="직선", font=("맑은 고딕", 10))

    # 다각형 (별 모양)
    points = [250, 200, 270, 240, 310, 240, 280, 270, 290, 310, 250, 290, 210, 310, 220, 270, 190, 240, 230, 240]
    canvas.create_polygon(points, fill="lightyellow", outline="orange", width=2)
    canvas.create_text(250, 320, text="다각형", font=("맑은 고딕", 10))


# 도형 그리기
draw_basic_shapes()

# 지우기 버튼
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="지우기", command=lambda: canvas.delete("all"),
          font=("맑은 고딕", 12), bg="orange").pack(side="left", padx=10)
tk.Button(btn_frame, text="다시 그리기", command=draw_basic_shapes,
          font=("맑은 고딕", 12), bg="lightgreen").pack(side="left", padx=10)

root.mainloop()