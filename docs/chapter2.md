# Chapter 2: Tkinter UI 요소 완전 정복

## 👋 GUI 프로그램의 세계로!

안녕하세요! Chapter 1에서 파이썬 기초를 배웠으니, 이제 진짜 재미있는 부분을 시작해봅시다! 

지금까지는 검은 화면에 글자만 나오는 프로그램을 만들었는데, 이번에는 **버튼, 입력창, 메뉴가 있는 진짜 프로그램**<!-- -->을 만들어보겠습니다.

## 🎯 이번 챕터에서 배울 것들

**Tkinter를 선택하는 이유:**

- ✅ 파이썬에 기본으로 포함되어 있음 (별도 설치 불필요)
- ✅ 배우기 쉬움 (초보자 친화적)
- ✅ 윈도우, 맥, 리눅스 모두에서 동작
- ✅ KRenamer 같은 데스크톱 앱에 완벽

**학습할 UI 요소들:**

- 🖼️ **기본 구조**: 창(Window)과 기본 설정들
- 📝 **텍스트 요소**: Label, Entry, Text
- 🔘 **버튼과 체크박스**: Button, Checkbutton, Radiobutton
- 📋 **목록과 선택**: Listbox, Combobox
- 🖼️ **레이아웃**: Frame, 배치 관리자들
- 🎨 **고급 요소**: Canvas, Menu, Scrollbar

## 📚 1. 기본 구조 - 모든 GUI의 출발점

### 첫 번째 창 만들어보기

```python linenums="1" title="src/chapter2/01_basic_window.py"
import tkinter as tk

print("🎉 첫 번째 GUI 프로그램을 만들어보자!")

# 1단계: 기본 창 만들기
root = tk.Tk()  # 새로운 창을 만듭니다
root.title("내 첫 번째 GUI 프로그램")  # 창 제목 설정
root.geometry("400x300")  # 창 크기 설정 (가로x세로)

# 2단계: 창 보여주기 (이것이 없으면 창이 안 보여요!)
print("창을 보여줍니다... 창을 닫으려면 X 버튼을 눌러주세요!")
root.mainloop()

print("프로그램이 종료되었습니다.")
```

![기본 창 예제](images/ch2_basic_window.png)

*위 코드를 실행하면 간단한 GUI 창이 나타납니다. 제목 표시줄과 크기가 설정된 기본 창의 모습입니다.*

!!! tip "💡 tkinter 기본 구조 이해하기"
    **모든 tkinter 프로그램의 필수 3단계:**
    
    1. **`import tkinter as tk`** → tkinter 라이브러리 가져오기
    2. **`root = tk.Tk()`** → 메인 창 만들기  
    3. **`root.mainloop()`** → 창 보여주고 사용자 입력 기다리기

### 창 설정 옵션들

```python linenums="15" title="src/chapter2/02_window_config.py"
import tkinter as tk

root = tk.Tk()

# 창 설정 옵션들
root.title("창 설정 연습")                    # 제목
root.geometry("500x400")                   # 크기
root.resizable(True, False)               # 가로만 크기 조절 가능
root.minsize(300, 200)                    # 최소 크기
root.maxsize(800, 600)                    # 최대 크기
root.configure(bg="lightblue")            # 배경색

# 창을 화면 중앙에 배치하기
def center_window():
    root.update_idletasks()
    width = 500
    height = 400
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

center_window()
root.mainloop()
```

## 📝 2. 텍스트 요소들 - 정보를 보여주고 받기

### Label - 텍스트와 이미지 표시

```python linenums="1" title="src/chapter2/03_labels.py"
import tkinter as tk

root = tk.Tk()
root.title("Label 연습")
root.geometry("500x400")
root.configure(bg="white")

# 기본 라벨
basic_label = tk.Label(root, text="안녕하세요! 이것은 기본 라벨입니다.")
basic_label.pack(pady=10)

# 스타일이 적용된 라벨
styled_label = tk.Label(
    root,
    text="🎨 예쁘게 꾸민 라벨",
    font=("맑은 고딕", 16, "bold"),    # 폰트 설정
    fg="blue",                         # 글자색
    bg="lightyellow",                  # 배경색
    width=20,                          # 너비 (글자 수)
    height=2                           # 높이 (줄 수)
)
styled_label.pack(pady=10)

# 여러 줄 라벨
multiline_label = tk.Label(
    root,
    text="여러 줄로 된 라벨입니다.\n두 번째 줄\n세 번째 줄",
    font=("맑은 고딕", 12),
    justify=tk.LEFT,                   # 텍스트 정렬
    bg="lightgreen"
)
multiline_label.pack(pady=10)

# 동적으로 변하는 라벨
dynamic_var = tk.StringVar()
dynamic_var.set("변경 가능한 텍스트")

dynamic_label = tk.Label(
    root,
    textvariable=dynamic_var,          # StringVar 사용
    font=("맑은 고딕", 14),
    fg="red"
)
dynamic_label.pack(pady=10)

# 텍스트를 변경하는 버튼
def change_text():
    import random
    texts = ["안녕하세요!", "Hello!", "こんにちは!", "Bonjour!", "¡Hola!"]
    dynamic_var.set(random.choice(texts))

change_button = tk.Button(root, text="텍스트 변경", command=change_text)
change_button.pack(pady=10)

root.mainloop()
```

![Label 예제들](images/ch2_labels.png)

*Label 위젯의 다양한 스타일링 옵션들을 보여주는 예제입니다. 기본 라벨, 스타일 적용된 라벨, 여러 줄 라벨, 그리고 동적으로 변경되는 라벨을 확인할 수 있습니다.*

### Entry - 한 줄 텍스트 입력

Entry 위젯은 사용자로부터 한 줄의 텍스트를 입력받을 때 사용합니다. 단계별로 살펴보겠습니다.

#### 🔹 1단계: 기본 Entry 만들기

```python linenums="1" title="src/chapter2/04a_basic_entry.py"
import tkinter as tk

root = tk.Tk()
root.title("Entry 기본 사용법")
root.geometry("400x200")

# 기본 입력창
tk.Label(root, text="이름을 입력하세요:", font=("맑은 고딕", 12)).pack(pady=10)
name_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30)
name_entry.pack(pady=5)

# 입력값 가져오기
def show_input():
    user_input = name_entry.get()  # Entry에서 텍스트 가져오기
    result_label.config(text=f"입력하신 내용: {user_input}")

tk.Button(root, text="입력값 확인", command=show_input).pack(pady=10)

result_label = tk.Label(root, text="", font=("맑은 고딕", 11), fg="blue")
result_label.pack()

root.mainloop()
```

#### 🔹 2단계: 다양한 Entry 스타일

```python linenums="15" title="src/chapter2/04b_entry_styles.py"
import tkinter as tk

root = tk.Tk()
root.title("Entry 다양한 스타일")
root.geometry("500x300")

# 일반 텍스트 입력창
tk.Label(root, text="이름:", font=("맑은 고딕", 12)).pack(pady=5)
name_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30)
name_entry.pack(pady=5)

# 비밀번호 입력창 (별표로 숨김)
tk.Label(root, text="비밀번호:", font=("맑은 고딕", 12)).pack(pady=5)
password_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30, show="*")
password_entry.pack(pady=5)

# 읽기 전용 입력창
tk.Label(root, text="읽기 전용:", font=("맑은 고딕", 12)).pack(pady=5)
readonly_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30, state="readonly")
readonly_entry.insert(0, "이 텍스트는 수정할 수 없습니다")
readonly_entry.pack(pady=5)

root.mainloop()
```

#### 🔹 3단계: 입력값 검증과 처리

