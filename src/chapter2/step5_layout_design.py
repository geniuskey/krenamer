import tkinter as tk
from tkinter import ttk  # 더 예쁜 위젯들

def create_modern_gui():
    """현대적인 GUI 만들기"""
    
    root = tk.Tk()
    root.title("현대적인 KRenamer 미리보기")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")
    
    # 스타일 설정
    style = ttk.Style()
    style.theme_use('clam')  # 모던한 테마
    
    # 메인 컨테이너
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # 제목 영역 (1행)
    title_frame = ttk.LabelFrame(main_frame, text="KRenamer - 파일명 변경 도구", padding="10")
    title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
    
    welcome_label = ttk.Label(
        title_frame,
        text="🎉 KRenamer에 오신 것을 환영합니다!",
        font=("맑은 고딕", 14, "bold")
    )
    welcome_label.pack()
    
    # 왼쪽 패널 - 파일 목록 (2행, 1열)
    left_frame = ttk.LabelFrame(main_frame, text="📂 파일 목록", padding="10")
    left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
    
    # 파일 목록 (Treeview 사용)
    file_tree = ttk.Treeview(left_frame, columns=('size', 'type'), show='tree headings', height=15)
    file_tree.heading('#0', text='파일명')
    file_tree.heading('size', text='크기')
    file_tree.heading('type', text='종류')
    
    file_tree.column('#0', width=200)
    file_tree.column('size', width=80)
    file_tree.column('type', width=80)
    
    # 스크롤바 추가
    tree_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=file_tree.yview)
    file_tree.configure(yscrollcommand=tree_scroll.set)
    
    file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    # 샘플 데이터 추가
    file_tree.insert('', tk.END, text='📄 문서1.pdf', values=('1.2MB', 'PDF'))
    file_tree.insert('', tk.END, text='🖼️ 사진1.jpg', values=('2.5MB', 'IMAGE'))
    file_tree.insert('', tk.END, text='🎵 음악1.mp3', values=('4.1MB', 'AUDIO'))
    file_tree.insert('', tk.END, text='📝 메모.txt', values=('1KB', 'TEXT'))
    
    # 오른쪽 패널 - 설정 및 미리보기 (2행, 2열)
    right_frame = ttk.LabelFrame(main_frame, text="⚙️ 변경 설정", padding="10")
    right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
    
    # 탭 위젯으로 설정 구분
    notebook = ttk.Notebook(right_frame)
    notebook.pack(fill=tk.BOTH, expand=True)
    
    # 탭 1: 기본 설정
    basic_tab = ttk.Frame(notebook)
    notebook.add(basic_tab, text='기본 설정')
    
    # 접두사 설정
    ttk.Label(basic_tab, text="접두사:").grid(row=0, column=0, sticky=tk.W, pady=5)
    prefix_var = tk.StringVar(value="NEW_")
    prefix_entry = ttk.Entry(basic_tab, textvariable=prefix_var, width=20)
    prefix_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
    
    # 접미사 설정
    ttk.Label(basic_tab, text="접미사:").grid(row=1, column=0, sticky=tk.W, pady=5)
    suffix_var = tk.StringVar(value="_COPY")
    suffix_entry = ttk.Entry(basic_tab, textvariable=suffix_var, width=20)
    suffix_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
    
    # 옵션 체크박스들
    ttk.Label(basic_tab, text="옵션:").grid(row=2, column=0, sticky=tk.W, pady=(15, 5))
    
    lowercase_var = tk.BooleanVar()
    ttk.Checkbutton(basic_tab, text="소문자로 변환", variable=lowercase_var).grid(row=3, column=0, columnspan=2, sticky=tk.W)
    
    remove_spaces_var = tk.BooleanVar()
    ttk.Checkbutton(basic_tab, text="공백 제거", variable=remove_spaces_var).grid(row=4, column=0, columnspan=2, sticky=tk.W)
    
    add_numbers_var = tk.BooleanVar()
    ttk.Checkbutton(basic_tab, text="순번 추가", variable=add_numbers_var).grid(row=5, column=0, columnspan=2, sticky=tk.W)
    
    # 탭 2: 미리보기
    preview_tab = ttk.Frame(notebook)
    notebook.add(preview_tab, text='미리보기')
    
    ttk.Label(preview_tab, text="변경 결과 미리보기:").pack(anchor=tk.W, pady=(0, 5))
    
    preview_text = tk.Text(preview_tab, height=10, width=30, font=("맑은 고딕", 9))
    preview_text.pack(fill=tk.BOTH, expand=True)
    
    # 샘플 미리보기 텍스트
    preview_text.insert(tk.END, """📄 문서1.pdf → NEW_문서1_COPY.pdf
🖼️ 사진1.jpg → NEW_사진1_COPY.jpg  
🎵 음악1.mp3 → NEW_음악1_COPY.mp3
📝 메모.txt → NEW_메모_COPY.txt

✨ 4개 파일이 변경됩니다.""")
    
    # 하단 버튼 영역 (3행)
    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    # 진행률 표시
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(bottom_frame, variable=progress_var, maximum=100)
    progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    
    # 실행 버튼들
    ttk.Button(bottom_frame, text="미리보기 🔍", width=12).pack(side=tk.RIGHT, padx=2)
    ttk.Button(bottom_frame, text="실행하기 ▶️", width=12).pack(side=tk.RIGHT, padx=2)
    ttk.Button(bottom_frame, text="초기화 🔄", width=12).pack(side=tk.RIGHT, padx=2)
    
    # 그리드 가중치 설정 (창 크기 변경시 반응형으로)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(1, weight=1)
    
    return root

# 프로그램 실행
if __name__ == "__main__":
    print("🎨 현대적인 GUI 데모를 시작합니다!")
    app = create_modern_gui()
    app.mainloop()
    print("프로그램이 종료되었습니다.")