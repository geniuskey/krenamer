import tkinter as tk
import random

root = tk.Tk()
root.title("상호작용하는 Canvas")
root.geometry("700x600")

# Canvas
canvas = tk.Canvas(root, width=650, height=450, bg="white", relief=tk.RAISED, bd=2)
canvas.pack(padx=25, pady=10)

# 그리기 상태 변수들
current_color = "black"
drawing = False
last_x = 0
last_y = 0
shapes = []  # 생성된 도형들을 저장

# 마우스 이벤트 함수들
def start_draw(event):
    global drawing, last_x, last_y
    drawing = True
    last_x = event.x
    last_y = event.y

def draw_line(event):
    global last_x, last_y
    if drawing:
        canvas.create_line(last_x, last_y, event.x, event.y, 
                          fill=current_color, width=3, capstyle=tk.ROUND)
        last_x = event.x
        last_y = event.y

def stop_draw(event):
    global drawing
    drawing = False

# 도형 추가 함수들
def add_random_circle():
    x = random.randint(50, 600)
    y = random.randint(50, 400)
    size = random.randint(20, 60)
    color = random.choice(["red", "blue", "green", "yellow", "purple", "orange"])
    
    shape_id = canvas.create_oval(x-size//2, y-size//2, x+size//2, y+size//2, 
                                 fill=color, outline="black", width=2)
    shapes.append(shape_id)

def add_random_rectangle():
    x = random.randint(50, 600)
    y = random.randint(50, 400)
    width = random.randint(30, 80)
    height = random.randint(30, 80)
    color = random.choice(["lightblue", "lightgreen", "lightyellow", "lightpink", "lightgray"])
    
    shape_id = canvas.create_rectangle(x, y, x+width, y+height, 
                                      fill=color, outline="black", width=2)
    shapes.append(shape_id)

def clear_canvas():
    canvas.delete("all")
    shapes.clear()

def change_color(color):
    global current_color
    current_color = color

# 마우스 바인딩
canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw_line)
canvas.bind("<ButtonRelease-1>", stop_draw)

# 컨트롤 패널
control_frame = tk.Frame(root)
control_frame.pack(fill=tk.X, padx=25, pady=10)

# 색상 버튼들
color_frame = tk.Frame(control_frame)
color_frame.pack(side=tk.LEFT)

tk.Label(color_frame, text="색상:", font=("맑은 고딕", 11, "bold")).pack(side=tk.LEFT)

colors = [("검정", "black"), ("빨강", "red"), ("파랑", "blue"), ("초록", "green")]
for name, color in colors:
    tk.Button(color_frame, text=name, bg=color, fg="white" if color == "black" else "black",
              command=lambda c=color: change_color(c), width=6, font=("맑은 고딕", 9)).pack(side=tk.LEFT, padx=2)

# 도형 버튼들
shape_frame = tk.Frame(control_frame)
shape_frame.pack(side=tk.RIGHT)

tk.Button(shape_frame, text="랜덤 원", command=add_random_circle, 
          font=("맑은 고딕", 10), bg="lightblue").pack(side=tk.LEFT, padx=5)
tk.Button(shape_frame, text="랜덤 사각형", command=add_random_rectangle, 
          font=("맑은 고딕", 10), bg="lightgreen").pack(side=tk.LEFT, padx=5)
tk.Button(shape_frame, text="모두 지우기", command=clear_canvas, 
          font=("맑은 고딕", 10), bg="lightcoral").pack(side=tk.LEFT, padx=5)

# 안내 텍스트
info_label = tk.Label(root, text="🖱️ 마우스로 자유롭게 그리거나 버튼을 눌러 도형을 추가해보세요!", 
                     font=("맑은 고딕", 11), fg="gray")
info_label.pack(pady=5)

# 초기 안내 텍스트를 캔버스에 표시
canvas.create_text(325, 200, text="여기서 그림을 그려보세요! 🎨", 
                  font=("맑은 고딕", 16, "bold"), fill="gray")

root.mainloop()