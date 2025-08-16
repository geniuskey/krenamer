import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("고급 레이아웃 - Grid와 Pack 조합")
root.geometry("700x500")

# 메인 컨테이너
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# 상단 영역 - Grid 사용
top_section = tk.LabelFrame(main_frame, text="사용자 정보 입력", font=("맑은 고딕", 12, "bold"))
top_section.pack(fill=tk.X, pady=(0, 10))

# Grid로 입력 필드들 배치
tk.Label(top_section, text="이름:", font=("맑은 고딕", 11)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
name_entry = tk.Entry(top_section, font=("맑은 고딕", 11), width=30)
name_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

tk.Label(top_section, text="이메일:", font=("맑은 고딕", 11)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
email_entry = tk.Entry(top_section, font=("맑은 고딕", 11), width=30)
email_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

tk.Label(top_section, text="부서:", font=("맑은 고딕", 11)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
dept_combo = ttk.Combobox(top_section, values=["개발팀", "디자인팀", "기획팀", "마케팅팀"], 
                         font=("맑은 고딕", 11), state="readonly")
dept_combo.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

tk.Button(top_section, text="저장", font=("맑은 고딕", 11), bg="lightblue").grid(row=2, column=2, padx=10, pady=5)

# 그리드 가중치 설정
top_section.columnconfigure(1, weight=1)

# 중앙 영역 - Notebook (탭)
notebook = ttk.Notebook(main_frame)
notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

# 탭 1: 파일 목록
tab1 = tk.Frame(notebook)
notebook.add(tab1, text="📁 파일 관리")

# 파일 목록용 프레임
file_frame = tk.Frame(tab1)
file_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Label(file_frame, text="파일 목록:", font=("맑은 고딕", 11, "bold")).pack(anchor="w")
file_listbox = tk.Listbox(file_frame, font=("맑은 고딕", 10), height=10)
file_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

# 샘플 파일들
sample_files = ["project_plan.docx", "design_mockup.png", "database_schema.sql", 
                "user_manual.pdf", "source_code.py", "test_results.xlsx"]
for file in sample_files:
    file_listbox.insert(tk.END, file)

# 탭 2: 설정
tab2 = tk.Frame(notebook)
notebook.add(tab2, text="⚙️ 설정")

settings_frame = tk.LabelFrame(tab2, text="애플리케이션 설정", font=("맑은 고딕", 11, "bold"))
settings_frame.pack(fill=tk.X, padx=10, pady=10)

# 체크박스들
tk.Checkbutton(settings_frame, text="자동 저장 활성화", font=("맑은 고딕", 10)).pack(anchor="w", padx=20, pady=5)
tk.Checkbutton(settings_frame, text="알림 표시", font=("맑은 고딕", 10)).pack(anchor="w", padx=20, pady=5)
tk.Checkbutton(settings_frame, text="다크 모드", font=("맑은 고딕", 10)).pack(anchor="w", padx=20, pady=5)

# 탭 3: 통계
tab3 = tk.Frame(notebook)
notebook.add(tab3, text="📊 통계")

stats_text = """파일 처리 통계:

총 파일 수: 1,247개
처리 완료: 1,195개
오류 발생: 12개
대기 중: 40개

처리율: 95.8%
평균 처리 시간: 0.3초/파일"""

tk.Label(tab3, text=stats_text, font=("맑은 고딕", 11), justify="left", anchor="nw").pack(padx=20, pady=20, fill=tk.BOTH)

# 하단 상태바
status_frame = tk.Frame(main_frame, bg="lightgray", relief=tk.SUNKEN, bd=1)
status_frame.pack(fill=tk.X)

tk.Label(status_frame, text="준비됨", bg="lightgray", font=("맑은 고딕", 9)).pack(side=tk.LEFT, padx=10, pady=2)
tk.Label(status_frame, text="파일: 6개", bg="lightgray", font=("맑은 고딕", 9)).pack(side=tk.RIGHT, padx=10, pady=2)

root.mainloop()