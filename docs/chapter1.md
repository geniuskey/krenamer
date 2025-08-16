# Chapter 1: Python 기초

## 환영합니다!

안녕하세요! 이 챕터에서는 **파일명을 쉽게 바꿔주는 프로그램(KRenamer)**<!-- -->을 만들기 위해 필요한 파이썬 기초를 차근차근 배워보겠습니다. 

프로그래밍이 처음이시거나 파이썬이 낯설어도 걱정하지 마세요! 실생활에서 자주 하는 일들(파일명 바꾸기, 정리하기)을 코드로 만들어보면서 자연스럽게 배울 수 있습니다.

## 이번 챕터에서 배울 것들

### Python 기초 - 변수와 데이터 타입

**파일 관리 프로그램을 위한 기본 데이터 구조**

**1. 문자열 (str)** - 텍스트 데이터
```python
program_name = "KRenamer"
file_name = "내문서.txt"
```
*용도: 파일명, 경로, 프로그램 이름 등 텍스트 데이터*

**2. 정수 (int)** - 숫자 데이터
```python
file_count = 5
file_size = 1024
```
*용도: 파일 개수, 파일 크기, 순서 번호 등 숫자 데이터*

**3. 불린 (bool)** - 참/거짓 데이터
```python
is_running = True
has_error = False
```
*용도: 프로그램 상태, 조건 확인, 성공/실패 여부*

**4. 리스트 (list)** - 여러 데이터 모음
```python
my_files = ["사진.jpg", "문서.pdf", "음악.mp3"]
```
*용도: 여러 파일 목록, 설정값들, 처리 결과 등*

### 우리가 만들 프로그램의 핵심 기능들

- **여러 파일의 이름을 한 번에 바꾸기** - 수십, 수백 개의 파일도 클릭 몇 번으로!
- **파일들에 순서대로 번호 매기기** - 001, 002, 003... 형태로 자동 정리
- **파일명에서 특정 단어 바꾸기** - "임시"를 "최종"으로 한 번에 변경
- **파일 크기 보여주기** - 1048576 바이트를 1MB로 쉽게 표시

### 이런 기능들을 만들기 위해 배워야 할 파이썬 기초들

- **변수와 데이터** - 파일 정보를 저장하는 방법
- **문자열 다루기** - 파일명을 자유자재로 바꾸는 방법  
- **리스트 사용하기** - 여러 파일을 한 번에 관리하는 방법
- **조건문과 반복문** - 파일들을 하나씩 처리하는 방법
- **함수 만들기** - 같은 작업을 반복하지 않는 방법
- **클래스 기초** - 코드를 깔끔하게 정리하는 방법
- **예외 처리** - 오류가 발생해도 안전하게 처리하는 방법
- **정규표현식** - 복잡한 패턴을 찾고 바꾸는 방법

## 단계별 학습하기

### 1단계: 변수 만들어보기

파이썬에서 정보를 저장하는 방법을 배워봅시다. 마치 서류를 정리할 때 폴더에 라벨을 붙이는 것처럼, 데이터에 이름표를 붙여주는 것입니다.

#### 기본 변수 사용법

```python
# 간단한 정보 저장하기 (src/chapter1/step1_variables.py)
print("=== 변수 사용해보기 ===")

# 텍스트 정보 저장 (문자열)
program_name = "KRenamer"
file_name = "내 문서.txt"

# 숫자 정보 저장
file_count = 5
file_size = 1024

# 참/거짓 정보 저장 (불린)
is_running = True
has_error = False

# 여러 개 정보 저장 (리스트)
my_files = ["사진1.jpg", "문서.pdf", "음악.mp3"]

# 결과 확인하기
print(f"프로그램 이름: {program_name}")
print(f"파일 개수: {file_count}개")
print(f"프로그램 실행중: {is_running}")
print(f"내 파일들: {my_files}")
```

#### 실행 결과
```
=== 변수 사용해보기 ===
프로그램 이름: KRenamer
파일 개수: 5개
프로그램 실행중: True
내 파일들: ['사진1.jpg', '문서.pdf', '음악.mp3']
```

#### 이해하기 쉬운 변수명 사용하기

- `program_name` → 프로그램 이름이구나!
- `file_count` → 파일 개수구나!
- `my_files` → 내 파일 목록이구나!

변수명을 보면 무엇을 저장하는지 바로 알 수 있게 만드는 것이 중요합니다. 이렇게 하면 나중에 코드를 다시 볼 때도, 다른 사람이 코드를 볼 때도 쉽게 이해할 수 있어요.

### 2단계: 파일명 다루어보기

