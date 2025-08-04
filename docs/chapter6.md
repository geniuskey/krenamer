# Chapter 6: 고급 기능 만들기

이번 챕터에서는 지금까지 만든 파일명 변경 도구를 **전문적인 프로그램**<!-- -->으로 업그레이드해보겠습니다.

Chapter 5에서 기본적인 파일명 변경 기능을 만들었다면, 이번에는 **더 똑똑하고 편리한** 기능들을 추가해보겠습니다.

## 🎯 이번 챕터에서 만들 것들

- **Step 1**: 파일 필터링 기능 (크기, 확장자별로 골라내기)
- **Step 2**: 설정 저장하기 (자주 쓰는 설정을 기억하게 하기)
- **Step 3**: 작업 기록 남기기 (뭘 바꿨는지 추적하고 되돌리기)
- **Step 4**: 사용자 친화적인 UI 만들기

이런 기능들이 있으면 훨씬 더 편리하게 사용할 수 있겠죠?

## 💡 고급 기능이 필요한 이유

실제로 파일명을 바꾸다보면 이런 상황들을 만나게 됩니다:

### 현실적인 문제들
- **"JPG 파일만 골라서 바꾸고 싶어"** → 확장자 필터링 필요
- **"너무 작은 파일들은 제외하고 싶어"** → 크기 필터링 필요  
- **"자주 쓰는 설정을 매번 다시 입력하기 귀찮아"** → 설정 저장 필요
- **"실수로 바꿨는데 되돌리고 싶어"** → 작업 기록 필요

이런 문제들을 해결하기 위해 고급 기능을 만들어보겠습니다.

## Step 1: 파일 필터링 기능 만들기

먼저 **파일을 조건에 따라 골라내는** 기능을 만들어보겠습니다. 예를 들어 "JPG 파일만" 또는 "1MB 이상인 파일만" 같은 조건으로 필터링하는 거죠.

### 필터링이란?

필터링은 **조건에 맞는 것만 걸러내는** 것입니다. 커피 필터처럼요!

```
전체 파일들 → [필터] → 조건에 맞는 파일들만
```

### 어떤 필터들을 만들까요?

1. **확장자 필터**: ".jpg", ".png" 같은 확장자로 필터링
2. **크기 필터**: "1MB 이상", "10KB 이하" 같은 크기로 필터링
3. **이름 필터**: "photo"가 들어간 파일만 같은 이름으로 필터링

### 기본 필터 클래스 만들기

먼저 모든 필터의 **기본 틀**<!-- -->을 만들어보겠습니다:

```python title="src/chapter6/simple_filters.py"
class BaseFilter:
    """모든 필터의 기본 클래스"""
    
    def matches(self, file_path):
        """이 파일이 필터 조건에 맞는지 확인"""
        # 하위 클래스에서 구현할 예정
        return True
    
    def get_description(self):
        """필터가 뭘 하는지 설명"""
        return "기본 필터"
```

이건 **템플릿**<!-- -->같은 거예요. 실제 필터들은 이걸 상속받아서 만들 예정입니다.

### 확장자 필터 만들기

가장 쉬운 확장자 필터부터 만들어보겠습니다:

```python
import os

class ExtensionFilter(BaseFilter):
    """확장자로 필터링하는 클래스"""
    
    def __init__(self, extensions):
        # 허용할 확장자 목록 (예: [".jpg", ".png"])
        self.extensions = [ext.lower() for ext in extensions]
    
    def matches(self, file_path):
        # 파일의 확장자 구하기
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # 허용된 확장자인지 확인
        return ext in self.extensions
    
    def get_description(self):
        ext_str = ", ".join(self.extensions)
        return f"확장자: {ext_str}"
```

### 사용 예시

```python
# JPG와 PNG 파일만 필터링
filter = ExtensionFilter([".jpg", ".png"])

# 테스트
print(filter.matches("photo.jpg"))    # True
print(filter.matches("document.txt")) # False
print(filter.get_description())       # "확장자: .jpg, .png"
```

### 크기 필터 만들기

이번에는 파일 크기로 필터링하는 기능을 만들어보겠습니다:

