"""
미리보기 패널
"""

import tkinter as tk
from tkinter import ttk
import os


class PreviewPanel:
    """미리보기 패널"""
    
    def __init__(self, parent, engine):
        self.parent = parent
        self.engine = engine
        self.preview_tree = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """미리보기 패널 UI 설정"""
        # 미리보기 프레임
        preview_frame = ttk.LabelFrame(self.parent, text="실시간 미리보기", padding="5")
        preview_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 트리뷰로 미리보기 표시
        columns = ("original", "new", "status")
        self.preview_tree = ttk.Treeview(preview_frame, columns=columns, show="tree headings")
        
        self.preview_tree.heading("#0", text="순번")
        self.preview_tree.heading("original", text="원본 파일명")
        self.preview_tree.heading("new", text="새 파일명")
        self.preview_tree.heading("status", text="상태")
        
        # 컬럼 너비 설정
        self.preview_tree.column("#0", width=50, minwidth=50)
        self.preview_tree.column("original", width=200, minwidth=150)
        self.preview_tree.column("new", width=200, minwidth=150)
        self.preview_tree.column("status", width=80, minwidth=60)
        
        preview_scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.preview_tree.yview)
        self.preview_tree.config(yscrollcommand=preview_scrollbar.set)
        
        self.preview_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
    
    def update_preview(self):
        """미리보기 업데이트"""
        # 기존 항목들 제거
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        if not self.engine.files:
            return
        
        # 리네임 계획 생성
        rename_plan = self.engine.generate_rename_plan()
        
        # 미리보기 트리에 추가
        for index, (original_name, new_name, matches) in enumerate(rename_plan):
            # 상태 텍스트
            if not matches:
                status = "제외"
                tag = "excluded"
            elif original_name == new_name:
                status = "변경없음"
                tag = "unchanged"
            else:
                status = "변경"
                tag = "changed"
            
            # 트리에 항목 추가
            item = self.preview_tree.insert("", "end", text=str(index + 1), 
                                          values=(original_name, new_name, status), 
                                          tags=(tag,))
        
        # 태그별 스타일 설정
        self.preview_tree.tag_configure("excluded", foreground="gray")
        self.preview_tree.tag_configure("unchanged", foreground="blue")
        self.preview_tree.tag_configure("changed", foreground="green")
    
    def clear_preview(self):
        """미리보기 내용 지우기"""
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)