파일명을 바꾸는 것이 우리 프로그램의 핵심이에요! 파일명은 텍스트(문자열)이기 때문에, 문자열을 다루는 방법을 배워봅시다.

#### 문자열 조작 기본기

```python
# 파일명 바꾸기 연습 (src/chapter1/step2_filename_processing.py)
print("=== 파일명 바꾸기 연습 ===")

# 원본 파일명
filename = "내 사진 (복사본).jpg"
print(f"원본 파일명: {filename}")

# 1) 파일명과 확장자 나누기
import os
name_part, extension = os.path.splitext(filename)
print(f"파일명 부분: '{name_part}'")
print(f"확장자 부분: '{extension}'")

# 2) 특별한 문자들 제거하기
cleaned_name = filename.replace("(복사본)", "")  # (복사본) 제거
cleaned_name = cleaned_name.replace("  ", " ")   # 두 번 띄어쓰기를 한 번으로
print(f"정리된 파일명: '{cleaned_name}'")

# 3) 공백을 밑줄로 바꾸기
underscore_name = cleaned_name.replace(" ", "_")
print(f"밑줄로 연결: '{underscore_name}'")

# 4) 대소문자 바꾸기
print(f"소문자로: '{filename.lower()}'")
print(f"대문자로: '{filename.upper()}'")

# 5) 앞뒤에 글자 추가하기
prefix = "NEW_"
suffix = "_BACKUP"
new_filename = prefix + name_part + suffix + extension
print(f"최종 결과: '{new_filename}'")
```

#### 실행 결과
```
=== 파일명 바꾸기 연습 ===
원본 파일명: 내 사진 (복사본).jpg
파일명 부분: '내 사진 (복사본)'
확장자 부분: '.jpg'
정리된 파일명: '내 사진 .jpg'
밑줄로 연결: '내_사진_.jpg'
소문자로: '내 사진 (복사본).jpg'
대문자로: '내 사진 (복사본).JPG'
최종 결과: 'NEW_내 사진 (복사본)_BACKUP.jpg'
```

#### 파일명 변경의 핵심 함수들

- `replace()` → 원하는 글자를 다른 글자로 바꾸기
- `lower()`, `upper()` → 대소문자 바꾸기  
- `+` 또는 f-string → 앞뒤에 글자 추가하기
- `os.path.splitext()` → 파일명과 확장자 분리하기

이제 여러분은 파일명을 자유자재로 바꿀 수 있어요! 이런 기본 기능들이 모여서 강력한 파일 관리 프로그램이 됩니다.

### 3단계: 여러 파일 한 번에 처리하기

실제로는 파일 하나가 아니라 여러 개를 한 번에 처리해야 해요. 파이썬의 **리스트**<!-- -->와 **반복문**<!-- -->을 사용해봅시다!

#### 반복문으로 여러 파일 처리하기

```python
# 여러 파일 처리하기 (src/chapter1/step3_multiple_files.py)
print("=== 여러 파일 한 번에 처리하기 ===")

# 여러 파일명을 리스트에 저장
my_files = [
    "휴가사진_001.jpg",
    "휴가사진_002.jpg", 
    "중요문서_v1.2.pdf",
    "백업파일_2023_12_15.zip"
]

print("원본 파일들:")
for file in my_files:
    print(f"  - {file}")

# 모든 파일에 접두사 "정리된_" 추가하기
print("\n접두사 '정리된_' 추가 결과:")
renamed_files = []
for file in my_files:
    new_name = "정리된_" + file
    renamed_files.append(new_name)
    print(f"  {file} → {new_name}")

# 더 간단한 방법: 리스트 컴프리헨션 (고급 기법)
print("\n더 간단한 방법으로 해보기:")
quick_renamed = ["NEW_" + file for file in my_files]
for i, file in enumerate(my_files):
    print(f"  {file} → {quick_renamed[i]}")
```

#### 실행 결과
```
=== 여러 파일 한 번에 처리하기 ===
원본 파일들:
  - 휴가사진_001.jpg
  - 휴가사진_002.jpg
  - 중요문서_v1.2.pdf
  - 백업파일_2023_12_15.zip

접두사 '정리된_' 추가 결과:
  휴가사진_001.jpg → 정리된_휴가사진_001.jpg
  휴가사진_002.jpg → 정리된_휴가사진_002.jpg
  중요문서_v1.2.pdf → 정리된_중요문서_v1.2.pdf
  백업파일_2023_12_15.zip → 정리된_백업파일_2023_12_15.zip

더 간단한 방법으로 해보기:
  휴가사진_001.jpg → NEW_휴가사진_001.jpg
  휴가사진_002.jpg → NEW_휴가사진_002.jpg
  중요문서_v1.2.pdf → NEW_중요문서_v1.2.pdf
  백업파일_2023_12_15.zip → NEW_백업파일_2023_12_15.zip
```

