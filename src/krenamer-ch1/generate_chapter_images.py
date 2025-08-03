#!/usr/bin/env python3
"""
삽화 생성 스크립트 - KRenamer 문서용
각 챕터별로 적절한 삽화를 생성합니다.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os
from pathlib import Path

# 한글 폰트 설정 (Windows 환경)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 컬러 팔레트
COLORS = {
    'primary': '#4A90E2',
    'secondary': '#7ED321', 
    'accent': '#F5A623',
    'warning': '#D0021B',
    'background': '#F8F9FA',
    'text': '#333333',
    'light_gray': '#E6E6E6',
    'dark_gray': '#666666'
}

def create_chapter1_python_basics():
    """Chapter 1: Python 기초 - 변수와 데이터 타입 설명"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # 배경 설정
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_facecolor(COLORS['background'])
    
    # 제목
    ax.text(5, 7.5, 'Python 기초: 변수와 데이터 타입', 
            fontsize=20, fontweight='bold', ha='center', color=COLORS['text'])
    
    # 변수 박스들
    variables = [
        {'name': 'program_name', 'value': '"KRenamer"', 'type': 'str', 'x': 1, 'y': 6},
        {'name': 'file_count', 'value': '5', 'type': 'int', 'x': 5.5, 'y': 6},
        {'name': 'is_running', 'value': 'True', 'type': 'bool', 'x': 1, 'y': 4.5},
        {'name': 'my_files', 'value': '["a.txt", "b.jpg"]', 'type': 'list', 'x': 5.5, 'y': 4.5}
    ]
    
    type_colors = {
        'str': COLORS['primary'],
        'int': COLORS['secondary'], 
        'bool': COLORS['accent'],
        'list': COLORS['warning']
    }
    
    for var in variables:
        # 변수 박스
        box = FancyBboxPatch((var['x']-0.4, var['y']-0.8), 3.5, 1.2,
                            boxstyle="round,pad=0.1", 
                            facecolor=type_colors[var['type']], 
                            alpha=0.7, edgecolor='black', linewidth=1)
        ax.add_patch(box)
        
        # 변수명
        ax.text(var['x'], var['y']-0.1, var['name'], 
                fontsize=12, fontweight='bold', color='white')
        # 값
        ax.text(var['x'], var['y']-0.4, var['value'], 
                fontsize=10, color='white')
        # 타입
        ax.text(var['x'], var['y']-0.7, f"({var['type']})", 
                fontsize=9, style='italic', color='white')
    
    # 화살표와 설명
    ax.annotate('문자열 데이터', xy=(1.5, 5.2), xytext=(0.5, 3),
                arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2),
                fontsize=11, color=COLORS['text'])
    
    ax.annotate('숫자 데이터', xy=(6, 5.2), xytext=(7.5, 3),
                arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2),
                fontsize=11, color=COLORS['text'])
    
    # 하단 설명
    ax.text(5, 2, '파일 관리 프로그램을 위한 기본 데이터 구조', 
            fontsize=14, ha='center', color=COLORS['text'],
            bbox=dict(boxstyle="round,pad=0.5", facecolor=COLORS['light_gray']))
    
    ax.text(5, 0.5, 'Chapter 1에서는 이런 기본 개념들을 배워서\n실제 파일명 변경 프로그램을 만듭니다!', 
            fontsize=12, ha='center', color=COLORS['dark_gray'])
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    plt.tight_layout()
    return fig

