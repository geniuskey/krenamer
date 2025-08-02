# Chapter 2: Tkinter GUI 기초

## 👋 GUI 프로그램의 세계로!

안녕하세요! Chapter 1에서 파이썬 기초를 배웠으니, 이제 진짜 재미있는 부분을 시작해봅시다! 

지금까지는 검은 화면에 글자만 나오는 프로그램을 만들었는데, 이번에는 **버튼, 입력창, 메뉴가 있는 진짜 프로그램**을 만들어보겠습니다. 마치 윈도우즈의 메모장이나 계산기처럼요!

## 🎯 이번 챕터에서 배울 것들

우리가 만들 GUI(그래픽 사용자 인터페이스) 프로그램:
- 🖼️ 창(윈도우) 만들기
- 🔘 버튼 추가하고 클릭 이벤트 처리하기
- 📝 텍스트 입력창과 출력 화면 만들기
- 📋 파일 목록을 보여주는 리스트
- 🎨 예쁘게 배치하고 색상 꾸미기

**Tkinter를 사용하는 이유:**
- ✅ 파이썬에 기본으로 포함되어 있음 (별도 설치 불필요)
- ✅ 배우기 쉬움 (초보자 친화적)
- ✅ 윈도우, 맥, 리눅스 모두에서 동작
- ✅ KRenamer 같은 간단한 프로그램에 완벽

## 📚 단계별 학습하기

### 1단계: 첫 번째 창 만들어보기 🖼️

프로그래밍에서 "Hello World!"는 전통입니다. GUI에서는 "첫 번째 창 만들기"가 그 시작이에요!

```python linenums="1" title="src/krenamer-ch2/step1_hello_window.py"
import tkinter as tk

print("🎉 첫 번째 GUI 프로그램을 만들어보자!")

# 1단계: 기본 창 만들기
root = tk.Tk()  # 새로운 창을 만듭니다
root.title("내 첫 번째 GUI 프로그램")  # 창 제목 설정
root.geometry("400x300")  # 창 크기 설정 (가로x세로)

# 2단계: 간단한 텍스트 추가
welcome_label = tk.Label(root, text="안녕하세요! GUI 세계에 오신 것을 환영합니다! 🎉")
welcome_label.pack(pady=20)  # 창에 추가하고 위아래 여백 20픽셀

# 3단계: 창 보여주기 (이것이 없으면 창이 안 보여요!)
print("창을 보여줍니다... 창을 닫으려면 X 버튼을 눌러주세요!")
root.mainloop()

print("프로그램이 종료되었습니다. 수고하셨습니다!")
```

!!! tip "💡 tkinter 기본 구조 이해하기"
    **모든 tkinter 프로그램의 기본 구조:**
    
    1. `import tkinter as tk` → tkinter 라이브러리 가져오기
    2. `root = tk.Tk()` → 메인 창 만들기  
    3. 위젯들 추가하기 (버튼, 라벨 등)
    4. `root.mainloop()` → 창 보여주고 사용자 입력 기다리기

### 2단계: 버튼 추가하고 클릭해보기 🔘

창만 있으면 재미없죠! 클릭할 수 있는 버튼을 추가해봅시다.

```python linenums="20" title="src/krenamer-ch2/step2_buttons.py"
import tkinter as tk

def button_clicked():
    """버튼이 클릭되었을 때 실행되는 함수"""
    print("🎉 버튼이 클릭되었어요!")
    # 라벨의 텍스트를 바꿔봅시다
    status_label.config(text="버튼이 클릭되었습니다! 👍")

def reset_button_clicked():
    """리셋 버튼이 클릭되었을 때 실행되는 함수"""
    print("🔄 리셋 버튼이 클릭되었어요!")
    status_label.config(text="초기 상태로 돌아왔습니다.")

# 메인 창 설정
root = tk.Tk()
root.title("버튼 클릭 연습")
root.geometry("500x400")
root.configure(bg="lightblue")  # 배경색 설정

# 제목 라벨
title_label = tk.Label(
    root, 
    text="🔘 버튼 클릭 연습 프로그램", 
    font=("맑은 고딕", 16, "bold"),
    bg="lightblue"
)
title_label.pack(pady=20)

# 설명 라벨
info_label = tk.Label(
    root,
    text="아래 버튼들을 클릭해보세요!",
    font=("맑은 고딕", 12),
    bg="lightblue"
)
info_label.pack(pady=10)

# 클릭 버튼
click_button = tk.Button(
    root,
    text="클릭하세요! 🖱️",
    command=button_clicked,  # 버튼이 클릭되면 button_clicked 함수 실행
    font=("맑은 고딕", 14),
    bg="lightgreen",
    fg="black",
    width=15,
    height=2
)
click_button.pack(pady=10)

# 리셋 버튼
reset_button = tk.Button(
    root,
    text="리셋 🔄",
    command=reset_button_clicked,
    font=("맑은 고딕", 12),
    bg="lightcoral",
    fg="black",
    width=10
)
reset_button.pack(pady=5)

# 상태 표시 라벨
status_label = tk.Label(
    root,
    text="버튼을 기다리고 있어요...",
    font=("맑은 고딕", 12),
    bg="lightblue",
    fg="darkblue"
)
status_label.pack(pady=20)

# 프로그램 실행
print("버튼 연습 프로그램이 시작됩니다!")
root.mainloop()
```