#### 반복문 이해하기

`for file in my_files:`는 "my_files 리스트에 있는 각 파일에 대해서"라는 뜻입니다.

마치 "서랍에 있는 각 서류에 대해서 도장을 찍자"와 같은 개념입니다! 

- `for` - "~에 대해서"
- `file` - 현재 처리 중인 파일 (변수명은 자유롭게 정할 수 있음)
- `in my_files` - "my_files 리스트 안에서"

**반복문의 핵심 개념:**

1. 리스트의 첫 번째 아이템부터 시작
2. 마지막 아이템까지 하나씩 처리
3. 각 단계에서 같은 작업을 반복 수행

### 4단계: 파일 정보 알아내기

실제 파일을 다루려면 파일이 어디에 있는지, 얼마나 큰지 등을 알아야 해요. 컴퓨터에서 파일 정보를 가져오는 방법을 배워봅시다!

#### pathlib로 파일 정보 가져오기

```python
# 파일 정보 알아내기 (src/chapter1/step4_file_info.py)
print("=== 파일 정보 알아내기 ===")

# pathlib 라이브러리 사용하기 (최신 방법)
from pathlib import Path

# 예시 파일 경로들
example_files = [
    "C:/Users/홍길동/Documents/보고서.pdf",
    "C:/Users/홍길동/Pictures/가족사진.jpg",
    "C:/Users/홍길동/Music/좋아하는노래.mp3"
]

for file_path in example_files:
    file_info = Path(file_path)
    
    print(f"\n파일 경로: {file_path}")
    print(f"   파일명만: {file_info.name}")
    print(f"   폴더 경로: {file_info.parent}")
    print(f"   확장자: {file_info.suffix}")
    print(f"   이름(확장자 제외): {file_info.stem}")
```

#### 실행 결과
```
=== 파일 정보 알아내기 ===

파일 경로: C:/Users/홍길동/Documents/보고서.pdf
   파일명만: 보고서.pdf
   폴더 경로: C:\Users\홍길동\Documents
   확장자: .pdf
   이름(확장자 제외): 보고서

파일 경로: C:/Users/홍길동/Pictures/가족사진.jpg
   파일명만: 가족사진.jpg
   폴더 경로: C:\Users\홍길동\Pictures
   확장자: .jpg
   이름(확장자 제외): 가족사진

파일 경로: C:/Users/홍길동/Music/좋아하는노래.mp3
   파일명만: 좋아하는노래.mp3
   폴더 경로: C:\Users\홍길동\Music
   확장자: .mp3
   이름(확장자 제외): 좋아하는노래
```

#### 왜 pathlib을 사용하나요?

전에는 `os.path`라는 것을 썼는데, 요즘은 `pathlib`를 더 많이 써요!

**pathlib의 장점:**

- **더 읽기 쉬움**: `file_info.name` (파일명이구나!)
- **더 사용하기 쉬움**: `file_info.parent` (부모 폴더구나!)
- **실수가 적음**: 자동으로 운영체제에 맞게 경로를 처리해줌
- **객체지향적**: 파일 경로를 하나의 객체로 다룰 수 있음

**pathlib의 핵심 속성들:**

- `.name` - 파일명 (확장자 포함)
- `.stem` - 파일명 (확장자 제외)  
- `.suffix` - 확장자
- `.parent` - 부모 디렉토리
- `.parts` - 경로의 각 부분들
- `.is_file()` - 파일인지 확인
- `.is_dir()` - 디렉토리인지 확인
- `.exists()` - 존재하는지 확인

### 5단계: 파일 크기를 예쁘게 표시하기

컴퓨터는 파일 크기를 바이트(byte)로 계산해요. 하지만 1048576 바이트보다는 1MB라고 하는 게 훨씬 이해하기 쉽죠!

#### 파일 크기 변환 함수 만들기

```python
# 파일 크기 예쁘게 만들기 (src/chapter1/step5_file_size.py)
def make_size_pretty(size_bytes):
    """파일 크기를 읽기 쉽게 바꿔주는 함수"""
    print(f"원래 크기: {size_bytes} 바이트")
    
    # 크기가 0이면 그냥 0B 반환
    if size_bytes == 0:
        return "0B"
    
    # 단위들: 바이트 → 킬로바이트 → 메가바이트 → 기가바이트
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    
    # 1024로 나누면서 적절한 단위 찾기
    for unit in units:
        if size_bytes < 1024.0:
            if unit == 'B':
                return f"{int(size_bytes)}{unit}"  # 바이트는 정수로
            else:
                return f"{size_bytes:.1f}{unit}"   # 나머지는 소수점 1자리
        size_bytes = size_bytes / 1024.0  # 1024로 나누기
    
    return f"{size_bytes:.1f}TB"  # 매우 큰 파일은 TB

# 테스트해보기
print("=== 파일 크기 예쁘게 만들기 ===")
test_sizes = [0, 512, 1024, 1536, 1048576, 1073741824]

for size in test_sizes:
    pretty_size = make_size_pretty(size)
    print(f"{size:>10} 바이트 = {pretty_size}")
    print()
```

