#!/usr/bin/env python3
"""
KRenamer Chapter 6 Step 5: 완전한 모듈 구조 실행 파일
Chapter 7 스타일의 패키지 구조 데모
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from gui.main_window import MainApplication
except ImportError as e:
    print(f"모듈 임포트 오류: {e}")
    print("step5 디렉토리에서 실행해주세요.")
    sys.exit(1)


def main():
    """메인 함수"""
    print("KRenamer Chapter 6 Step 5: 완전한 모듈 구조")
    print("=" * 50)
    print("학습 내용:")
    print("• Chapter 7 스타일의 패키지 구조 구현")
    print("• core/ 패키지: 비즈니스 로직과 인터페이스")
    print("• gui/ 패키지: UI 컴포넌트들")
    print("• utils/ 패키지: 공통 유틸리티 (향후 확장)")
    print("• 패키지 import 시스템 활용")
    print()
    print("핵심 개념:")
    print("• Python 패키지 시스템")
    print("• 모듈 설계 원칙")  
    print("• 확장 가능한 아키텍처")
    print("• Chapter 7으로의 자연스러운 연결")
    print()
    
    print("모듈 구조:")
    print("step5/")
    print("├── __init__.py              # 패키지 진입점")
    print("├── core/                    # 🧠 비즈니스 로직")
    print("│   ├── __init__.py")
    print("│   ├── interfaces.py        # 인터페이스 정의")
    print("│   └── engine.py            # 엔진 구현")
    print("├── gui/                     # 🎨 UI 컴포넌트") 
    print("│   ├── __init__.py")
    print("│   ├── interfaces.py        # GUI 인터페이스")
    print("│   ├── main_window.py       # 메인 윈도우")
    print("│   ├── file_panel.py        # 파일 패널")
    print("│   ├── options_panel.py     # 옵션 패널")
    print("│   └── preview_panel.py     # 미리보기 패널")
    print("└── utils/                   # 🔧 유틸리티")
    print("    └── __init__.py")
    print()
    
    try:
        app = MainApplication()
        print("GUI 애플리케이션을 시작합니다...")
        app.run()
        return 0
    except Exception as e:
        print(f"애플리케이션 실행 중 오류: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())