```python linenums="30" title="src/chapter2/04c_entry_validation.py"
import tkinter as tk
import tkinter.messagebox as msgbox

root = tk.Tk()
root.title("Entry 입력값 검증")
root.geometry("500x400")

# 입력 필드들
tk.Label(root, text="이름:", font=("맑은 고딕", 12)).pack(pady=5)
name_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30)
name_entry.pack(pady=5)

tk.Label(root, text="나이 (숫자만):", font=("맑은 고딕", 12)).pack(pady=5)
age_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30)
age_entry.pack(pady=5)

# 입력값 처리 함수
def process_input():
    name = name_entry.get()
    age = age_entry.get()
    
    # 입력값 검증
    if not name:
        msgbox.showwarning("입력 오류", "이름을 입력해주세요!")
        return
    
    if age and not age.isdigit():
        msgbox.showerror("입력 오류", "나이는 숫자만 입력해주세요!")
        return
    
    # 결과 표시
    result = f"안녕하세요, {name}님!"
    if age:
        result += f"\n나이: {age}세"
    
    msgbox.showinfo("입력 결과", result)

# 버튼과 기능
tk.Button(root, text="입력 처리", command=process_input, 
          font=("맑은 고딕", 12), bg="lightgreen").pack(pady=10)

def clear_all():
    name_entry.delete(0, tk.END)  # Entry 내용 지우기
    age_entry.delete(0, tk.END)

tk.Button(root, text="모두 지우기", command=clear_all,
          font=("맑은 고딕", 12), bg="lightcoral").pack(pady=5)

# Enter 키로 입력 처리
root.bind('<Return>', lambda event: process_input())

root.mainloop()
```

!!! tip "💡 Entry 위젯 핵심 포인트"
    - **`.get()`**: Entry에서 텍스트 가져오기
    - **`.insert(position, text)`**: 특정 위치에 텍스트 삽입
    - **`.delete(start, end)`**: 특정 범위의 텍스트 삭제
    - **`show="*"`**: 비밀번호처럼 문자를 숨김 처리
    - **`state="readonly"`**: 읽기 전용으로 설정

### Text - 여러 줄 텍스트 입력/표시

Text 위젯은 Entry와 달리 여러 줄의 텍스트를 다룰 때 사용합니다. 단계별로 알아보겠습니다.

#### 🔹 1단계: 기본 Text 위젯

```python linenums="1" title="src/chapter2/05a_basic_text.py"
import tkinter as tk

root = tk.Tk()
root.title("Text 기본 사용법")
root.geometry("500x300")

tk.Label(root, text="📝 여러 줄 텍스트 입력:", font=("맑은 고딕", 12, "bold")).pack(pady=5)

# 기본 Text 위젯
text_widget = tk.Text(
    root,
    height=10,
    width=50,
    font=("맑은 고딕", 11),
    wrap=tk.WORD,              # 단어 단위로 줄바꿈
    bg="lightyellow"
)
text_widget.pack(pady=10)

# 초기 텍스트 넣기
text_widget.insert(tk.END, "여기에 여러 줄의 텍스트를 입력할 수 있습니다.\n")
text_widget.insert(tk.END, "Enter를 눌러서 줄을 바꿀 수 있습니다.\n")
text_widget.insert(tk.END, "Text 위젯은 긴 문서 작성에 적합합니다.")

root.mainloop()
```

#### 🔹 2단계: 스크롤이 있는 Text

```python linenums="20" title="src/chapter2/05b_scrolled_text.py"
import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
root.title("스크롤 가능한 Text")
root.geometry("500x400")

tk.Label(root, text="📋 스크롤 가능한 텍스트:", font=("맑은 고딕", 12, "bold")).pack(pady=5)

# ScrolledText 사용 (자동으로 스크롤바가 추가됨)
scrolled_text = scrolledtext.ScrolledText(
    root,
    height=15,
    width=60,
    font=("맑은 고딕", 11),
    bg="lightblue"
)
scrolled_text.pack(pady=10, fill=tk.BOTH, expand=True)

# 많은 양의 텍스트 추가
for i in range(50):
    scrolled_text.insert(tk.END, f"이것은 {i+1}번째 줄입니다. 스크롤해서 아래 내용을 확인해보세요!\n")

root.mainloop()
```

#### 🔹 3단계: Text 조작 기능들

```python linenums="40" title="src/chapter2/05c_text_operations.py"
import tkinter as tk
import tkinter.messagebox as msgbox

root = tk.Tk()
root.title("Text 조작 기능")
root.geometry("600x500")

# Text 위젯
text_widget = tk.Text(root, height=15, width=70, font=("맑은 고딕", 11))
text_widget.pack(pady=10)

# 기능 버튼들
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

def add_sample_text():
    """샘플 텍스트 추가"""
    sample = """안녕하세요! Text 위젯 예제입니다.

Text 위젯의 특징:
• 여러 줄 텍스트 입력 가능
• 스크롤 기능 지원  
• 텍스트 서식 지원
• 검색 및 바꾸기 기능

이 위젯으로 간단한 텍스트 에디터를 만들 수 있습니다."""
    
    text_widget.insert(tk.END, sample)

def clear_all():
    """모든 텍스트 지우기"""
    text_widget.delete(1.0, tk.END)

def get_text_info():
    """텍스트 정보 표시"""
    content = text_widget.get(1.0, tk.END)
    lines = content.count('\n')
    chars = len(content.strip())  # 마지막 자동 개행 제외
    words = len(content.split())
    
    info = f"줄 수: {lines}\n글자 수: {chars}\n단어 수: {words}"
    msgbox.showinfo("텍스트 정보", info)

def save_text():
    """텍스트 내용 확인"""
    content = text_widget.get(1.0, tk.END)
    if content.strip():
        msgbox.showinfo("저장", f"다음 내용이 저장됩니다:\n\n{content[:100]}...")
    else:
        msgbox.showwarning("저장", "저장할 내용이 없습니다.")

# 버튼들
tk.Button(button_frame, text="샘플 텍스트 추가", command=add_sample_text,
          font=("맑은 고딕", 10), bg="lightgreen").pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="모두 지우기", command=clear_all,
          font=("맑은 고딕", 10), bg="lightcoral").pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="텍스트 정보", command=get_text_info,
          font=("맑은 고딕", 10), bg="lightblue").pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="내용 확인", command=save_text,
          font=("맑은 고딕", 10), bg="lightyellow").pack(side=tk.LEFT, padx=5)

root.mainloop()
```

!!! tip "💡 Text 위젯 핵심 포인트"
    - **Text vs Entry**: Entry는 한 줄, Text는 여러 줄
    - **위치 표시**: `"1.0"` = 1번째 줄, 0번째 문자 (첫 번째 위치)
    - **`tk.END`**: 텍스트의 마지막 위치
    - **`wrap=tk.WORD`**: 단어 단위로 줄바꿈 (긴 줄을 자동으로 감쌈)
    - **ScrolledText**: 스크롤바가 자동으로 추가된 Text 위젯

## 🔘 3. 버튼과 선택 요소들

### Button - 클릭 이벤트 처리

