# Chapter 9: MkDocs 적용하기

이번 챕터에서는 KRenamer 프로젝트에 MkDocs를 적용하여 전문적인 문서화 시스템을 구축하는 방법을 학습합니다. 현대적이고 사용자 친화적인 문서 사이트를 만들어 프로젝트의 완성도를 한층 높여보겠습니다.

## 🎯 학습 목표

- **MkDocs 설치**<!-- -->와 기본 설정
- **문서 구조 설계**<!-- -->와 네비게이션 구성
- **Material 테마** 적용과 커스터마이징
- **GitHub Pages** 배포 자동화
- **문서 최적화**<!-- -->와 SEO 적용

## 📚 MkDocs 개요

### MkDocs란?

MkDocs는 Markdown 문서를 정적 웹사이트로 변환해주는 파이썬 기반 도구입니다. 특히 프로젝트 문서화에 특화되어 있으며, 간단한 설정으로 전문적인 문서 사이트를 만들 수 있습니다.

!!! info "MkDocs의 장점"
    - **Markdown 기반**: 작성이 쉽고 Git과 호환성 우수
    - **라이브 리로드**: 개발 중 실시간 미리보기
    - **테마 지원**: Material for MkDocs 등 다양한 테마
    - **플러그인 생태계**: 검색, 코드 하이라이팅 등
    - **GitHub Pages 호환**: 자동 배포 지원

## 🚀 MkDocs 설정

### 1. 설치 및 초기 설정

````bash title="MkDocs 설치"
# MkDocs와 Material 테마 설치
pip install mkdocs mkdocs-material

# 플러그인 추가 설치
pip install mkdocs-macros-plugin mkdocs-glightbox
````

````bash title="프로젝트 초기화"
# 프로젝트 루트에서 실행
mkdocs new .

# 기본 구조 확인
tree docs/
````

### 2. mkdocs.yml 기본 설정

````yaml title="mkdocs.yml"
site_name: KRenamer Documentation
site_description: Korean Windows GUI file renaming tool documentation
site_author: KRenamer Team
site_url: https://geniuskey.github.io/krenamer

# Repository
repo_name: geniuskey/krenamer
repo_url: https://github.com/geniuskey/krenamer
edit_uri: edit/main/docs/

# Theme
theme:
  name: material
  language: ko
  palette:
    # Palette toggle for light mode
    - scheme: default
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
      primary: blue
      accent: blue
    # Palette toggle for dark mode
    - scheme: slate
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
      primary: blue
      accent: blue
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.path
    - navigation.top
    - search.highlight
    - search.share
    - content.code.copy
    - content.action.edit

# Navigation
nav:
  - Home: index.md
  - 시작하기:
    - 개요: overview.md
    - 설치 및 실행: installation.md
    - 기본 사용법: basic-usage.md
  - 튜토리얼:
    - Chapter 1 - Python 기초: chapter1.md
    - Chapter 2 - 기본 GUI 구조: chapter2.md
    - Chapter 3 - 드래그 앤 드롭: chapter3.md
    - Chapter 4 - 파일명 변경 로직: chapter4.md
    - Chapter 5 - 고급 조건과 기능: chapter5.md
    - Chapter 6 - 모듈화하기: chapter6.md
    - Chapter 7 - 단위 테스트: chapter7.md
    - Chapter 8 - MkDocs 적용: chapter8.md
    - Chapter 9 - GitHub Actions: chapter9.md
    - Chapter 10 - PyPI 배포: chapter10.md
    - Chapter 11 - PyInstaller: chapter11.md
  - API 문서:
    - 핵심 클래스: api/core.md
    - GUI 컴포넌트: api/gui.md
    - 유틸리티: api/utils.md

# Plugins
plugins:
  - search:
      lang: ko
  - macros
  - glightbox

# Extensions
markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.tabbed:
      alternate_style: true
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true

# Extra
extra:
  version:
    provider: mike
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/geniuskey/krenamer
    - icon: fontawesome/brands/python
      link: https://pypi.org/project/krenamer/

extra_css:
  - stylesheets/extra.css

extra_javascript:
  - javascripts/extra.js
````

### 3. 문서 구조 설계

````bash title="문서 디렉토리 구조"
docs/
├── index.md                 # 홈페이지
├── overview.md             # 프로젝트 개요
├── installation.md         # 설치 가이드
├── basic-usage.md          # 기본 사용법
├── chapter1.md             # 튜토리얼 챕터들
├── chapter2.md
├── ...
├── api/                    # API 문서
│   ├── core.md
│   ├── gui.md
│   └── utils.md
├── assets/                 # 이미지, 동영상 등
│   ├── images/
│   └── videos/
├── stylesheets/            # 커스텀 CSS
│   └── extra.css
└── javascripts/            # 커스텀 JS
    └── extra.js