```python
class SizeFilter(BaseFilter):
    """파일 크기로 필터링하는 클래스"""
    
    def __init__(self, min_size=0, max_size=0):
        self.min_size = min_size  # 최소 크기 (바이트)
        self.max_size = max_size  # 최대 크기 (바이트)
    
    def matches(self, file_path):
        try:
            # 파일 크기 확인
            file_size = os.path.getsize(file_path)
            
            # 최소 크기 체크
            if self.min_size > 0 and file_size < self.min_size:
                return False
            
            # 최대 크기 체크  
            if self.max_size > 0 and file_size > self.max_size:
                return False
            
            return True
        except:
            return False  # 파일을 읽을 수 없으면 제외
    
    def get_description(self):
        if self.min_size > 0 and self.max_size > 0:
            return f"크기: {self._format_size(self.min_size)} ~ {self._format_size(self.max_size)}"
        elif self.min_size > 0:
            return f"크기: {self._format_size(self.min_size)} 이상"
        elif self.max_size > 0:
            return f"크기: {self._format_size(self.max_size)} 이하"
        else:
            return "크기: 제한없음"
    
    def _format_size(self, size_bytes):
        """바이트를 읽기 쉬운 형태로 변환"""
        if size_bytes < 1024:
            return f"{size_bytes}B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f}KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f}MB"
```

### 사용 예시

```python
# 1MB 이상 10MB 이하의 파일만
filter = SizeFilter(min_size=1024*1024, max_size=10*1024*1024)

print(filter.get_description())  # "크기: 1.0MB ~ 10.0MB"
```

### 필터 관리자 만들기

이제 여러 개의 필터를 한번에 관리할 수 있는 **필터 관리자**<!-- -->를 만들어보겠습니다:

```python
class FilterManager:
    """여러 필터를 관리하는 클래스"""
    
    def __init__(self):
        self.filters = []  # 적용된 필터들 목록
    
    def add_filter(self, filter):
        """필터 추가"""
        self.filters.append(filter)
    
    def remove_filter(self, filter):
        """필터 제거"""
        if filter in self.filters:
            self.filters.remove(filter)
    
    def clear_filters(self):
        """모든 필터 제거"""
        self.filters.clear()
    
    def filter_files(self, file_list):
        """파일 목록을 필터링해서 조건에 맞는 것만 반환"""
        if not self.filters:
            return file_list  # 필터가 없으면 전체 반환
        
        filtered_files = []
        
        for file_path in file_list:
            # 모든 필터 조건을 만족하는지 확인
            passes_all_filters = True
            
            for filter in self.filters:
                if not filter.matches(file_path):
                    passes_all_filters = False
                    break
            
            if passes_all_filters:
                filtered_files.append(file_path)
        
        return filtered_files
    
    def get_filter_summary(self):
        """적용된 필터들의 설명 반환"""
        if not self.filters:
            return ["필터 없음"]
        
        return [filter.get_description() for filter in self.filters]
```

### 실제 사용 예시

```python
# 필터 관리자 생성
filter_manager = FilterManager()

# 필터들 추가
filter_manager.add_filter(ExtensionFilter([".jpg", ".png"]))
filter_manager.add_filter(SizeFilter(min_size=100*1024))  # 100KB 이상

# 파일 목록 필터링
file_list = ["photo.jpg", "small.png", "document.txt", "large.png"]
filtered = filter_manager.filter_files(file_list)

print("필터링된 파일들:", filtered)
print("적용된 필터:", filter_manager.get_filter_summary())
```

이제 기본적인 필터링 시스템이 완성되었습니다!

## Step 2: 설정 저장하기

사용자가 자주 사용하는 설정을 **기억해두고 나중에 불러올 수 있는** 기능을 만들어보겠습니다.

### 설정 저장이 왜 필요할까요?

매번 프로그램을 시작할 때마다 같은 설정을 다시 입력하는 건 번거롭죠. 특히:

- 자주 사용하는 접두사/접미사
- 자주 사용하는 필터 조건  
- 창 크기나 위치
- 기타 개인 설정들