```python linenums="1" title="src/chapter2/06_buttons.py"
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Button 연습")
root.geometry("500x400")
root.configure(bg="white")

# 클릭 횟수를 저장할 변수
click_count = 0
status_var = tk.StringVar()
status_var.set("버튼을 클릭해보세요!")

# 상태 표시 라벨
status_label = tk.Label(root, textvariable=status_var, font=("맑은 고딕", 14))
status_label.pack(pady=20)

# 기본 버튼
def basic_click():
    global click_count
    click_count += 1
    status_var.set(f"기본 버튼이 {click_count}번 클릭되었습니다!")

basic_button = tk.Button(
    root,
    text="기본 버튼",
    command=basic_click,
    font=("맑은 고딕", 12),
    width=15
)
basic_button.pack(pady=5)

# 스타일이 적용된 버튼들
style_frame = tk.Frame(root, bg="white")
style_frame.pack(pady=10)

tk.Button(style_frame, text="빨간 버튼", bg="red", fg="white",
          font=("맑은 고딕", 10, "bold"),
          command=lambda: status_var.set("빨간 버튼 클릭!")).pack(side=tk.LEFT, padx=5)

tk.Button(style_frame, text="파란 버튼", bg="blue", fg="white",
          font=("맑은 고딕", 10, "bold"),
          command=lambda: status_var.set("파란 버튼 클릭!")).pack(side=tk.LEFT, padx=5)

tk.Button(style_frame, text="초록 버튼", bg="green", fg="white",
          font=("맑은 고딕", 10, "bold"),
          command=lambda: status_var.set("초록 버튼 클릭!")).pack(side=tk.LEFT, padx=5)

# 비활성화 버튼
disabled_button = tk.Button(
    root,
    text="비활성화된 버튼",
    state=tk.DISABLED,
    font=("맑은 고딕", 12)
)
disabled_button.pack(pady=5)

# 버튼 활성화/비활성화 토글
def toggle_button():
    if disabled_button['state'] == tk.DISABLED:
        disabled_button.config(state=tk.NORMAL, text="활성화된 버튼")
        status_var.set("버튼이 활성화되었습니다!")
    else:
        disabled_button.config(state=tk.DISABLED, text="비활성화된 버튼")
        status_var.set("버튼이 비활성화되었습니다!")

toggle_btn = tk.Button(root, text="버튼 상태 토글", command=toggle_button,
                      font=("맑은 고딕", 12))
toggle_btn.pack(pady=5)

# 특별한 기능 버튼들
special_frame = tk.Frame(root, bg="white")
special_frame.pack(pady=15)

def show_message():
    messagebox.showinfo("메시지", "안녕하세요! 이것은 메시지 박스입니다.")

def confirm_action():
    result = messagebox.askyesno("확인", "정말로 실행하시겠습니까?")
    if result:
        status_var.set("사용자가 '예'를 선택했습니다!")
    else:
        status_var.set("사용자가 '아니오'를 선택했습니다!")

def reset_counter():
    global click_count
    click_count = 0
    status_var.set("카운터가 초기화되었습니다!")

tk.Button(special_frame, text="메시지 표시", command=show_message,
          font=("맑은 고딕", 11), bg="lightblue").pack(side=tk.LEFT, padx=5)

tk.Button(special_frame, text="확인 대화상자", command=confirm_action,
          font=("맑은 고딕", 11), bg="lightyellow").pack(side=tk.LEFT, padx=5)

tk.Button(special_frame, text="카운터 초기화", command=reset_counter,
          font=("맑은 고딕", 11), bg="lightcoral").pack(side=tk.LEFT, padx=5)

root.mainloop()
```

![Button 예제들](images/ch2_buttons.png)

*Button 위젯의 다양한 기능들을 보여주는 예제입니다. 기본 버튼, 색상이 적용된 버튼들, 그리고 메시지박스와 연동된 특별한 기능 버튼들을 확인할 수 있습니다.*

### Checkbutton과 Radiobutton - 선택 옵션

```python linenums="1" title="src/chapter2/07_checkradio.py"
import tkinter as tk

root = tk.Tk()
root.title("체크박스와 라디오버튼")
root.geometry("500x500")

# 체크박스 섹션
check_frame = tk.LabelFrame(root, text="🔲 체크박스 (여러 개 선택 가능)", 
                           font=("맑은 고딕", 12, "bold"), padx=10, pady=10)
check_frame.pack(pady=10, padx=20, fill="x")

# 체크박스 변수들
pizza_var = tk.BooleanVar()
burger_var = tk.BooleanVar()
chicken_var = tk.BooleanVar()
noodle_var = tk.BooleanVar()

tk.Label(check_frame, text="좋아하는 음식을 모두 선택하세요:", 
         font=("맑은 고딕", 11)).pack(anchor="w")

tk.Checkbutton(check_frame, text="🍕 피자", variable=pizza_var,
               font=("맑은 고딕", 11)).pack(anchor="w")
tk.Checkbutton(check_frame, text="🍔 햄버거", variable=burger_var,
               font=("맑은 고딕", 11)).pack(anchor="w")
tk.Checkbutton(check_frame, text="🍗 치킨", variable=chicken_var,
               font=("맑은 고딕", 11)).pack(anchor="w")
tk.Checkbutton(check_frame, text="🍜 라면", variable=noodle_var,
               font=("맑은 고딕", 11)).pack(anchor="w")

# 라디오버튼 섹션
radio_frame = tk.LabelFrame(root, text="🔘 라디오버튼 (하나만 선택 가능)", 
                           font=("맑은 고딕", 12, "bold"), padx=10, pady=10)
radio_frame.pack(pady=10, padx=20, fill="x")

# 라디오버튼 변수
color_var = tk.StringVar()
color_var.set("red")  # 기본값 설정

tk.Label(radio_frame, text="좋아하는 색깔을 하나 선택하세요:", 
         font=("맑은 고딕", 11)).pack(anchor="w")

colors = [("🔴 빨강", "red"), ("🔵 파랑", "blue"), ("🟢 초록", "green"), ("🟡 노랑", "yellow")]

for text, value in colors:
    tk.Radiobutton(radio_frame, text=text, variable=color_var, value=value,
                   font=("맑은 고딕", 11)).pack(anchor="w")

# 결과 표시 함수
def show_selections():
    # 체크박스 결과
    foods = []
    if pizza_var.get(): foods.append("피자")
    if burger_var.get(): foods.append("햄버거")
    if chicken_var.get(): foods.append("치킨")
    if noodle_var.get(): foods.append("라면")
    
    # 라디오버튼 결과
    selected_color = color_var.get()
    color_names = {"red": "빨강", "blue": "파랑", "green": "초록", "yellow": "노랑"}
    
    # 결과 메시지
    result = "📋 선택 결과:\n\n"
    
    if foods:
        result += f"좋아하는 음식: {', '.join(foods)}\n"
    else:
        result += "선택된 음식이 없습니다.\n"
    
    result += f"좋아하는 색깔: {color_names[selected_color]}"
    
    result_label.config(text=result)

# 버튼과 결과 표시 영역
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="선택 결과 보기", command=show_selections,
          font=("맑은 고딕", 12), bg="lightgreen").pack(side=tk.LEFT, padx=5)

def reset_selections():
    pizza_var.set(False)
    burger_var.set(False)
    chicken_var.set(False)
    noodle_var.set(False)
    color_var.set("red")
    result_label.config(text="선택을 초기화했습니다.")

tk.Button(button_frame, text="선택 초기화", command=reset_selections,
          font=("맑은 고딕", 12), bg="lightcoral").pack(side=tk.LEFT, padx=5)

# 결과 표시 라벨
result_label = tk.Label(root, text="위에서 선택을 하고 '선택 결과 보기'를 클릭하세요.",
                       font=("맑은 고딕", 11), fg="blue", justify="left")
result_label.pack(pady=20)

root.mainloop()
```

![체크박스와 라디오버튼 예제](images/ch2_checkradio.png)

*Checkbutton과 Radiobutton의 차이점을 보여주는 예제입니다. 체크박스는 여러 개를 동시에 선택할 수 있고, 라디오버튼은 하나만 선택할 수 있습니다. 선택 결과를 처리하는 방법도 함께 보여줍니다.*

## 📋 4. 목록과 선택 요소들

### Listbox - 목록 선택

Listbox는 여러 항목 중에서 하나 또는 여러 개를 선택할 수 있는 목록을 만들 때 사용합니다.

#### 🔹 1단계: 기본 Listbox

```python linenums="1" title="src/chapter2/08a_basic_listbox.py"
import tkinter as tk

root = tk.Tk()
root.title("Listbox 기본 사용법")
root.geometry("400x300")

tk.Label(root, text="📋 프로그래밍 언어 목록:", font=("맑은 고딕", 12, "bold")).pack(pady=10)

# 기본 Listbox (단일 선택)
listbox = tk.Listbox(root, height=8, font=("맑은 고딕", 11))
listbox.pack(pady=10)

# 목록에 항목 추가
languages = ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "Swift"]
for lang in languages:
    listbox.insert(tk.END, lang)  # 마지막에 항목 추가

# 선택된 항목 확인하기
def show_selection():
    selection = listbox.curselection()  # 선택된 항목의 인덱스
    if selection:
        selected_item = listbox.get(selection[0])  # 선택된 항목의 텍스트
        result_label.config(text=f"선택: {selected_item}")
    else:
        result_label.config(text="선택된 항목이 없습니다.")

tk.Button(root, text="선택 확인", command=show_selection, 
          font=("맑은 고딕", 11)).pack(pady=10)

result_label = tk.Label(root, text="", font=("맑은 고딕", 11), fg="blue")
result_label.pack()

root.mainloop()
```