!!! success "🎉 축하해요!"
    이제 버튼 클릭 이벤트를 처리할 수 있어요!
    
    **핵심 개념:**
    - `command=함수명` → 버튼 클릭시 실행할 함수 지정
    - `.config()` → 위젯의 속성을 나중에 변경
    - `font`, `bg`, `fg` → 글꼴, 배경색, 글자색 설정

### 3단계: 텍스트 입력받고 처리하기 📝

사용자가 직접 글을 입력할 수 있는 프로그램을 만들어봅시다. 파일명을 입력받아서 처리하는 연습이에요!

```python linenums="70" title="src/krenamer-ch2/step3_text_input.py"
import tkinter as tk
from pathlib import Path
import os

def process_filename():
    """입력된 파일명을 처리하는 함수"""
    # 입력창에서 텍스트 가져오기
    filename = filename_entry.get()
    
    if not filename:
        result_text.delete(1.0, tk.END)  # 기존 내용 삭제
        result_text.insert(tk.END, "⚠️ 파일명을 입력해주세요!")
        return
    
    # 파일명 분석하기 (Chapter 1에서 배운 내용!)
    try:
        file_path = Path(filename)
        name_part = file_path.stem  # 확장자 제외한 이름
        extension = file_path.suffix  # 확장자
        
        # 결과를 텍스트 박스에 표시
        result_text.delete(1.0, tk.END)  # 기존 내용 삭제
        result = f"""📁 파일명 분석 결과:

🔤 전체 파일명: {filename}
📝 이름 부분: {name_part}
📎 확장자: {extension}
📏 총 글자 수: {len(filename)}글자

✨ 변환 예시들:
• 소문자로: {filename.lower()}
• 대문자로: {filename.upper()}
• 공백 제거: {filename.replace(' ', '_')}
• 접두사 추가: NEW_{filename}
"""
        result_text.insert(tk.END, result)
        
    except Exception as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"❌ 오류가 발생했습니다: {e}")

def clear_all():
    """모든 내용 지우기"""
    filename_entry.delete(0, tk.END)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "입력창이 초기화되었습니다. 파일명을 입력해보세요! 📝")

# 메인 창 설정
root = tk.Tk()
root.title("파일명 분석기")
root.geometry("600x500")
root.configure(bg="white")

# 제목
title_label = tk.Label(
    root,
    text="📁 파일명 분석기",
    font=("맑은 고딕", 18, "bold"),
    bg="white",
    fg="darkblue"
)
title_label.pack(pady=15)

# 입력 섹션
input_frame = tk.Frame(root, bg="white")
input_frame.pack(pady=10)

input_label = tk.Label(
    input_frame,
    text="파일명을 입력하세요:",
    font=("맑은 고딕", 12),
    bg="white"
)
input_label.pack()

filename_entry = tk.Entry(
    input_frame,
    font=("맑은 고딕", 12),
    width=40,
    justify="center"
)
filename_entry.pack(pady=5)

# 버튼 섹션
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=10)

analyze_button = tk.Button(
    button_frame,
    text="분석하기 🔍",
    command=process_filename,
    font=("맑은 고딕", 12),
    bg="lightgreen",
    width=12
)
analyze_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(
    button_frame,
    text="초기화 🗑️",
    command=clear_all,
    font=("맑은 고딕", 12),
    bg="lightcoral",
    width=12
)
clear_button.pack(side=tk.LEFT, padx=5)

# 결과 표시 영역
result_label = tk.Label(
    root,
    text="📋 분석 결과:",
    font=("맑은 고딕", 12, "bold"),
    bg="white"
)
result_label.pack(pady=(20, 5))

result_text = tk.Text(
    root,
    height=15,
    width=70,
    font=("맑은 고딕", 10),
    bg="lightyellow",
    wrap=tk.WORD
)
result_text.pack(pady=5, padx=20)

# 초기 메시지
result_text.insert(tk.END, "파일명을 입력하고 '분석하기' 버튼을 눌러보세요! 📝")

print("파일명 분석기가 시작됩니다!")
root.mainloop()
```