````

## 📝 핵심 문서 작성

### 1. 홈페이지 (index.md)

````markdown title="docs/index.md"
# KRenamer

**Korean Windows GUI file renaming tool**

KRenamer는 윈도우 환경에서 파일명을 일괄적으로 변경할 수 있는 한국어 GUI 도구입니다. 드래그 앤 드롭 기능과 다양한 리네임 옵션을 지원하여 효율적인 파일 관리가 가능합니다.

## ✨ 주요 기능

=== "🎯 직관적 GUI"
    - 드래그 앤 드롭으로 파일 추가
    - 실시간 미리보기
    - 한국어 인터페이스

=== "🔧 다양한 리네임 방식"
    - 접두사/접미사 추가
    - 순번 매기기
    - 찾기/바꾸기
    - 정규표현식 지원

=== "🎛️ 고급 기능"
    - 조건부 필터링
    - 파일 크기별 처리
    - 확장자별 분류
    - 되돌리기 기능

## 🚀 빠른 시작

### 설치

```bash
pip install renamer
```

### 실행

```bash
# 명령어로 실행
renamer

# 또는 Python 모듈로 실행
python -m krenamer.main
```

### 기본 사용법

1. **파일 추가**: 파일을 드래그 앤 드롭하거나 '파일 추가' 버튼 클릭
2. **옵션 설정**: 접두사, 접미사, 순번 등 원하는 옵션 설정
3. **미리보기**: 변경될 파일명을 실시간으로 확인
4. **실행**: '이름 바꾸기' 버튼으로 일괄 변경

!!! tip "팁"
    정규표현식을 활용하면 복잡한 패턴의 파일명도 쉽게 변경할 수 있습니다!

## 📚 학습 가이드

KRenamer는 단순한 도구를 넘어 Python GUI 프로그래밍을 학습할 수 있는 교육 프로젝트입니다.

### 튜토리얼 시리즈

| 챕터                         | 주제             | 난이도 |
|----------------------------|----------------|--------|
| [Chapter 1](chapter1.md)   | Python 기초      | ⭐ |
| [Chapter 2](chapter2.md)   | Tkinter 기초     | ⭐⭐ |
| [Chapter 3](chapter3.md)   | 기본 GUI 구조      | ⭐⭐ |
| [Chapter 4](chapter4.md)   | 드래그 앤 드롭       | ⭐⭐ |
| [Chapter 5](chapter5.md)   | 파일명 변경 로직      | ⭐⭐⭐ |
| [Chapter 6](chapter6.md)   | 고급 조건과 기능      | ⭐⭐⭐ |
| [Chapter 7](chapter7.md)   | 모듈화하기          | ⭐⭐⭐⭐ |
| [Chapter 8](chapter8.md)   | 단위 테스트         | ⭐⭐⭐⭐ |
| [Chapter 9](chapter9.md)   | MkDocs 적용      | ⭐⭐⭐ |
| [Chapter 10](chapter10.md) | GitHub Actions | ⭐⭐⭐⭐ |
| [Chapter 11](chapter11.md) | PyPI 배포        | ⭐⭐⭐⭐ |
| [Chapter 12](chapter12.md) | PyInstaller    | ⭐⭐⭐ |

## 🛠️ 개발 정보

### 기술 스택

- **언어**: Python 3.8+
- **GUI**: tkinter
- **드래그 앤 드롭**: tkinterdnd2
- **패키징**: setuptools
- **테스트**: pytest
- **문서**: MkDocs

### 프로젝트 구조

```
src/
├── krenamer/
│   ├── core.py      # 파일 처리 엔진
│   ├── gui.py       # GUI 컴포넌트
│   └── main.py      # 메인 실행 파일
├── krenamer-ch1/    # 교육용 챕터별 코드
├── krenamer-ch2/
└── ...
```

## 🤝 기여하기

KRenamer는 오픈소스 프로젝트입니다. 기여를 환영합니다!