#### 🔹 2단계: 다중 선택 Listbox

```python linenums="30" title="src/chapter2/08b_multiple_listbox.py"
import tkinter as tk

root = tk.Tk()
root.title("다중 선택 Listbox")
root.geometry("400x400")

tk.Label(root, text="🍎 좋아하는 과일을 여러 개 선택하세요:", 
         font=("맑은 고딕", 11, "bold")).pack(pady=10)

# 다중 선택이 가능한 Listbox
multi_listbox = tk.Listbox(root, height=8, font=("맑은 고딕", 11),
                          selectmode=tk.MULTIPLE)  # 다중 선택 모드
multi_listbox.pack(pady=10)

fruits = ["🍎 사과", "🍌 바나나", "🍇 포도", "🍓 딸기", "🍑 체리", "🥝 키위", "🍊 오렌지", "🥭 망고"]
for fruit in fruits:
    multi_listbox.insert(tk.END, fruit)

def show_multiple_selection():
    selections = multi_listbox.curselection()  # 여러 개 선택된 인덱스들
    if selections:
        selected_fruits = [multi_listbox.get(i) for i in selections]
        result_text.config(text=f"선택된 과일:\n" + "\n".join(selected_fruits))
    else:
        result_text.config(text="선택된 과일이 없습니다.")

tk.Button(root, text="선택 결과 보기", command=show_multiple_selection,
          font=("맑은 고딕", 11), bg="lightgreen").pack(pady=10)

result_text = tk.Label(root, text="", font=("맑은 고딕", 10), fg="blue", justify=tk.LEFT)
result_text.pack(pady=10)

root.mainloop()
```

#### 🔹 3단계: Listbox 항목 추가/삭제

```python linenums="60" title="src/chapter2/08c_listbox_operations.py"
import tkinter as tk
import tkinter.simpledialog as simpledialog
from tkinter import messagebox

root = tk.Tk()
root.title("Listbox 항목 관리")
root.geometry("500x400")

tk.Label(root, text="📝 할 일 목록 관리", font=("맑은 고딕", 14, "bold")).pack(pady=10)

# 할 일 목록 Listbox
todo_listbox = tk.Listbox(root, height=10, font=("맑은 고딕", 11))
todo_listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# 초기 할 일들 추가
initial_todos = ["Python 공부하기", "GUI 프로그래밍 연습", "프로젝트 계획 세우기"]
for todo in initial_todos:
    todo_listbox.insert(tk.END, todo)

def add_todo():
    """새로운 할 일 추가"""
    new_todo = simpledialog.askstring("할 일 추가", "새로운 할 일을 입력하세요:")
    if new_todo:  # 빈 문자열이 아닌 경우
        todo_listbox.insert(tk.END, new_todo)
        messagebox.showinfo("추가 완료", f"'{new_todo}'가 추가되었습니다!")

def remove_todo():
    """선택된 할 일 삭제"""
    selection = todo_listbox.curselection()
    if selection:
        selected_todo = todo_listbox.get(selection[0])
        todo_listbox.delete(selection[0])
        messagebox.showinfo("삭제 완료", f"'{selected_todo}'가 삭제되었습니다!")
    else:
        messagebox.showwarning("선택 필요", "삭제할 항목을 선택해주세요!")

def clear_all():
    """모든 할 일 삭제"""
    if todo_listbox.size() > 0:  # 항목이 있는 경우
        result = messagebox.askyesno("전체 삭제", "모든 할 일을 삭제하시겠습니까?")
        if result:
            todo_listbox.delete(0, tk.END)  # 모든 항목 삭제

# 버튼들
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="➕ 할 일 추가", command=add_todo,
          font=("맑은 고딕", 10), bg="lightgreen").pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="❌ 선택 삭제", command=remove_todo,
          font=("맑은 고딕", 10), bg="lightcoral").pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="🗑️ 전체 삭제", command=clear_all,
          font=("맑은 고딕", 10), bg="orange").pack(side=tk.LEFT, padx=5)

root.mainloop()
```

!!! tip "💡 Listbox 핵심 포인트"
    - **`.curselection()`**: 선택된 항목의 인덱스 반환 (튜플 형태)
    - **`.get(index)`**: 특정 인덱스의 항목 텍스트 가져오기
    - **`.insert(position, text)`**: 항목 추가 (`tk.END`로 마지막에 추가)
    - **`.delete(index)`**: 항목 삭제 (인덱스 범위도 가능)
    - **`selectmode=tk.MULTIPLE`**: 다중 선택 모드
    - **`.size()`**: 총 항목 개수 확인

### Combobox - 드롭다운 선택

```python linenums="1" title="src/chapter2/09_combobox.py"
import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("Combobox 연습")
root.geometry("500x400")

# 기본 콤보박스
basic_frame = tk.LabelFrame(root, text="🔽 기본 콤보박스", padx=10, pady=10)
basic_frame.pack(pady=10, padx=20, fill="x")

tk.Label(basic_frame, text="국가를 선택하세요:", font=("맑은 고딕", 11)).pack(anchor="w")

country_combo = ttk.Combobox(basic_frame, font=("맑은 고딕", 11), width=30)
country_combo['values'] = ("대한민국", "미국", "일본", "중국", "독일", "프랑스", "영국", "캐나다")
country_combo.set("대한민국")  # 기본값 설정
country_combo.pack(pady=5)

# 읽기 전용 콤보박스
readonly_frame = tk.LabelFrame(root, text="🔒 읽기 전용 콤보박스", padx=10, pady=10)
readonly_frame.pack(pady=10, padx=20, fill="x")

tk.Label(readonly_frame, text="운영체제를 선택하세요:", font=("맑은 고딕", 11)).pack(anchor="w")

os_combo = ttk.Combobox(readonly_frame, font=("맑은 고딕", 11), width=30, state="readonly")
os_combo['values'] = ("Windows 11", "Windows 10", "macOS", "Ubuntu", "CentOS", "Debian")
os_combo.set("Windows 11")
os_combo.pack(pady=5)

# 편집 가능한 콤보박스
editable_frame = tk.LabelFrame(root, text="✏️ 편집 가능한 콤보박스", padx=10, pady=10)
editable_frame.pack(pady=10, padx=20, fill="x")

tk.Label(editable_frame, text="좋아하는 음식 (직접 입력도 가능):", font=("맑은 고딕", 11)).pack(anchor="w")

food_combo = ttk.Combobox(editable_frame, font=("맑은 고딕", 11), width=30)
food_combo['values'] = ("김치찌개", "불고기", "비빔밥", "삼겹살", "치킨", "피자", "햄버거", "파스타")
food_combo.pack(pady=5)

# 이벤트 처리 함수들
def on_country_change(event):
    selected = country_combo.get()
    print(f"선택된 국가: {selected}")

def on_os_change(event):
    selected = os_combo.get()
    print(f"선택된 OS: {selected}")

def show_selections():
    country = country_combo.get()
    os_name = os_combo.get()
    food = food_combo.get()
    
    result = f"📋 선택 결과:\n\n"
    result += f"국가: {country}\n"
    result += f"운영체제: {os_name}\n"
    result += f"좋아하는 음식: {food if food else '(선택 안함)'}"
    
    messagebox.showinfo("선택 결과", result)

def reset_all():
    country_combo.set("대한민국")
    os_combo.set("Windows 11")
    food_combo.set("")

# 이벤트 바인딩
country_combo.bind('<<ComboboxSelected>>', on_country_change)
os_combo.bind('<<ComboboxSelected>>', on_os_change)

# 버튼 영역
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

tk.Button(button_frame, text="선택 결과 보기", command=show_selections,
          font=("맑은 고딕", 12), bg="lightgreen").pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="초기화", command=reset_all,
          font=("맑은 고딕", 12), bg="lightcoral").pack(side=tk.LEFT, padx=5)

root.mainloop()
```

## 🖼️ 5. 레이아웃과 구조 요소들

### Frame - 위젯 그룹화