#### 실행 결과
```
=== 파일 크기 예쁘게 만들기 ===
원래 크기: 0 바이트
         0 바이트 = 0B

원래 크기: 512 바이트
       512 바이트 = 512B

원래 크기: 1024 바이트
      1024 바이트 = 1.0KB

원래 크기: 1536 바이트
      1536 바이트 = 1.5KB

원래 크기: 1048576 바이트
   1048576 바이트 = 1.0MB

원래 크기: 1073741824 바이트
1073741824 바이트 = 1.0GB
```

#### 1024가 뭔가요?

컴퓨터는 2진법을 사용해서 1024 (=2¹⁰)를 기준으로 계산해요!

**파일 크기 단위 체계:**

- 1 KB = 1,024 바이트
- 1 MB = 1,024 KB = 1,048,576 바이트  
- 1 GB = 1,024 MB = 1,073,741,824 바이트
- 1 TB = 1,024 GB = 1,099,511,627,776 바이트

**왜 1000이 아니라 1024인가요?**

컴퓨터는 모든 것을 0과 1로 표현합니다(2진법). 그래서:

- 2¹ = 2
- 2² = 4  
- 2³ = 8
- ...
- 2¹⁰ = 1024

1024는 2의 거듭제곱이라서 컴퓨터가 처리하기에 효율적인 숫자입니다!

### 6단계: 오류가 생겨도 안전하게!

프로그램을 사용하다 보면 예상치 못한 일들이 생겨요. 파일이 없다거나, 이미 같은 이름의 파일이 있다거나... 이런 상황에 대비해봅시다!

#### 안전한 예외 처리

```python
# 안전한 파일명 변경하기 (src/chapter1/step6_error_handling.py)
def safe_rename_file(old_name, new_name):
    """안전하게 파일명을 바꾸는 함수"""
    print(f"'{old_name}'을 '{new_name}'으로 바꾸려고 해요...")
    
    try:
        # 1단계: 원본 파일이 정말 있는지 확인
        import os
        if not os.path.exists(old_name):
            print(f"❌ 앗! '{old_name}' 파일을 찾을 수 없어요!")
            return False
        
        # 2단계: 새 이름으로 된 파일이 이미 있는지 확인  
        if os.path.exists(new_name):
            print(f"⚠️  '{new_name}' 파일이 이미 있어요!")
            print("   같은 이름의 파일이 있으면 덮어써질 수 있어요.")
            return False
        
        # 3단계: 실제로는 파일명을 바꾸지 않고 시뮬레이션만
        print(f"✅ 성공! '{old_name}' → '{new_name}'으로 바뀔 예정이에요")
        return True
        
    except PermissionError:
        print("🚫 권한이 없어서 파일을 바꿀 수 없어요!")
        print("   (파일이 다른 프로그램에서 사용 중일 수도 있어요)")
        return False
    
    except Exception as e:
        print(f"😵 예상치 못한 문제가 생겼어요: {e}")
        print("   개발자에게 문의해주세요!")
        return False

# 테스트해보기
print("=== 안전한 파일명 변경 테스트 ===")

# 존재하지 않는 파일 테스트
safe_rename_file("없는파일.txt", "새파일.txt")
print()

# 실제 존재할 만한 파일 테스트  
safe_rename_file("C:/Windows/System32/notepad.exe", "새이름.exe")
print()
```

#### 실행 결과
```
=== 안전한 파일명 변경 테스트 ===
'없는파일.txt'을 '새파일.txt'으로 바꾸려고 해요...
❌ 앗! '없는파일.txt' 파일을 찾을 수 없어요!

'C:/Windows/System32/notepad.exe'을 '새이름.exe'으로 바꾸려고 해요...
🚫 권한이 없어서 파일을 바꿀 수 없어요!
   (파일이 다른 프로그램에서 사용 중일 수도 있어요)
```

#### 왜 try-except를 사용하나요?

**프로그램이 갑자기 멈추는 것을 방지하기 위해서예요!**

**try-except 구조:**

