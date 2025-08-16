import tkinter as tk
import math

root = tk.Tk()
root.title("Canvas로 차트 그리기")
root.geometry("800x550")

# Canvas
canvas = tk.Canvas(root, width=750, height=500, bg="white", relief=tk.RAISED, bd=2)
canvas.pack(padx=25, pady=25)

# 데이터
file_data = {
    "문서": 45,
    "이미지": 30, 
    "동영상": 15,
    "음악": 25,
    "기타": 10
}

monthly_data = [120, 150, 180, 200, 175, 220, 250, 280, 240, 300, 320, 350]
months = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]

colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]

# 제목
canvas.create_text(375, 30, text="📊 파일 유형별 분포 및 월별 처리량", 
                  font=("맑은 고딕", 16, "bold"), fill="darkblue")

# 1. 파이 차트 그리기
pie_center_x, pie_center_y = 200, 260
pie_radius = 80

total = sum(file_data.values())
start_angle = 0

canvas.create_text(180, 120, text="파일 유형별 분포", font=("맑은 고딕", 12, "bold"))

for i, (category, value) in enumerate(file_data.items()):
    # 각도 계산
    extent = (value / total) * 360
    
    # 파이 조각 그리기
    canvas.create_arc(pie_center_x - pie_radius, pie_center_y - pie_radius,
                     pie_center_x + pie_radius, pie_center_y + pie_radius,
                     start=start_angle, extent=extent, fill=colors[i], outline="white", width=2)
    
    # 레이블 위치 계산
    label_angle = math.radians(start_angle + extent/2)
    label_x = pie_center_x + (pie_radius + 30) * math.cos(label_angle)
    label_y = pie_center_y + (pie_radius + 30) * math.sin(label_angle)
    
    # 레이블과 값 표시
    canvas.create_text(label_x, label_y, text=f"{category}\n{value}개", 
                      font=("맑은 고딕", 9), anchor="center")
    
    start_angle += extent

# 2. 막대 차트 그리기
bar_start_x = 400
bar_start_y = 350
bar_width = 20
bar_spacing = 25
max_value = max(monthly_data)

canvas.create_text(550, 120, text="월별 파일 처리량", font=("맑은 고딕", 12, "bold"))

# Y축
canvas.create_line(bar_start_x - 10, 150, bar_start_x - 10, bar_start_y + 10, 
                  fill="black", width=2)
# X축  
canvas.create_line(bar_start_x - 10, bar_start_y + 10, 
                  bar_start_x + len(monthly_data) * bar_spacing + 10, bar_start_y + 10, 
                  fill="black", width=2)

# Y축 레이블
for i in range(0, max_value + 1, 100):
    y = bar_start_y - (i / max_value) * 200
    canvas.create_line(bar_start_x - 15, y, bar_start_x - 5, y, fill="gray")
    canvas.create_text(bar_start_x - 20, y, text=str(i), font=("맑은 고딕", 8), anchor="e")

# 막대들 그리기
for i, (month, value) in enumerate(zip(months, monthly_data)):
    x = bar_start_x + i * bar_spacing
    bar_height = (value / max_value) * 200
    
    # 막대
    canvas.create_rectangle(x, bar_start_y - bar_height, x + bar_width, bar_start_y,
                           fill=colors[i % len(colors)], outline="black")
    
    # 월 레이블
    canvas.create_text(x + bar_width//2, bar_start_y + 25, text=month, 
                      font=("맑은 고딕", 8), anchor="center")
    
    # 값 표시
    canvas.create_text(x + bar_width//2, bar_start_y - bar_height - 10, text=str(value), 
                      font=("맑은 고딕", 8), anchor="center")

# 범례
legend_y = 420
canvas.create_text(375, legend_y, text="범례:", font=("맑은 고딕", 11, "bold"))

legend_start_x = 100
for i, (category, color) in enumerate(zip(file_data.keys(), colors)):
    x = legend_start_x + i * 120
    canvas.create_rectangle(x, legend_y + 15, x + 15, legend_y + 30, fill=color, outline="black")
    canvas.create_text(x + 25, legend_y + 22, text=category, font=("맑은 고딕", 10), anchor="w")

# 통계 정보
stats_text = f"총 파일 수: {total}개 | 월 평균: {sum(monthly_data)//12}개"
canvas.create_text(375, 470, text=stats_text, font=("맑은 고딕", 11), fill="darkgreen")

root.mainloop()