```python linenums="1" title="src/chapter2/10_frames_layout.py"
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Frame과 레이아웃 관리")
root.geometry("700x500")

# === pack 레이아웃 매니저 예시 ===
pack_frame = tk.LabelFrame(root, text="📦 Pack 레이아웃", padx=5, pady=5)
pack_frame.pack(side=tk.LEFT, padx=10, pady=10, fill="both", expand=True)

# 상단, 중간, 하단 프레임
top_frame = tk.Frame(pack_frame, bg="lightblue", height=50)
top_frame.pack(side=tk.TOP, fill="x", pady=2)
tk.Label(top_frame, text="상단 (TOP)", bg="lightblue").pack()

middle_frame = tk.Frame(pack_frame, bg="lightgreen")
middle_frame.pack(side=tk.TOP, fill="both", expand=True, pady=2)
tk.Label(middle_frame, text="중간 (확장됨)", bg="lightgreen").pack(expand=True)

bottom_frame = tk.Frame(pack_frame, bg="lightcoral", height=50)
bottom_frame.pack(side=tk.BOTTOM, fill="x", pady=2)
tk.Label(bottom_frame, text="하단 (BOTTOM)", bg="lightcoral").pack()

# === grid 레이아웃 매니저 예시 ===
grid_frame = tk.LabelFrame(root, text="🔲 Grid 레이아웃", padx=5, pady=5)
grid_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill="both", expand=True)

# 격자 형태로 위젯 배치
for i in range(3):
    for j in range(3):
        btn = tk.Button(grid_frame, text=f"({i},{j})", width=8, height=2)
        btn.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")

# 격자 크기 조절을 위한 가중치 설정
for i in range(3):
    grid_frame.grid_rowconfigure(i, weight=1)
    grid_frame.grid_columnconfigure(i, weight=1)

root.mainloop()
```

### 레이아웃 매니저 심화

```python linenums="30" title="src/chapter2/11_advanced_layout.py"
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("고급 레이아웃 예시")
root.geometry("800x600")

# 메인 컨테이너
main_container = ttk.Frame(root, padding="10")
main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# 제목 영역
title_frame = ttk.LabelFrame(main_container, text="🎨 고급 레이아웃 데모", padding="10")
title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

title_label = ttk.Label(title_frame, text="복잡한 GUI 레이아웃 구성하기", 
                       font=("맑은 고딕", 16, "bold"))
title_label.pack()

# 왼쪽 패널 - 설정
left_panel = ttk.LabelFrame(main_container, text="⚙️ 설정", padding="10")
left_panel.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

# 설정 옵션들
ttk.Label(left_panel, text="사용자 이름:").grid(row=0, column=0, sticky=tk.W, pady=2)
name_entry = ttk.Entry(left_panel, width=20)
name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))

ttk.Label(left_panel, text="테마:").grid(row=1, column=0, sticky=tk.W, pady=2)
theme_combo = ttk.Combobox(left_panel, values=["밝음", "어두움", "자동"], width=17)
theme_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
theme_combo.set("밝음")

# 체크박스 옵션들
options_frame = ttk.LabelFrame(left_panel, text="옵션", padding="5")
options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

auto_save_var = tk.BooleanVar(value=True)
ttk.Checkbutton(options_frame, text="자동 저장", variable=auto_save_var).pack(anchor="w")

notifications_var = tk.BooleanVar()
ttk.Checkbutton(options_frame, text="알림 표시", variable=notifications_var).pack(anchor="w")

# 오른쪽 패널 - 미리보기
right_panel = ttk.LabelFrame(main_container, text="👀 미리보기", padding="10")
right_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))

# 탭 위젯 사용
notebook = ttk.Notebook(right_panel)
notebook.pack(fill="both", expand=True)

# 탭 1: 텍스트
text_tab = ttk.Frame(notebook)
notebook.add(text_tab, text="텍스트")

text_widget = tk.Text(text_tab, height=10, width=30, font=("맑은 고딕", 10))
text_widget.pack(fill="both", expand=True, padx=5, pady=5)
text_widget.insert("1.0", "여기에 미리보기 내용이 표시됩니다.\n\n설정을 변경하면 실시간으로 업데이트됩니다.")

# 탭 2: 그래프 (간단한 Canvas 예시)
canvas_tab = ttk.Frame(notebook)
notebook.add(canvas_tab, text="그래프")

canvas = tk.Canvas(canvas_tab, width=300, height=200, bg="white")
canvas.pack(padx=5, pady=5)

# 간단한 그래프 그리기
canvas.create_line(50, 150, 250, 50, fill="blue", width=2)
canvas.create_oval(45, 145, 55, 155, fill="red")
canvas.create_oval(245, 45, 255, 55, fill="red")
canvas.create_text(150, 180, text="샘플 그래프", font=("맑은 고딕", 12))

# 하단 버튼 영역
bottom_frame = ttk.Frame(main_container)
bottom_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

# 진행률 표시
progress_var = tk.DoubleVar()
progress = ttk.Progressbar(bottom_frame, variable=progress_var, maximum=100)
progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

# 버튼들
def apply_settings():
    progress_var.set(0)
    for i in range(101):
        progress_var.set(i)
        root.update()
        root.after(10)  # 0.01초 대기
    
    name = name_entry.get() or "익명"
    theme = theme_combo.get()
    auto_save = "켜짐" if auto_save_var.get() else "꺼짐"
    notifications = "켜짐" if notifications_var.get() else "꺼짐"
    
    result = f"사용자: {name}\n테마: {theme}\n자동저장: {auto_save}\n알림: {notifications}"
    text_widget.delete("1.0", tk.END)
    text_widget.insert("1.0", f"설정이 적용되었습니다!\n\n{result}")

ttk.Button(bottom_frame, text="설정 적용", command=apply_settings).pack(side=tk.RIGHT, padx=2)
ttk.Button(bottom_frame, text="초기화").pack(side=tk.RIGHT, padx=2)
ttk.Button(bottom_frame, text="저장").pack(side=tk.RIGHT, padx=2)

# 그리드 가중치 설정 (반응형 레이아웃)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_container.columnconfigure(0, weight=1)
main_container.columnconfigure(1, weight=2)  # 오른쪽 패널이 더 넓게
main_container.rowconfigure(1, weight=1)
left_panel.columnconfigure(1, weight=1)

root.mainloop()
```

## 🎨 6. 고급 위젯들

### Canvas - 그림 그리기

Canvas는 그림을 그리거나 도형을 표시할 수 있는 위젯입니다. 게임, 차트, 그래픽 도구 등을 만들 때 사용됩니다.

#### 🔹 1단계: 기본 도형 그리기

```python linenums="1" title="src/chapter2/12a_basic_canvas.py"
import tkinter as tk

root = tk.Tk()
root.title("Canvas 기본 도형")
root.geometry("600x400")

# 캔버스 생성
canvas = tk.Canvas(root, width=500, height=300, bg="white", bd=2, relief="sunken")
canvas.pack(pady=20)

# 기본 도형들 그리기
def draw_basic_shapes():
    # 직사각형
    canvas.create_rectangle(50, 50, 150, 100, fill="lightblue", outline="blue", width=2)
    canvas.create_text(100, 110, text="직사각형", font=("맑은 고딕", 10))
    
    # 원 (타원)
    canvas.create_oval(200, 50, 300, 150, fill="lightgreen", outline="green", width=2)
    canvas.create_text(250, 160, text="원", font=("맑은 고딕", 10))
    
    # 직선
    canvas.create_line(350, 50, 450, 150, fill="red", width=3)
    canvas.create_text(400, 160, text="직선", font=("맑은 고딕", 10))
    
    # 다각형 (별 모양)
    points = [250, 200, 270, 240, 310, 240, 280, 270, 290, 310, 250, 290, 210, 310, 220, 270, 190, 240, 230, 240]
    canvas.create_polygon(points, fill="lightyellow", outline="orange", width=2)
    canvas.create_text(250, 320, text="다각형", font=("맑은 고딕", 10))

# 도형 그리기
draw_basic_shapes()

# 지우기 버튼
tk.Button(root, text="지우기", command=lambda: canvas.delete("all"), 
          font=("맑은 고딕", 12), bg="orange").pack(pady=10)
tk.Button(root, text="다시 그리기", command=draw_basic_shapes,
          font=("맑은 고딕", 12), bg="lightgreen").pack()

root.mainloop()
```

