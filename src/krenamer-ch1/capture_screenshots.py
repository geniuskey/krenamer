#!/usr/bin/env python3
"""
스크린샷 캡처 스크립트
각 챕터의 tkinter 예제를 실행하여 스크린샷을 생성합니다.
"""

import tkinter as tk
from tkinter import ttk
import time
from pathlib import Path
import sys

# PIL 설치 확인 및 설치
try:
    from PIL import ImageGrab, Image
except ImportError:
    print("PIL(Pillow) 라이브러리가 필요합니다. 설치중...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    from PIL import ImageGrab, Image


class ScreenshotCapture:
    """스크린샷 캡처를 위한 클래스"""
    
    def __init__(self):
        self.docs_images_path = Path(__file__).parent.parent.parent / "docs" / "images"
        self.docs_images_path.mkdir(exist_ok=True)
    
    def capture_chapter1_example(self):
        """Chapter 1 예제 스크린샷"""
        print("Chapter 1 screenshot generation...")
        
        # Chapter 1 스타일 GUI 만들기
        root = tk.Tk()
        root.title("KRenamer - Chapter 1: 기본 GUI 구조")
        root.geometry("700x500")
        root.configure(bg="#f0f0f0")
        
        # 윈도우를 화면 중앙에 배치
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
        
        # 파일 리스트박스와 스크롤바 프레임
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
        
        # 리스트박스와 스크롤바 배치
        files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 예시 파일들 추가
        example_files = [
            "문서1.txt",
            "이미지_001.jpg", 
            "프레젠테이션.pdf",
            "음악파일.mp3",
            "비디오_클립.mp4",
            "스프레드시트.xlsx",
            "README.md",
            "config.json"
        ]
        
        for file in example_files:
            files_listbox.insert(tk.END, file)
        
        # 버튼 프레임
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 15))
        
        # 버튼들
        add_button = ttk.Button(button_frame, text="파일 추가", width=12)
        add_button.pack(side=tk.LEFT, padx=(0, 10))
        
        remove_button = ttk.Button(button_frame, text="파일 제거", width=12)
        remove_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = ttk.Button(button_frame, text="전체 지우기", width=12)
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        rename_button = ttk.Button(button_frame, text="이름 변경", width=12)
        rename_button.pack(side=tk.LEFT)
        
        # 상태바
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        status_label = ttk.Label(
            status_frame, 
            text="KRenamer Chapter 1 - 기본 GUI 구조를 학습합니다.",
            font=("맑은 고딕", 9),
            foreground="gray"
        )
        status_label.pack(side=tk.LEFT)
        
        count_label = ttk.Label(
            status_frame,
            text="파일: 8개",
            font=("맑은 고딕", 9),
            foreground="blue"
        )
        count_label.pack(side=tk.RIGHT)
        
        # 그리드 가중치 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # 화면 업데이트 후 스크린샷
        root.update()
        time.sleep(0.5)  # UI가 완전히 렌더링되도록 대기
        
        # 윈도우 스크린샷 캡처
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        width = root.winfo_width()
        height = root.winfo_height()
        
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot.save(self.docs_images_path / "chapter1_screenshot.png")
        
        root.destroy()
        print("  chapter1_screenshot.png saved")
    
    def capture_chapter2_example(self):
        """Chapter 2 스타일 예제 스크린샷"""
        print("Chapter 2 screenshot generation...")
        
        root = tk.Tk()
        root.title("파일명 분석기")
        root.geometry("600x500")
        root.configure(bg="white")
        
        self.center_window(root, 600, 500)
        
        # 제목
        title_label = tk.Label(
            root,
            text="파일명 분석기",
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
        # 예시 텍스트 입력
        filename_entry.insert(0, "내 중요한 문서 (복사본).pdf")
        
        # 버튼 섹션
        button_frame = tk.Frame(root, bg="white")
        button_frame.pack(pady=10)
        
        analyze_button = tk.Button(
            button_frame,
            text="분석하기",
            font=("맑은 고딕", 12),
            bg="lightgreen",
            width=12
        )
        analyze_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = tk.Button(
            button_frame,
            text="초기화",
            font=("맑은 고딕", 12),
            bg="lightcoral",
            width=12
        )
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # 결과 표시 영역
        result_label = tk.Label(
            root,
            text="분석 결과:",
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
        sample_result = """파일명 분석 결과:

전체 파일명: 내 중요한 문서 (복사본).pdf
이름 부분: 내 중요한 문서 (복사본)
확장자: .pdf
총 글자 수: 18글자

변환 예시들:
• 소문자로: 내 중요한 문서 (복사본).pdf
• 대문자로: 내 중요한 문서 (복사본).PDF
• 공백 제거: 내_중요한_문서_(복사본).pdf
• 접두사 추가: NEW_내 중요한 문서 (복사본).pdf"""
        
        result_text.insert(tk.END, sample_result)
        
        root.update()
        time.sleep(0.5)
        
        # 스크린샷 캡처
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        width = root.winfo_width()
        height = root.winfo_height()
        
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot.save(self.docs_images_path / "chapter2_screenshot.png")
        
        root.destroy()
        print("  chapter2_screenshot.png saved")
    
    def capture_modern_gui_example(self):
        """현대적인 GUI 예제 스크린샷"""
        print("Modern GUI screenshot generation...")
        
        root = tk.Tk()
        root.title("현대적인 KRenamer 미리보기")
        root.geometry("800x600")
        root.configure(bg="#f0f0f0")
        
        self.center_window(root, 800, 600)
        
        # 스타일 설정
        style = ttk.Style()
        style.theme_use('clam')
        
        # 메인 컨테이너
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목 영역
        title_frame = ttk.LabelFrame(main_frame, text="KRenamer - 파일명 변경 도구", padding="10")
        title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        welcome_label = ttk.Label(
            title_frame,
            text="KRenamer에 오신 것을 환영합니다!",
            font=("맑은 고딕", 14, "bold")
        )
        welcome_label.pack()
        
        # 왼쪽 패널 - 파일 목록
        left_frame = ttk.LabelFrame(main_frame, text="파일 목록", padding="10")
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
        file_tree.insert('', tk.END, text='문서1.pdf', values=('1.2MB', 'PDF'))
        file_tree.insert('', tk.END, text='사진1.jpg', values=('2.5MB', 'IMAGE'))
        file_tree.insert('', tk.END, text='음악1.mp3', values=('4.1MB', 'AUDIO'))
        file_tree.insert('', tk.END, text='메모.txt', values=('1KB', 'TEXT'))
        
        # 오른쪽 패널 - 설정 및 미리보기
        right_frame = ttk.LabelFrame(main_frame, text="변경 설정", padding="10")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # 탭 위젯으로 설정 구분
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 탭 1: 기본 설정
        basic_tab = ttk.Frame(notebook)
        notebook.add(basic_tab, text='기본 설정')
        
        # 접두사 설정
        ttk.Label(basic_tab, text="접두사:").grid(row=0, column=0, sticky=tk.W, pady=5)
        prefix_entry = ttk.Entry(basic_tab, width=20)
        prefix_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        prefix_entry.insert(0, "NEW_")
        
        # 접미사 설정
        ttk.Label(basic_tab, text="접미사:").grid(row=1, column=0, sticky=tk.W, pady=5)
        suffix_entry = ttk.Entry(basic_tab, width=20)
        suffix_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        suffix_entry.insert(0, "_COPY")
        
        # 옵션 체크박스들
        ttk.Label(basic_tab, text="옵션:").grid(row=2, column=0, sticky=tk.W, pady=(15, 5))
        
        ttk.Checkbutton(basic_tab, text="소문자로 변환").grid(row=3, column=0, columnspan=2, sticky=tk.W)
        ttk.Checkbutton(basic_tab, text="공백 제거").grid(row=4, column=0, columnspan=2, sticky=tk.W)
        ttk.Checkbutton(basic_tab, text="순번 추가").grid(row=5, column=0, columnspan=2, sticky=tk.W)
        
        # 탭 2: 미리보기
        preview_tab = ttk.Frame(notebook)
        notebook.add(preview_tab, text='미리보기')
        
        ttk.Label(preview_tab, text="변경 결과 미리보기:").pack(anchor=tk.W, pady=(0, 5))
        
        preview_text = tk.Text(preview_tab, height=10, width=30, font=("맑은 고딕", 9))
        preview_text.pack(fill=tk.BOTH, expand=True)
        
        # 샘플 미리보기 텍스트
        preview_content = """문서1.pdf → NEW_문서1_COPY.pdf
사진1.jpg → NEW_사진1_COPY.jpg  
음악1.mp3 → NEW_음악1_COPY.mp3
메모.txt → NEW_메모_COPY.txt

4개 파일이 변경됩니다."""
        preview_text.insert(tk.END, preview_content)
        
        # 하단 버튼 영역
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 진행률 표시
        progress_bar = ttk.Progressbar(bottom_frame, maximum=100, value=0)
        progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # 실행 버튼들
        ttk.Button(bottom_frame, text="미리보기", width=12).pack(side=tk.RIGHT, padx=2)
        ttk.Button(bottom_frame, text="실행하기", width=12).pack(side=tk.RIGHT, padx=2)
        ttk.Button(bottom_frame, text="초기화", width=12).pack(side=tk.RIGHT, padx=2)
        
        # 그리드 가중치 설정
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        root.update()
        time.sleep(0.5)
        
        # 스크린샷 캡처
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        width = root.winfo_width()
        height = root.winfo_height()
        
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot.save(self.docs_images_path / "modern_gui_screenshot.png")
        
        root.destroy()
        print("  modern_gui_screenshot.png saved")
    
    def center_window(self, window, width, height):
        """윈도우를 화면 중앙에 배치"""
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def capture_all_screenshots(self):
        """모든 스크린샷 캡처"""
        print("tkinter screenshot generation started...")
        
        try:
            self.capture_chapter1_example()
            self.capture_chapter2_example()
            self.capture_modern_gui_example()
            
            print(f"\nAll screenshots generated successfully! ({self.docs_images_path})")
            
            # 생성된 스크린샷 파일 목록 출력
            print("\nGenerated screenshot files:")
            for img_file in self.docs_images_path.glob("*screenshot*.png"):
                print(f"  - {img_file.name}")
                
        except Exception as e:
            print(f"Error during screenshot generation: {e}")


if __name__ == "__main__":
    try:
        capturer = ScreenshotCapture()
        capturer.capture_all_screenshots()
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Please check if PIL (Pillow) is installed: pip install pillow")