- `try:` → "이 코드를 실행해보세요"
- `except:` → "문제가 생기면 이렇게 처리하세요"

이렇게 하면 사용자가 실수해도 프로그램이 안전하게 동작합니다!

**예외 처리의 종류:**

- `FileNotFoundError` - 파일을 찾을 수 없을 때
- `PermissionError` - 권한이 없을 때
- `FileExistsError` - 같은 이름의 파일이 이미 있을 때
- `Exception` - 모든 예외를 잡는 범용 예외처리

**예외 처리의 장점:**

1. **안정성** - 프로그램이 갑자기 종료되지 않음
2. **사용자 친화적** - 오류 상황을 친절하게 알려줌
3. **디버깅 도움** - 문제의 원인을 파악할 수 있음
4. **복구 가능** - 오류 상황에서도 다른 작업을 계속할 수 있음

## 클래스로 코드 정리하기

### 7단계: 나만의 파일 관리자 만들기

지금까지 배운 것들을 모아서 **클래스(Class)**<!-- -->라는 것을 만들어봅시다. 클래스는 관련된 기능들을 하나로 묶어주는 상자 같은 거예요!

#### 파일 관리자 클래스 설계

```python
# 나만의 파일 관리자 클래스 (src/chapter1/step7_file_manager_class.py)
class MyFileManager:
    """내가 만든 파일 관리자"""
    
    def __init__(self):
        """파일 관리자를 처음 만들 때 실행되는 함수"""
        print("🎉 새로운 파일 관리자가 만들어졌어요!")
        self.my_files = []  # 내 파일들을 저장할 리스트
        self.total_renamed = 0  # 지금까지 바꾼 파일 개수
    
    def add_file(self, file_path):
        """파일을 관리 목록에 추가하기"""
        if file_path not in self.my_files:
            self.my_files.append(file_path)
            print(f"📁 '{file_path}' 파일을 추가했어요!")
        else:
            print(f"⚠️  '{file_path}' 파일은 이미 있어요!")
    
    def show_files(self):
        """현재 관리 중인 파일들 보여주기"""
        print(f"\n📋 현재 관리 중인 파일: {len(self.my_files)}개")
        for i, file_path in enumerate(self.my_files, 1):
            print(f"   {i}. {file_path}")
    
    def add_prefix_to_all(self, prefix):
        """모든 파일에 접두사 추가하기"""
        print(f"\n✨ 모든 파일에 '{prefix}' 접두사 추가 결과:")
        new_names = []
        
        for file_path in self.my_files:
            from pathlib import Path
            file_info = Path(file_path)
            new_name = prefix + file_info.name
            new_full_path = file_info.parent / new_name
            new_names.append(str(new_full_path))
            print(f"   📄 {file_info.name} → {new_name}")
        
        return new_names
    
    def add_numbers_to_all(self, start_number=1):
        """모든 파일에 순서대로 번호 매기기"""
        print(f"\n🔢 {start_number}번부터 순서대로 번호 매기기:")
        new_names = []
        
        for i, file_path in enumerate(self.my_files):
            from pathlib import Path
            file_info = Path(file_path)
            number = start_number + i
            new_name = f"{number:03d}_{file_info.name}"  # 001, 002, 003...
            new_full_path = file_info.parent / new_name
            new_names.append(str(new_full_path))
            print(f"   📄 {file_info.name} → {new_name}")
        
        return new_names
```

#### 클래스가 뭔가요?

클래스는 **관련된 기능들을 하나로 묶어놓은 설계도**<!-- -->입니다!

**클래스의 핵심 개념들:**

- `MyFileManager()` → 새로운 파일 관리자 하나 만들기 (인스턴스 생성)
- `self.my_files` → 이 관리자가 기억하고 있는 파일 목록 (인스턴스 변수)
- `self.add_file()` → 이 관리자에게 "파일 추가해줘"라고 부탁하기 (메소드)

**클래스 vs 함수의 차이점:**

| 구분 | 함수 | 클래스 |
|------|------|--------|
| **용도** | 특정 작업 하나를 수행 | 관련된 여러 기능을 묶어서 관리 |
| **데이터** | 매번 새로 받아야 함 | 내부에 데이터를 기억하고 있음 |
| **예시** | `add_prefix("NEW_", file)` | `manager.add_prefix("NEW_")` |

**객체지향 프로그래밍의 장점:**

1. **코드 정리** - 관련 기능들이 한 곳에 모여 있음
2. **데이터 보호** - `self.my_files`는 클래스 내부에서만 직접 접근 가능  
3. **재사용성** - 여러 개의 파일 관리자를 독립적으로 만들 수 있음
4. **확장성** - 나중에 새로운 기능을 쉽게 추가할 수 있음