- [이슈 리포트](https://github.com/geniuskey/krenamer/issues)
- [기능 제안](https://github.com/geniuskey/krenamer/discussions)
- [풀 리퀘스트](https://github.com/geniuskey/krenamer/pulls)

자세한 내용은 [기여 가이드](contributing.md)를 참조하세요.

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE.md) 파일을 참조하세요.
````

### 2. 설치 가이드 (installation.md)

````markdown title="docs/installation.md"
# 설치 및 실행

KRenamer를 설치하고 실행하는 다양한 방법을 안내합니다.

## 📦 설치 방법

### 방법 1: PyPI에서 설치 (권장)

```bash
pip install renamer
```

### 방법 2: GitHub에서 직접 설치

```bash
# 최신 개발 버전
pip install git+https://github.com/geniuskey/krenamer.git

# 특정 릴리스 버전
pip install git+https://github.com/geniuskey/krenamer.git@v1.0.0
```

### 방법 3: 소스 코드에서 설치

```bash
# 저장소 클론
git clone https://github.com/geniuskey/krenamer.git
cd renamer

# 개발 모드로 설치
pip install -e .
```

## 🔧 의존성

### 필수 의존성

- **Python 3.8+**
- **tkinter** (Python 표준 라이브러리)

### 선택적 의존성

- **tkinterdnd2** (드래그 앤 드롭 기능)

```bash
pip install tkinterdnd2
```

!!! note "tkinterdnd2 없이도 실행 가능"
    tkinterdnd2가 설치되지 않은 경우에도 KRenamer는 정상 동작하며, 
    파일 추가 버튼을 통해 파일을 선택할 수 있습니다.

## 🚀 실행 방법

### GUI 모드 실행

```bash
# 명령어로 실행
renamer

# 또는 Python 모듈로 실행
python -m krenamer.main
```

### 특정 챕터 실행

```bash
# Chapter 1 (Python 기초)
cd src/krenamer-ch1
python main.py

# Chapter 2 (기본 GUI)
cd src/krenamer-ch2
python main.py
```

## 🎯 설치 확인

설치가 제대로 되었는지 확인하는 방법:

```python
# Python에서 확인
import krenamer
print(krenamer.__version__)

# 또는 명령어로 확인
python -c "import krenamer; print(krenamer.__version__)"
```

## 🐛 문제 해결

### 일반적인 문제들

#### 1. tkinterdnd2 설치 실패

```bash
# Windows에서 Visual C++ 빌드 도구 필요
# Microsoft C++ Build Tools 설치 후 재시도
pip install tkinterdnd2
```

#### 2. Python 버전 호환성

```bash
# Python 버전 확인
python --version

# 3.8 이상이어야 함
```

#### 3. 한글 폰트 문제

KRenamer는 "맑은 고딕" 폰트를 사용합니다. 윈도우에서는 기본 제공되지만, 
다른 OS에서는 대체 폰트가 사용될 수 있습니다.

#### 4. 실행 권한 문제

```bash
# Linux/macOS에서 실행 권한 추가
chmod +x src/krenamer/main.py
```

## 🔄 업데이트

### PyPI 버전 업데이트

```bash
pip install --upgrade renamer
```

### 개발 버전 업데이트

```bash
cd renamer
git pull origin main
pip install -e .
```

## 🗑️ 제거

```bash
pip uninstall renamer
```

!!! warning "설정 파일"
    제거 시 사용자 설정 파일은 자동으로 삭제되지 않습니다.
    필요하다면 `~/.krenamer/` 디렉토리를 수동으로 삭제하세요.
````

### 3. API 문서 (api/core.md)

````markdown title="docs/api/core.md"
# Core API

KRenamer의 핵심 파일 처리 엔진인 `RenameEngine` 클래스의 API 문서입니다.

## RenameEngine

::: krenamer.core.RenameEngine
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

파일 리네임 작업을 담당하는 핵심 클래스입니다.

### 주요 특징

- 다양한 리네임 방식 지원
- 조건부 필터링
- 안전한 파일 처리
- 미리보기 기능

### 사용 예시

```python
from krenamer.core import RenameEngine

# 엔진 초기화
engine = RenameEngine()

# 파일 추가
engine.add_file("/path/to/file1.txt")
engine.add_file("/path/to/file2.jpg")

# 접두사 설정
engine.prefix = "NEW_"

# 리네임 계획 생성
plan = engine.generate_rename_plan()

# 실행
result = engine.execute_rename()
```

## 메서드 상세

### add_file()

```python
def add_file(self, file_path: str) -> bool:
    """파일을 리네임 대상 목록에 추가
    
    Args:
        file_path: 추가할 파일의 경로
        
    Returns:
        bool: 추가 성공 여부
        
    Raises:
        FileNotFoundError: 파일이 존재하지 않는 경우
    """
```

### remove_file()

```python
def remove_file(self, file_path: str) -> bool:
    """파일을 리네임 대상 목록에서 제거
    
    Args:
        file_path: 제거할 파일의 경로
        
    Returns:
        bool: 제거 성공 여부
    """
```

### generate_rename_plan()

```python
def generate_rename_plan(self) -> List[Tuple[str, str]]:
    """현재 설정에 따른 리네임 계획 생성
    
    Returns:
        List[Tuple[str, str]]: (원본 경로, 새 경로) 튜플의 리스트
    """
```

### execute_rename()

```python
def execute_rename(self) -> Dict[str, Any]:
    """리네임 실행
    
    Returns:
        Dict[str, Any]: 실행 결과
        {
            'success': int,     # 성공한 파일 수
            'failed': int,      # 실패한 파일 수
            'errors': List[str] # 오류 메시지 목록
        }
    """
```

## 설정 속성

### 기본 리네임 옵션

| 속성 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `prefix` | str | "" | 접두사 |
| `suffix` | str | "" | 접미사 |
| `find_text` | str | "" | 찾을 텍스트 |
| `replace_text` | str | "" | 바꿀 텍스트 |
| `use_regex` | bool | False | 정규표현식 사용 |

### 순번 매기기 옵션

| 속성 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `numbering_enabled` | bool | False | 순번 매기기 활성화 |
| `numbering_start` | int | 1 | 시작 번호 |
| `numbering_digits` | int | 3 | 자릿수 |
| `numbering_position` | str | "prefix" | 위치 (prefix/suffix) |

### 필터 조건

| 속성 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `filter_by_size` | bool | False | 크기로 필터링 |
| `min_size` | int | 0 | 최소 크기 (bytes) |
| `max_size` | int | 0 | 최대 크기 (bytes) |
| `filter_by_extension` | bool | False | 확장자로 필터링 |
| `allowed_extensions` | List[str] | [] | 허용 확장자 목록 |

## 예외 처리

### FileProcessingError

```python
class FileProcessingError(Exception):
    """파일 처리 중 발생하는 오류"""
    pass
```

### RenameConflictError

```python
class RenameConflictError(Exception):
    """파일명 충돌로 인한 오류"""
    pass
```

## 이벤트 콜백

### 진행률 콜백

```python
def set_progress_callback(self, callback: Callable[[int, int], None]):
    """진행률 콜백 설정
    
    Args:
        callback: (current, total) -> None 형태의 콜백 함수
    """
```

### 오류 콜백

```python
def set_error_callback(self, callback: Callable[[str, str], None]):
    """오류 콜백 설정
    
    Args:
        callback: (file_path, error_message) -> None 형태의 콜백 함수
    """
```

## 성능 최적화

### 대용량 파일 처리

```python
# 배치 처리 설정
engine.batch_size = 100  # 한 번에 처리할 파일 수

# 멀티스레딩 활성화
engine.use_threading = True
engine.max_workers = 4
```

### 메모리 사용량 최적화

```python
# 파일 정보 캐싱 비활성화 (메모리 절약)
engine.cache_file_info = False

# 대용량 파일 스트리밍 처리
engine.streaming_mode = True
```
```

## 🎨 테마 커스터마이징

### 1. 커스텀 CSS

```css title="docs/stylesheets/extra.css"
/* 한국어 폰트 최적화 */
.md-typeset {
  font-family: "Noto Sans KR", "Malgun Gothic", "맑은 고딕", sans-serif;
}

/* 코드 블록 스타일링 */
.md-typeset .highlight {
  border-radius: 8px;
  border: 1px solid var(--md-code-bg-color);
}

/* 커스텀 색상 */
:root {
  --md-primary-fg-color: #1976d2;
  --md-accent-fg-color: #2196f3;
}

/* 홈페이지 히어로 섹션 */
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 2rem;
  margin: -2rem -2rem 2rem -2rem;
  text-align: center;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.hero p {
  font-size: 1.2rem;
  opacity: 0.9;
}

/* 기능 카드 스타일 */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.feature-card {
  background: var(--md-code-bg-color);
  padding: 2rem;
  border-radius: 8px;
  border: 1px solid var(--md-default-fg-color--lightest);
}

.feature-card h3 {
  color: var(--md-primary-fg-color);
  margin-bottom: 1rem;
}

/* 반응형 테이블 */
.md-typeset table {
  font-size: 0.9rem;
}

@media screen and (max-width: 768px) {
  .md-typeset table {
    font-size: 0.8rem;
  }
}
````

### 2. 커스텀 JavaScript

````javascript title="docs/javascripts/extra.js"
// 다크 모드 토글 개선
document.addEventListener('DOMContentLoaded', function() {
  // 시스템 다크 모드 감지
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
  
  function updateTheme(e) {
    if (e.matches) {
      document.body.setAttribute('data-md-color-scheme', 'slate');
    } else {
      document.body.setAttribute('data-md-color-scheme', 'default');
    }
  }
  
  prefersDark.addListener(updateTheme);
  updateTheme(prefersDark);
});

// 코드 복사 기능 강화
document.addEventListener('DOMContentLoaded', function() {
  const codeBlocks = document.querySelectorAll('pre code');
  
  codeBlocks.forEach(function(block) {
    const button = document.createElement('button');
    button.className = 'copy-button';
    button.textContent = '복사';
    button.addEventListener('click', function() {
      navigator.clipboard.writeText(block.textContent).then(function() {
        button.textContent = '복사됨!';
        setTimeout(function() {
          button.textContent = '복사';
        }, 2000);
      });
    });
    
    block.parentNode.insertBefore(button, block.nextSibling);
  });
});

// 진행률 표시
function updateProgress() {
  const chapters = document.querySelectorAll('[data-chapter]');
  const completed = document.querySelectorAll('[data-chapter][data-completed="true"]');
  const progress = (completed.length / chapters.length) * 100;
  
  const progressBar = document.querySelector('.progress-bar');
  if (progressBar) {
    progressBar.style.width = progress + '%';
  }
}

// 검색 결과 하이라이팅
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.querySelector('.md-search__input');
  if (searchInput) {
    searchInput.addEventListener('input', function() {
      const query = this.value.toLowerCase();
      const results = document.querySelectorAll('.md-search-result');
      
      results.forEach(function(result) {
        const text = result.textContent.toLowerCase();
        if (text.includes(query)) {
          result.style.display = 'block';
        } else {
          result.style.display = 'none';
        }
      });
    });
  }
});
````