def create_chapter2_tkinter_gui():
    """Chapter 2: Tkinter GUI 기초 - GUI 구성 요소"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_facecolor(COLORS['background'])
    
    # 제목
    ax.text(6, 9.5, 'Tkinter GUI 구성 요소', 
            fontsize=20, fontweight='bold', ha='center', color=COLORS['text'])
    
    # GUI 윈도우 프레임
    window_frame = patches.Rectangle((1, 1), 10, 7, linewidth=3, 
                                   edgecolor=COLORS['text'], facecolor='white', alpha=0.9)
    ax.add_patch(window_frame)
    
    # 윈도우 타이틀바
    title_bar = patches.Rectangle((1, 7.5), 10, 0.5, linewidth=1,
                                edgecolor=COLORS['text'], facecolor=COLORS['primary'])
    ax.add_patch(title_bar)
    ax.text(6, 7.75, 'KRenamer - 파일명 변경 도구', 
            fontsize=12, ha='center', color='white', fontweight='bold')
    
    # GUI 요소들
    # 라벨
    label_box = patches.Rectangle((2, 6.5), 8, 0.5, linewidth=1,
                                edgecolor=COLORS['dark_gray'], facecolor=COLORS['light_gray'])
    ax.add_patch(label_box)
    ax.text(6, 6.75, '파일 목록:', fontsize=12, ha='center', fontweight='bold')
    
    # 리스트박스
    listbox = patches.Rectangle((2, 4), 6, 2, linewidth=2,
                              edgecolor=COLORS['primary'], facecolor='white')
    ax.add_patch(listbox)
    
    # 리스트 아이템들
    files = ['문서1.pdf', '사진1.jpg', '음악1.mp3', '메모.txt']
    for i, file in enumerate(files):
        ax.text(2.2, 5.5 - i*0.4, file, fontsize=10, va='center')
    
    # 스크롤바
    scrollbar = patches.Rectangle((8, 4), 0.3, 2, linewidth=1,
                                edgecolor=COLORS['dark_gray'], facecolor=COLORS['light_gray'])
    ax.add_patch(scrollbar)
    
    # 버튼들
    buttons = [
        {'text': '파일 추가', 'x': 2, 'color': COLORS['secondary']},
        {'text': '파일 제거', 'x': 4, 'color': COLORS['warning']},
        {'text': '이름 변경', 'x': 6, 'color': COLORS['accent']},
        {'text': '전체 지우기', 'x': 8, 'color': COLORS['dark_gray']}
    ]
    
    for btn in buttons:
        button_box = FancyBboxPatch((btn['x'], 2.5), 1.5, 0.6,
                                   boxstyle="round,pad=0.05",
                                   facecolor=btn['color'], alpha=0.8,
                                   edgecolor='black', linewidth=1)
        ax.add_patch(button_box)
        ax.text(btn['x'] + 0.75, 2.8, btn['text'], 
                fontsize=9, ha='center', color='white', fontweight='bold')
    
    # 상태바
    status_bar = patches.Rectangle((2, 1.5), 8, 0.4, linewidth=1,
                                 edgecolor=COLORS['dark_gray'], facecolor=COLORS['light_gray'])
    ax.add_patch(status_bar)
    ax.text(2.2, 1.7, '파일 4개가 준비되었습니다.', fontsize=10, va='center')
    
    # 설명 화살표들
    ax.annotate('Label\n(텍스트 표시)', xy=(6, 6.5), xytext=(9.5, 8),
                arrowprops=dict(arrowstyle='->', color=COLORS['accent'], lw=2),
                fontsize=10, ha='center', color=COLORS['text'])
    
    ax.annotate('Listbox\n(파일 목록)', xy=(5, 5), xytext=(9.5, 6),
                arrowprops=dict(arrowstyle='->', color=COLORS['accent'], lw=2),
                fontsize=10, ha='center', color=COLORS['text'])
    
    ax.annotate('Button\n(사용자 액션)', xy=(5, 2.8), xytext=(9.5, 4),
                arrowprops=dict(arrowstyle='->', color=COLORS['accent'], lw=2),
                fontsize=10, ha='center', color=COLORS['text'])
    
    ax.text(6, 0.5, 'Chapter 2에서는 이런 GUI 요소들을 조합해서\n사용자 친화적인 인터페이스를 만듭니다!', 
            fontsize=12, ha='center', color=COLORS['dark_gray'])
    
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.tight_layout()
    return fig

def create_chapter3_gui_structure():
    """Chapter 3: 기본 GUI 구조 - 레이아웃 설계"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.set_facecolor(COLORS['background'])
    
    # 제목
    ax.text(6, 7.5, '기본 GUI 구조 및 레이아웃', 
            fontsize=20, fontweight='bold', ha='center', color=COLORS['text'])
    
    # 그리드 레이아웃 표시
    # 메인 컨테이너
    main_container = patches.Rectangle((1, 1), 10, 5.5, linewidth=3,
                                     edgecolor=COLORS['primary'], facecolor='none')
    ax.add_patch(main_container)
    ax.text(1.2, 6.3, 'Main Frame', fontsize=10, fontweight='bold', color=COLORS['primary'])
    
    # Row 0: 제목 영역
    title_area = patches.Rectangle((1.5, 5.5), 9, 0.8, linewidth=2,
                                 edgecolor=COLORS['secondary'], facecolor=COLORS['secondary'], alpha=0.3)
    ax.add_patch(title_area)
    ax.text(6, 5.9, 'Title Area (Row 0)', fontsize=12, ha='center', fontweight='bold')
    
    # Row 1: 파일 목록 영역
    file_area = patches.Rectangle((1.5, 3), 9, 2, linewidth=2,
                                edgecolor=COLORS['accent'], facecolor=COLORS['accent'], alpha=0.3)
    ax.add_patch(file_area)
    ax.text(6, 4, 'File List Area (Row 1)\nListbox + Scrollbar', 
            fontsize=12, ha='center', fontweight='bold')
    
    # Row 2: 버튼 영역
    button_area = patches.Rectangle((1.5, 2), 9, 0.8, linewidth=2,
                                  edgecolor=COLORS['warning'], facecolor=COLORS['warning'], alpha=0.3)
    ax.add_patch(button_area)
    ax.text(6, 2.4, 'Button Area (Row 2)', fontsize=12, ha='center', fontweight='bold')
    
    # Row 3: 상태바
    status_area = patches.Rectangle((1.5, 1.2), 9, 0.6, linewidth=2,
                                  edgecolor=COLORS['dark_gray'], facecolor=COLORS['dark_gray'], alpha=0.3)
    ax.add_patch(status_area)
    ax.text(6, 1.5, 'Status Bar (Row 3)', fontsize=12, ha='center', fontweight='bold')
    
    # 그리드 라인 표시
    for i in range(5):
        ax.axhline(y=1.2 + i*1.3, xmin=0.125, xmax=0.875, color=COLORS['text'], linestyle='--', alpha=0.5)
    
    # 레이아웃 설명
    ax.text(1, 0.7, 'Grid Layout:', fontsize=12, fontweight='bold', color=COLORS['text'])
    ax.text(1, 0.4, '• Row 가중치: Row 1이 확장 가능 (weight=1)', fontsize=10, color=COLORS['text'])
    ax.text(1, 0.1, '• Column 가중치: 전체 폭 확장 (weight=1)', fontsize=10, color=COLORS['text'])
    
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.tight_layout()
    return fig