!!! note "🤔 새로 배운 위젯들"
    - **Entry**: 한 줄 텍스트 입력창
        - `.get()` → 입력된 텍스트 가져오기
        - `.delete(0, tk.END)` → 모든 텍스트 삭제
    
    - **Text**: 여러 줄 텍스트 표시/입력 영역
        - `.insert(tk.END, 텍스트)` → 텍스트 추가
        - `.delete(1.0, tk.END)` → 모든 텍스트 삭제
    
    - **Frame**: 다른 위젯들을 그룹으로 묶는 컨테이너

### 4단계: 파일 목록 관리하기 📋

이제 진짜 KRenamer다운 기능을 만들어봅시다! 파일 목록을 추가하고 관리하는 프로그램이에요.

```python linenums="150" title="src/krenamer-ch2/step4_file_list.py"
import tkinter as tk
from tkinter import messagebox

class FileListManager:
    """파일 목록을 관리하는 클래스"""
    
    def __init__(self):
        self.files = []  # 파일 목록 저장
        
    def add_file(self, filename):
        """파일 추가"""
        if filename and filename not in self.files:
            self.files.append(filename)
            return True
        return False
    
    def remove_file(self, filename):
        """파일 제거"""
        if filename in self.files:
            self.files.remove(filename)
            return True
        return False
    
    def get_file_count(self):
        """총 파일 개수 반환"""
        return len(self.files)

# 전역 변수
file_manager = FileListManager()

def add_file_to_list():
    """파일을 목록에 추가하는 함수"""
    filename = file_entry.get().strip()
    
    if not filename:
        messagebox.showwarning("입력 오류", "파일명을 입력해주세요!")
        return
    
    if file_manager.add_file(filename):
        # 리스트박스에 추가
        file_listbox.insert(tk.END, filename)
        file_entry.delete(0, tk.END)  # 입력창 초기화
        update_status()
        print(f"✅ '{filename}' 파일이 추가되었습니다.")
    else:
        messagebox.showinfo("중복 파일", "이미 존재하는 파일명입니다!")

def remove_selected_file():
    """선택된 파일을 목록에서 제거"""
    try:
        selected_index = file_listbox.curselection()[0]  # 선택된 항목의 인덱스
        selected_file = file_listbox.get(selected_index)  # 선택된 파일명
        
        # 파일 매니저에서 제거
        if file_manager.remove_file(selected_file):
            file_listbox.delete(selected_index)  # 리스트박스에서 제거
            update_status()
            print(f"🗑️ '{selected_file}' 파일이 제거되었습니다.")
        
    except IndexError:
        messagebox.showwarning("선택 오류", "제거할 파일을 선택해주세요!")

def clear_all_files():
    """모든 파일 제거"""
    if file_manager.get_file_count() == 0:
        messagebox.showinfo("알림", "제거할 파일이 없습니다!")
        return
    
    # 확인 대화상자
    result = messagebox.askyesno("확인", "정말로 모든 파일을 제거하시겠습니까?")
    if result:
        file_manager.files.clear()
        file_listbox.delete(0, tk.END)
        update_status()
        print("🧹 모든 파일이 제거되었습니다.")

def update_status():
    """상태 표시줄 업데이트"""
    count = file_manager.get_file_count()
    status_label.config(text=f"총 {count}개의 파일이 관리되고 있습니다.")

def show_file_info():
    """선택된 파일의 정보 표시"""
    try:
        selected_index = file_listbox.curselection()[0]
        selected_file = file_listbox.get(selected_index)
        
        from pathlib import Path
        file_path = Path(selected_file)
        
        info = f"""📁 파일 정보:

📄 파일명: {selected_file}
📝 이름: {file_path.stem}
📎 확장자: {file_path.suffix}
📏 길이: {len(selected_file)}글자
📍 목록 위치: {selected_index + 1}번째
"""
        messagebox.showinfo("파일 정보", info)
        
    except IndexError:
        messagebox.showwarning("선택 오류", "정보를 볼 파일을 선택해주세요!")

# 메인 창 설정
root = tk.Tk()
root.title("파일 목록 관리자")
root.geometry("700x600")
root.configure(bg="white")

# 제목
title_label = tk.Label(
    root,
    text="📋 파일 목록 관리자",
    font=("맑은 고딕", 18, "bold"),
    bg="white",
    fg="darkgreen"
)
title_label.pack(pady=15)

# 파일 추가 섹션
add_frame = tk.Frame(root, bg="white")
add_frame.pack(pady=10)

tk.Label(
    add_frame,
    text="추가할 파일명:",
    font=("맑은 고딕", 12),
    bg="white"
).pack(side=tk.LEFT)

file_entry = tk.Entry(
    add_frame,
    font=("맑은 고딕", 12),
    width=30
)
file_entry.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(
    add_frame,
    text="추가 ➕",
    command=add_file_to_list,
    font=("맑은 고딕", 11),
    bg="lightgreen"
)
add_button.pack(side=tk.LEFT, padx=5)

# 파일 목록 표시 섹션
list_frame = tk.Frame(root, bg="white")
list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

tk.Label(
    list_frame,
    text="📂 파일 목록:",
    font=("맑은 고딕", 12, "bold"),
    bg="white"
).pack(anchor=tk.W)

# 스크롤바가 있는 리스트박스
scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

file_listbox = tk.Listbox(
    list_frame,
    font=("맑은 고딕", 11),
    height=15,
    yscrollcommand=scrollbar.set
)
file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=file_listbox.yview)

# 버튼 섹션
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=10)

remove_button = tk.Button(
    button_frame,
    text="선택 제거 🗑️",
    command=remove_selected_file,
    font=("맑은 고딕", 11),
    bg="lightcoral"
)
remove_button.pack(side=tk.LEFT, padx=5)

info_button = tk.Button(
    button_frame,
    text="파일 정보 ℹ️",
    command=show_file_info,
    font=("맑은 고딕", 11),
    bg="lightblue"
)
info_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(
    button_frame,
    text="전체 삭제 🧹",
    command=clear_all_files,
    font=("맑은 고딕", 11),
    bg="orange"
)
clear_button.pack(side=tk.LEFT, padx=5)

# 상태 표시줄
status_label = tk.Label(
    root,
    text="파일을 추가해보세요!",
    font=("맑은 고딕", 10),
    bg="lightgray",
    relief=tk.SUNKEN,
    anchor=tk.W
)
status_label.pack(side=tk.BOTTOM, fill=tk.X)

# Enter 키로 파일 추가
file_entry.bind('<Return>', lambda event: add_file_to_list())

print("파일 목록 관리자가 시작됩니다!")
root.mainloop()
```