#### 🔹 2단계: 마우스로 그리기

```python linenums="30" title="src/chapter2/12b_interactive_canvas.py"
import tkinter as tk

root = tk.Tk()
root.title("마우스로 그리기")
root.geometry("600x500")

tk.Label(root, text="🎨 마우스를 드래그해서 그림을 그려보세요!", 
         font=("맑은 고딕", 12, "bold")).pack(pady=10)

# 캔버스 생성
canvas = tk.Canvas(root, width=500, height=350, bg="white", bd=2, relief="sunken")
canvas.pack(pady=10)

# 그리기 관련 변수들
drawing = False
last_x, last_y = 0, 0
current_color = "black"
current_width = 2

def start_drawing(event):
    """마우스 버튼을 누르면 그리기 시작"""
    global drawing, last_x, last_y
    drawing = True
    last_x, last_y = event.x, event.y

def draw_line(event):
    """마우스를 드래그하면 선 그리기"""
    global drawing, last_x, last_y
    if drawing:
        canvas.create_line(last_x, last_y, event.x, event.y, 
                          fill=current_color, width=current_width, capstyle="round")
        last_x, last_y = event.x, event.y

def stop_drawing(event):
    """마우스 버튼을 떼면 그리기 중단"""
    global drawing
    drawing = False

# 마우스 이벤트 바인딩
canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw_line)
canvas.bind("<ButtonRelease-1>", stop_drawing)

# 색상 변경 함수들
def change_color(color):
    global current_color
    current_color = color

def change_width(width):
    global current_width
    current_width = width

# 컨트롤 버튼들
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

# 색상 버튼들
colors = [("검정", "black"), ("빨강", "red"), ("파랑", "blue"), ("초록", "green")]
for name, color in colors:
    tk.Button(control_frame, text=name, bg=color, fg="white" if color == "black" else "black",
              command=lambda c=color: change_color(c), font=("맑은 고딕", 10)).pack(side=tk.LEFT, padx=2)

# 굵기 버튼들
tk.Label(control_frame, text=" | 굵기:", font=("맑은 고딕", 10)).pack(side=tk.LEFT, padx=5)
for width in [1, 3, 5, 8]:
    tk.Button(control_frame, text=str(width), width=3,
              command=lambda w=width: change_width(w), font=("맑은 고딕", 10)).pack(side=tk.LEFT, padx=1)

# 지우기 버튼
tk.Button(control_frame, text="🗑️ 전체 지우기", command=lambda: canvas.delete("all"),
          font=("맑은 고딕", 10), bg="orange").pack(side=tk.LEFT, padx=10)

root.mainloop()
```

#### 🔹 3단계: 간단한 그래프 그리기

```python linenums="60" title="src/chapter2/12c_canvas_chart.py"
import tkinter as tk
import math

root = tk.Tk()
root.title("Canvas로 차트 그리기")
root.geometry("700x500")

# 캔버스 생성
canvas = tk.Canvas(root, width=600, height=400, bg="white", bd=2, relief="sunken")
canvas.pack(pady=20)

def draw_bar_chart():
    """막대 그래프 그리기"""
    canvas.delete("all")
    
    # 데이터
    data = [("Python", 85), ("Java", 70), ("C++", 60), ("JavaScript", 75), ("Go", 45)]
    colors = ["#3776ab", "#f89820", "#00599c", "#f7df1e", "#00add8"]
    
    # 제목
    canvas.create_text(300, 30, text="📊 프로그래밍 언어 인기도", font=("맑은 고딕", 14, "bold"))
    
    # 막대 그래프 그리기
    bar_width = 80
    max_height = 200
    start_x = 80
    base_y = 350
    
    for i, (lang, score) in enumerate(data):
        x = start_x + i * 100
        height = (score / 100) * max_height
        
        # 막대
        canvas.create_rectangle(x, base_y - height, x + bar_width, base_y,
                               fill=colors[i], outline="black")
        
        # 언어 이름
        canvas.create_text(x + bar_width//2, base_y + 20, text=lang, font=("맑은 고딕", 10))
        
        # 점수
        canvas.create_text(x + bar_width//2, base_y - height - 15, text=str(score), 
                          font=("맑은 고딕", 10, "bold"))

def draw_line_chart():
    """선 그래프 그리기"""
    canvas.delete("all")
    
    # 제목
    canvas.create_text(300, 30, text="📈 월별 방문자 수", font=("맑은 고딕", 14, "bold"))
    
    # 축 그리기
    canvas.create_line(80, 350, 520, 350, fill="black", width=2)  # X축
    canvas.create_line(80, 80, 80, 350, fill="black", width=2)   # Y축
    
    # 데이터
    months = ["1월", "2월", "3월", "4월", "5월", "6월"]
    visitors = [120, 150, 180, 140, 200, 170]
    
    # 선 그래프 그리기
    points = []
    for i, (month, visitor) in enumerate(zip(months, visitors)):
        x = 80 + (i + 1) * 70
        y = 350 - (visitor / 250) * 200  # 스케일 조정
        
        points.extend([x, y])
        
        # 데이터 포인트
        canvas.create_oval(x-4, y-4, x+4, y+4, fill="red", outline="darkred")
        
        # 월 표시
        canvas.create_text(x, 370, text=month, font=("맑은 고딕", 9))
        
        # 방문자 수 표시
        canvas.create_text(x, y-15, text=str(visitor), font=("맑은 고딕", 9))
    
    # 선 연결
    if len(points) > 2:
        canvas.create_line(points, fill="blue", width=3)
    
    # 축 레이블
    canvas.create_text(300, 390, text="월", font=("맑은 고딕", 12))
    canvas.create_text(50, 200, text="방문자", font=("맑은 고딕", 12))

def draw_pie_chart():
    """원형 그래프 그리기"""
    canvas.delete("all")
    
    # 제목
    canvas.create_text(300, 30, text="🥧 운영체제 점유율", font=("맑은 고딕", 14, "bold"))
    
    # 데이터
    data = [("Windows", 60, "#0078d4"), ("macOS", 25, "#000000"), ("Linux", 15, "#fcc624")]
    
    center_x, center_y = 200, 200
    radius = 80
    start_angle = 0
    
    for name, percentage, color in data:
        # 각도 계산 (360도 = 100%)
        angle = percentage * 3.6
        
        # 파이 조각 그리기 (근사적으로 다각형 사용)
        points = [center_x, center_y]
        for i in range(int(angle) + 1):
            radian = math.radians(start_angle + i)
            x = center_x + radius * math.cos(radian)
            y = center_y + radius * math.sin(radian)
            points.extend([x, y])
        
        canvas.create_polygon(points, fill=color, outline="white", width=2)
        
        # 레이블 위치 계산
        label_angle = math.radians(start_angle + angle/2)
        label_x = center_x + (radius + 40) * math.cos(label_angle)
        label_y = center_y + (radius + 40) * math.sin(label_angle)
        
        # 레이블
        canvas.create_text(label_x, label_y, text=f"{name}\n{percentage}%", 
                          font=("맑은 고딕", 10), justify="center")
        
        start_angle += angle

# 버튼들
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="📊 막대 그래프", command=draw_bar_chart,
          font=("맑은 고딕", 11), bg="lightblue").pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="📈 선 그래프", command=draw_line_chart,
          font=("맑은 고딕", 11), bg="lightgreen").pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="🥧 원형 그래프", command=draw_pie_chart,
          font=("맑은 고딕", 11), bg="lightyellow").pack(side=tk.LEFT, padx=5)

# 초기 차트 표시
draw_bar_chart()

root.mainloop()
```

!!! tip "💡 Canvas 핵심 포인트"
    - **`.create_rectangle(x1, y1, x2, y2)`**: 직사각형 그리기
    - **`.create_oval(x1, y1, x2, y2)`**: 원/타원 그리기
    - **`.create_line(x1, y1, x2, y2)`**: 직선 그리기
    - **`.create_polygon(points)`**: 다각형 그리기 (points는 [x1,y1,x2,y2,...] 형태)
    - **`.create_text(x, y, text="...")`**: 텍스트 표시
    - **`.delete("all")`**: 모든 그림 지우기
    - **마우스 이벤트**: `<Button-1>`, `<B1-Motion>`, `<ButtonRelease-1>`
    - **색상과 스타일**: `fill`, `outline`, `width` 옵션으로 꾸미기