## 🚀 배포 설정

### 1. GitHub Pages 자동 배포

````yaml title=".github/workflows/docs.yml"
name: Deploy Documentation

on:
  push:
    branches: [ main ]
    paths: [ 'docs/**', 'mkdocs.yml' ]
  pull_request:
    branches: [ main ]
    paths: [ 'docs/**', 'mkdocs.yml' ]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v4
      
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        pip install mkdocs mkdocs-material
        pip install mkdocs-macros-plugin mkdocs-glightbox
        
    - name: Build documentation
      run: mkdocs build --clean --strict
      
    - name: Setup Pages
      uses: actions/configure-pages@v3
      
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v2
      with:
        path: ./site

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v2
````

### 2. 다중 버전 배포 (Mike)

````bash title="다중 버전 관리"
# Mike 설치
pip install mike

# 버전 배포
mike deploy --push --update-aliases 1.0 latest
mike deploy --push 1.1
mike deploy --push 2.0 latest

# 기본 버전 설정
mike set-default --push latest

# 버전 목록 확인
mike list
````

## 📊 분석 및 최적화

### 1. Google Analytics 연동

````yaml title="mkdocs.yml (추가)"
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
````

### 2. SEO 최적화

````yaml title="mkdocs.yml (추가)"
plugins:
  - meta
  - sitemap:
      use_directory_urls: false