!!! success "🏆 대단해요!"
    이제 진짜 프로그램 같은 기능들을 만들 수 있어요!
    
    **새로 배운 것들:**
    - **Listbox**: 목록을 표시하고 선택할 수 있는 위젯
    - **Scrollbar**: 스크롤 기능 추가
    - **messagebox**: 알림창, 확인창 표시
    - **이벤트 바인딩**: Enter 키 등의 키보드 이벤트 처리

### 5단계: 레이아웃 관리와 예쁘게 꾸미기 🎨

지금까지는 `.pack()`만 사용했는데, 더 정교한 레이아웃을 만들어봅시다!

```python linenums="280" title="src/krenamer-ch2/step5_layout_design.py"
import tkinter as tk
from tkinter import ttk  # 더 예쁜 위젯들

def create_modern_gui():
    """현대적인 GUI 만들기"""
    
    root = tk.Tk()
    root.title("현대적인 KRenamer 미리보기")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")
    
    # 스타일 설정
    style = ttk.Style()
    style.theme_use('clam')  # 모던한 테마
    
    # 메인 컨테이너
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # 제목 영역 (1행)
    title_frame = ttk.LabelFrame(main_frame, text="KRenamer - 파일명 변경 도구", padding="10")
    title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
    
    welcome_label = ttk.Label(
        title_frame,
        text="🎉 KRenamer에 오신 것을 환영합니다!",
        font=("맑은 고딕", 14, "bold")
    )
    welcome_label.pack()
    
    # 왼쪽 패널 - 파일 목록 (2행, 1열)
    left_frame = ttk.LabelFrame(main_frame, text="📂 파일 목록", padding="10")
    left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
    
    # 파일 목록 (Treeview 사용)
    file_tree = ttk.Treeview(left_frame, columns=('size', 'type'), show='tree headings', height=15)
    file_tree.heading('#0', text='파일명')
    file_tree.heading('size', text='크기')
    file_tree.heading('type', text='종류')
    
    file_tree.column('#0', width=200)
    file_tree.column('size', width=80)
    file_tree.column('type', width=80)
    
    # 스크롤바 추가
    tree_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=file_tree.yview)
    file_tree.configure(yscrollcommand=tree_scroll.set)
    
    file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    # 샘플 데이터 추가
    file_tree.insert('', tk.END, text='📄 문서1.pdf', values=('1.2MB', 'PDF'))
    file_tree.insert('', tk.END, text='🖼️ 사진1.jpg', values=('2.5MB', 'IMAGE'))
    file_tree.insert('', tk.END, text='🎵 음악1.mp3', values=('4.1MB', 'AUDIO'))
    file_tree.insert('', tk.END, text='📝 메모.txt', values=('1KB', 'TEXT'))
    
    # 오른쪽 패널 - 설정 및 미리보기 (2행, 2열)
    right_frame = ttk.LabelFrame(main_frame, text="⚙️ 변경 설정", padding="10")
    right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
    
    # 탭 위젯으로 설정 구분
    notebook = ttk.Notebook(right_frame)
    notebook.pack(fill=tk.BOTH, expand=True)
    
    # 탭 1: 기본 설정
    basic_tab = ttk.Frame(notebook)
    notebook.add(basic_tab, text='기본 설정')
    
    # 접두사 설정
    ttk.Label(basic_tab, text="접두사:").grid(row=0, column=0, sticky=tk.W, pady=5)
    prefix_var = tk.StringVar(value="NEW_")
    prefix_entry = ttk.Entry(basic_tab, textvariable=prefix_var, width=20)
    prefix_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
    
    # 접미사 설정
    ttk.Label(basic_tab, text="접미사:").grid(row=1, column=0, sticky=tk.W, pady=5)
    suffix_var = tk.StringVar(value="_COPY")
    suffix_entry = ttk.Entry(basic_tab, textvariable=suffix_var, width=20)
    suffix_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
    
    # 옵션 체크박스들
    ttk.Label(basic_tab, text="옵션:").grid(row=2, column=0, sticky=tk.W, pady=(15, 5))
    
    lowercase_var = tk.BooleanVar()
    ttk.Checkbutton(basic_tab, text="소문자로 변환", variable=lowercase_var).grid(row=3, column=0, columnspan=2, sticky=tk.W)
    
    remove_spaces_var = tk.BooleanVar()
    ttk.Checkbutton(basic_tab, text="공백 제거", variable=remove_spaces_var).grid(row=4, column=0, columnspan=2, sticky=tk.W)
    
    add_numbers_var = tk.BooleanVar()
    ttk.Checkbutton(basic_tab, text="순번 추가", variable=add_numbers_var).grid(row=5, column=0, columnspan=2, sticky=tk.W)
    
    # 탭 2: 미리보기
    preview_tab = ttk.Frame(notebook)
    notebook.add(preview_tab, text='미리보기')
    
    ttk.Label(preview_tab, text="변경 결과 미리보기:").pack(anchor=tk.W, pady=(0, 5))
    
    preview_text = tk.Text(preview_tab, height=10, width=30, font=("맑은 고딕", 9))
    preview_text.pack(fill=tk.BOTH, expand=True)
    
    # 샘플 미리보기 텍스트
    preview_text.insert(tk.END, """📄 문서1.pdf → NEW_문서1_COPY.pdf
🖼️ 사진1.jpg → NEW_사진1_COPY.jpg  
🎵 음악1.mp3 → NEW_음악1_COPY.mp3
📝 메모.txt → NEW_메모_COPY.txt

✨ 4개 파일이 변경됩니다.""")
    
    # 하단 버튼 영역 (3행)
    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    # 진행률 표시
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(bottom_frame, variable=progress_var, maximum=100)
    progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    
    # 실행 버튼들
    ttk.Button(bottom_frame, text="미리보기 🔍", width=12).pack(side=tk.RIGHT, padx=2)
    ttk.Button(bottom_frame, text="실행하기 ▶️", width=12).pack(side=tk.RIGHT, padx=2)
    ttk.Button(bottom_frame, text="초기화 🔄", width=12).pack(side=tk.RIGHT, padx=2)
    
    # 그리드 가중치 설정 (창 크기 변경시 반응형으로)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(1, weight=1)
    
    return root

# 프로그램 실행
if __name__ == "__main__":
    print("🎨 현대적인 GUI 데모를 시작합니다!")
    app = create_modern_gui()
    app.mainloop()
    print("프로그램이 종료되었습니다.")
```