이런 것들을 자동으로 기억해뒀다가 다음에 프로그램을 켤 때 자동으로 복원해주면 편리합니다.

### 설정을 어디에 저장할까요?

설정을 저장하는 방법은 여러 가지가 있습니다:

1. **JSON 파일**: 사람이 읽기 쉽고 편집하기 쉬움
2. **INI 파일**: 윈도우에서 전통적으로 사용
3. **데이터베이스**: 복잡한 설정에 적합

우리는 **JSON 파일**<!-- -->을 사용하겠습니다. 간단하고 다른 플랫폼에서도 잘 동작하거든요.

### 간단한 설정 관리자 만들기

```python title="src/chapter6/settings_manager.py"
import json
import os
from pathlib import Path

class SimpleSettingsManager:
    """간단한 설정 관리 클래스"""
    
    def __init__(self, app_name="KRenamer"):
        self.app_name = app_name
        
        # 설정 파일이 저장될 경로 설정
        self.config_dir = self._get_config_directory()
        self.config_file = self.config_dir / "settings.json"
        
        # 설정 디렉토리 생성
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # 기본 설정들
        self.default_settings = {
            "rename_options": {
                "prefix": "",
                "suffix": "", 
                "find_text": "",
                "replace_text": ""
            },
            "window": {
                "width": 800,
                "height": 600
            },
            "filters": {
                "remember_last_used": True
            }
        }
        
        # 현재 설정 로드
        self.current_settings = self.load_settings()
    
    def _get_config_directory(self):
        """운영체제별 설정 디렉토리 경로 반환"""
        if os.name == 'nt':  # 윈도우
            config_dir = Path.home() / "AppData" / "Local" / self.app_name
        else:  # 맥, 리눅스
            config_dir = Path.home() / f".{self.app_name.lower()}"
        
        return config_dir
```

### 설정 로드하기

```python
def load_settings(self):
    """설정 파일을 불러오기"""
    if self.config_file.exists():
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                loaded_settings = json.load(f)
            
            # 기본 설정과 합치기 (새로운 설정 항목이 추가된 경우 대비)
            return self._merge_settings(self.default_settings, loaded_settings)
            
        except Exception as e:
            print(f"설정 로드 실패: {e}")
    
    # 로드 실패시 기본 설정 반환
    return self.default_settings.copy()

def _merge_settings(self, default, loaded):
    """기본 설정과 로드된 설정을 합치기"""
    result = default.copy()
    
    for key, value in loaded.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # 딕셔너리인 경우 재귀적으로 합치기
            result[key] = self._merge_settings(result[key], value)
        else:
            # 일반 값인 경우 그대로 사용
            result[key] = value
    
    return result
```

### 설정 저장하기

```python
def save_settings(self):
    """현재 설정을 파일에 저장"""
    try:
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.current_settings, f, indent=2, ensure_ascii=False)
        print("설정이 저장되었습니다.")
    except Exception as e:
        print(f"설정 저장 실패: {e}")
```

### 편리한 설정 접근 방법

설정을 쉽게 읽고 쓸 수 있는 **헬퍼 메서드**<!-- -->들을 만들어보겠습니다:

```python
def get(self, path, default=None):
    """점 표기법으로 설정 값 읽기"""
    # 예: get("rename_options.prefix")
    keys = path.split('.')
    value = self.current_settings
    
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default

def set(self, path, value):
    """점 표기법으로 설정 값 쓰기"""
    # 예: set("rename_options.prefix", "새_")
    keys = path.split('.')
    settings = self.current_settings
    
    # 마지막 키 전까지 딕셔너리들을 찾아가기
    for key in keys[:-1]:
        if key not in settings:
            settings[key] = {}
        settings = settings[key]
    
    # 마지막 키에 값 저장
    settings[keys[-1]] = value
```

### 사용 예시

```python
# 설정 관리자 생성
settings = SimpleSettingsManager()

# 설정 읽기
prefix = settings.get("rename_options.prefix", "")
window_width = settings.get("window.width", 800)

# 설정 쓰기
settings.set("rename_options.prefix", "새_")
settings.set("window.width", 1000)

# 파일에 저장
settings.save_settings()
```

