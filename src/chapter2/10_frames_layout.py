import tkinter as tk

root = tk.Tk()
root.title("Frame을 이용한 레이아웃")
root.geometry("600x400")

# 상단 프레임 - 제목
top_frame = tk.Frame(root, bg="lightblue", height=60)
top_frame.pack(fill=tk.X, padx=5, pady=5)
top_frame.pack_propagate(False)  # 프레임 크기 고정

title_label = tk.Label(top_frame, text="📋 파일 관리 프로그램", 
                      font=("맑은 고딕", 16, "bold"), bg="lightblue")
title_label.pack(expand=True)

# 중앙 프레임 - 좌우로 분할
center_frame = tk.Frame(root)
center_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# 왼쪽 프레임 - 파일 목록
left_frame = tk.Frame(center_frame, bg="lightgray", width=200)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
left_frame.pack_propagate(False)

tk.Label(left_frame, text="📁 파일 목록", font=("맑은 고딕", 12, "bold"), 
         bg="lightgray").pack(pady=10)

files = ["문서1.txt", "이미지1.jpg", "데이터.csv", "프로그램.py"]
for file in files:
    tk.Button(left_frame, text=file, width=20, 
              font=("맑은 고딕", 10)).pack(pady=2, padx=10)

# 오른쪽 프레임 - 상세 정보
right_frame = tk.Frame(center_frame, bg="white", relief=tk.RAISED, bd=2)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.Label(right_frame, text="📄 파일 정보", font=("맑은 고딕", 12, "bold"), 
         bg="white").pack(pady=10)

info_text = """파일명: 문서1.txt
크기: 15.2 KB
수정일: 2024-08-06
타입: 텍스트 파일

파일을 선택하면 여기에
상세 정보가 표시됩니다."""

tk.Label(right_frame, text=info_text, font=("맑은 고딕", 10), 
         bg="white", justify=tk.LEFT, anchor="nw").pack(padx=20, pady=10, fill=tk.BOTH)

# 하단 프레임 - 버튼들
bottom_frame = tk.Frame(root, bg="lightgray", height=50)
bottom_frame.pack(fill=tk.X, padx=5, pady=5)
bottom_frame.pack_propagate(False)

tk.Button(bottom_frame, text="새로고침", font=("맑은 고딕", 11)).pack(side=tk.LEFT, padx=10, pady=10)
tk.Button(bottom_frame, text="삭제", font=("맑은 고딕", 11)).pack(side=tk.LEFT, padx=5, pady=10)
tk.Button(bottom_frame, text="이름변경", font=("맑은 고딕", 11)).pack(side=tk.LEFT, padx=5, pady=10)
tk.Button(bottom_frame, text="종료", font=("맑은 고딕", 11)).pack(side=tk.RIGHT, padx=10, pady=10)

root.mainloop()