### Menu - 메뉴바

대부분의 GUI 응용프로그램에는 맨 위에 메뉴바가 있습니다. 파일, 편집, 보기, 도움말 등의 메뉴를 만들어 보겠습니다.

#### 🔹 1단계: 기본 메뉴 만들기

```python linenums="1" title="src/chapter2/13a_basic_menu.py"
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("기본 메뉴 예제")
root.geometry("500x300")

# 간단한 기능들
def new_document():
    messagebox.showinfo("새 문서", "새 문서를 만듭니다!")

def open_document():
    messagebox.showinfo("열기", "문서를 엽니다!")

def save_document():
    messagebox.showinfo("저장", "문서를 저장합니다!")

def show_about():
    messagebox.showinfo("프로그램 정보", "간단한 메뉴 예제\n버전 1.0")

# 메뉴바 생성 - 이것이 계층의 최상위!
menubar = tk.Menu(root)
root.config(menu=menubar)  # 루트 윈도우에 메뉴바 연결

# 파일 메뉴 만들기
file_menu = tk.Menu(menubar, tearoff=0)  # tearoff=0으로 띄어낼 수 없게 만들기
menubar.add_cascade(label="파일", menu=file_menu)  # 메뉴바에 추가

# 파일 메뉴 항목들
file_menu.add_command(label="새로 만들기", command=new_document)
file_menu.add_command(label="열기...", command=open_document)
file_menu.add_separator()  # 구분선 추가
file_menu.add_command(label="저장", command=save_document)
file_menu.add_separator()
file_menu.add_command(label="종료", command=root.quit)

# 도움말 메뉴
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="도움말", menu=help_menu)
help_menu.add_command(label="프로그램 정보", command=show_about)

# 메인 내용 영역
tk.Label(root, text="🎆 메뉴바가 생겼어요!", 
         font=("맑은 고딕", 16, "bold")).pack(expand=True)

root.mainloop()
```

#### 🔹 2단계: 텍스트 에디터 메뉴

```python linenums="30" title="src/chapter2/13b_text_editor_menu.py"
import tkinter as tk
from tkinter import messagebox, filedialog

root = tk.Tk()
root.title("텍스트 에디터 - 메뉴 예제")
root.geometry("600x400")

# 텍스트 위젯 생성
text_widget = tk.Text(root, font=("맑은 고딕", 12), wrap=tk.WORD)
text_widget.pack(fill="both", expand=True, padx=5, pady=5)

# 파일 관련 기능들
def new_file():
    if text_widget.get(1.0, tk.END).strip():  # 내용이 있는지 확인
        if messagebox.askyesno("새 파일", "현재 내용을 지우고 새 파일을 만들까요?"):
            text_widget.delete(1.0, tk.END)
    else:
        text_widget.delete(1.0, tk.END)

def open_file():
    filename = filedialog.askopenfilename(
        title="파일 열기",
        filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")]
    )
    if filename:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                text_widget.delete(1.0, tk.END)
                text_widget.insert(1.0, content)
                root.title(f"텍스트 에디터 - {filename.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("오류", f"파일을 열 수 없습니다: {e}")

def save_file():
    filename = filedialog.asksaveasfilename(
        title="파일 저장",
        defaultextension=".txt",
        filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")]
    )
    if filename:
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                content = text_widget.get(1.0, tk.END)
                file.write(content)
            messagebox.showinfo("저장 완료", f"파일이 저장되었습니다!\n{filename}")
            root.title(f"텍스트 에디터 - {filename.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("오류", f"파일을 저장할 수 없습니다: {e}")

# 편집 기능들
def cut_text():
    text_widget.event_generate("<<Cut>>")

def copy_text():
    text_widget.event_generate("<<Copy>>")

def paste_text():
    text_widget.event_generate("<<Paste>>")

def select_all():
    text_widget.tag_add(tk.SEL, "1.0", tk.END)
    text_widget.mark_set(tk.INSERT, "1.0")
    text_widget.see(tk.INSERT)

# 메뉴바 생성
menubar = tk.Menu(root)
root.config(menu=menubar)

# 파일 메뉴
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="파일", menu=file_menu)
file_menu.add_command(label="새로 만들기", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="열기...", command=open_file, accelerator="Ctrl+O")
file_menu.add_separator()
file_menu.add_command(label="저장...", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="종료", command=root.quit, accelerator="Ctrl+Q")

# 편집 메뉴
edit_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="편집", menu=edit_menu)
edit_menu.add_command(label="잘라내기", command=cut_text, accelerator="Ctrl+X")
edit_menu.add_command(label="복사", command=copy_text, accelerator="Ctrl+C")
edit_menu.add_command(label="붙여넣기", command=paste_text, accelerator="Ctrl+V")
edit_menu.add_separator()
edit_menu.add_command(label="모두 선택", command=select_all, accelerator="Ctrl+A")

# 키보드 단축키 바인딩
root.bind('<Control-n>', lambda e: new_file())
root.bind('<Control-o>', lambda e: open_file())
root.bind('<Control-s>', lambda e: save_file())
root.bind('<Control-q>', lambda e: root.quit())

# 초기 텍스트
text_widget.insert(1.0, """📝 텍스트 에디터 예제

이 간단한 텍스트 에디터로 다음 기능들을 체험해보세요:

📁 파일 메뉴:
- 새로 만들기 (Ctrl+N)
- 열기 (Ctrl+O)
- 저장 (Ctrl+S)
- 종료 (Ctrl+Q)

✂️ 편집 메뉴:
- 잘라내기 (Ctrl+X)
- 복사 (Ctrl+C)
- 붙여넣기 (Ctrl+V)
- 모두 선택 (Ctrl+A)

⌨️ 키보드 단축키도 지원합니다!

이 내용을 수정해보고, 파일로 저장해보세요.
""")

root.mainloop()
```

#### 🔹 3단계: 고급 메뉴 (서브메뉴, 체크표시)

