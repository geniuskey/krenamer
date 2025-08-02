# KRenamer 개발 가이드

KRenamer 개발을 위한 설정 및 워크플로우 가이드입니다.

## 🚀 빠른 시작

### 1. 개발 환경 설정

```bash
# 저장소 클론
git clone https://github.com/geniuskey/krenamer.git
cd krenamer

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows

# 개발 의존성 설치
pip install -e .[dev]
```

### 2. 개발 실행

```bash
# 직접 실행
cd src/krenamer
python main.py

# 또는 패키지로 실행
krenamer
```

## 🛠️ 개발 도구

### Make 스크립트 사용

Windows에서 `make.bat` 스크립트를 사용하여 다양한 작업을 수행할 수 있습니다:

```bash
# 도움말 보기
make help

# 실행 파일 빌드
make exe

# 문서 빌드 및 미리보기
make docs
make serve

# 테스트 실행
make test

# 정리
make clean
```

### 주요 명령어

| 명령어 | 설명 | 출력 |
|--------|------|------|
| `make exe` | PyInstaller로 단일 실행 파일 생성 | `dist/KRenamer.exe` |
| `make wheel` | Wheel 패키지 빌드 | `dist/*.whl` |
| `make build` | 모든 패키지 빌드 | `dist/` 폴더 |
| `make docs` | MkDocs 문서 빌드 | `site/` 폴더 |
| `make clean` | 빌드 아티팩트 정리 | - |

## 📁 프로젝트 구조

```
krenamer/
├── src/krenamer/           # 메인 소스 코드
│   ├── __init__.py
│   ├── main.py            # 애플리케이션 진입점
│   ├── gui.py             # GUI 인터페이스
│   └── core.py            # 파일 처리 엔진
├── assets/                # 아이콘, 이미지 등
├── docs/                  # 문서 (MkDocs)
├── .github/workflows/     # GitHub Actions
├── krenamer.spec          # PyInstaller 설정
├── version_info.txt       # 실행 파일 메타데이터
├── make.bat              # Windows 빌드 스크립트
├── pyproject.toml        # 패키지 설정
└── README.md             # 프로젝트 설명
```

## 🔄 개발 워크플로우

### 1. 기능 개발

1. **브랜치 생성**: `git checkout -b feature/new-feature`
2. **개발**: 코드 작성 및 테스트
3. **테스트**: `make test`
4. **문서 업데이트**: 필요시 README 또는 docs 업데이트
5. **커밋**: `git commit -m "Add new feature"`

### 2. 빌드 테스트

```bash
# 실행 파일 빌드 테스트
make exe

# 실행 파일 실행 테스트
dist/KRenamer.exe

# 패키지 빌드 테스트
make build
```

### 3. 문서 작업

```bash
# 문서 로컬 서버 시작
make serve

# 문서 수정 후 빌드
make docs
```

### 4. 릴리즈

```bash
# 1. 버전 업데이트 (pyproject.toml, __init__.py)
# 2. 모든 빌드 테스트
make clean
make build
make exe

# 3. TestPyPI에 업로드 (테스트)
make publish-test

# 4. PyPI에 업로드 (프로덕션)
make publish
```

## 🧪 테스트

### 자동 테스트

```bash
# 기본 테스트
make test

# 수동 import 테스트
cd src/krenamer
python -c "import main; print('✓ Import successful')"
```

### GUI 테스트

```bash
# GUI 애플리케이션 실행
python src/krenamer/main.py

# 실행 파일 테스트
make exe
dist/KRenamer.exe
```

## 📦 빌드 상세

### PyInstaller 설정

`krenamer.spec` 파일에서 빌드 설정을 관리:

- **onefile**: 단일 실행 파일 생성
- **console**: GUI 모드 (False)
- **icon**: 애플리케이션 아이콘
- **version_file**: 실행 파일 메타데이터

### 빌드 최적화

- **UPX 압축**: 실행 파일 크기 최적화
- **Hidden imports**: 필요한 모듈 명시적 포함
- **Data files**: tkinterdnd2 DLL 파일 포함

## 🚀 배포

### PyPI 배포

1. **계정 설정**: PyPI 계정 생성 및 API 토큰 설정
2. **테스트 배포**: `make publish-test`
3. **프로덕션 배포**: `make publish`

### GitHub Releases

1. **태그 생성**: `git tag v1.0.0`
2. **푸시**: `git push origin v1.0.0`
3. **실행 파일 첨부**: `dist/KRenamer.exe`를 릴리즈에 첨부

## 🐛 문제 해결

### 일반적인 문제

1. **PyInstaller 빌드 실패**
   - 가상환경에서 빌드
   - 의존성 확인: `pip install pyinstaller`

2. **tkinterdnd2 관련 오류**
   - DLL 파일 경로 확인
   - `.spec` 파일의 `datas` 섹션 확인

3. **문서 빌드 실패**
   - MkDocs 의존성 확인: `pip install mkdocs mkdocs-material`

### 디버깅

```bash
# 자세한 빌드 로그
pyinstaller --clean --log-level DEBUG krenamer.spec

# Import 오류 디버깅
python -c "import sys; print(sys.path)"
cd src && python -c "import krenamer; print('OK')"
```

## 📞 지원

- **이슈 제보**: [GitHub Issues](https://github.com/geniuskey/krenamer/issues)
- **개발 문의**: 프로젝트 Discussion 페이지 활용