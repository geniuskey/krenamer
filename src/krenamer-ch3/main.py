#!/usr/bin/env python3
"""
KRenamer Chapter 2: Basic Tkinter GUI Structure
기본적인 tkinter 윈도우를 생성하는 예제

이 챕터에서는 KRenamer의 기본 GUI 구조를 배웁니다:
- tkinter 기본 위젯 사용법
- 윈도우 레이아웃 설계
- 기본적인 이벤트 처리
"""

import tkinter as tk
from tkinter import ttk


class BasicKRenamerGUI:
    """
    KRenamer Chapter 1: 기본 GUI 구조
    
    이 클래스는 파일 리네이머의 기본적인 GUI 구조를 구현합니다.
    실제 파일 처리 기능은 다음 챕터에서 추가됩니다.
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_widgets()
    
    def setup_window(self):
        """윈도우 기본 설정"""
        self.root.title("KRenamer - Chapter 1: 기본 GUI 구조")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # 윈도우를 화면 중앙에 배치
        self.center_window()
        
        # 윈도우 최소 크기 설정
        self.root.minsize(600, 400)
    
    def center_window(self):
        """윈도우를 화면 중앙에 배치"""
        self.root.update_idletasks()
        width = 700
        height = 500
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_widgets(self):
        """GUI 위젯들 설정 및 배치"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 파일 목록 영역 라벨
        files_label = ttk.Label(
            main_frame, 
            text="파일 목록:", 
            font=("맑은 고딕", 10, "bold")
        )
        files_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # 파일 목록 프레임 (리스트박스 + 스크롤바)
        listbox_frame = ttk.Frame(main_frame)
        listbox_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # 파일 리스트박스
        self.files_listbox = tk.Listbox(
            listbox_frame, 
            height=15,
            font=("맑은 고딕", 9),
            selectmode=tk.EXTENDED  # 다중 선택 가능
        )
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        self.files_listbox.config(yscrollcommand=scrollbar.set)
        
        # 리스트박스와 스크롤바 배치
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 버튼 프레임
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 15))
        
        # 파일 추가 버튼
        self.add_button = ttk.Button(
            button_frame, 
            text="파일 추가", 
            command=self.add_files,
            width=12
        )
        self.add_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 파일 제거 버튼
        self.remove_button = ttk.Button(
            button_frame, 
            text="파일 제거", 
            command=self.remove_files,
            width=12
        )
        self.remove_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 전체 지우기 버튼
        self.clear_button = ttk.Button(
            button_frame, 
            text="전체 지우기", 
            command=self.clear_files,
            width=12
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 이름 변경 버튼
        self.rename_button = ttk.Button(
            button_frame, 
            text="이름 변경", 
            command=self.rename_files,
            width=12
        )
        self.rename_button.pack(side=tk.LEFT)
        
        # 상태바
        self.status_var = tk.StringVar()
        self.status_var.set("KRenamer Chapter 1 - 기본 GUI 구조를 학습합니다.")
        
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        status_label = ttk.Label(
            status_frame, 
            textvariable=self.status_var,
            font=("맑은 고딕", 9),
            foreground="gray"
        )
        status_label.pack(side=tk.LEFT)
        
        # 파일 개수 표시
        self.file_count_var = tk.StringVar()
        self.file_count_var.set("파일: 0개")
        
        count_label = ttk.Label(
            status_frame,
            textvariable=self.file_count_var,
            font=("맑은 고딕", 9),
            foreground="blue"
        )
        count_label.pack(side=tk.RIGHT)
        
        # 그리드 가중치 설정 (창 크기 조절 시 확장)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)  # 파일 목록 영역이 확장
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 초기 버튼 상태 설정
        self.update_button_states()
    
    def add_files(self):
        """파일 추가 (예시 파일들)"""
        self.status_var.set("파일 추가 기능 - 예시 파일들을 추가합니다.")
        
        # 예시 파일들을 리스트에 추가
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
            self.files_listbox.insert(tk.END, file)
        
        self.update_file_count()
        self.update_button_states()
        self.status_var.set(f"{len(example_files)}개의 예시 파일이 추가되었습니다.")
    
    def remove_files(self):
        """선택된 파일 제거"""
        selection = self.files_listbox.curselection()
        if selection:
            # 선택된 파일 개수 저장
            removed_count = len(selection)
            
            # 역순으로 삭제 (인덱스 오류 방지)
            for index in reversed(selection):
                self.files_listbox.delete(index)
            
            self.update_file_count()
            self.update_button_states()
            self.status_var.set(f"{removed_count}개의 파일이 제거되었습니다.")
        else:
            self.status_var.set("제거할 파일을 선택해주세요.")
    
    def clear_files(self):
        """모든 파일 제거"""
        if self.files_listbox.size() > 0:
            removed_count = self.files_listbox.size()
            self.files_listbox.delete(0, tk.END)
            
            self.update_file_count()
            self.update_button_states()
            self.status_var.set(f"모든 파일({removed_count}개)이 제거되었습니다.")
        else:
            self.status_var.set("제거할 파일이 없습니다.")
    
    def rename_files(self):
        """파일명 변경 (다음 챕터에서 구현)"""
        if self.files_listbox.size() > 0:
            self.status_var.set("이름 변경 기능은 Chapter 3에서 구현됩니다.")
        else:
            self.status_var.set("변경할 파일이 없습니다.")
    
    def update_file_count(self):
        """파일 개수 업데이트"""
        count = self.files_listbox.size()
        self.file_count_var.set(f"파일: {count}개")
    
    def update_button_states(self):
        """버튼 상태 업데이트"""
        has_files = self.files_listbox.size() > 0
        
        # 파일이 있을 때만 활성화되는 버튼들
        state = tk.NORMAL if has_files else tk.DISABLED
        self.remove_button.config(state=state)
        self.clear_button.config(state=state)
        self.rename_button.config(state=state)
    
    def run(self):
        """애플리케이션 실행"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n프로그램이 사용자에 의해 종료되었습니다.")
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")


def main():
    """메인 함수"""
    print("KRenamer Chapter 1: 기본 GUI 구조")
    print("=" * 40)
    print("이 예제에서 배우는 내용:")
    print("• tkinter 기본 위젯 사용법")
    print("• 윈도우 레이아웃 설계")
    print("• 기본적인 이벤트 처리")
    print("• 사용자 인터페이스 설계")
    print()
    print("GUI 윈도우를 시작합니다...")
    
    try:
        app = BasicKRenamerGUI()
        app.run()
    except Exception as e:
        print(f"애플리케이션 시작 중 오류 발생: {e}")
        return 1
    
    print("KRenamer Chapter 1 완료!")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())