```python linenums="90" title="src/chapter2/13c_advanced_menu.py"
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("고급 메뉴 기능 예제")
root.geometry("600x400")

# 상태 변수들
dark_mode = tk.BooleanVar()
word_wrap = tk.BooleanVar(value=True)  # 기본값: 켜짐
show_status = tk.BooleanVar(value=True)
font_size = tk.IntVar(value=12)

# UI 요소들
text_widget = tk.Text(root, font=("맑은 고딕", font_size.get()), wrap=tk.WORD)
text_widget.pack(fill="both", expand=True, padx=5, pady=5)

status_frame = tk.Frame(root, height=25, bg="lightgray")
status_label = tk.Label(status_frame, text="준비 완료", bg="lightgray", anchor="w")
status_label.pack(side="left", padx=5)
status_frame.pack(fill="x", side="bottom")

# 기능 함수들
def toggle_dark_mode():
    if dark_mode.get():
        # 다크 모드 적용
        text_widget.config(bg="#2b2b2b", fg="white", insertbackground="white")
        root.configure(bg="#1e1e1e")
        status_frame.configure(bg="#1e1e1e")
        status_label.configure(bg="#1e1e1e", fg="white")
        status_label.config(text="다크 모드 활성화")
    else:
        # 라이트 모드 적용
        text_widget.config(bg="white", fg="black", insertbackground="black")
        root.configure(bg="white")
        status_frame.configure(bg="lightgray")
        status_label.configure(bg="lightgray", fg="black")
        status_label.config(text="라이트 모드 활성화")

def toggle_word_wrap():
    if word_wrap.get():
        text_widget.config(wrap=tk.WORD)
        status_label.config(text="줄바꿈 켜짐")
    else:
        text_widget.config(wrap=tk.NONE)
        status_label.config(text="줄바꿈 꺼짐")

def toggle_status_bar():
    if show_status.get():
        status_frame.pack(fill="x", side="bottom")
        status_label.config(text="상태바 표시")
    else:
        status_frame.pack_forget()

def change_font_size(size):
    font_size.set(size)
    text_widget.config(font=("맑은 고딕", size))
    status_label.config(text=f"글꼴 크기: {size}")

def show_preferences():
    messagebox.showinfo("환경설정", f"현재 설정:\n\n다크모드: {'켜짐' if dark_mode.get() else '꺼짐'}\n줄바꿈: {'켜짐' if word_wrap.get() else '꺼짐'}\n상태바: {'보이기' if show_status.get() else '숨기기'}\n글꼴 크기: {font_size.get()}")

# 메뉴바 생성
menubar = tk.Menu(root)
root.config(menu=menubar)

# 파일 메뉴
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="파일", menu=file_menu)
file_menu.add_command(label="새로 만들기", accelerator="Ctrl+N")
file_menu.add_command(label="열기...", accelerator="Ctrl+O")
file_menu.add_separator()

# 서브메뉴: 최근에 열었던 파일
recent_menu = tk.Menu(file_menu, tearoff=0)
file_menu.add_cascade(label="최근 파일", menu=recent_menu)
recent_files = ["document1.txt", "note.txt", "readme.md"]
for file in recent_files:
    recent_menu.add_command(label=file, command=lambda f=file: messagebox.showinfo("파일 열기", f"'{f}'를 엽니다"))

file_menu.add_separator()
file_menu.add_command(label="종료", command=root.quit)

# 보기 메뉴 (체크박스 있는 메뉴)
view_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="보기", menu=view_menu)

# 체크박스 메뉴 항목들
view_menu.add_checkbutton(label="다크 모드", variable=dark_mode, command=toggle_dark_mode)
view_menu.add_checkbutton(label="줄 바꿈", variable=word_wrap, command=toggle_word_wrap)
view_menu.add_checkbutton(label="상태바 보이기", variable=show_status, command=toggle_status_bar)
view_menu.add_separator()

# 서브메뉴: 글꼴 크기
font_menu = tk.Menu(view_menu, tearoff=0)
view_menu.add_cascade(label="글꼴 크기", menu=font_menu)
for size in [10, 12, 14, 16, 18, 20]:
    font_menu.add_radiobutton(label=f"{size}점", variable=font_size, value=size, 
                             command=lambda s=size: change_font_size(s))

# 도구 메뉴
tools_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="도구", menu=tools_menu)
tools_menu.add_command(label="환경설정...", command=show_preferences)
tools_menu.add_separator()
tools_menu.add_command(label="단어 수 세기", 
                      command=lambda: messagebox.showinfo("단어 수", f"현재 문서의 단어 수: {len(text_widget.get(1.0, tk.END).split())}개"))

# 도움말 메뉴
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="도움말", menu=help_menu)
help_menu.add_command(label="사용법", command=lambda: messagebox.showinfo("사용법", "이 프로그램은 고급 메뉴 기능을 시연합니다."))
help_menu.add_separator()
help_menu.add_command(label="프로그램 정보", command=lambda: messagebox.showinfo("정보", "고급 메뉴 예제\n버전 2.0\n\ntkinter 메뉴 시스템 데모"))

# 초기 텍스트
text_widget.insert(1.0, """🎆 고급 메뉴 기능 데모

이 예제에서 볼 수 있는 고급 메뉴 기능들:

🔹 체크박스 메뉴:
- 보기 > 다크 모드 (on/off 상태 체크)
- 보기 > 줄 바꿈 (on/off 상태 체크)
- 보기 > 상태바 보이기 (on/off 상태 체크)

🔹 라디오버튼 메뉴:
- 보기 > 글꼴 크기 (여러 선택지 중 하나만 선택)

🔹 서브메뉴:
- 파일 > 최근 파일 (하위 메뉴)
- 보기 > 글꼴 크기 (하위 메뉴)

🔹 다양한 기능:
- 도구 > 환경설정 (현재 상태 보기)
- 도구 > 단어 수 세기 (동적 계산)

메뉴를 클릭해서 다양한 기능들을 체험해보세요!
""")

root.mainloop()
```

!!! tip "💡 Menu 핵심 포인트"
    - **`tk.Menu(parent, tearoff=0)`**: 메뉴 생성 (tearoff=0으로 떼어낼 수 없게)
    - **`.add_cascade(label, menu)`**: 상위 메뉴에 하위 메뉴 추가
    - **`.add_command(label, command)`**: 일반 메뉴 항목 추가
    - **`.add_checkbutton(label, variable, command)`**: 체크박스 메뉴 항목
    - **`.add_radiobutton(label, variable, value)`**: 라디오버튼 메뉴 항목
    - **`.add_separator()`**: 구분선 추가
    - **`accelerator="Ctrl+N"`**: 단축키 표시 (실제 기능은 bind로 구현)
    - **`root.config(menu=menubar)`**: 루트 윈도우에 메뉴바 연결

## 🧪 실습 과제

### 🌟 기본 도전과제

#### 1. 개인 정보 입력 폼 만들기
- Entry, Combobox, Checkbutton을 사용
- 이름, 나이, 성별, 취미 입력
- 입력 검증 및 결과 표시

#### 2. 간단한 계산기
- Button으로 숫자와 연산자 배치
- Entry로 결과 표시
- 기본 사칙연산 구현

#### 3. 색상 팔레트
- Canvas에 색상 샘플 표시
- Button으로 색상 선택
- 선택된 색상으로 배경색 변경

### 🚀 고급 도전과제

#### 4. 미니 그림판
- Canvas에 자유 그리기
- 색상 선택, 붓 크기 조절
- 저장/불러오기 기능

#### 5. 할 일 관리자
- Listbox로 할 일 목록 표시
- Entry로 새 할 일 추가
- 완료/삭제 기능 구현

## 🎯 Chapter 2 정리

### ✅ 배운 UI 요소들

**기본 구조:**

- [ ] Window 설정 (제목, 크기, 위치)
- [ ] 이벤트 루프 (`mainloop()`)

**텍스트 요소:**

- [ ] Label (정적 텍스트 표시)
- [ ] Entry (한 줄 입력)
- [ ] Text (여러 줄 입력/표시)

**버튼과 선택:**

- [ ] Button (클릭 이벤트)
- [ ] Checkbutton (다중 선택)
- [ ] Radiobutton (단일 선택)

**목록과 선택:**

- [ ] Listbox (목록 선택)
- [ ] Combobox (드롭다운)

**레이아웃:**

- [ ] Frame (그룹화)
- [ ] pack, grid, place (배치 관리자)

**고급 요소:**

- [ ] Canvas (그리기)
- [ ] Menu (메뉴바)
- [ ] Scrollbar (스크롤)

### 🌟 핵심 개념

**이벤트 기반 프로그래밍:**
```python
def event_handler():
    # 사용자 액션에 반응하는 코드
    pass

button = tk.Button(root, text="클릭", command=event_handler)
```

**위젯 속성 설정:**
```python
widget = tk.Widget(
    parent,
    text="텍스트",
    font=("맑은 고딕", 12),
    bg="색상",
    command=함수
)
```

**동적 내용 업데이트:**
```python
var = tk.StringVar()
label = tk.Label(root, textvariable=var)
var.set("새로운 내용")  # 자동으로 업데이트됨
```

---

!!! success "🎉 Chapter 2 완주 축하드려요!"
    Tkinter의 모든 핵심 UI 요소들을 성공적으로 마스터했습니다!
    
    **이제 할 수 있는 것들:**

    - ✅ 모든 종류의 GUI 위젯 사용하기
    - ✅ 복잡한 레이아웃 구성하기
    - ✅ 사용자 입력 처리하고 검증하기
    - ✅ 이벤트 기반 프로그래밍하기
    - ✅ 실용적인 데스크톱 애플리케이션 설계하기

!!! tip "🚀 다음 단계 준비하기"
    **Chapter 3에서는:**

    - Chapter 2에서 배운 모든 요소들을 조합
    - 실제 KRenamer 애플리케이션 구조 만들기
    - 체계적인 클래스 설계와 이벤트 처리
    - 실용적인 파일 관리 GUI 완성
    
    이제 진짜 KRenamer를 만들어봅시다!