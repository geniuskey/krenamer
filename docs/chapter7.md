# Chapter 7: 전문적인 모듈화 아키텍처

이번 챕터에서는 지금까지 학습한 내용을 바탕으로 **실무에서 사용할 수 있는 전문적인 모듈화 아키텍처**<!-- -->를 구현합니다. 단순히 동작하는 코드를 넘어서, **유지보수가 가능하고 확장 가능한 소프트웨어**<!-- -->를 만드는 방법을 배웁니다.

## 🎯 학습 목표

- **모듈화 설계 원칙** 이해와 적용
- **관심사의 분리(Separation of Concerns)** 실습
- **의존성 주입(Dependency Injection)** 패턴 구현
- **재사용 가능한 컴포넌트** 설계
- **확장 가능한 아키텍처** 구축

## 🏗️ 아키텍처 설계 철학

### 왜 모듈화가 중요한가?

지금까지의 Chapter들에서는 **하나의 파일에 모든 기능을 구현**<!-- -->했습니다. 이는 학습 목적으로는 좋지만, 실제 소프트웨어에서는 다음과 같은 문제가 발생합니다:

**🚨 문제점들:**

- **코드 복잡성 증가**: 파일이 커질수록 이해하기 어려움
- **유지보수 어려움**: 한 기능을 수정하면 다른 기능에 영향을 줄 수 있음
- **팀 작업 제약**: 여러 개발자가 동시에 작업하기 어려움
- **테스트 어려움**: 특정 기능만 독립적으로 테스트하기 어려움
- **재사용성 부족**: 다른 프로젝트에서 일부만 가져다 쓰기 어려움

### Chapter 7의 해결책: 체계적인 모듈화

```
src/chapter7/
├── main.py                    # 애플리케이션 진입점
├── __init__.py               # 패키지 선언
│
├── core/                     # 🧠 비즈니스 로직 계층
│   ├── __init__.py          
│   ├── engine.py            # 파일명 변경 엔진
│   └── conditions.py        # 조건 필터링 로직
│
├── gui/                      # 🎨 프레젠테이션 계층  
│   ├── __init__.py
│   ├── main_window.py       # 메인 창 조정자
│   ├── file_panel.py        # 파일 목록 관리 컴포넌트
│   ├── options_tabs.py      # 옵션 설정 컴포넌트
│   └── preview_panel.py     # 미리보기 컴포넌트
│
└── utils/                    # 🔧 공통 유틸리티 계층
    ├── __init__.py
    └── file_utils.py        # 파일 관련 헬퍼 함수들
```

## 🔍 모듈화 설계 원칙

### 1. 관심사의 분리 (Separation of Concerns)

각 모듈이 **하나의 명확한 책임**<!-- -->만을 가집니다:

#### 🧠 Core 계층: 비즈니스 로직
```python
# core/engine.py - 파일명 변경의 핵심 로직
class RenameEngine:
    """
    순수한 비즈니스 로직만 담당:
    - 파일명 생성 알고리즘
    - 변경 실행 로직  
    - 조건 적용
    
    GUI나 사용자 입력과는 완전히 독립적
    """
    
    def generate_new_name(self, file_path, index):
        """파일명 생성 알고리즘 - GUI와 무관한 순수 로직"""
        # 복잡한 파일명 변경 로직...
        return new_filename
```

#### 🎨 GUI 계층: 사용자 인터페이스
```python
# gui/file_panel.py - 파일 목록 UI만 담당
class FilePanel:
    """
    파일 목록 표시와 관리만 담당:
    - 리스트박스 위젯 관리
    - 파일 추가/제거 UI
    - 사용자 입력 처리
    
    파일명 변경 로직은 전혀 알지 못함
    """
    
    def add_files_dialog(self):
        """파일 선택 UI - 비즈니스 로직과 분리"""
        files = filedialog.askopenfilenames()
        # Engine에게 위임
        self.engine.add_files(files)
```

### 2. 단일 책임 원칙 (Single Responsibility Principle)

각 클래스는 **변경되어야 하는 이유가 하나**<!-- -->만 있어야 합니다:

```python
# ❌ 나쁜 예: 여러 책임을 가진 클래스
class BadRenamerClass:
    def show_file_list(self):      # UI 책임
        pass
    def rename_files(self):        # 비즈니스 로직 책임  
        pass
    def save_settings(self):       # 데이터 저장 책임
        pass

# ✅ 좋은 예: 책임이 분리된 클래스들
class FilePanel:           # UI만 담당
    def show_file_list(self): pass

class RenameEngine:        # 비즈니스 로직만 담당  
    def rename_files(self): pass

class SettingsManager:     # 데이터 저장만 담당
    def save_settings(self): pass
```