def create_file_operation_flow():
    """파일 처리 흐름도"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.set_facecolor(COLORS['background'])
    
    # 제목
    ax.text(7, 9.5, 'KRenamer 파일 처리 흐름', 
            fontsize=20, fontweight='bold', ha='center', color=COLORS['text'])
    
    # 단계별 박스
    steps = [
        {'text': '1. 파일 선택\n(드래그&드롭)', 'x': 2, 'y': 8, 'color': COLORS['primary']},
        {'text': '2. 파일 목록\n추가', 'x': 7, 'y': 8, 'color': COLORS['secondary']},
        {'text': '3. 이름 변경\n규칙 설정', 'x': 12, 'y': 8, 'color': COLORS['accent']},
        {'text': '4. 미리보기\n확인', 'x': 2, 'y': 5, 'color': COLORS['warning']},
        {'text': '5. 실제 파일\n이름 변경', 'x': 7, 'y': 5, 'color': COLORS['primary']},
        {'text': '6. 결과 확인\n및 피드백', 'x': 12, 'y': 5, 'color': COLORS['secondary']}
    ]
    
    for step in steps:
        # 박스 그리기
        box = FancyBboxPatch((step['x']-1, step['y']-0.7), 2, 1.4,
                            boxstyle="round,pad=0.2",
                            facecolor=step['color'], alpha=0.8,
                            edgecolor='black', linewidth=2)
        ax.add_patch(box)
        
        # 텍스트 추가
        ax.text(step['x'], step['y'], step['text'], 
                fontsize=11, ha='center', va='center', 
                color='white', fontweight='bold')
    
    # 화살표 연결
    arrows = [
        ((3, 8), (6, 8)),  # 1->2
        ((8, 8), (11, 8)), # 2->3
        ((12, 7.3), (12, 5.7)), # 3->4 (아래로)
        ((11, 5), (8, 5)), # 4->5
        ((6, 5), (3, 5)),  # 5->6
    ]
    
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=3, color=COLORS['text']))
    
    # 중앙 설명
    explanation_box = FancyBboxPatch((5, 2), 4, 1.5,
                                   boxstyle="round,pad=0.3",
                                   facecolor=COLORS['light_gray'], alpha=0.9,
                                   edgecolor=COLORS['text'], linewidth=2)
    ax.add_patch(explanation_box)
    
    ax.text(7, 2.75, '안전한 파일 처리', 
            fontsize=14, ha='center', fontweight='bold', color=COLORS['text'])
    ax.text(7, 2.25, '• 미리보기로 확인\n• 오류 처리\n• 사용자 피드백', 
            fontsize=11, ha='center', color=COLORS['dark_gray'])
    
    ax.text(7, 0.5, '각 챕터에서 이 흐름의 다른 부분을 구현합니다', 
            fontsize=12, ha='center', color=COLORS['dark_gray'])
    
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.tight_layout()
    return fig

def create_drag_drop_illustration():
    """드래그 앤 드롭 기능 설명"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.set_facecolor(COLORS['background'])
    
    # 제목
    ax.text(6, 7.5, '드래그 앤 드롭 파일 추가', 
            fontsize=20, fontweight='bold', ha='center', color=COLORS['text'])
    
    # 파일 탐색기 윈도우
    explorer = patches.Rectangle((0.5, 4), 4, 3, linewidth=2,
                               edgecolor=COLORS['text'], facecolor='white')
    ax.add_patch(explorer)
    ax.text(2.5, 6.7, '파일 탐색기', fontsize=12, ha='center', fontweight='bold')
    
    # 파일들
    files = ['문서.pdf', '사진.jpg', '음악.mp3']
    for i, file in enumerate(files):
        file_box = patches.Rectangle((0.8, 5.8 - i*0.5), 3.4, 0.4, 
                                   facecolor=COLORS['light_gray'], edgecolor=COLORS['dark_gray'])
        ax.add_patch(file_box)
        ax.text(0.9, 6 - i*0.5, file, fontsize=10, va='center')
    
    # 화살표 (드래그 표시)
    ax.annotate('', xy=(7.5, 5.5), xytext=(4.5, 5.5),
               arrowprops=dict(arrowstyle='->', lw=4, color=COLORS['accent']))
    ax.text(6, 6, '드래그', fontsize=12, ha='center', color=COLORS['accent'], fontweight='bold')
    
    # KRenamer 윈도우
    krenamer = patches.Rectangle((7.5, 2), 4, 5, linewidth=3,
                               edgecolor=COLORS['primary'], facecolor='white')
    ax.add_patch(krenamer)
    ax.text(9.5, 6.7, 'KRenamer', fontsize=12, ha='center', fontweight='bold', color=COLORS['primary'])
    
    # 드롭 영역
    drop_area = patches.Rectangle((8, 3), 3, 3, linewidth=2,
                                edgecolor=COLORS['secondary'], facecolor=COLORS['secondary'], 
                                alpha=0.3, linestyle='--')
    ax.add_patch(drop_area)
    ax.text(9.5, 4.5, '여기에 드롭!', fontsize=12, ha='center', 
            color=COLORS['secondary'], fontweight='bold')
    
    # 결과 표시
    result_box = FancyBboxPatch((2, 0.5), 8, 1,
                               boxstyle="round,pad=0.2",
                               facecolor=COLORS['light_gray'], alpha=0.9,
                               edgecolor=COLORS['text'], linewidth=1)
    ax.add_patch(result_box)
    
    ax.text(6, 1, '결과: 파일들이 자동으로 목록에 추가됩니다!', 
            fontsize=12, ha='center', fontweight='bold', color=COLORS['text'])
    
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.tight_layout()
    return fig

