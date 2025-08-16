#!/usr/bin/env python3
"""
KRenamer Chapter 7 - Complete Modular File Renaming Tool
완성된 모듈화 파일 리네이머 애플리케이션

이 챕터에서는 다음과 같은 완성된 기능들을 제공합니다:
- 완전한 GUI 인터페이스
- 드래그 앤 드롭 지원
- 다양한 리네임 전략
- 조건부 필터링
- 설정 저장/로드
- 오류 처리 및 로깅
"""

import sys
import tkinter as tk
from tkinter import messagebox

# Chapter 7용 import 경로 설정
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from chapter7.gui.main_window import RenamerGUI
except ImportError:
    print("오류: GUI 모듈을 찾을 수 없습니다.")
    print("chapter7 디렉토리에서 실행해주세요.")
    sys.exit(1)


def main():
    """메인 함수"""
    print("KRenamer Chapter 7 - 완성된 모듈화 파일 리네이머")
    print("=" * 50)
    print("이 챕터에서 제공하는 완성된 기능들:")
    print("- 완전한 GUI 인터페이스")
    print("- 드래그 앤 드롭 지원")
    print("- 다양한 리네임 전략")
    print("- 조건부 필터링")
    print("- 설정 저장/로드")
    print("- 오류 처리 및 로깅")
    print()
    
    try:
        app = RenamerGUI()
        app.run()
    except Exception as e:
        # GUI 초기화 실패 시 에러 메시지 표시
        root = tk.Tk()
        root.withdraw()  # 메인 창 숨기기
        messagebox.showerror(
            "KRenamer Chapter 7 오류", 
            f"Chapter 7 애플리케이션을 시작할 수 없습니다:\n{str(e)}\n\n"
            "tkinterdnd2 패키지가 설치되어 있는지 확인하세요.\n"
            "설치 명령: pip install tkinterdnd2"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()