!!! tip "🎨 GUI 디자인 팁"
    **레이아웃 관리자 종류:**
    - **pack()**: 간단한 수직/수평 배치
    - **grid()**: 격자 형태로 정교한 배치 (추천!)
    - **place()**: 절대 좌표로 배치 (특수한 경우에만)
    
    **ttk 위젯의 장점:**
    - 운영체제 기본 스타일을 따라감
    - 더 현대적이고 예쁜 외관
    - 테마 변경 가능

## 🧪 직접 해보기 (실습 과제)

### 🌟 기본 도전과제

#### 1. 계산기 만들기 🧮
```python
# 간단한 계산기 GUI를 만들어보세요!
# 힌트: 
# - 숫자 버튼들 (0-9)
# - 연산자 버튼들 (+, -, *, /)
# - 결과 표시 라벨
# - 계산 로직 구현
```

#### 2. 색상 변경기 🎨
```python
# 버튼을 누르면 배경색이 바뀌는 프로그램
# 힌트:
# - 여러 색상 버튼들
# - root.configure(bg="색상명") 사용
# - 현재 색상 표시 라벨
```

### 🚀 고급 도전과제

#### 3. 간단한 메모장 📝
```python
# 텍스트를 입력하고 저장/불러오기 기능
# 힌트:
# - Text 위젯 사용
# - 파일 저장/열기 기능
# - 메뉴바 추가 (tkinter.Menu)
```