def save_all_images():
    """모든 이미지 생성 및 저장"""
    # 이미지 저장 경로
    docs_images_path = Path(__file__).parent.parent.parent / "docs" / "images"
    docs_images_path.mkdir(exist_ok=True)
    
    print("Chapter images generation started...")
    
    # Chapter 1: Python 기초
    print("  Chapter 1: Python basics illustration...")
    fig1 = create_chapter1_python_basics()
    fig1.savefig(docs_images_path / "chapter1_python_basics.png", 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig1)
    
    # Chapter 2: Tkinter GUI
    print("  Chapter 2: Tkinter GUI illustration...")
    fig2 = create_chapter2_tkinter_gui()
    fig2.savefig(docs_images_path / "chapter2_tkinter_gui.png", 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig2)
    
    # Chapter 3: GUI 구조
    print("  Chapter 3: GUI structure illustration...")
    fig3 = create_chapter3_gui_structure()
    fig3.savefig(docs_images_path / "chapter3_gui_structure.png", 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig3)
    
    # 파일 처리 흐름도
    print("  File operation flow diagram...")
    fig4 = create_file_operation_flow()
    fig4.savefig(docs_images_path / "file_operation_flow.png", 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig4)
    
    # 드래그 앤 드롭 설명
    print("  Drag and drop illustration...")
    fig5 = create_drag_drop_illustration()
    fig5.savefig(docs_images_path / "drag_drop_illustration.png", 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig5)
    
    print(f"All illustrations generated successfully! ({docs_images_path})")
    
    # 생성된 파일 목록 출력
    print("\nGenerated image files:")
    for img_file in docs_images_path.glob("*.png"):
        print(f"  - {img_file.name}")

if __name__ == "__main__":
    try:
        save_all_images()
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Please check if matplotlib is installed: pip install matplotlib")