**실제 KRenamer에서 클래스 사용 예시:**

```python
# 사진 정리용 관리자
photo_manager = MyFileManager()
photo_manager.add_file("IMG_001.jpg")
photo_manager.add_file("IMG_002.jpg")

# 문서 정리용 관리자 (별도)
document_manager = MyFileManager() 
document_manager.add_file("report.pdf")
document_manager.add_file("memo.txt")

# 각각 독립적으로 작업 가능
photo_manager.add_prefix("2024_")
document_manager.add_numbers_to_all(start=1)
```

### 8단계: 파일 관리자 사용해보기

#### 클래스 실제 사용 예제

```python
# 파일 관리자 사용해보기
print("=== 나만의 파일 관리자 사용해보기 ===")

# 1단계: 새로운 파일 관리자 만들기
my_manager = MyFileManager()

# 2단계: 파일들 추가하기
test_files = [
    "C:/Users/내이름/Documents/중요한문서.pdf",
    "C:/Users/내이름/Pictures/가족사진.jpg", 
    "C:/Users/내이름/Music/좋아하는노래.mp3",
    "C:/Users/내이름/Desktop/메모.txt"
]

print("\n📁 파일들을 관리자에 추가하는 중...")
for file_name in test_files:
    my_manager.add_file(file_name)

# 3단계: 현재 파일 목록 확인하기
my_manager.show_files()

# 4단계: 모든 파일에 접두사 추가해보기
my_manager.add_prefix_to_all("정리완료_")

print("\n" + "="*50)

# 5단계: 모든 파일에 순번 매기기
my_manager.add_numbers_to_all(start_number=1)

print("\n🎉 파일 관리자 사용 완료!")
```

#### 실행 결과 미리보기

```
=== 나만의 파일 관리자 사용해보기 ===
🎉 새로운 파일 관리자가 만들어졌어요!

📁 파일들을 관리자에 추가하는 중...
📁 'C:/Users/내이름/Documents/중요한문서.pdf' 파일을 추가했어요!
📁 'C:/Users/내이름/Pictures/가족사진.jpg' 파일을 추가했어요!
📁 'C:/Users/내이름/Music/좋아하는노래.mp3' 파일을 추가했어요!
📁 'C:/Users/내이름/Desktop/메모.txt' 파일을 추가했어요!

📋 현재 관리 중인 파일: 4개
   1. C:/Users/내이름/Documents/중요한문서.pdf
   2. C:/Users/내이름/Pictures/가족사진.jpg
   3. C:/Users/내이름/Music/좋아하는노래.mp3
   4. C:/Users/내이름/Desktop/메모.txt

✨ 모든 파일에 '정리완료_' 접두사 추가 결과:
   📄 중요한문서.pdf → 정리완료_중요한문서.pdf
   📄 가족사진.jpg → 정리완료_가족사진.jpg
   📄 좋아하는노래.mp3 → 정리완료_정리완료_좋아하는노래.mp3
   📄 메모.txt → 정리완료_메모.txt

==================================================

🔢 1번부터 순서대로 번호 매기기:
   📄 중요한문서.pdf → 001_중요한문서.pdf
   📄 가족사진.jpg → 002_가족사진.jpg
   📄 좋아하는노래.mp3 → 003_좋아하는노래.mp3
   📄 메모.txt → 004_메모.txt

🎉 파일 관리자 사용 완료!
```

#### 축하합니다! 

클래스를 사용해서 코드를 깔끔하게 정리하는 방법을 배웠어요!

**클래스의 주요 장점:**

- **코드 정리**: 관련된 기능들을 한 곳에 모음
- **데이터 보호**: `self.my_files`는 클래스 내부에서만 직접 접근 가능
- **재사용**: 여러 개의 파일 관리자를 만들 수 있음
- **확장성**: 나중에 새로운 기능을 쉽게 추가할 수 있음

## 추가로 알아두면 좋은 고급 기법들 

### 9단계: 똑똑한 리스트 만들기 (리스트 컴프리헨션)

파이썬에는 리스트를 더 쉽고 빠르게 만드는 방법이 있어요. 마치 "조건에 맞는 것들만 골라서 새 리스트 만들기"처럼요!