## Step 3: 작업 기록 남기기

사용자가 **뭘 바꿨는지 추적하고 실수했을 때 되돌릴 수 있는** 기능을 만들어보겠습니다.

### 작업 기록이 왜 필요할까요?

파일명을 바꾸다가 실수할 수 있습니다:

- **잘못된 설정으로 100개 파일을 한번에 바꿨어!**
- **원래 이름이 뭐였는지 기억이 안나!**
- **되돌리고 싶은데 방법이 없어!**

이런 상황을 방지하기 위해 **작업 기록(히스토리)**<!-- -->을 남겨두는 거죠.

### 간단한 작업 기록 시스템 만들기

```python title="src/chapter6/simple_history.py"
import json
from datetime import datetime
from pathlib import Path

class SimpleHistoryManager:
    """간단한 작업 기록 관리자"""
    
    def __init__(self, config_dir):
        self.config_dir = Path(config_dir)
        self.history_file = self.config_dir / "history.json"
        self.current_session = None
        
    def start_session(self, session_name):
        """새로운 작업 세션 시작"""
        self.current_session = {
            "session_name": session_name,
            "timestamp": datetime.now().isoformat(),
            "actions": []
        }
        return self.current_session
    
    def add_action(self, action_type, original_path, new_path, success=True, error=""):
        """현재 세션에 작업 기록 추가"""
        if not self.current_session:
            return
        
        action = {
            "type": action_type,
            "original_path": original_path,
            "new_path": new_path,
            "success": success,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        
        self.current_session["actions"].append(action)
    
    def end_session(self):
        """현재 세션 종료하고 저장"""
        if not self.current_session:
            return
        
        # 기존 히스토리 로드
        history = self.load_history()
        
        # 새 세션 추가
        history.append(self.current_session)
        
        # 너무 많아지면 오래된 것 삭제 (최대 50개만 보관)
        if len(history) > 50:
            history = history[-50:]
        
        # 파일에 저장
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"히스토리 저장 실패: {e}")
        
        self.current_session = None
    
    def load_history(self):
        """히스토리 파일 로드"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"히스토리 로드 실패: {e}")
        
        return []
```

### 되돌리기 기능 만들기

```python
def rollback_session(self, session_index):
    """특정 세션의 작업을 되돌리기"""
    history = self.load_history()
    
    if session_index < 0 or session_index >= len(history):
        return {"success": 0, "failed": 0, "errors": ["잘못된 세션 번호"]}
    
    session = history[session_index]
    result = {"success": 0, "failed": 0, "errors": []}
    
    # 성공한 작업들을 역순으로 되돌리기
    successful_actions = [a for a in session["actions"] if a["success"]]
    
    for action in reversed(successful_actions):
        if action["type"] == "rename":
            try:
                # new_path에서 original_path로 되돌리기
                import os
                if os.path.exists(action["new_path"]):
                    os.rename(action["new_path"], action["original_path"])
                    result["success"] += 1
                else:
                    result["failed"] += 1
                    result["errors"].append(f"파일을 찾을 수 없음: {action['new_path']}")
            except Exception as e:
                result["failed"] += 1
                result["errors"].append(f"되돌리기 실패: {str(e)}")
    
    return result

def get_history_summary(self):
    """히스토리 요약 정보 반환"""
    history = self.load_history()
    summary = []
    
    for i, session in enumerate(reversed(history)):  # 최신순으로
        session_info = {
            "index": len(history) - 1 - i,  # 실제 인덱스
            "name": session["session_name"],
            "timestamp": session["timestamp"],
            "total_actions": len(session["actions"]),
            "successful_actions": len([a for a in session["actions"] if a["success"]])
        }
        summary.append(session_info)
    
    return summary
```

### 사용 예시

```python
# 히스토리 관리자 생성
history = SimpleHistoryManager("./config")

# 작업 세션 시작
history.start_session("일괄 파일명 변경")

# 작업들 기록
history.add_action("rename", "old1.txt", "new1.txt", True)
history.add_action("rename", "old2.txt", "new2.txt", True)
history.add_action("rename", "old3.txt", "new3.txt", False, "권한 없음")

# 세션 종료
history.end_session()

# 히스토리 확인
summary = history.get_history_summary()
print("최근 작업들:", summary)

# 필요시 되돌리기
rollback_result = history.rollback_session(0)  # 가장 최근 세션 되돌리기
print("되돌리기 결과:", rollback_result)
```