### 3. 의존성 주입 (Dependency Injection)

컴포넌트들이 **필요한 의존성을 외부에서 받아옵니다**:

```python
# gui/file_panel.py
class FilePanel:
    def __init__(self, parent, engine, variables, status_callback):
        """
        의존성을 외부에서 주입받음:
        - engine: 비즈니스 로직 처리용
        - variables: UI 상태 관리용  
        - status_callback: 상태 알림용
        """
        self.engine = engine              # 엔진을 주입받음
        self.variables = variables        # 변수들을 주입받음
        self.status_callback = status_callback  # 콜백을 주입받음
```

**장점:**

- **테스트 용이**: Mock 객체로 쉽게 대체 가능
- **유연성 증대**: 다른 엔진으로 쉽게 교체 가능
- **결합도 감소**: 각 컴포넌트가 독립적

## 📦 각 모듈의 역할과 설계

### Core 계층: 비즈니스 로직의 핵심

#### `core/engine.py` - 리네임 엔진
```python
class RenameEngine:
    """파일명 변경의 모든 비즈니스 로직을 담당하는 핵심 클래스"""
    
    def __init__(self):
        # 설정 상태 관리
        self.method = "prefix"
        self.prefix_text = ""
        # ... 기타 설정들
        
        # 의존성: 조건 검사기 주입
        self.condition_checker = FileConditionChecker()
    
    def generate_new_name(self, file_path, index):
        """
        파일명 생성 알고리즘:
        1. 기본 변경 (접두사, 접미사, 순번 등)
        2. 패턴 기반 변경 (정규식)
        3. 일괄 변환 (대소문자, 특수문자 처리)
        """
        original_name = os.path.basename(file_path)
        name, ext = os.path.splitext(original_name)
        
        # 기본 리네임 방식 적용
        if self.method == "prefix":
            new_name = f"{self.prefix_text}{name}"
        elif self.method == "suffix":
            new_name = f"{name}{self.suffix_text}"
        # ... 기타 방식들
        
        # 일괄 변환 적용
        new_name = self.apply_transformations(new_name)
        
        return new_name + ext
    
    def generate_rename_plan(self):
        """
        실행 전 미리보기 생성:
        - 조건 필터링 적용
        - 각 파일의 변경 결과 계산
        - 충돌 검사
        """
        plan = []
        for index, file_path in enumerate(self.files):
            if self.matches_conditions(file_path):
                new_name = self.generate_new_name(file_path, index)
                plan.append((os.path.basename(file_path), new_name, True))
        return plan
```

#### `core/conditions.py` - 조건 필터링
```python
class FileConditionChecker:
    """파일 필터링 조건을 검사하는 전문 클래스"""
    
    def matches_conditions(self, file_path):
        """
        다중 조건 검사:
        - 파일 크기 조건
        - 수정 날짜 조건  
        - 확장자 조건
        
        모든 조건을 만족해야 True 반환
        """
        if self.use_size_condition:
            if not self._check_size_condition(file_path):
                return False
        
        if self.use_date_condition:
            if not self._check_date_condition(file_path):
                return False
                
        return True
```

### GUI 계층: 사용자 인터페이스 컴포넌트

#### `gui/main_window.py` - 메인 창 조정자
```python
class RenamerGUI:
    """
    메인 창의 역할:
    - 전체 레이아웃 관리
    - 컴포넌트들 간의 상호작용 조정
    - 이벤트 바인딩
    - 전체 상태 관리
    """
    
    def __init__(self):
        # 1. 엔진 생성
        self.engine = RenameEngine()
        
        # 2. UI 변수들 초기화
        self.setup_variables()
        
        # 3. GUI 컴포넌트들 생성 및 조합
        self.setup_widgets()
    
    def setup_widgets(self):
        """컴포넌트 조합 - 의존성 주입 패턴"""
        # 파일 패널 생성 (의존성 주입)
        self.file_panel = FilePanel(
            parent=left_frame,
            engine=self.engine,           # 엔진 주입
            variables=self.get_file_variables(),  # 변수들 주입
            status_callback=self.update_status    # 콜백 주입
        )
        
        # 옵션 탭들 생성
        self.options_tabs = OptionsTabs(
            parent=center_frame,
            variables=self.get_option_variables(),
            update_callback=self.update_preview
        )
```

