# KRenamer 테스트 시스템

이 디렉토리는 KRenamer의 포괄적인 테스트 시스템을 포함합니다. Chapter 8 문서 사양에 맞춰 체계적으로 구성되어 있습니다.

## 📁 디렉토리 구조

```
tests/
├── conftest.py                 # 공통 픽스처 설정
├── pytest.ini                 # pytest 설정 파일  
├── unit/                       # 단위 테스트
│   ├── test_core.py           # 핵심 기능 테스트
│   ├── test_gui_components.py # GUI 컴포넌트 테스트
│   ├── test_imports.py        # 임포트 및 기본 기능 테스트
│   ├── test_file_utils.py     # 파일 유틸리티 테스트
│   ├── test_string_utils.py   # 문자열 유틸리티 테스트
│   └── test_renamer_engine.py # 리네임 엔진 종합 테스트
├── integration/                # 통합 테스트
│   └── test_rename_workflow.py # 전체 워크플로우 테스트
├── fixtures/                   # 테스트 데이터
├── utils/                      # 테스트 유틸리티
│   └── helpers.py             # 헬퍼 함수들
└── README.md                   # 이 파일
```

## 🚀 테스트 실행

### 전체 테스트 실행
```bash
pytest
```

### 단위 테스트만 실행
```bash
pytest -m unit
```

### 통합 테스트만 실행
```bash
pytest -m integration
```

### GUI 테스트 제외하고 실행
```bash
pytest -m "not gui"
```

### 빠른 테스트만 실행 (GUI, slow 테스트 제외)
```bash
pytest -m "not gui and not slow"
```

### 특정 테스트 파일 실행
```bash
pytest tests/unit/test_core.py
```

### 상세한 출력으로 실행
```bash
pytest -v
```

## 🏷️ 테스트 마커

테스트는 다음 마커로 분류됩니다:

- `unit`: 빠른 단위 테스트
- `integration`: 느린 통합 테스트  
- `gui`: GUI가 필요한 테스트
- `filesystem`: 실제 파일 시스템을 사용하는 테스트
- `slow`: 시간이 오래 걸리는 테스트

## 📋 테스트 범위

### 단위 테스트 (unit/)

- **test_core.py**: RenameEngine 기본 기능
  - 파일 추가/제거
  - 리네임 규칙 적용
  - 조건부 필터링
  - 문자열 변환

- **test_gui_components.py**: GUI 컴포넌트
  - GUI 클래스 구조
  - 엔진-GUI 통합
  - 헤드리스 환경 대응

- **test_imports.py**: 기본 기능
  - 모듈 임포트
  - 의존성 검사
  - 기본 동작 확인

- **test_file_utils.py**: 파일 유틸리티
  - 파일 정보 추출
  - 확장자 처리
  - 크기 조건 검사
  - 안전한 파일명 처리

- **test_string_utils.py**: 문자열 유틸리티
  - 대소문자 변환
  - 공백 처리
  - 특수문자 제거
  - 패턴 매칭

- **test_renamer_engine.py**: 리네임 엔진 종합
  - 모든 리네임 규칙
  - 복합 조건 처리
  - 오류 처리
  - 중복 처리

### 통합 테스트 (integration/)

- **test_rename_workflow.py**: 전체 워크플로우
  - 완전한 리네임 프로세스
  - 복잡한 시나리오
  - 오류 복구
  - 실제 파일 시스템 테스트

## 🔧 픽스처

`conftest.py`에서 제공하는 주요 픽스처들:

- `temp_dir`: 임시 디렉토리
- `sample_files`: 다양한 샘플 파일들
- `rename_engine`: 깨끗한 RenameEngine 인스턴스
- `temp_files`: 기존 호환성을 위한 임시 파일들
- `mock_settings`: 향후 설정 시스템용 모킹 객체

## 🛠️ 테스트 도구

### 권장 pytest 플러그인

```bash
# 기본 플러그인들
pip install pytest pytest-cov pytest-mock pytest-xdist

# 선택사항 (GUI 테스트용)
pip install pytest-qt
```

### 커버리지 측정

```bash
# HTML 리포트 생성
pytest --cov=krenamer --cov-report=html

# 터미널에 커버리지 표시
pytest --cov=krenamer --cov-report=term-missing
```

### 병렬 테스트 실행

```bash
# CPU 코어 수만큼 병렬 실행
pytest -n auto
```

## 📝 테스트 작성 가이드

### 새 테스트 추가 시

1. 적절한 디렉토리 선택 (unit/ 또는 integration/)
2. 기존 테스트 파일에 추가하거나 새 파일 생성
3. 적절한 마커 추가 (`@pytest.mark.unit` 등)
4. 픽스처 활용하여 설정 간소화
5. 명확한 테스트 함수명과 docstring 작성

### 테스트 명명 규칙

- 파일: `test_*.py`
- 클래스: `Test*`
- 함수: `test_*`
- 한국어 docstring으로 테스트 목적 설명

### 예시

```python
@pytest.mark.unit
class TestNewFeature:
    """새로운 기능 테스트"""
    
    def test_basic_operation(self, rename_engine):
        """기본 동작 테스트"""
        # Arrange
        rename_engine.new_feature = True
        
        # Act
        result = rename_engine.do_something()
        
        # Assert
        assert result is not None
```

## 🔍 트러블슈팅

### GUI 테스트가 실패하는 경우
```bash
# GUI 테스트 건너뛰기
pytest -m "not gui"
```

### 모듈 임포트 오류
- `src/` 디렉토리가 올바른 위치에 있는지 확인
- `PYTHONPATH` 환경변수 설정 확인

### 파일 권한 오류
- 임시 디렉토리 접근 권한 확인
- Windows에서는 관리자 권한으로 실행

## 📊 현재 테스트 현황

- **총 테스트 수**: 102개
- **단위 테스트**: 86개  
- **통합 테스트**: 10개
- **GUI 테스트**: 7개
- **파일시스템 테스트**: 4개

테스트를 통해 KRenamer의 안정성과 품질을 보장하고 있습니다.