## Step 4: 모든 기능을 GUI에 통합하기

이제 지금까지 만든 모든 고급 기능들을 **실제 GUI에 연결해서** 사용할 수 있게 만들어보겠습니다.

### 통합된 메인 애플리케이션

```python title="src/chapter6/main.py"
import tkinter as tk
from tkinter import ttk, messagebox
from rename_engine import RenameEngine  # Chapter 5에서 만든 것
from simple_filters import FilterManager, ExtensionFilter, SizeFilter
from settings_manager import SimpleSettingsManager
from simple_history import SimpleHistoryManager

class AdvancedRenamerGUI:
    """고급 기능이 포함된 파일명 변경 GUI"""
    
    def __init__(self):
        self.root = tk.Tk()
        
        # 핵심 컴포넌트들 초기화
        self.engine = RenameEngine()
        self.filter_manager = FilterManager()
        self.settings = SimpleSettingsManager()
        self.history = SimpleHistoryManager(self.settings.config_dir)
        
        self.setup_window()
        self.setup_widgets()
        self.load_saved_settings()
    
    def setup_window(self):
        self.root.title("KRenamer - Advanced")
        
        # 저장된 창 크기 불러오기
        width = self.settings.get("window.width", 900)
        height = self.settings.get("window.height", 700)
        self.root.geometry(f"{width}x{height}")
        
        # 종료시 설정 저장
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_widgets(self):
        # 메뉴바 추가
        self.setup_menubar()
        
        # 기존 GUI 구성들 (Chapter 5에서 만든 것들)
        # + 필터 버튼들 추가
        
        # 필터 섹션
        filter_frame = ttk.LabelFrame(self.root, text="파일 필터", padding="10")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(filter_frame, text="필터 설정", 
                  command=self.show_filter_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="필터 초기화", 
                  command=self.clear_filters).pack(side=tk.LEFT, padx=5)
        
        # 필터 상태 표시
        self.filter_status_var = tk.StringVar(value="필터 없음")
        ttk.Label(filter_frame, textvariable=self.filter_status_var).pack(side=tk.LEFT, padx=20)
    
    def setup_menubar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 파일 메뉴
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="파일", menu=file_menu)
        file_menu.add_command(label="설정 저장", command=self.save_current_settings)
        file_menu.add_command(label="종료", command=self.on_closing)
        
        # 히스토리 메뉴
        history_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="히스토리", menu=history_menu)
        history_menu.add_command(label="작업 기록 보기", command=self.show_history)
        history_menu.add_command(label="최근 작업 되돌리기", command=self.rollback_last)
    
    def show_filter_dialog(self):
        """간단한 필터 설정 대화상자"""
        dialog = tk.Toplevel(self.root)
        dialog.title("필터 설정")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 확장자 필터
        ext_frame = ttk.LabelFrame(dialog, text="확장자 필터", padding="10")
        ext_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(ext_frame, text="확장자 (쉼표로 구분):").pack(anchor=tk.W)
        ext_entry = ttk.Entry(ext_frame, width=40)
        ext_entry.pack(fill=tk.X, pady=5)
        ext_entry.insert(0, ".jpg,.png,.gif")  # 기본값
        
        # 크기 필터
        size_frame = ttk.LabelFrame(dialog, text="크기 필터", padding="10")
        size_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(size_frame, text="최소 크기 (KB):").pack(anchor=tk.W)
        min_size_entry = ttk.Entry(size_frame, width=20)
        min_size_entry.pack(anchor=tk.W, pady=2)
        
        ttk.Label(size_frame, text="최대 크기 (MB):").pack(anchor=tk.W)
        max_size_entry = ttk.Entry(size_frame, width=20)
        max_size_entry.pack(anchor=tk.W, pady=2)
        
        # 버튼들
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def apply_filters():
            # 기존 필터 제거
            self.filter_manager.clear_filters()
            
            # 확장자 필터 적용
            ext_text = ext_entry.get().strip()
            if ext_text:
                extensions = [ext.strip() for ext in ext_text.split(",")]
                self.filter_manager.add_filter(ExtensionFilter(extensions))
            
            # 크기 필터 적용
            try:
                min_kb = float(min_size_entry.get() or 0) * 1024
                max_mb = float(max_size_entry.get() or 0) * 1024 * 1024
                if min_kb > 0 or max_mb > 0:
                    self.filter_manager.add_filter(SizeFilter(int(min_kb), int(max_mb)))
            except ValueError:
                pass
            
            self.update_filter_status()
            dialog.destroy()
        
        ttk.Button(button_frame, text="적용", command=apply_filters).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="취소", command=dialog.destroy).pack(side=tk.RIGHT)
    
    def update_filter_status(self):
        """필터 상태 표시 업데이트"""
        summary = self.filter_manager.get_filter_summary()
        if len(summary) == 1 and summary[0] == "필터 없음":
            self.filter_status_var.set("필터 없음")
        else:
            self.filter_status_var.set(f"필터 {len(summary)}개 적용")
    
    def clear_filters(self):
        """모든 필터 제거"""
        self.filter_manager.clear_filters()
        self.update_filter_status()
        messagebox.showinfo("알림", "모든 필터가 제거되었습니다.")
    
    def execute_rename_with_history(self):
        """히스토리 추적이 포함된 파일명 변경"""
        if not self.engine.files:
            messagebox.showwarning("경고", "변경할 파일이 없습니다.")
            return
        
        # 필터 적용
        filtered_files = self.filter_manager.filter_files(self.engine.files)
        if not filtered_files:
            messagebox.showwarning("경고", "필터 조건에 맞는 파일이 없습니다.")
            return
        
        # 확인 대화상자
        result = messagebox.askyesno("확인", f"{len(filtered_files)}개 파일의 이름을 변경하시겠습니까?")
        if not result:
            return
        
        # 히스토리 세션 시작
        from datetime import datetime
        session_name = f"일괄 변경 {datetime.now().strftime('%H:%M')}"
        self.history.start_session(session_name)
        
        try:
            # 필터링된 파일들만 엔진에 설정
            original_files = self.engine.files.copy()
            self.engine.files = filtered_files
            
            # 실행
            results = self.engine.execute_rename()
            
            # 히스토리에 기록
            for old_path, new_path in results.get('renamed_files', []):
                self.history.add_action("rename", old_path, new_path, True)
            
            # 실패한 것들도 기록
            for error in results.get('errors', []):
                self.history.add_action("rename", "", "", False, error)
            
            # 결과 표시
            message = f"성공: {results['success']}개"
            if results['failed'] > 0:
                message += f", 실패: {results['failed']}개"
            messagebox.showinfo("완료", message)
            
        finally:
            # 원래 파일 목록 복원
            self.engine.files = original_files
            # 히스토리 세션 종료
            self.history.end_session()
    
    def show_history(self):
        """작업 기록 보기 창"""
        history_window = tk.Toplevel(self.root)
        history_window.title("작업 기록")
        history_window.geometry("600x400")
        
        # 히스토리 목록
        frame = ttk.Frame(history_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 리스트박스
        listbox = tk.Listbox(frame)
        listbox.pack(fill=tk.BOTH, expand=True)
        
        # 히스토리 로드
        summary = self.history.get_history_summary()
        for session in summary:
            timestamp = session["timestamp"][:16].replace("T", " ")  # 간단히 표시
            text = f"{timestamp} - {session['name']} ({session['successful_actions']}개 성공)"
            listbox.insert(tk.END, text)
        
        # 되돌리기 버튼
        def rollback_selected():
            selection = listbox.curselection()
            if selection:
                index = summary[selection[0]]["index"]
                result = messagebox.askyesno("확인", "선택한 작업을 되돌리시겠습니까?")
                if result:
                    rollback_result = self.history.rollback_session(index)
                    messagebox.showinfo("완료", f"되돌리기 완료: {rollback_result['success']}개 성공")
                    history_window.destroy()
        
        ttk.Button(frame, text="선택한 작업 되돌리기", 
                  command=rollback_selected).pack(pady=10)
    
    def rollback_last(self):
        """최근 작업 되돌리기"""
        summary = self.history.get_history_summary()
        if not summary:
            messagebox.showinfo("알림", "되돌릴 작업이 없습니다.")
            return
        
        result = messagebox.askyesno("확인", "최근 작업을 되돌리시겠습니까?")
        if result:
            rollback_result = self.history.rollback_session(summary[0]["index"])
            messagebox.showinfo("완료", f"되돌리기 완료: {rollback_result['success']}개 성공")
    
    def save_current_settings(self):
        """현재 설정 저장"""
        # GUI의 현재 설정들을 settings에 저장
        # (실제로는 각 입력 필드의 값들을 읽어서 저장)
        self.settings.save_settings()
        messagebox.showinfo("알림", "설정이 저장되었습니다.")
    
    def load_saved_settings(self):
        """저장된 설정 불러오기"""
        # 저장된 설정을 GUI에 적용
        # (실제로는 설정값들을 읽어서 각 입력 필드에 적용)
        pass
    
    def on_closing(self):
        """프로그램 종료시 처리"""
        # 현재 창 크기 저장
        self.settings.set("window.width", self.root.winfo_width())
        self.settings.set("window.height", self.root.winfo_height())
        self.save_current_settings()
        self.root.destroy()

if __name__ == "__main__":
    app = AdvancedRenamerGUI()
    app.root.mainloop()
```

