#!/usr/bin/env python3
"""
Chapter 3-6 GUI 진화 스크린샷 캡처
각 챕터별 GUI 변화를 보여주는 스크린샷 생성
"""

import tkinter as tk
from tkinter import ttk
import time
from pathlib import Path
import sys

try:
    from PIL import ImageGrab, Image
except ImportError:
    print("PIL(Pillow) 라이브러리가 필요합니다. 설치중...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    from PIL import ImageGrab, Image


class ChapterProgressionCapture:
    """챕터별 GUI 진화 스크린샷 캡처"""
    
    def __init__(self):
        self.docs_images_path = Path(__file__).parent.parent.parent / "docs" / "images"
        self.docs_images_path.mkdir(exist_ok=True)
    
    def center_window(self, window, width, height):
        """윈도우를 화면 중앙에 배치"""
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
        
        # 창을 맨 앞으로 가져오기
        window.lift()
        window.attributes('-topmost', True)
        window.after_idle(window.attributes, '-topmost', False)
        window.focus_force()
    
    def capture_chapter3_basic_gui(self):
        """Chapter 3: BasicKRenamerGUI - 기본 GUI 구조"""
        print("Chapter 3: Basic GUI structure screenshot...")
        
        root = tk.Tk()
        root.title("KRenamer - Chapter 3: 기본 GUI 구조")
        root.geometry("700x500")
        root.configure(bg="#f0f0f0")
        
        self.center_window(root, 700, 500)
        
        # 메인 프레임
        main_frame = ttk.Frame(root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 파일 목록 라벨
        files_label = ttk.Label(
            main_frame, 
            text="파일 목록:", 
            font=("맑은 고딕", 10, "bold")
        )
        files_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # 파일 리스트박스 프레임
        listbox_frame = ttk.Frame(main_frame)
        listbox_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # 파일 리스트박스
        files_listbox = tk.Listbox(
            listbox_frame, 
            height=15,
            font=("맑은 고딕", 9),
            selectmode=tk.EXTENDED
        )
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=files_listbox.yview)
        files_listbox.config(yscrollcommand=scrollbar.set)
        
        files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 기본 예시 파일들
        basic_files = [
            "문서1.txt",
            "이미지_001.jpg", 
            "프레젠테이션.pdf",
            "음악파일.mp3"
        ]
        
        for file in basic_files:
            files_listbox.insert(tk.END, file)
        
        # 기본 버튼들
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 15))
        
        ttk.Button(button_frame, text="파일 추가", width=12).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="파일 제거", width=12).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="전체 지우기", width=12).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="이름 변경", width=12).pack(side=tk.LEFT)
        
        # 상태바
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(status_frame, text="KRenamer Chapter 3 - 기본 GUI 구조", 
                 font=("맑은 고딕", 9), foreground="gray").pack(side=tk.LEFT)
        ttk.Label(status_frame, text="파일: 4개", 
                 font=("맑은 고딕", 9), foreground="blue").pack(side=tk.RIGHT)
        
        # 그리드 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        root.update()
        time.sleep(1.0)  # 대기 시간 증가
        
        # 스크린샷 캡처
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        width = root.winfo_width()
        height = root.winfo_height()
        
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot.save(self.docs_images_path / "chapter3_basic_gui.png")
        
        root.destroy()
        print("  chapter3_basic_gui.png saved")
    
    def capture_chapter4_dragdrop_gui(self):
        """Chapter 4: DragDropRenamerGUI - 드래그앤드롭 기능 추가"""
        print("Chapter 4: Drag & Drop GUI screenshot...")
        
        root = tk.Tk()
        root.title("KRenamer - Chapter 4: 드래그 앤 드롭 기능")
        root.geometry("750x550")
        root.configure(bg="#f0f0f0")
        
        self.center_window(root, 750, 550)
        
        # 메인 프레임
        main_frame = ttk.Frame(root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(
            main_frame,
            text="KRenamer - 파일명 변경 도구",
            font=("맑은 고딕", 14, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # 드래그 앤 드롭 안내
        drop_frame = ttk.LabelFrame(main_frame, text="파일 추가", padding="10")
        drop_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        drop_label = tk.Label(
            drop_frame,
            text="파일을 여기에 드래그 앤 드롭하세요",
            font=("맑은 고딕", 11),
            bg="#e8f4fd",
            fg="#0066cc",
            relief="ridge",
            bd=2,
            height=3
        )
        drop_label.pack(fill=tk.X)
        
        # 파일 정보 표시를 위한 Treeview
        files_frame = ttk.LabelFrame(main_frame, text="파일 목록", padding="10")
        files_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # Treeview 생성
        tree = ttk.Treeview(files_frame, columns=('size', 'type'), show='tree headings', height=10)
        tree.heading('#0', text='파일명')
        tree.heading('size', text='크기')
        tree.heading('type', text='종류')
        
        tree.column('#0', width=300)
        tree.column('size', width=100)
        tree.column('type', width=100)
        
        # 스크롤바
        tree_scroll = ttk.Scrollbar(files_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 샘플 파일 데이터
        sample_files = [
            ("보고서_2024.pdf", "1.2MB", "PDF"),
            ("프로젝트_사진.jpg", "2.5MB", "IMAGE"),
            ("회의록_최종.docx", "456KB", "WORD"),
            ("데이터_분석.xlsx", "3.1MB", "EXCEL"),
            ("프레젠테이션.pptx", "8.7MB", "PPT"),
            ("README.md", "2KB", "TEXT")
        ]
        
        for filename, size, filetype in sample_files:
            tree.insert('', tk.END, text=filename, values=(size, filetype))
        
        # 향상된 버튼들
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 15))
        
        ttk.Button(button_frame, text="폴더 추가", width=12).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="선택 제거", width=12).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="모두 제거", width=12).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="미리보기", width=12).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="이름 변경", width=12).pack(side=tk.LEFT)
        
        # 향상된 상태바
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(status_frame, text="드래그 앤 드롭으로 파일을 추가하세요", 
                 font=("맑은 고딕", 9), foreground="gray").pack(side=tk.LEFT)
        ttk.Label(status_frame, text="파일: 6개 | 총 크기: 16.1MB", 
                 font=("맑은 고딕", 9), foreground="blue").pack(side=tk.RIGHT)
        
        # 그리드 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        root.update()
        time.sleep(1.0)  # 대기 시간 증가
        
        # 스크린샷 캡처
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        width = root.winfo_width()
        height = root.winfo_height()
        
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot.save(self.docs_images_path / "chapter4_dragdrop_gui.png")
        
        root.destroy()
        print("  chapter4_dragdrop_gui.png saved")
    
    def capture_chapter5_rename_gui(self):
        """Chapter 5: RenamerGUI - 파일명 변경 로직과 미리보기"""
        print("Chapter 5: Rename logic GUI screenshot...")
        
        root = tk.Tk()
        root.title("KRenamer - Chapter 5: 파일명 변경 로직")
        root.geometry("900x650")
        root.configure(bg="#f0f0f0")
        
        self.center_window(root, 900, 650)
        
        # 메인 프레임
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(
            main_frame,
            text="KRenamer - 파일명 변경 도구",
            font=("맑은 고딕", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # 왼쪽: 파일 목록
        left_frame = ttk.LabelFrame(main_frame, text="파일 목록", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # 파일 리스트
        files_tree = ttk.Treeview(left_frame, columns=('size',), show='tree headings', height=15)
        files_tree.heading('#0', text='파일명')
        files_tree.heading('size', text='크기')
        files_tree.column('#0', width=250)
        files_tree.column('size', width=80)
        
        files_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=files_tree.yview)
        files_tree.configure(yscrollcommand=files_scroll.set)
        
        files_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        files_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 샘플 데이터
        for i, (name, size) in enumerate([
            ("project_report.pdf", "1.2MB"),
            ("meeting_notes.docx", "456KB"),
            ("presentation.pptx", "2.8MB"),
            ("data_analysis.xlsx", "890KB"),
            ("photo_001.jpg", "3.2MB"),
            ("photo_002.jpg", "2.9MB")
        ]):
            files_tree.insert('', tk.END, text=name, values=(size,))
        
        # 중앙: 설정 패널
        settings_frame = ttk.LabelFrame(main_frame, text="이름 변경 설정", padding="10")
        settings_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # 접두사/접미사
        ttk.Label(settings_frame, text="접두사:").grid(row=0, column=0, sticky=tk.W, pady=2)
        prefix_entry = ttk.Entry(settings_frame, width=20)
        prefix_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        prefix_entry.insert(0, "NEW_")
        
        ttk.Label(settings_frame, text="접미사:").grid(row=1, column=0, sticky=tk.W, pady=2)
        suffix_entry = ttk.Entry(settings_frame, width=20)
        suffix_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        suffix_entry.insert(0, "_COPY")
        
        # 찾기/바꾸기
        ttk.Separator(settings_frame, orient=tk.HORIZONTAL).grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(settings_frame, text="찾기:").grid(row=3, column=0, sticky=tk.W, pady=2)
        find_entry = ttk.Entry(settings_frame, width=20)
        find_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        find_entry.insert(0, "_")
        
        ttk.Label(settings_frame, text="바꾸기:").grid(row=4, column=0, sticky=tk.W, pady=2)
        replace_entry = ttk.Entry(settings_frame, width=20)
        replace_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        replace_entry.insert(0, "-")
        
        # 옵션들
        ttk.Separator(settings_frame, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Checkbutton(settings_frame, text="순번 매기기").grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=2)
        ttk.Checkbutton(settings_frame, text="소문자로 변환").grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=2)
        ttk.Checkbutton(settings_frame, text="정규식 사용").grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # 미리보기 버튼
        ttk.Button(settings_frame, text="미리보기 생성").grid(row=9, column=0, columnspan=2, pady=(15, 5))
        
        # 오른쪽: 미리보기 결과
        preview_frame = ttk.LabelFrame(main_frame, text="미리보기", padding="10")
        preview_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # 미리보기 트리
        preview_tree = ttk.Treeview(preview_frame, columns=('new_name',), show='tree headings', height=15)
        preview_tree.heading('#0', text='원본 이름')
        preview_tree.heading('new_name', text='새 이름')
        preview_tree.column('#0', width=200)
        preview_tree.column('new_name', width=200)
        
        preview_scroll = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=preview_tree.yview)
        preview_tree.configure(yscrollcommand=preview_scroll.set)
        
        preview_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 미리보기 샘플 데이터
        preview_samples = [
            ("project_report.pdf", "NEW_project-report_COPY.pdf"),
            ("meeting_notes.docx", "NEW_meeting-notes_COPY.docx"),
            ("presentation.pptx", "NEW_presentation_COPY.pptx"),
            ("data_analysis.xlsx", "NEW_data-analysis_COPY.xlsx"),
            ("photo_001.jpg", "NEW_photo-001_COPY.jpg"),
            ("photo_002.jpg", "NEW_photo-002_COPY.jpg")
        ]
        
        for orig, new in preview_samples:
            preview_tree.insert('', tk.END, text=orig, values=(new,))
        
        # 하단 버튼들
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=2, column=0, columnspan=3, pady=(15, 0))
        
        ttk.Button(bottom_frame, text="파일 추가").pack(side=tk.LEFT, padx=2)
        ttk.Button(bottom_frame, text="선택 제거").pack(side=tk.LEFT, padx=2)
        ttk.Button(bottom_frame, text="설정 저장").pack(side=tk.LEFT, padx=2)
        ttk.Button(bottom_frame, text="설정 불러오기").pack(side=tk.LEFT, padx=2)
        
        # 진행률 표시
        progress = ttk.Progressbar(bottom_frame, length=200, mode='determinate')
        progress.pack(side=tk.LEFT, padx=(20, 10))
        progress['value'] = 0
        
        ttk.Button(bottom_frame, text="이름 변경 실행", style="Accent.TButton").pack(side=tk.RIGHT, padx=2)
        
        # 상태바
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(status_frame, text="미리보기가 생성되었습니다. 이름 변경을 실행하려면 '이름 변경 실행' 버튼을 클릭하세요.", 
                 font=("맑은 고딕", 9), foreground="green").pack(side=tk.LEFT)
        ttk.Label(status_frame, text="파일: 6개 | 변경 예정: 6개", 
                 font=("맑은 고딕", 9), foreground="blue").pack(side=tk.RIGHT)
        
        # 그리드 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        root.update()
        time.sleep(1.0)  # 대기 시간 증가
        
        # 스크린샷 캡처
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        width = root.winfo_width()
        height = root.winfo_height()
        
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot.save(self.docs_images_path / "chapter5_rename_gui.png")
        
        root.destroy()
        print("  chapter5_rename_gui.png saved")
    
    def capture_chapter6_advanced_gui(self):
        """Chapter 6: AdvancedRenamerGUI - 고급 조건과 필터링"""
        print("Chapter 6: Advanced GUI screenshot...")
        
        root = tk.Tk()
        root.title("KRenamer - Chapter 6: 고급 조건과 기능")
        root.geometry("1000x700")
        root.configure(bg="#f0f0f0")
        
        self.center_window(root, 1000, 700)
        
        # 메인 프레임
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목과 메뉴바 영역
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        title_label = ttk.Label(
            header_frame,
            text="KRenamer Pro - 고급 파일명 변경 도구",
            font=("맑은 고딕", 16, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        # 툴바
        toolbar_frame = ttk.Frame(header_frame)
        toolbar_frame.pack(side=tk.RIGHT)
        ttk.Button(toolbar_frame, text="설정", width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="도움말", width=8).pack(side=tk.LEFT, padx=2)
        
        # 메인 컨텐츠 영역
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 탭 위젯
        notebook = ttk.Notebook(content_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 탭 1: 파일 관리
        files_tab = ttk.Frame(notebook)
        notebook.add(files_tab, text='파일 관리')
        
        # 파일 관리 영역을 3열로 분할
        files_paned = ttk.PanedWindow(files_tab, orient=tk.HORIZONTAL)
        files_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 파일 목록 (왼쪽)
        files_frame = ttk.LabelFrame(files_paned, text="파일 목록 (필터 적용됨)", padding="5")
        files_paned.add(files_frame, weight=2)
        
        files_tree = ttk.Treeview(files_frame, columns=('size', 'date', 'type'), show='tree headings', height=18)
        files_tree.heading('#0', text='파일명')
        files_tree.heading('size', text='크기')
        files_tree.heading('date', text='수정일')
        files_tree.heading('type', text='형식')
        
        files_tree.column('#0', width=200)
        files_tree.column('size', width=80)
        files_tree.column('date', width=100)
        files_tree.column('type', width=60)
        
        files_tree.pack(fill=tk.BOTH, expand=True)
        
        # 필터 샘플 데이터 (필터링 된 결과)
        filtered_files = [
            ("report_2024.pdf", "1.2MB", "2024-01-15", "PDF"),
            ("analysis_2024.xlsx", "890KB", "2024-01-20", "XLSX"),
            ("presentation_2024.pptx", "2.8MB", "2024-02-01", "PPTX"),
            ("summary_2024.docx", "456KB", "2024-02-10", "DOCX")
        ]
        
        for name, size, date, ftype in filtered_files:
            files_tree.insert('', tk.END, text=name, values=(size, date, ftype))
        
        # 필터 조건 (중앙)
        filter_frame = ttk.LabelFrame(files_paned, text="필터 조건", padding="5")
        files_paned.add(filter_frame, weight=1)
        
        # 크기 필터
        ttk.Label(filter_frame, text="파일 크기 필터:", font=("맑은 고딕", 9, "bold")).pack(anchor=tk.W, pady=(0, 5))
        size_frame = ttk.Frame(filter_frame)
        size_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(size_frame, text="최소:").grid(row=0, column=0, sticky=tk.W)
        min_size = ttk.Entry(size_frame, width=10)
        min_size.grid(row=0, column=1, padx=2)
        min_size.insert(0, "100KB")
        
        ttk.Label(size_frame, text="최대:").grid(row=1, column=0, sticky=tk.W)
        max_size = ttk.Entry(size_frame, width=10)
        max_size.grid(row=1, column=1, padx=2)
        max_size.insert(0, "10MB")
        
        # 날짜 필터
        ttk.Label(filter_frame, text="수정일 필터:", font=("맑은 고딕", 9, "bold")).pack(anchor=tk.W, pady=(10, 5))
        date_frame = ttk.Frame(filter_frame)
        date_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Checkbutton(date_frame, text="최근 30일").pack(anchor=tk.W)
        ttk.Checkbutton(date_frame, text="2024년").pack(anchor=tk.W)
        
        # 확장자 필터
        ttk.Label(filter_frame, text="파일 형식:", font=("맑은 고딕", 9, "bold")).pack(anchor=tk.W, pady=(10, 5))
        ext_frame = ttk.Frame(filter_frame)
        ext_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Checkbutton(ext_frame, text="문서 (.pdf, .docx)").pack(anchor=tk.W)
        ttk.Checkbutton(ext_frame, text="스프레드시트 (.xlsx)").pack(anchor=tk.W)
        ttk.Checkbutton(ext_frame, text="프레젠테이션 (.pptx)").pack(anchor=tk.W)
        
        ttk.Button(filter_frame, text="필터 적용").pack(pady=(15, 5), fill=tk.X)
        ttk.Button(filter_frame, text="필터 초기화").pack(pady=2, fill=tk.X)
        
        # 미리보기 (오른쪽)
        preview_frame = ttk.LabelFrame(files_paned, text="변경 미리보기", padding="5")
        files_paned.add(preview_frame, weight=2)
        
        preview_tree = ttk.Treeview(preview_frame, columns=('new_name', 'status'), show='tree headings', height=18)
        preview_tree.heading('#0', text='현재 이름')
        preview_tree.heading('new_name', text='새 이름')
        preview_tree.heading('status', text='상태')
        
        preview_tree.column('#0', width=180)
        preview_tree.column('new_name', width=180)
        preview_tree.column('status', width=60)
        
        preview_tree.pack(fill=tk.BOTH, expand=True)
        
        # 미리보기 데이터
        for orig, size, date, ftype in filtered_files:
            new_name = f"FILTERED_{orig}"
            preview_tree.insert('', tk.END, text=orig, values=(new_name, "OK"))
        
        # 탭 2: 고급 설정
        advanced_tab = ttk.Frame(notebook)
        notebook.add(advanced_tab, text='고급 설정')
        
        # 고급 설정 내용
        adv_frame = ttk.Frame(advanced_tab)
        adv_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 프리셋 관리
        preset_frame = ttk.LabelFrame(adv_frame, text="설정 프리셋", padding="10")
        preset_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5), pady=(0, 5))
        
        ttk.Label(preset_frame, text="저장된 프리셋:").pack(anchor=tk.W)
        preset_combo = ttk.Combobox(preset_frame, values=["기본 설정", "문서 정리", "사진 정리", "백업 파일"])
        preset_combo.pack(fill=tk.X, pady=2)
        preset_combo.set("문서 정리")
        
        preset_btn_frame = ttk.Frame(preset_frame)
        preset_btn_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Button(preset_btn_frame, text="불러오기").pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(preset_btn_frame, text="저장").pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_btn_frame, text="삭제").pack(side=tk.LEFT, padx=2)
        
        # 히스토리 관리
        history_frame = ttk.LabelFrame(adv_frame, text="작업 히스토리", padding="10")
        history_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0), pady=(0, 5))
        
        history_list = tk.Listbox(history_frame, height=8)
        history_list.pack(fill=tk.BOTH, expand=True)
        
        history_items = [
            "2024-01-15 14:30 - 12개 파일 이름 변경",
            "2024-01-15 09:15 - 8개 파일 접두사 추가",
            "2024-01-14 16:45 - 25개 파일 번호 매기기",
            "2024-01-14 11:20 - 15개 파일 확장자 변경"
        ]
        
        for item in history_items:
            history_list.insert(tk.END, item)
        
        ttk.Button(history_frame, text="실행 취소").pack(fill=tk.X, pady=(5, 0))
        
        # 탭 3: 통계
        stats_tab = ttk.Frame(notebook)
        notebook.add(stats_tab, text='통계')
        
        stats_frame = ttk.Frame(stats_tab)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(stats_frame, text="파일 처리 통계", font=("맑은 고딕", 14, "bold")).pack(pady=(0, 10))
        
        stats_info = [
            "현재 로드된 파일: 4개",
            "필터 조건에 맞는 파일: 4개",
            "변경 예정 파일: 4개",
            "예상 소요 시간: 2초",
            "",
            "총 처리된 파일 (전체): 157개",
            "성공한 작업: 155개",
            "실패한 작업: 2개",
            "평균 처리 시간: 1.2초/파일"
        ]
        
        for info in stats_info:
            ttk.Label(stats_frame, text=info, font=("맑은 고딕", 10)).pack(anchor=tk.W, pady=1)
        
        # 하단 제어 패널
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 왼쪽 버튼들
        left_buttons = ttk.Frame(control_frame)
        left_buttons.pack(side=tk.LEFT)
        
        ttk.Button(left_buttons, text="파일 추가").pack(side=tk.LEFT, padx=2)
        ttk.Button(left_buttons, text="폴더 추가").pack(side=tk.LEFT, padx=2)
        ttk.Button(left_buttons, text="선택 제거").pack(side=tk.LEFT, padx=2)
        ttk.Button(left_buttons, text="모두 제거").pack(side=tk.LEFT, padx=2)
        
        # 오른쪽 실행 버튼들
        right_buttons = ttk.Frame(control_frame)
        right_buttons.pack(side=tk.RIGHT)
        
        # 진행률 표시
        progress_frame = ttk.Frame(right_buttons)
        progress_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(progress_frame, text="진행률:").pack()
        progress = ttk.Progressbar(progress_frame, length=150, mode='determinate')
        progress.pack()
        progress['value'] = 0
        
        ttk.Button(right_buttons, text="미리보기 생성").pack(side=tk.LEFT, padx=2)
        ttk.Button(right_buttons, text="실행", style="Accent.TButton").pack(side=tk.LEFT, padx=2)
        
        # 상태바
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Separator(status_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 5))
        
        status_text = ttk.Label(status_frame, 
                               text="필터 조건이 적용되었습니다. 4개 파일이 조건에 맞습니다. 미리보기를 확인하고 실행하세요.", 
                               font=("맑은 고딕", 9), foreground="green")
        status_text.pack(side=tk.LEFT)
        
        file_count = ttk.Label(status_frame, text="총 파일: 4개 | 필터됨: 4개 | 변경 예정: 4개", 
                              font=("맑은 고딕", 9), foreground="blue")
        file_count.pack(side=tk.RIGHT)
        
        # 그리드 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        root.update()
        time.sleep(1.0)  # 대기 시간 증가
        
        # 스크린샷 캡처
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        width = root.winfo_width()
        height = root.winfo_height()
        
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot.save(self.docs_images_path / "chapter6_advanced_gui.png")
        
        root.destroy()
        print("  chapter6_advanced_gui.png saved")
    
    def capture_all_progression_screenshots(self):
        """모든 챕터 진화 스크린샷 캡처"""
        print("Chapter 3-6 GUI progression screenshots generation started...")
        
        try:
            self.capture_chapter3_basic_gui()
            self.capture_chapter4_dragdrop_gui()
            self.capture_chapter5_rename_gui()
            self.capture_chapter6_advanced_gui()
            
            print(f"\nAll chapter progression screenshots generated! ({self.docs_images_path})")
            
            # 생성된 스크린샷 파일 목록 출력
            print("\nGenerated chapter progression screenshots:")
            chapter_screenshots = [
                "chapter3_basic_gui.png",
                "chapter4_dragdrop_gui.png", 
                "chapter5_rename_gui.png",
                "chapter6_advanced_gui.png"
            ]
            
            for screenshot in chapter_screenshots:
                screenshot_path = self.docs_images_path / screenshot
                if screenshot_path.exists():
                    print(f"  - {screenshot}")
                
        except Exception as e:
            print(f"Error during screenshot generation: {e}")


if __name__ == "__main__":
    try:
        capturer = ChapterProgressionCapture()
        capturer.capture_all_progression_screenshots()
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Please check if PIL (Pillow) is installed: pip install pillow")