"""
KRenamer Chapter 2: Tkinter GUI 기초
메인 실행 파일 - 모든 단계별 예제를 실행할 수 있습니다.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def run_step(step_number):
    """특정 단계의 예제를 실행하는 함수"""
    step_files = {
        1: "step1_hello_window.py",
        2: "step2_buttons.py", 
        3: "step3_text_input.py",
        4: "step4_file_list.py",
        5: "step5_layout_design.py"
    }
    
    if step_number not in step_files:
        messagebox.showerror("오류", "해당 단계를 찾을 수 없습니다!")
        return
    
    script_path = os.path.join(os.path.dirname(__file__), step_files[step_number])
    
    if not os.path.exists(script_path):
        messagebox.showerror("파일 오류", f"파일을 찾을 수 없습니다: {step_files[step_number]}")
        return
    
    try:
        print(f"🚀 {step_files[step_number]} 실행 중...")
        exec(open(script_path, encoding='utf-8').read())
    except Exception as e:
        messagebox.showerror("실행 오류", f"스크립트 실행 중 오류가 발생했습니다:\n{e}")

def show_about():
    """프로그램 정보 표시"""
    about_text = """🎉 KRenamer Chapter 2: Tkinter GUI 기초

이 프로그램은 Tkinter GUI 프로그래밍을 단계별로 학습할 수 있도록 
구성된 교육용 도구입니다.

📚 학습 단계:
1️⃣ 첫 번째 창 만들기
2️⃣ 버튼과 이벤트 처리
3️⃣ 텍스트 입력과 처리
4️⃣ 파일 목록 관리
5️⃣ 현대적인 레이아웃 디자인

각 단계를 차례대로 학습하면서 
GUI 프로그래밍의 기초를 익혀보세요! 💪"""
    
    messagebox.showinfo("프로그램 정보", about_text)

# 메인 런처 GUI
def create_launcher():
    """학습 단계 선택 런처 생성"""
    
    root = tk.Tk()
    root.title("KRenamer Chapter 2 - 학습 런처")
    root.geometry("500x700")
    root.configure(bg="#f8f9fa")
    root.resizable(False, False)
    
    # 제목 영역
    title_frame = tk.Frame(root, bg="#343a40", height=80)
    title_frame.pack(fill=tk.X)
    title_frame.pack_propagate(False)
    
    title_label = tk.Label(
        title_frame,
        text="🎓 KRenamer Chapter 2",
        font=("맑은 고딕", 20, "bold"),
        bg="#343a40",
        fg="white"
    )
    title_label.pack(expand=True)
    
    # 메인 콘텐츠 영역
    content_frame = tk.Frame(root, bg="#f8f9fa")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # 단계별 버튼들
    steps = [
        ("첫 번째 창 만들기", "기본 tkinter 창과 라벨 만들기", "#28a745"),
        ("버튼과 이벤트", "버튼 클릭 이벤트 처리하기", "#007bff"),
        ("텍스트 입력과 처리", "Entry, Text 위젯으로 파일명 분석", "#17a2b8"),
        ("파일 목록 관리", "Listbox로 파일 목록 관리하기", "#fd7e14"),
        ("현대적인 레이아웃", "ttk와 grid로 전문적인 GUI", "#6f42c1")
    ]
    
    for i, (title, desc, color) in enumerate(steps, 1):
        # 단계별 프레임
        step_frame = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=1)
        step_frame.pack(fill=tk.X, pady=5)
        
        # 단계 버튼
        step_button = tk.Button(
            step_frame,
            text=title,
            font=("맑은 고딕", 12, "bold"),
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            command=lambda step=i: run_step(step),
            height=2,
            cursor="hand2"
        )
        step_button.pack(fill=tk.X, padx=10, pady=5)
        
        # 단계 설명
        desc_label = tk.Label(
            step_frame,
            text=desc,
            font=("맑은 고딕", 10),
            bg="white",
            fg="#6c757d"
        )
        desc_label.pack(pady=(0, 10))
    
    # 하단 버튼 영역
    bottom_frame = tk.Frame(root, bg="#f8f9fa")
    bottom_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
    
    # 정보 버튼
    about_button = tk.Button(
        bottom_frame,
        text="ℹ️ 프로그램 정보",
        font=("맑은 고딕", 10),
        bg="#6c757d",
        fg="white",
        command=show_about,
        width=15
    )
    about_button.pack(side=tk.LEFT)
    
    # 종료 버튼
    exit_button = tk.Button(
        bottom_frame,
        text="❌ 종료",
        font=("맑은 고딕", 10),
        bg="#dc3545",
        fg="white",
        command=root.quit,
        width=15
    )
    exit_button.pack(side=tk.RIGHT)
    
    return root

if __name__ == "__main__":
    print("🎓 KRenamer Chapter 2 학습 런처를 시작합니다!")
    print("=" * 50)
    
    launcher = create_launcher()
    launcher.mainloop()
    
    print("학습 런처가 종료되었습니다. 수고하셨습니다! 👏")