## 🎯 완성된 고급 기능들

### 이제 우리 프로그램이 할 수 있는 것들

1. **똑똑한 필터링**: 원하는 파일들만 골라서 작업
2. **설정 기억하기**: 자주 쓰는 설정을 자동으로 저장/복원
3. **작업 추적하기**: 뭘 바꿨는지 기록하고 실수시 되돌리기
4. **사용자 친화적 UI**: 메뉴, 대화상자, 상태 표시 등

### 사용자 경험이 어떻게 개선되었나?

**Before (Chapter 5)**:
- 기본적인 파일명 변경만 가능
- 모든 파일에 대해 일괄 적용
- 실수하면 되돌릴 방법 없음
- 매번 설정을 다시 입력해야 함

**After (Chapter 6)**:
- 조건에 맞는 파일만 선택적으로 처리
- 실수해도 안전하게 되돌리기 가능
- 자주 쓰는 설정은 자동으로 기억
- 작업 기록을 통한 투명한 관리

## 📚 이번 챕터에서 배운 핵심 개념들

### 1. 필터 패턴
```python
# 조건을 만족하는 항목만 걸러내기
filtered_items = [item for item in items if condition(item)]
```

### 2. 설정 관리 패턴  
```python
# 점 표기법으로 중첩된 설정에 쉽게 접근
settings.get("ui.window.width", 800)
settings.set("ui.window.width", 1000)
```

### 3. 작업 추적 패턴
```python
# 작업을 세션 단위로 묶어서 관리
session = start_session("작업명")
add_action("rename", old, new, success)
end_session()
```

## 🎯 다음 단계 예고

다음 [Chapter 7](chapter7.md)에서는 프로그램을 완전히 완성하고 배포 준비를 해보겠습니다:

- **패키지 구조 정리**: 프로젝트를 깔끔하게 정리
- **테스트 코드 작성**: 버그 없는 안정적인 프로그램 만들기
- **문서화**: 사용자 가이드와 개발자 문서 작성
- **배포 준비**: 다른 사람들도 쉽게 설치할 수 있게 패키징

---

!!! success "Chapter 6 완료!"
    고급 기능들을 성공적으로 구현했습니다! 
    이제 정말 전문적인 파일 관리 도구가 되었네요.

!!! tip "연습 과제"
    - 날짜 필터 추가하기 (특정 날짜 이후에 수정된 파일만)
    - 설정 프리셋 기능 만들기 (자주 쓰는 설정 조합을 이름으로 저장)
    - 정규표현식 필터 추가하기
    - 다국어 지원 기능 추가하기