## 🎯 Chapter 2 정리

### ✅ 배운 것들 체크해보기

**Tkinter 기초:**
- [ ] 창 만들기 (`tk.Tk()`, `mainloop()`)
- [ ] 기본 위젯들 (Label, Button, Entry, Text)
- [ ] 이벤트 처리 (`command`, 함수 연결)
- [ ] 레이아웃 관리 (pack, grid)

**GUI 프로그래밍 개념:**
- [ ] 사용자 인터페이스 설계
- [ ] 이벤트 기반 프로그래밍
- [ ] 위젯 속성 설정 (색상, 폰트, 크기)
- [ ] 사용자 입력 처리와 검증

**실전 기능들:**
- [ ] 파일 목록 관리
- [ ] 상태 표시 및 피드백
- [ ] 에러 처리와 사용자 알림
- [ ] 반응형 레이아웃

### 🌟 최종 점검 문제

다음 코드를 보고 어떤 GUI가 만들어질지 상상할 수 있나요?

```python
import tkinter as tk

root = tk.Tk()
root.title("미스터리 프로그램")

label = tk.Label(root, text="클릭하세요!")
button = tk.Button(root, text="마법 버튼", 
                  command=lambda: label.config(text="마법이 일어났어요! ✨"))

label.pack(pady=10)
button.pack(pady=5)
root.mainloop()
```

**답:** 라벨과 버튼이 있는 창이 나타나고, 버튼을 클릭하면 라벨의 텍스트가 바뀝니다!

---

!!! success "🎉 Chapter 2 완주 축하드려요!"
    GUI 프로그래밍의 기초를 성공적으로 마스터했습니다!
    
    **이제 할 수 있는 것들:**
    - ✅ 버튼, 입력창, 리스트가 있는 프로그램 만들기
    - ✅ 사용자 클릭 이벤트 처리하기
    - ✅ 예쁘고 사용하기 쉬운 인터페이스 디자인
    - ✅ 파일 정보를 화면에 표시라기
    - ✅ 현대적인 GUI 레이아웃 구성

!!! tip "🚀 다음 단계 준비하기"
    **Chapter 3에서는:**
    - 드래그 앤 드롭으로 파일 가져오기
    - 실제 파일 시스템과 연동하기
    - 파일 탐색기와 같은 고급 기능
    
    Chapter 1과 2에서 배운 모든 내용이 합쳐집니다!