#### `gui/file_panel.py` - 파일 관리 컴포넌트
```python
class FilePanel:
    """
    파일 목록 관리 전담 컴포넌트:
    - 독립적으로 재사용 가능
    - 명확한 인터페이스
    - 단일 책임
    """
    
    def __init__(self, parent, engine, variables, status_callback):
        """의존성 주입을 통한 느슨한 결합"""
        self.engine = engine                    # 비즈니스 로직
        self.variables = variables              # UI 상태
        self.status_callback = status_callback  # 외부 통신
    
    def add_files(self, file_paths):
        """
        파일 추가 처리:
        1. UI 업데이트
        2. 엔진에 데이터 전달
        3. 상태 알림
        """
        # 엔진에게 비즈니스 로직 위임
        added_count = self.engine.add_files(file_paths)
        
        # UI 업데이트
        self.refresh_file_list()
        
        # 상태 알림 (의존성 주입된 콜백 사용)
        if self.status_callback:
            self.status_callback(f"{added_count}개 파일 추가됨")
```

#### `gui/options_tabs.py` - 옵션 설정 컴포넌트
```python
class OptionsTabs:
    """
    탭별 옵션 설정 관리:
    - 기본 변경 탭
    - 패턴 기반 탭  
    - 조건부 필터링 탭
    - 일괄 작업 탭
    """
    
    def setup_basic_tab(self):
        """기본 변경 탭 - 동적 UI 필드 관리"""
        # 라디오 버튼으로 방식 선택
        ttk.Radiobutton(method_frame, text="접두사", 
                       variable=self.basic_method, value="prefix",
                       command=self.update_basic_fields).pack(side=tk.LEFT)
        
        # 동적으로 표시/숨김 처리되는 입력 필드들
        self.basic_widgets['text_entry'] = ttk.Entry(...)
        self.basic_widgets['number_entry'] = ttk.Entry(...)
        
    def update_basic_fields(self):
        """선택된 방식에 따라 관련 필드만 표시"""
        method = self.basic_method.get()
        
        # 모든 필드 숨기기
        for widget in self.basic_widgets.values():
            widget.grid_remove()
        
        # 선택된 방식에 맞는 필드만 표시
        if method == "prefix":
            self.basic_widgets['text_entry'].grid(...)
```

### Utils 계층: 공통 유틸리티

#### `utils/file_utils.py` - 파일 관련 헬퍼
```python
def format_file_size(size_bytes):
    """파일 크기를 읽기 쉬운 형태로 포맷"""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    # ... 더 큰 단위들

def convert_size_to_bytes(size_value, size_unit):
    """크기 값과 단위를 바이트로 변환"""
    if size_unit == "KB":
        return size_value * 1024
    elif size_unit == "MB":
        return size_value * 1024 * 1024
    # ... 더 큰 단위들
```

## 🔄 컴포넌트 간 상호작용 패턴

### 데이터 흐름 (Data Flow)

```
1. 사용자 입력 → FilePanel
2. FilePanel → RenameEngine (비즈니스 로직)
3. RenameEngine → PreviewPanel (결과 표시)
4. 옵션 변경 → OptionsTabs → RenameEngine
5. RenameEngine → 모든 GUI 컴포넌트 (상태 동기화)
```

### 이벤트 전파 패턴

```python
# main_window.py - 이벤트 중앙 집중 관리
def setup_bindings(self):
    """이벤트 바인딩 - 컴포넌트 간 통신"""
    
    # 변수 변경 시 미리보기 자동 업데이트
    self.basic_text.trace_add('write', self.on_option_changed)
    self.basic_method.trace_add('write', self.on_option_changed)
    
def on_option_changed(self, *args):
    """옵션 변경 시 엔진 동기화 및 미리보기 업데이트"""
    # 1. GUI → Engine 데이터 동기화
    self.sync_engine_settings()
    
    # 2. 미리보기 업데이트
    self.preview_panel.update_preview()

def sync_engine_settings(self):
    """GUI 설정을 엔진에 동기화"""
    self.engine.method = self.basic_method.get()
    self.engine.prefix_text = self.basic_text.get()
    # ... 기타 설정들
```

## 🧪 모듈화의 장점 실증

### 1. 독립적 테스트 가능