extra:
  seo:
    title: "KRenamer - Korean File Renaming Tool"
    description: "Korean Windows GUI file renaming tool with drag & drop support"
    keywords: "file rename, korean gui, windows tool, python"
    author: "KRenamer Team"
    og_image: "assets/images/krenamer-og.png"
````

### 3. 검색 최적화

````yaml title="mkdocs.yml (추가)"
plugins:
  - search:
      lang: 
        - ko
        - en
      separator: '[\s\-\.]+'
      min_search_length: 2
      prebuild_index: true
````

## 🧪 문서 테스트

### 1. 링크 검증

````bash title="링크 체크 스크립트"
#!/bin/bash
# check_docs.sh

# 문서 빌드
mkdocs build --clean

# 링크 검증 (linkchecker 사용)
pip install linkchecker
linkchecker site/

# 맞춤법 검사 (hunspell 사용)
find docs/ -name "*.md" -exec hunspell -l -d ko_KR {} \;
````

### 2. 자동화된 문서 테스트

````python title="tests/test_docs.py"
import os
import re
from pathlib import Path
import pytest
from mkdocs.config import load_config
from mkdocs.commands.build import build

def test_mkdocs_config():
    """MkDocs 설정 파일 유효성 검사"""
    config = load_config('mkdocs.yml')
    assert config['site_name'] == 'KRenamer Documentation'
    assert 'material' in config['theme']['name']

