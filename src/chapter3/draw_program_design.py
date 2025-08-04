# -*- coding: utf-8 -*-
"""
Chapter 3: KRenamer 프로그램 설계도 그리기
matplotlib을 사용해서 우리가 만들 프로그램의 모습을 시각화합니다.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import matplotlib.font_manager as fm
from pathlib import Path

# 한글 폰트 설정
plt.rcParams['font.family'] = ['Malgun Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_krenamer_design():
    """KRenamer 프로그램 설계도 생성"""
    
    # 그림 설정
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # 메인 윈도우 프레임
    main_window = FancyBboxPatch(
        (0.5, 0.5), 9, 7,
        boxstyle="round,pad=0.1",
        facecolor='#f0f0f0',
        edgecolor='#333333',
        linewidth=2
    )
    ax.add_patch(main_window)
    
    # 제목 바
    title_bar = FancyBboxPatch(
        (0.6, 6.8), 8.8, 0.6,
        boxstyle="round,pad=0.05",
        facecolor='#4a90e2',
        edgecolor='#2c5aa0',
        linewidth=1
    )
    ax.add_patch(title_bar)
    
    # 제목 텍스트
    ax.text(5, 7.1, '📁 KRenamer - 파일명 변경 도구', 
            ha='center', va='center', fontsize=14, color='white', weight='bold')
    
    # 설명 라벨
    ax.text(5, 6.4, '여러 파일의 이름을 한 번에 쉽게 바꿀 수 있는 도구입니다.', 
            ha='center', va='center', fontsize=10, color='#666666')
    
    # 파일 목록 영역
    file_list_area = FancyBboxPatch(
        (0.8, 2.2), 8.4, 3.8,
        boxstyle="round,pad=0.05",
        facecolor='white',
        edgecolor='#cccccc',
        linewidth=1
    )
    ax.add_patch(file_list_area)
    
    # 파일 목록 제목
    ax.text(1.2, 5.7, '📂 파일 목록 (5개)', ha='left', va='center', 
            fontsize=12, weight='bold', color='#333333')
    
    # 파일 목록 내용 박스
    file_content_box = FancyBboxPatch(
        (1.0, 2.5), 8.0, 3.0,
        boxstyle="square,pad=0.05",
        facecolor='#fafafa',
        edgecolor='#dddddd',
        linewidth=1
    )
    ax.add_patch(file_content_box)
    
    # 파일 목록 아이템들
    files = [
        '📄 회의록_2024.txt',
        '📷 가족여행_제주도.jpg',
        '🎵 좋아하는_팝송.mp3',
        '📊 월간보고서_3월.xlsx',
        '🎬 추억의_영화.mp4'
    ]
    
    for i, file_name in enumerate(files):
        y_pos = 5.2 - (i * 0.4)
        # 선택된 파일들 (1번째, 3번째) 하이라이트
        if i in [0, 2]:
            highlight = FancyBboxPatch(
                (1.1, y_pos - 0.15), 7.8, 0.3,
                boxstyle="square,pad=0.02",
                facecolor='#e3f2fd',
                edgecolor='#2196f3',
                linewidth=1
            )
            ax.add_patch(highlight)
        
        ax.text(1.3, y_pos, file_name, ha='left', va='center', 
                fontsize=10, color='#333333')
    
    # 스크롤바 표시
    scrollbar = FancyBboxPatch(
        (8.8, 2.5), 0.15, 3.0,
        boxstyle="square,pad=0.01",
        facecolor='#cccccc',
        edgecolor='#999999'
    )
    ax.add_patch(scrollbar)
    
    # 스크롤 핸들
    scroll_handle = FancyBboxPatch(
        (8.82, 4.0), 0.11, 0.8,
        boxstyle="round,pad=0.01",
        facecolor='#666666',
        edgecolor='#444444'
    )
    ax.add_patch(scroll_handle)
    
    # 버튼 영역
    buttons = [
        ('📁 파일 추가', 1.2, '#4caf50'),
        ('🗑️ 파일 제거', 3.0, '#f44336'),
        ('🧹 모두 지우기', 4.8, '#ff9800'),
        ('✨ 이름 변경', 7.5, '#2196f3')
    ]
    
    for btn_text, x_pos, color in buttons:
        if btn_text == '✨ 이름 변경':
            # 메인 버튼을 오른쪽에 배치
            btn_width, btn_height = 1.4, 0.4
            x_pos = 7.8
        else:
            btn_width, btn_height = 1.4, 0.4
        
        button = FancyBboxPatch(
            (x_pos, 1.5), btn_width, btn_height,
            boxstyle="round,pad=0.05",
            facecolor=color,
            edgecolor='#333333',
            linewidth=1
        )
        ax.add_patch(button)
        
        ax.text(x_pos + btn_width/2, 1.7, btn_text, 
                ha='center', va='center', fontsize=9, 
                color='white', weight='bold')
    
    # 상태바
    status_bar = FancyBboxPatch(
        (0.6, 0.6), 8.8, 0.4,
        boxstyle="square,pad=0.02",
        facecolor='#f5f5f5',
        edgecolor='#cccccc',
        linewidth=1
    )
    ax.add_patch(status_bar)
    
    # 상태바 내용
    ax.text(1.0, 0.8, '5개의 파일이 추가되었습니다. 파일을 선택하고 이름을 변경해보세요!', 
            ha='left', va='center', fontsize=9, color='#666666')
    
    ax.text(8.8, 0.8, '파일 5개', ha='right', va='center', 
            fontsize=9, color='#2196f3', weight='bold')
    
    # 제목 추가
    ax.text(5, 7.8, 'KRenamer 프로그램 설계도', ha='center', va='center', 
            fontsize=16, weight='bold', color='#333333')
    
    # 설명 박스들 (Chapter 2 요소 매핑)
    mappings = [
        ('Label\n제목과 설명', 0.2, 6.5, '#e8f5e8'),
        ('Listbox\n파일 목록', 0.2, 4.0, '#fff3e0'),
        ('Button\n기능 버튼들', 0.2, 1.7, '#e3f2fd'),
        ('StringVar\n상태 표시', 0.2, 0.8, '#fce4ec')
    ]
    
    for text, x, y, color in mappings:
        mapping_box = FancyBboxPatch(
            (x, y - 0.3), 1.5, 0.6,
            boxstyle="round,pad=0.05",
            facecolor=color,
            edgecolor='#cccccc',
            linewidth=1
        )
        ax.add_patch(mapping_box)
        
        ax.text(x + 0.75, y, text, ha='center', va='center', 
                fontsize=8, color='#333333', weight='bold')
    
    # 화살표들 (매핑 표시)
    arrow_props = dict(arrowstyle='->', lw=1.5, color='#666666')
    
    # Label -> 제목 영역
    ax.annotate('', xy=(2.5, 7.1), xytext=(1.7, 6.5), arrowprops=arrow_props)
    
    # Listbox -> 파일 목록
    ax.annotate('', xy=(2.5, 4.0), xytext=(1.7, 4.0), arrowprops=arrow_props)
    
    # Button -> 버튼 영역
    ax.annotate('', xy=(2.5, 1.7), xytext=(1.7, 1.7), arrowprops=arrow_props)
    
    # StringVar -> 상태바
    ax.annotate('', xy=(2.5, 0.8), xytext=(1.7, 0.8), arrowprops=arrow_props)
    
    plt.tight_layout()
    
    # 이미지 저장
    output_path = Path(__file__).parent.parent.parent / "docs" / "images" / "ch3_program_design.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"프로그램 설계도가 저장되었습니다: {output_path}")
    
    # 화면에 표시 (선택사항)
    # plt.show()
    
    plt.close()

def create_ui_elements_mapping():
    """Chapter 2 UI 요소들이 어떻게 사용되는지 보여주는 다이어그램"""
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # 제목
    ax.text(5, 5.5, 'Chapter 2 → Chapter 3: UI 요소 활용', 
            ha='center', va='center', fontsize=16, weight='bold', color='#333333')
    
    # Chapter 2 요소들 (왼쪽)
    ch2_elements = [
        ('Label', 4.5, '#e8f5e8'),
        ('Listbox', 3.8, '#fff3e0'),
        ('Button', 3.1, '#e3f2fd'),
        ('Frame', 2.4, '#f3e5f5'),
        ('StringVar', 1.7, '#fce4ec')
    ]
    
    for element, y, color in ch2_elements:
        element_box = FancyBboxPatch(
            (0.5, y - 0.25), 2.0, 0.5,
            boxstyle="round,pad=0.05",
            facecolor=color,
            edgecolor='#333333',
            linewidth=1
        )
        ax.add_patch(element_box)
        
        ax.text(1.5, y, element, ha='center', va='center', 
                fontsize=12, weight='bold', color='#333333')
    
    # Chapter 3 활용 (오른쪽)
    ch3_usage = [
        ('제목과 설명 표시', 4.5, '#e8f5e8'),
        ('파일 목록 관리', 3.8, '#fff3e0'),
        ('사용자 액션 처리', 3.1, '#e3f2fd'),
        ('화면 영역 구분', 2.4, '#f3e5f5'),
        ('실시간 상태 업데이트', 1.7, '#fce4ec')
    ]
    
    for usage, y, color in ch3_usage:
        usage_box = FancyBboxPatch(
            (7.0, y - 0.25), 2.5, 0.5,
            boxstyle="round,pad=0.05",
            facecolor=color,
            edgecolor='#333333',
            linewidth=1
        )
        ax.add_patch(usage_box)
        
        ax.text(8.25, y, usage, ha='center', va='center', 
                fontsize=10, color='#333333')
    
    # 화살표들
    arrow_props = dict(arrowstyle='->', lw=2, color='#2196f3')
    
    for i, (_, y, _) in enumerate(ch2_elements):
        ax.annotate('', xy=(6.8, y), xytext=(2.7, y), arrowprops=arrow_props)
    
    # 중앙 텍스트
    ax.text(5, 3.1, '실제 활용', ha='center', va='center', 
            fontsize=14, weight='bold', color='#2196f3',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='#2196f3'))
    
    plt.tight_layout()
    
    # 이미지 저장
    output_path = Path(__file__).parent.parent.parent / "docs" / "images" / "ch3_ui_mapping.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"UI 요소 매핑 다이어그램이 저장되었습니다: {output_path}")
    
    plt.close()

def create_development_steps():
    """KRenamer 개발 단계를 보여주는 플로우차트"""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # 제목
    ax.text(6, 7.5, 'KRenamer 개발 단계별 구성', 
            ha='center', va='center', fontsize=16, weight='bold', color='#333333')
    
    # 단계별 박스들
    steps = [
        ('1단계\n기본 창과 제목', 2, 6, '#e8f5e8'),
        ('2단계\n파일 목록 영역', 6, 6, '#fff3e0'),
        ('3단계\n버튼 영역', 10, 6, '#e3f2fd'),
        ('4단계\n상태바', 4, 4, '#f3e5f5'),
        ('5단계\n완성된 구조', 8, 4, '#fce4ec')
    ]
    
    for step_text, x, y, color in steps:
        step_box = FancyBboxPatch(
            (x - 1, y - 0.5), 2, 1,
            boxstyle="round,pad=0.1",
            facecolor=color,
            edgecolor='#333333',
            linewidth=2
        )
        ax.add_patch(step_box)
        
        ax.text(x, y, step_text, ha='center', va='center', 
                fontsize=11, weight='bold', color='#333333')
    
    # 연결 화살표들
    arrow_props = dict(arrowstyle='->', lw=2, color='#666666')
    
    # 1 -> 2
    ax.annotate('', xy=(5, 6), xytext=(3, 6), arrowprops=arrow_props)
    
    # 2 -> 3
    ax.annotate('', xy=(9, 6), xytext=(7, 6), arrowprops=arrow_props)
    
    # 2 -> 4 (아래로)
    ax.annotate('', xy=(4, 4.5), xytext=(6, 5.5), arrowprops=arrow_props)
    
    # 3 -> 5 (아래로)
    ax.annotate('', xy=(8, 4.5), xytext=(10, 5.5), arrowprops=arrow_props)
    
    # 4 -> 5
    ax.annotate('', xy=(7, 4), xytext=(5, 4), arrowprops=arrow_props)
    
    # 각 단계별 주요 기능 설명
    descriptions = [
        ('• Label로 제목 표시\n• 창 크기 및 배치', 2, 5),
        ('• Listbox + Scrollbar\n• 파일 개수 표시', 6, 5),
        ('• 기능별 Button들\n• 상태에 따른 활성화', 10, 5),
        ('• StringVar로 상태 표시\n• 실시간 업데이트', 4, 3),
        ('• 모든 요소 통합\n• 완전한 애플리케이션', 8, 3)
    ]
    
    for desc, x, y in descriptions:
        ax.text(x, y, desc, ha='center', va='top', 
                fontsize=9, color='#666666',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', 
                         edgecolor='#cccccc', alpha=0.8))
    
    # 하단 정리
    summary_box = FancyBboxPatch(
        (1, 1), 10, 1,
        boxstyle="round,pad=0.1",
        facecolor='#f0f8ff',
        edgecolor='#2196f3',
        linewidth=2
    )
    ax.add_patch(summary_box)
    
    ax.text(6, 1.5, '🎯 최종 결과: Chapter 2의 모든 UI 요소들이 실제 애플리케이션으로 완성!', 
            ha='center', va='center', fontsize=12, weight='bold', color='#2196f3')
    
    plt.tight_layout()
    
    # 이미지 저장
    output_path = Path(__file__).parent.parent.parent / "docs" / "images" / "ch3_development_steps.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"개발 단계 플로우차트가 저장되었습니다: {output_path}")
    
    plt.close()

def main():
    """메인 함수"""
    print("Chapter 3 설계도 및 다이어그램을 생성합니다...")
    
    try:
        # 1. 프로그램 설계도
        create_krenamer_design()
        
        # 2. UI 요소 매핑
        create_ui_elements_mapping()
        
        # 3. 개발 단계 플로우차트
        create_development_steps()
        
        print("\n모든 다이어그램이 성공적으로 생성되었습니다!")
        print("생성된 파일들:")
        print("  - ch3_program_design.png (프로그램 설계도)")
        print("  - ch3_ui_mapping.png (UI 요소 매핑)")
        print("  - ch3_development_steps.png (개발 단계)")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()