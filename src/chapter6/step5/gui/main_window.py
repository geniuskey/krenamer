"""
메인 애플리케이션 윈도우
"""

import tkinter as tk
from tkinter import ttk, messagebox

from ..core.engine import RenameEngineService
from .file_panel import FilePanel
from .options_panel import OptionsPanel
from .preview_panel import PreviewPanel
from .interfaces import DataChangeNotifierProtocol, StatusReporterProtocol

# 드래그 앤 드롭 지원 (선택적)
try:
    from tkinterdnd2 import TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


class MainApplication:
    """
    메인 애플리케이션 클래스
    완전히 모듈화된 구조 - Chapter 7 예고
    """
    
    def __init__(self):
        # 윈도우 초기화
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
        
        # 엔진 생성
        self.engine = RenameEngineService()
        
        # 상태 변수
        self.status_var = tk.StringVar(value="완전한 모듈 구조가 준비되었습니다 - Chapter 7 예고!")
        
        # UI 구성
        self.setup_window()
        self.setup_widgets()
        
        # 초기 상태
        self.on_data_changed()
    
    def setup_window(self):
        """윈도우 기본 설정"""
        self.root.title("Chapter 6 Step 5: 완전한 모듈 구조 (Chapter 7 예고)")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        self.center_window()
    
    def center_window(self):
        """윈도우 중앙 배치"""
        self.root.update_idletasks()
        width, height = 1200, 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_widgets(self):
        """위젯 구성 - 완전한 모듈 구조"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 상단: 설명
        info_frame = ttk.LabelFrame(main_frame, text="Step 5: 완전한 모듈 구조 (Chapter 7 예고)", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_text = (
            "이 단계에서는 Chapter 7 스타일의 완전한 모듈 구조를 구현합니다:\n"
            "• core/ 패키지: 비즈니스 로직과 인터페이스 (engine.py, interfaces.py)\n"
            "• gui/ 패키지: UI 컴포넌트들 (main_window.py, file_panel.py, options_panel.py, preview_panel.py)\n" 
            "• utils/ 패키지: 공통 유틸리티 (향후 확장)\n"
            "• 패키지 import 시스템과 __init__.py 파일 활용"
        )
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)
        
        # 모듈 구조 설명
        structure_frame = ttk.LabelFrame(main_frame, text="모듈 구조", padding="10")
        structure_frame.pack(fill=tk.X, pady=(0, 10))
        
        structure_text = (
            "step5/\n"
            "├── __init__.py              # 패키지 진입점\n"
            "├── core/                    # 🧠 비즈니스 로직\n"
            "│   ├── __init__.py\n" 
            "│   ├── interfaces.py        # 인터페이스 정의\n"
            "│   └── engine.py            # 엔진 구현\n"
            "├── gui/                     # 🎨 UI 컴포넌트\n"
            "│   ├── __init__.py\n"
            "│   ├── interfaces.py        # GUI 인터페이스\n"
            "│   ├── main_window.py       # 메인 윈도우\n"
            "│   ├── file_panel.py        # 파일 패널\n"
            "│   ├── options_panel.py     # 옵션 패널\n"
            "│   └── preview_panel.py     # 미리보기 패널\n"
            "└── utils/                   # 🔧 유틸리티 (향후)\n"
            "    └── __init__.py"
        )
        ttk.Label(structure_frame, text=structure_text, font=("Consolas", 9), justify=tk.LEFT).pack(anchor=tk.W)
        
        # 메인 레이아웃
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        left_panel = ttk.Frame(paned)
        paned.add(left_panel, weight=1)
        
        right_panel = ttk.Frame(paned)
        paned.add(right_panel, weight=1)
        
        # 모듈화된 컴포넌트들 생성
        self.file_panel = FilePanel(
            parent=left_panel,
            engine=self.engine,
            notifier=self,
            status_reporter=self
        )
        
        self.options_panel = OptionsPanel(
            parent=left_panel,
            engine=self.engine,
            notifier=self
        )
        
        self.preview_panel = PreviewPanel(
            parent=right_panel,
            engine=self.engine
        )
        
        # 실행 버튼
        button_frame = ttk.Frame(left_panel)
        button_frame.pack(pady=(10, 0))
        
        ttk.Button(button_frame, text="미리보기 새로고침", command=self.refresh_preview).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="이름 변경 실행", command=self.execute_rename).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Chapter 7 미리보기", command=self.show_chapter7_preview).pack(side=tk.LEFT)
        
        # 상태바
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X)
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT)
    
    # DataChangeNotifierProtocol 구현
    def on_data_changed(self):
        """데이터 변경 알림 처리"""
        self.refresh_preview()
    
    # StatusReporterProtocol 구현
    def report_status(self, message: str):
        """상태 보고 처리"""
        self.status_var.set(message)
    
    def refresh_preview(self):
        """미리보기 새로고침"""
        self.preview_panel.refresh()
    
    def show_chapter7_preview(self):
        """Chapter 7 미리보기 대화상자"""
        preview_text = (
            "🎯 Chapter 7에서 추가될 기능들:\n\n"
            "📁 완전한 패키지 분리:\n"
            "• core/conditions.py - 고급 필터링 로직\n"
            "• utils/file_utils.py - 파일 관련 헬퍼 함수들\n"
            "• utils/validation.py - 유효성 검사 도구들\n\n"
            "🔧 고급 기능들:\n"
            "• 조건부 필터링 (파일 크기, 날짜, 확장자)\n"
            "• 설정 저장/로드 시스템\n"
            "• 플러그인 아키텍처\n"
            "• 다국어 지원\n\n"
            "🏗️ 아키텍처 패턴:\n"
            "• Factory Pattern으로 엔진 생성\n"
            "• Observer Pattern으로 이벤트 처리\n"
            "• Strategy Pattern으로 리네임 전략\n"
            "• Command Pattern으로 실행 취소\n\n"
            "Chapter 6에서 배운 모든 개념들이 Chapter 7에서 완성됩니다!"
        )
        
        messagebox.showinfo("Chapter 7 미리보기", preview_text)
    
    def execute_rename(self):
        """파일명 변경 실행"""
        if not hasattr(self.engine, 'files') or not self.engine.files:
            self.report_status("변경할 파일이 없습니다")
            messagebox.showwarning("경고", "변경할 파일이 없습니다")
            return
        
        warnings = self.engine.validate_settings()
        if warnings:
            if not messagebox.askyesno("경고", f"다음 경고가 있습니다:\n{warnings[0]}\n\n계속 진행하시겠습니까?"):
                return
        
        plan = self.engine.generate_rename_plan()
        change_count = sum(1 for item in plan if item['changed'])
        
        if change_count == 0:
            self.report_status("변경될 파일이 없습니다")
            messagebox.showinfo("정보", "변경될 파일이 없습니다")
            return
        
        if not messagebox.askyesno("확인", f"{change_count}개 파일의 이름을 변경하시겠습니까?"):
            return
        
        result = self.engine.execute_rename()
        success_count = result['success_count']
        errors = result['errors']
        
        if errors:
            error_msg = f"{success_count}개 파일 변경 완료.\n오류:\n" + "\n".join(errors[:5])
            if len(errors) > 5:
                error_msg += f"\n... 외 {len(errors)-5}개"
            messagebox.showwarning("완료", error_msg)
        else:
            messagebox.showinfo("완료", f"{success_count}개 파일의 이름이 변경되었습니다")
        
        self.report_status(f"변경 완료: {success_count}개 성공, {len(errors)}개 오류")
        
        # UI 새로고침
        self.file_panel.refresh()
        self.refresh_preview()
    
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()