```python linenums="255" title="똑똑한 리스트 만들기"
print("=== 똑똑한 리스트 만들기 ===")

files = [
    "문서.pdf", "사진.jpg", "음악.mp3", 
    "압축파일.zip", "메모.txt", "그림.png", "매우긴파일명이있는문서.docx"
]

print("📂 원본 파일들:")
for file in files:
    print(f"   - {file}")

# 방법 1: 전통적인 방법 - 이미지 파일만 찾기
print("\n🖼️  방법 1 (전통적): 이미지 파일만 찾기")
image_files_old = []
for file in files:
    if file.endswith(('.jpg', '.png')):
        image_files_old.append(file)
print(f"   결과: {image_files_old}")

# 방법 2: 리스트 컴프리헨션 - 한 줄로!
print("\n🚀 방법 2 (똑똑한 방법): 이미지 파일만 찾기")
image_files_new = [file for file in files if file.endswith(('.jpg', '.png'))]
print(f"   결과: {image_files_new}")

# 더 많은 예시들
print("\n✨ 더 많은 똑똑한 리스트 만들기:")

# 확장자 제거하기
names_only = [file.split('.')[0] for file in files]
print(f"📝 확장자 제거: {names_only}")

# 긴 파일명만 선택하기 (8글자 이상)
long_names = [file for file in files if len(file) > 8]
print(f"📏 긴 파일명들: {long_names}")

# 조건에 따라 다르게 처리하기
processed = [file.upper() if file.endswith('.txt') else file for file in files]
print(f"🔄 txt는 대문자로: {processed}")
```

!!! tip "💡 리스트 컴프리헨션 읽는 법"
    `[뭘_만들지 for 각_항목 in 원본_리스트 if 조건]`
    
    - `file` → 각각의 파일을 의미
    - `for file in files` → files 리스트의 각 파일에 대해
    - `if file.endswith('.jpg')` → jpg로 끝나는 파일만
    - `file.upper()` → 대문자로 바꿔서 새 리스트에 넣기

## 🧪 직접 해보기 (실습 과제)

### 🌟 기본 도전과제

이제 여러분이 직접 해볼 차례예요! 차근차근 해보세요.

#### 1. 파일명 깔끔하게 만들기 🧹
```python
def clean_my_filename(filename):
    """파일명을 깔끔하게 정리하는 함수를 만들어보세요!"""
    # 힌트: 
    # - 공백을 언더스코어(_)로 바꾸기
    # - 특수문자 (, ), [, ] 제거하기  
    # - 연속된 언더스코어를 하나로 만들기
    
    # 여기에 코드를 작성해보세요!
    pass

# 테스트해보기
test_filename = "내 중요한 문서 (복사본) [최종].pdf"
print(f"원본: {test_filename}")
print(f"정리: {clean_my_filename(test_filename)}")
# 기대 결과: "내_중요한_문서_최종.pdf"
```

#### 2. 확장자별로 파일 분류하기 📂
```python
def sort_files_by_type(file_list):
    """파일들을 확장자별로 분류하는 함수를 만들어보세요!"""
    # 힌트:
    # - 딕셔너리를 만들어서 확장자를 키로 사용
    # - 같은 확장자끼리 리스트로 묶기
    
    # 여기에 코드를 작성해보세요!
    pass

# 테스트해보기
my_files = ["사진1.jpg", "문서.pdf", "사진2.jpg", "음악.mp3", "메모.txt", "노래2.mp3"]
sorted_files = sort_files_by_type(my_files)
print("확장자별 분류 결과:")
for ext, files in sorted_files.items():
    print(f"  {ext}: {files}")
```

### 🚀 고급 도전과제

#### 3. 똑똑한 파일명 만들기 🤖
```python
def make_smart_filename(original_name, options):
    """여러 옵션을 받아서 파일명을 똑똑하게 바꾸는 함수"""
    # options 예시:
    # {
    #     'add_date': True,        # 현재 날짜 추가
    #     'add_number': 1,         # 순번 추가  
    #     'make_lowercase': True,  # 소문자로 변경
    #     'remove_spaces': True    # 공백 제거
    # }
    
    # 도전해보세요!
    pass

# 테스트해보기
options = {
    'add_date': True,
    'add_number': 5,
    'make_lowercase': True,
    'remove_spaces': True
}
result = make_smart_filename("My Important File.txt", options)
print(f"똑똑한 파일명: {result}")
```

**해결 방법 힌트:**

1. `from datetime import datetime` - 날짜 처리용
2. `name, ext = os.path.splitext(original_name)` - 파일명과 확장자 분리
3. `if options.get('add_date'):` - 옵션 확인
4. `datetime.now().strftime("%Y%m%d")` - 날짜 포맷팅
5. 순서: 날짜 → 번호 → 원본이름 → 소문자 → 공백제거

**기대 결과:**
```
똑똑한 파일명: 20241215_005_my_important_file.txt
```

#### 막히면 어떻게 하나요?

**걱정하지 마세요!** 프로그래밍에서 막히는 건 당연해요.

