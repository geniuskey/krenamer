#!/usr/bin/env python3
"""
KRenamer Chapter 6 Main Launcher
Chapter 6: 2-패널 레이아웃에서 모듈화로의 점진적 전환

이 런처를 통해 Chapter 6의 각 단계를 체험할 수 있습니다:
- Step 1: 기능별 클래스 분리
- Step 2: UI와 로직 완전 분리  
- Step 3: 패널별 컴포넌트 분리
- Step 4: 의존성 주입 패턴 적용
- Step 5: 완전한 모듈 구조 (Chapter 7 예고)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import sys
from pathlib import Path


class Chapter6Launcher:
    """Chapter 6 학습 단계별 런처"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KRenamer Chapter 6: 2-패널 레이아웃에서 모듈화로")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # 현재 디렉토리 경로
        self.chapter_dir = Path(__file__).parent
        
        self.setup_widgets()
        self.center_window()
    
    def center_window(self):
        """윈도우를 화면 중앙에 배치"""
        self.root.update_idletasks()
        width = 800
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_widgets(self):
        """위젯 설정"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 제목
        title_label = ttk.Label(
            main_frame, 
            text="KRenamer Chapter 6", 
            font=("맑은 고딕", 18, "bold")
        )
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="2-패널 레이아웃에서 모듈화로",
            font=("맑은 고딕", 14),
            foreground="blue"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # 설명
        desc_frame = ttk.LabelFrame(main_frame, text="학습 목표", padding="15")
        desc_frame.pack(fill=tk.X, pady=(0, 15))
        
        desc_text = (
            "Chapter 6에서는 Chapter 5의 통합된 코드를 Chapter 7의 모듈화 구조로\n"
            "점진적으로 전환하는 과정을 배웁니다.\n\n"
            "✅ 단일 클래스에서 다중 클래스 구조로의 전환\n"
            "✅ UI와 비즈니스 로직의 완전한 분리\n"
            "✅ 컴포넌트 간 의존성 주입 패턴 구현\n"
            "✅ 점진적 리팩토링 기법 습득\n"
            "✅ Chapter 7의 완전 모듈화 구조 준비"
        )
        ttk.Label(desc_frame, text=desc_text, justify=tk.LEFT).pack(anchor=tk.W)
        
        # 단계별 버튼들
        self.create_step_buttons(main_frame)
        
        # 하단 정보
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(pady=(20, 0), fill=tk.X)
        
        ttk.Separator(info_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 15))
        
        info_text = "💡 각 단계를 순서대로 실행하여 점진적 모듈화 과정을 체험하세요."
        info_label = ttk.Label(
            info_frame,
            text=info_text,
            font=("맑은 고딕", 10),
            foreground="gray"
        )
        info_label.pack()
        
        # 종료 버튼
        ttk.Button(
            main_frame,
            text="종료",
            command=self.root.quit,
            width=10
        ).pack(pady=(15, 0))
    
    def create_step_buttons(self, parent):
        """단계별 버튼 생성"""
        steps = [
            {
                "title": "Step 1: 기능별 클래스 분리",
                "desc": "거대한 GUI 클래스를 기능별로 분할\n→ FileManager, RenameEngine, GUI 클래스",
                "file": "step1_class_separation.py",
                "concepts": "단일 책임 원칙, 객체 조합"
            },
            {
                "title": "Step 2: UI와 로직 완전 분리", 
                "desc": "GUI와 비즈니스 로직의 완전한 분리\n→ Engine은 GUI 의존성 없는 순수 로직",
                "file": "step2_ui_logic_separation.py",
                "concepts": "관심사의 분리, MVC 패턴 기초"
            },
            {
                "title": "Step 3: 패널별 컴포넌트 분리",
                "desc": "UI를 기능별 패널 컴포넌트로 분할\n→ FilePanel, OptionsPanel, PreviewPanel",
                "file": "step3_panel_components.py", 
                "concepts": "컴포넌트 패턴, 콜백 통신"
            },
            {
                "title": "Step 4: 의존성 주입 적용",
                "desc": "컴포넌트 간 느슨한 결합 구현\n→ 인터페이스 기반 의존성 주입",
                "file": "step4_dependency_injection.py",
                "concepts": "DI 패턴, 제어의 역전"
            },
            {
                "title": "Step 5: 완전한 모듈 구조",
                "desc": "Chapter 7 스타일의 패키지 구조\n→ core/, gui/, utils/ 모듈 분리",
                "file": "step5/main.py",
                "concepts": "패키지 시스템, Chapter 7 예고"
            }
        ]
        
        # 버튼 프레임
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        for i, step in enumerate(steps):
            # 각 단계별 프레임
            step_frame = ttk.LabelFrame(button_frame, text=step["title"], padding="10")
            step_frame.pack(fill=tk.X, pady=(0, 10))
            
            # 왼쪽: 설명
            left_frame = ttk.Frame(step_frame)
            left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            desc_label = ttk.Label(
                left_frame,
                text=step["desc"],
                font=("맑은 고딕", 9),
                justify=tk.LEFT
            )
            desc_label.pack(anchor=tk.W, pady=(0, 5))
            
            concept_label = ttk.Label(
                left_frame,
                text=f"핵심 개념: {step['concepts']}",
                font=("맑은 고딕", 8),
                foreground="blue"
            )
            concept_label.pack(anchor=tk.W)
            
            # 오른쪽: 버튼과 상태
            right_frame = ttk.Frame(step_frame)
            right_frame.pack(side=tk.RIGHT, padx=(10, 0))
            
            # 실행 버튼
            run_btn = ttk.Button(
                right_frame,
                text=f"Step {i+1} 실행",
                command=lambda f=step["file"]: self.run_step(f),
                width=15
            )
            run_btn.pack(pady=(0, 5))
            
            # 파일 존재 여부 표시
            file_path = self.chapter_dir / step["file"]
            if file_path.exists():
                status_label = ttk.Label(
                    right_frame,
                    text="✅ 사용 가능",
                    font=("맑은 고딕", 8),
                    foreground="green"
                )
            else:
                status_label = ttk.Label(
                    right_frame,
                    text="❌ 파일 없음",
                    font=("맑은 고딕", 8),
                    foreground="red"
                )
                run_btn.config(state=tk.DISABLED)
            
            status_label.pack()
    
    def run_step(self, filename):
        """선택된 단계 실행"""
        file_path = self.chapter_dir / filename
        
        if not file_path.exists():
            messagebox.showerror(
                "오류",
                f"파일을 찾을 수 없습니다:\n{file_path}"
            )
            return
        
        try:
            # Step 5는 특별 처리 (디렉토리 변경 필요)
            if filename.startswith("step5/"):
                step5_dir = self.chapter_dir / "step5"
                subprocess.Popen([
                    sys.executable,
                    "main.py"
                ], cwd=str(step5_dir))
            else:
                # 일반 단계들
                subprocess.Popen([
                    sys.executable,
                    str(file_path)
                ], cwd=str(self.chapter_dir))
            
            # 런처는 계속 실행 상태 유지
            
        except Exception as e:
            messagebox.showerror(
                "실행 오류",
                f"단계 실행 중 오류가 발생했습니다:\n{e}"
            )
    
    def run(self):
        """런처 실행"""
        self.root.mainloop()


def main():
    """메인 함수"""
    print("KRenamer Chapter 6 Launcher")
    print("=" * 40)
    print("2-패널 레이아웃에서 모듈화로의 점진적 전환을 학습하세요!")
    print()
    print("학습 단계:")
    print("Step 1: 기능별 클래스 분리")
    print("Step 2: UI와 로직 완전 분리") 
    print("Step 3: 패널별 컴포넌트 분리")
    print("Step 4: 의존성 주입 패턴 적용")
    print("Step 5: 완전한 모듈 구조 (Chapter 7 예고)")
    print()
    
    try:
        launcher = Chapter6Launcher()
        launcher.run()
        return 0
    except Exception as e:
        print(f"런처 실행 중 오류: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())