import tkinter as tk
from pathlib import Path
import os

def process_filename():
    """입력된 파일명을 처리하는 함수"""
    # 입력창에서 텍스트 가져오기
    filename = filename_entry.get()
    
    if not filename:
        result_text.delete(1.0, tk.END)  # 기존 내용 삭제
        result_text.insert(tk.END, "⚠️ 파일명을 입력해주세요!")
        return
    
    # 파일명 분석하기 (Chapter 1에서 배운 내용!)
    try:
        file_path = Path(filename)
        name_part = file_path.stem  # 확장자 제외한 이름
        extension = file_path.suffix  # 확장자
        
        # 결과를 텍스트 박스에 표시
        result_text.delete(1.0, tk.END)  # 기존 내용 삭제
        result = f"""📁 파일명 분석 결과:

🔤 전체 파일명: {filename}
📝 이름 부분: {name_part}
📎 확장자: {extension}
📏 총 글자 수: {len(filename)}글자

✨ 변환 예시들:
• 소문자로: {filename.lower()}
• 대문자로: {filename.upper()}
• 공백 제거: {filename.replace(' ', '_')}
• 접두사 추가: NEW_{filename}
"""
        result_text.insert(tk.END, result)
        
    except Exception as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"❌ 오류가 발생했습니다: {e}")

def clear_all():
    """모든 내용 지우기"""
    filename_entry.delete(0, tk.END)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "입력창이 초기화되었습니다. 파일명을 입력해보세요! 📝")

# 메인 창 설정
root = tk.Tk()
root.title("파일명 분석기")
root.geometry("600x500")
root.configure(bg="white")

# 제목
title_label = tk.Label(
    root,
    text="📁 파일명 분석기",
    font=("맑은 고딕", 18, "bold"),
    bg="white",
    fg="darkblue"
)
title_label.pack(pady=15)

# 입력 섹션
input_frame = tk.Frame(root, bg="white")
input_frame.pack(pady=10)

input_label = tk.Label(
    input_frame,
    text="파일명을 입력하세요:",
    font=("맑은 고딕", 12),
    bg="white"
)
input_label.pack()

filename_entry = tk.Entry(
    input_frame,
    font=("맑은 고딕", 12),
    width=40,
    justify="center"
)
filename_entry.pack(pady=5)

# 버튼 섹션
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=10)

analyze_button = tk.Button(
    button_frame,
    text="분석하기 🔍",
    command=process_filename,
    font=("맑은 고딕", 12),
    bg="lightgreen",
    width=12
)
analyze_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(
    button_frame,
    text="초기화 🗑️",
    command=clear_all,
    font=("맑은 고딕", 12),
    bg="lightcoral",
    width=12
)
clear_button.pack(side=tk.LEFT, padx=5)

# 결과 표시 영역
result_label = tk.Label(
    root,
    text="📋 분석 결과:",
    font=("맑은 고딕", 12, "bold"),
    bg="white"
)
result_label.pack(pady=(20, 5))

result_text = tk.Text(
    root,
    height=15,
    width=70,
    font=("맑은 고딕", 10),
    bg="lightyellow",
    wrap=tk.WORD
)
result_text.pack(pady=5, padx=20)

# 초기 메시지
result_text.insert(tk.END, "파일명을 입력하고 '분석하기' 버튼을 눌러보세요! 📝")

print("파일명 분석기가 시작됩니다!")
root.mainloop()