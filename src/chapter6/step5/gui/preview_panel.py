"""
미리보기 패널
"""

import tkinter as tk
from tkinter import ttk

from ..core.interfaces import FileEngineProtocol


class PreviewPanel:
    """
    미리보기 표시 UI 컴포넌트
    완전히 모듈화된 구조
    """
    
    def __init__(self, parent: tk.Widget, engine: FileEngineProtocol):
        self.parent = parent
        self.engine = engine
        
        # UI 변수들
        self.stats_var = tk.StringVar()
        
        # 위젯 생성
        self.create_widgets()
    
    def create_widgets(self):
        """위젯 생성"""
        self.frame = ttk.LabelFrame(self.parent, text="미리보기 [모듈화]", padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        info_frame = ttk.Frame(self.frame)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(info_frame, textvariable=self.stats_var, font=("맑은 고딕", 9), foreground="blue").pack(side=tk.LEFT)
        
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("index", "original", "new", "status")
        self.preview_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        self.preview_tree.heading("index", text="순번")
        self.preview_tree.heading("original", text="원본 파일명")
        self.preview_tree.heading("new", text="새 파일명")
        self.preview_tree.heading("status", text="상태")
        
        self.preview_tree.column("index", width=50)
        self.preview_tree.column("original", width=200)
        self.preview_tree.column("new", width=200)
        self.preview_tree.column("status", width=80)
        
        preview_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.preview_tree.yview)
        self.preview_tree.config(yscrollcommand=preview_scrollbar.set)
        
        self.preview_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def refresh(self):
        """미리보기 새로고침"""
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        plan = self.engine.generate_rename_plan()
        
        if not plan:
            self.stats_var.set("변경할 파일이 없습니다")
            return
        
        changed_count = sum(1 for item in plan if item['changed'])
        self.stats_var.set(f"총 {len(plan)}개 파일 중 {changed_count}개 변경 예정")
        
        for i, item in enumerate(plan):
            if item['changed']:
                status = "변경됨"
                tags = ("changed",)
            else:
                status = "동일"
                tags = ("same",)
            
            self.preview_tree.insert("", tk.END, values=(
                i + 1,
                item['original'], 
                item['new'], 
                status
            ), tags=tags)
        
        self.preview_tree.tag_configure("changed", foreground="blue")
        self.preview_tree.tag_configure("same", foreground="gray")