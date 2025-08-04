# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

class KRenamer:
    """KRenamer 애플리케이션 메인 클래스"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_title()
    
    def setup_window(self):
        """창 기본 설정 - Chapter 2에서 배운 내용!"""
        self.root.title("KRenamer - 파일명 변경 도구")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        self.root.minsize(500, 400)
        
        # 창을 화면 중앙에 배치 (Chapter 2 기법)
        self.center_window()
    
    def center_window(self):
        """창을 화면 중앙에 배치"""
        self.root.update_idletasks()
        width = 600
        height = 500
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_title(self):
        """제목 영역 만들기 - Label 사용"""
        # 메인 제목 (Chapter 2의 Label 활용)
        title_label = tk.Label(
            self.root,
            text="📁 KRenamer",
            font=("맑은 고딕", 20, "bold"),
            fg="darkblue",
            bg="lightblue",
            height=2
        )
        title_label.pack(fill=tk.X, padx=10, pady=10)
        
        # 설명 라벨
        desc_label = tk.Label(
            self.root,
            text="여러 파일의 이름을 한 번에 쉽게 바꿀 수 있는 도구입니다.",
            font=("맑은 고딕", 11),
            fg="gray"
        )
        desc_label.pack(pady=(0, 10))
    
    def run(self):
        """프로그램 실행"""
        self.root.mainloop()

# 프로그램 실행
if __name__ == "__main__":
    app = KRenamer()
    app.run()