def test_all_markdown_files_exist():
    """네비게이션에 명시된 모든 마크다운 파일 존재 확인"""
    config = load_config('mkdocs.yml')
    docs_dir = Path(config['docs_dir'])
    
    for nav_item in config['nav']:
        if isinstance(nav_item, dict):
            for key, value in nav_item.items():
                if isinstance(value, str) and value.endswith('.md'):
                    file_path = docs_dir / value
                    assert file_path.exists(), f"Missing file: {value}"

def test_internal_links():
    """내부 링크 유효성 검사"""
    docs_dir = Path('docs')
    for md_file in docs_dir.rglob('*.md'):
        content = md_file.read_text(encoding='utf-8')
        
        # 마크다운 링크 패턴 찾기
        links = re.findall(r'\[.*?\]\((.*?)\)', content)
        
        for link in links:
            if link.startswith(('http', 'https', 'mailto')):
                continue  # 외부 링크는 스킵
                
            # 상대 경로 링크 검증
            if link.endswith('.md'):
                link_path = (md_file.parent / link).resolve()
                assert link_path.exists(), f"Broken link in {md_file}: {link}"

def test_code_blocks_syntax():
    """코드 블록 문법 유효성 검사"""
    docs_dir = Path('docs')
    for md_file in docs_dir.rglob('*.md'):
        content = md_file.read_text(encoding='utf-8')
        
        # 코드 블록 패턴 찾기
        code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', content, re.DOTALL)
        
        for lang, code in code_blocks:
            if lang == 'python':
                # Python 코드 문법 검사
                try:
                    compile(code, f'<{md_file}>', 'exec')
                except SyntaxError as e:
                    pytest.fail(f"Python syntax error in {md_file}: {e}")

def test_docs_build():
    """문서 빌드 테스트"""
    config = load_config('mkdocs.yml')
    build(config)
    
    # 생성된 HTML 파일 확인
    site_dir = Path(config['site_dir'])
    assert (site_dir / 'index.html').exists()
    assert (site_dir / 'sitemap.xml').exists()
````

## 🎯 베스트 프랙티스

### 1. 문서 작성 가이드라인

!!! tip "효과적인 문서 작성"
    - **명확한 제목**: 내용을 정확히 반영하는 제목 사용
    - **단계별 설명**: 복잡한 과정은 단계별로 나누어 설명
    - **실행 가능한 예제**: 모든 코드 예제는 실제로 동작해야 함
    - **스크린샷 활용**: GUI 관련 내용은 스크린샷 포함
    - **다국어 고려**: 한국어와 영어 사용자 모두 고려

### 2. 콘텐츠 구조화

````markdown
# 표준 문서 구조 템플릿

## 🎯 학습 목표
- 명확한 학습 목표 제시

## 📚 개념 설명
- 핵심 개념의 이론적 배경

## 🚀 실습
- 단계별 실습 과정

## 💡 핵심 정리
- 주요 내용 요약

## 🔗 다음 단계
- 연관 내용으로의 연결
````

### 3. 성능 최적화

````yaml title="성능 최적화 설정"
# 이미지 최적화
extra:
  optimize_images: true
  
# 검색 인덱스 최적화
plugins:
  - search:
      prebuild_index: true
      min_search_length: 2
      
# 캐싱 설정
extra:
  cache:
    enabled: true
    ttl: 3600
````

## 🏁 마무리

MkDocs를 활용한 문서화 시스템 구축을 통해:

- ✅ **전문적인 문서 사이트** 생성
- ✅ **자동화된 배포 파이프라인** 구성
- ✅ **사용자 친화적인 인터페이스** 제공
- ✅ **검색 및 네비게이션** 최적화
- ✅ **다국어 지원** 및 **반응형 디자인**

!!! success "Chapter 8 완료!"
    MkDocs를 성공적으로 적용했습니다! 
    이제 GitHub Actions를 통한 자동화를 학습해보겠습니다.

!!! tip "추가 학습 자료"
    - [MkDocs 공식 문서](https://www.mkdocs.org/)
    - [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
    - [GitHub Pages 배포 가이드](https://docs.github.com/en/pages)
    - [Mike 다중 버전 관리](https://github.com/jimporter/mike)