```python
# 엔진만 독립적으로 테스트
def test_rename_engine():
    engine = RenameEngine()
    engine.method = "prefix"
    engine.prefix_text = "new_"
    
    result = engine.generate_new_name("test.txt", 0)
    assert result == "new_test.txt"

# GUI 컴포넌트도 독립적으로 테스트  
def test_file_panel():
    mock_engine = MockRenameEngine()
    panel = FilePanel(parent, mock_engine, variables, callback)
    # ... 테스트 코드
```

### 2. 쉬운 확장성

**새로운 리네임 방식 추가:**
```python
# engine.py만 수정하면 됨
def generate_new_name(self, file_path, index):
    # 기존 코드...
    elif self.method == "random":  # 새 방식 추가
        new_name = f"{random.randint(1000, 9999)}_{name}"
```

**새로운 UI 컴포넌트 추가:**
```python
# 새로운 패널 클래스 생성
class AdvancedOptionsPanel:
    def __init__(self, parent, engine, variables):
        # ... 독립적인 새 패널
```

### 3. 팀 협업 용이성

```
개발자 A: core/ 모듈 담당 (백엔드 로직)
개발자 B: gui/ 모듈 담당 (프론트엔드)  
개발자 C: utils/ 모듈 담당 (공통 기능)

→ 각자 독립적으로 작업 가능
→ 명확한 인터페이스를 통해 통합
```

## 🚀 실행 및 동작 확인

### 기본 실행
```bash
cd src/chapter7
python main.py
```

### 구조 탐색
```python
# 각 모듈을 개별적으로 사용 가능
from chapter7.core import RenameEngine
from chapter7.gui import FilePanel

# 엔진을 독립적으로 사용
engine = RenameEngine()
engine.add_files(["test1.txt", "test2.txt"])
plan = engine.generate_rename_plan()
```

## 📊 아키텍처 비교: Before vs After

### 이전 (모노리식)
```
❌ 문제점:
- 한 파일에 모든 기능 (500+ 라인)
- GUI와 로직이 섞임
- 특정 기능만 테스트하기 어려움  
- 코드 재사용 불가
- 팀 작업 시 충돌 위험
```

### Chapter 7 (모듈화)
```
✅ 개선점:
- 기능별 독립 모듈 (각 100라인 내외)
- GUI와 로직 완전 분리
- 각 모듈별 독립 테스트 가능
- 컴포넌트 재사용 가능
- 병렬 개발 가능
- 확장 용이
```

## 🎯 실습 과제

### 기본 과제

1. **모듈 이해하기**: 각 모듈의 역할과 상호작용 파악
2. **의존성 추적하기**: 어떤 컴포넌트가 어떤 의존성을 가지는지 분석
3. **새 기능 추가하기**: 모듈 구조를 깨뜨리지 않고 새 기능 추가

### 심화 과제

1. **새로운 GUI 패널 작성**: 기존 패턴을 따라 새로운 설정 패널 구현
2. **새로운 엔진 기능**: 정규식 기반 고급 리네임 기능 추가
3. **설정 저장 모듈**: 사용자 설정을 파일에 저장/로드하는 모듈 추가

## 🏆 Chapter 7에서 배운 핵심 가치

### 1. **소프트웨어 아키텍처 사고방식**

- 코드를 "작성"하는 것에서 "설계"하는 것으로 발전
- 미래의 변경과 확장을 고려한 구조

### 2. **전문적인 개발 실무 경험**  

- 실제 소프트웨어 회사에서 사용하는 모듈화 패턴
- 유지보수와 협업을 고려한 코드 구조

### 3. **확장 가능한 사고**

- "완성"이 아닌 "진화 가능한" 소프트웨어 설계
- 새로운 요구사항에 유연하게 대응할 수 있는 구조

---

!!! success "Chapter 7 완료!"
    축하합니다! 전문적인 모듈화 아키텍처를 성공적으로 구현했습니다!
    
    **달성한 것들:**

    - ✅ 체계적인 관심사 분리
    - ✅ 재사용 가능한 컴포넌트 설계
    - ✅ 확장 가능한 아키텍처 구축
    - ✅ 전문적인 소프트웨어 개발 경험
    - ✅ 실무에서 통용되는 설계 패턴 습득


!!! note "실무 활용"
    Chapter 7의 모듈화 패턴은 실제 소프트웨어 개발 현장에서 널리 사용됩니다. 
    이 경험을 바탕으로 더 복잡한 애플리케이션도 체계적으로 설계할 수 있습니다.