**문제 해결 전략:**

1. **천천히 단계별로** - 큰 문제를 작은 부분으로 나누어 생각하기
2. **이전 예시 참고** - 위에서 배운 코드들을 다시 보기
3. **작은 것부터** - 전체를 다 만들려 하지 말고 일부분부터 시작
4. **테스트하며 진행** - 조금씩 만들어가며 print()로 확인하기
5. **인터넷 검색** - "python 파일명 바꾸기" 같은 키워드로 검색

**디버깅 팁:**
```python
# 단계별로 테스트
이름 = "My Important File.txt"
print(f"1. 원본: {filename}")
print(f"2. 소문자: {filename.lower()}")
print(f"3. 공백제거: {filename.lower().replace(' ', '_')}")
# ... 단계별로 확인
```

## 🎯 다음에는 뭘 배우나요?

Chapter 1에서 배운 파이썬 기초가 다음 챕터들에서 어떻게 쓰이는지 미리 봅시다!

### 🗺️ 우리의 학습 여정

```
Chapter 1 (지금!) → Chapter 2 → Chapter 3 → ... → Chapter 11
    📝 파이썬           🖼️ GUI          🖱️ 드래그앤드롭        🚀 프로그램 배포
     기초              화면 만들기        파일 끌어다 놓기         다른 사람도 사용
```

**다음 챕터들에서 사용될 오늘 배운 내용들:**

- **Chapter 2** 🖼️: 클래스로 화면 구성 요소들 만들기
- **Chapter 3** 🖱️: 파일 정보 처리와 리스트로 파일 관리
- **Chapter 4** ✏️: 문자열 처리로 실제 파일명 바꾸기
- **Chapter 5** 🔧: 예외 처리로 안전한 파일 작업
- **Chapter 6+** 🚀: 더 전문적인 프로그램 만들기

## 🎓 Chapter 1 졸업 시험!

### ✅ 내가 배운 것들 체크해보기

**파이썬 기초 (기본 중의 기본!)**

- [ ] 변수에 값 저장하기 (`name = "파일명"`)
- [ ] 문자열 바꾸기 (`filename.replace(" ", "_")`)
- [ ] 리스트 사용하기 (`my_files = ["a.txt", "b.jpg"]`)
- [ ] 반복문으로 여러 작업 하기 (`for file in files:`)
- [ ] 함수 만들어서 코드 정리하기 (`def my_function():`)

**파일 다루기 (KRenamer의 핵심!)**

- [ ] 파일 경로 분석하기 (`Path(file_path).name`)
- [ ] 파일명과 확장자 나누기 (`os.path.splitext()`)
- [ ] 파일 크기 예쁘게 표시하기 (`1024 → 1KB`)
- [ ] 안전하게 오류 처리하기 (`try-except`)

**고급 기법들 (보너스!)**

- [ ] 클래스로 코드 정리하기 (`class FileManager:`)
- [ ] 리스트 컴프리헨션 (`[f for f in files if ...]`)

### 🌟 최종 점검 문제

다음 코드가 뭘 하는지 이해할 수 있나요?

```python
files = ["사진 (복사본).jpg", "문서.pdf", "음악.mp3"]
cleaned = [f.replace(" (복사본)", "") for f in files if f.endswith('.jpg')]
print(cleaned)  # 결과: ['사진.jpg']
```

이해했다면 Chapter 1 졸업! 🎉

---

### Chapter 1 완주 축하드려요!

파이썬 기초를 배웠습니다!

**이제 할 수 있는 것들:**

- ✅ 변수와 리스트로 데이터 관리
- ✅ 파일명을 마음대로 바꾸기
- ✅ 반복문으로 여러 파일 한 번에 처리
- ✅ 클래스로 깔끔한 코드 작성
- ✅ 안전한 오류 처리
- ✅ 정규표현식과 pathlib 활용
- ✅ 리스트 컴프리헨션과 고급 기법

**다음 단계 준비하기**

**Chapter 2에서는:**

- 화면에 버튼과 입력창 만들기
- 마우스 클릭 이벤트 처리하기
- 예쁜 GUI 프로그램 완성하기

오늘 배운 파이썬 기초가 모두 사용됩니다!

**한 번 더 연습하고 싶다면:**

- `src/chapter1/main.py` 파일을 실행해보세요
- 각 단계별 예제 파일들도 개별적으로 돌려보세요
- 연습 문제들을 직접 풀어보세요

이제 여러분은 파이썬의 기초를 탄탄히 다진 대민입니다. 다음 챕터에서 더 흥미로운 GUI 프로그래밍의 세계로 다어가 봅시다!