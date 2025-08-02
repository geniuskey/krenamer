# KRenamer Chapter 2: Tkinter GUI 기초

## 📖 개요

이 디렉토리는 KRenamer 프로젝트의 Chapter 2에 해당하는 학습 자료들을 포함하고 있습니다. Tkinter를 사용한 GUI 프로그래밍의 기초를 단계별로 배울 수 있도록 구성되어 있습니다.

## 🎯 학습 목표

- Tkinter 기본 위젯들의 사용법 익히기
- 이벤트 기반 프로그래밍 이해하기
- GUI 레이아웃 관리 방법 학습하기
- 사용자 친화적인 인터페이스 설계 원칙 이해하기

## 📁 파일 구조

```
src/krenamer-ch2/
├── main.py                    # 학습 런처 (모든 단계를 선택해서 실행)
├── step1_hello_window.py      # 1단계: 첫 번째 창 만들기
├── step2_buttons.py           # 2단계: 버튼과 이벤트 처리
├── step3_text_input.py        # 3단계: 텍스트 입력과 처리
├── step4_file_list.py         # 4단계: 파일 목록 관리
├── step5_layout_design.py     # 5단계: 현대적인 레이아웃 디자인
└── README.md                  # 이 파일
```

## 🚀 실행 방법

### 방법 1: 학습 런처 사용 (권장)
```bash
cd src/krenamer-ch2
python main.py
```
학습 런처가 실행되어 각 단계를 선택해서 학습할 수 있습니다.

### 방법 2: 개별 단계 실행
```bash
cd src/krenamer-ch2
python step1_hello_window.py      # 1단계만 실행
python step2_buttons.py           # 2단계만 실행
# ... 등등
```

## 📚 학습 단계별 상세 설명

### 1단계: 첫 번째 창 만들기 (`step1_hello_window.py`)
- **학습 내용**: tkinter 기본 구조, 창 생성, 라벨 위젯
- **핵심 개념**: `tk.Tk()`, `mainloop()`, `Label`, `pack()`
- **실행 결과**: 간단한 환영 메시지가 있는 창

### 2단계: 버튼과 이벤트 처리 (`step2_buttons.py`)
- **학습 내용**: 버튼 위젯, 이벤트 처리, 함수 연결
- **핵심 개념**: `Button`, `command` 매개변수, 콜백 함수
- **실행 결과**: 클릭 가능한 버튼들과 상태 변화

### 3단계: 텍스트 입력과 처리 (`step3_text_input.py`)
- **학습 내용**: 입력 위젯, 텍스트 처리, 파일명 분석
- **핵심 개념**: `Entry`, `Text`, `.get()`, `.insert()`
- **실행 결과**: 파일명을 입력받아 분석하는 프로그램

### 4단계: 파일 목록 관리 (`step4_file_list.py`)
- **학습 내용**: 리스트 위젯, 스크롤바, 대화상자
- **핵심 개념**: `Listbox`, `Scrollbar`, `messagebox`
- **실행 결과**: 파일 목록을 추가/제거/관리하는 프로그램

### 5단계: 현대적인 레이아웃 (`step5_layout_design.py`)
- **학습 내용**: ttk 위젯, grid 레이아웃, 탭 위젯
- **핵심 개념**: `ttk`, `grid()`, `Notebook`, `Treeview`
- **실행 결과**: 전문적인 외관의 KRenamer 미리보기

## 💡 학습 팁

1. **순서대로 학습하세요**: 각 단계는 이전 단계의 지식을 바탕으로 구성되어 있습니다.

2. **코드를 직접 수정해보세요**: 예제 코드의 값들을 바꿔보면서 어떤 변화가 일어나는지 관찰해보세요.

3. **에러를 두려워하지 마세요**: 에러 메시지를 읽고 문제를 해결하는 과정도 중요한 학습입니다.

4. **문서를 참고하세요**: 
   - [Tkinter 공식 문서](https://docs.python.org/3/library/tkinter.html)
   - [Real Python Tkinter 튜토리얼](https://realpython.com/python-gui-tkinter/)

## 🛠️ 요구사항

- Python 3.6 이상
- tkinter (Python 표준 라이브러리에 포함)
- Windows/Mac/Linux 지원

## ❓ 문제 해결

### 한글 폰트가 제대로 표시되지 않는 경우
```python
# 시스템에 맞는 폰트로 변경
font=("Arial", 12)  # Windows
font=("San Francisco", 12)  # Mac
font=("Ubuntu", 12)  # Linux
```

### tkinter가 설치되지 않은 경우
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter

# Mac (Homebrew)
brew install python-tk
```

## 🎓 다음 단계

Chapter 2를 완료하면 다음 내용을 학습할 수 있습니다:
- **Chapter 3**: 드래그 앤 드롭 기능 구현
- **Chapter 4**: 실제 파일명 변경 로직
- **Chapter 5**: 고급 필터링 및 설정 관리

---

💪 열심히 학습하여 멋진 GUI 프로그램을 만들어보세요!