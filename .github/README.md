# KRenamer CI/CD 설정 가이드

이 디렉토리는 KRenamer 프로젝트의 GitHub Actions 워크플로우와 CI/CD 자동화 설정을 포함합니다.

## 📁 파일 구조

```
.github/
├── workflows/
│   ├── docs.yml              # 문서 빌드 및 배포
│   ├── python-package.yml    # 패키지 테스트 및 빌드  
│   ├── python-publish.yml    # PyPI 배포
│   └── test-docs.yml         # 문서 테스트
└── README.md                 # 이 파일
```

## 🚀 워크플로우 설명

### 1. 문서 빌드 및 배포 (`docs.yml`)

**트리거 조건:**
- `main` 브랜치에 push할 때
- `docs/`, `mkdocs.yml`, `src/krenamer/` 디렉토리 변경 시
- Pull Request 생성 시

**주요 기능:**
- Python 환경 설정 (3.12)
- MkDocs 및 관련 플러그인 설치
- Sphinx API 문서 생성
- MkDocs로 최종 문서 빌드
- GitHub Pages 배포

**의존성:**
- `mkdocs`
- `mkdocs-material`  
- `mkdocs-minify-plugin`
- `pymdown-extensions`
- `sphinx`
- `sphinx-rtd-theme`

### 2. 패키지 테스트 (`python-package.yml`)

**트리거 조건:**
- `main` 브랜치에 push할 때

**주요 기능:**
- Python 3.8-3.13 다중 버전 테스트
- flake8 린팅
- pytest 테스트 실행

**테스트 매트릭스:**
- Python 버전: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- OS: Ubuntu Latest

### 3. PyPI 배포 (`python-publish.yml`)

**트리거 조건:**
- GitHub Release 생성 시

**주요 기능:**
- 패키지 빌드
- PyPI에 자동 배포

**필요한 시크릿:**
- `PYPI_API_TOKEN`: PyPI API 토큰

## 🔧 설정 방법

### 1. GitHub Pages 활성화

1. GitHub 리포지토리 → **Settings** → **Pages**
2. **Source**: GitHub Actions 선택
3. 워크플로우가 자동으로 실행되어 문서 배포

### 2. PyPI 배포 설정

1. PyPI 계정 생성 및 API 토큰 발급
2. GitHub 리포지토리 → **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret**:
   - Name: `PYPI_API_TOKEN`
   - Value: 발급받은 PyPI API 토큰

### 3. 브랜치 보호 규칙 (권장)

1. GitHub 리포지토리 → **Settings** → **Branches**
2. **Add rule** → Branch name pattern: `main`
3. 다음 옵션 활성화:
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Status checks: `build (3.8)`, `build (3.9)`, etc.

## 📋 워크플로우 실행 조건 상세

### 자동 실행

| 워크플로우 | 실행 조건 | 목적 |
|-----------|-----------|------|
| `docs.yml` | docs/ 변경 시 | 문서 자동 업데이트 |
| `python-package.yml` | main 브랜치 push | 코드 품질 검증 |
| `python-publish.yml` | Release 생성 | 패키지 배포 |

### 수동 실행

GitHub Actions 탭에서 워크플로우를 수동으로 실행할 수 있습니다:

1. **Actions** 탭 이동
2. 실행할 워크플로우 선택
3. **Run workflow** 버튼 클릭

## 🐛 트러블슈팅

### 문서 배포 실패

**문제**: GitHub Pages 배포가 실패하는 경우

**해결책**:
1. Settings → Pages에서 GitHub Actions 선택 확인
2. 워크플로우 권한 확인:
   ```yaml
   permissions:
     contents: read
     pages: write
     id-token: write
   ```

### PyPI 배포 실패

**문제**: PyPI 토큰 오류

**해결책**:
1. PyPI에서 새 API 토큰 생성
2. GitHub Secrets에 `PYPI_API_TOKEN` 정확히 설정
3. 토큰 스코프가 해당 패키지에 대해 활성화되어 있는지 확인

### 테스트 실패

**문제**: Python 버전 호환성 이슈

**해결책**:
1. `requirements.txt` 또는 `pyproject.toml`에서 의존성 버전 확인
2. 코드에서 사용하는 Python 기능이 모든 테스트 버전에서 지원되는지 확인

## 📚 추가 자료

- [GitHub Actions 공식 문서](https://docs.github.com/en/actions)
- [PyPI 배포 가이드](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [MkDocs 문서](https://www.mkdocs.org/)
- [pytest 문서](https://docs.pytest.org/)

## 🔄 워크플로우 커스터마이징

### Python 버전 변경

`python-package.yml`의 매트릭스 수정:

```yaml
strategy:
  matrix:
    python-version: ["3.9", "3.10", "3.11", "3.12"]  # 원하는 버전만 선택
```

### 테스트 조건 추가

각 워크플로우에 단계 추가:

```yaml
- name: Run additional tests
  run: |
    pytest tests/integration/
    pytest tests/performance/
```

### 알림 설정

워크플로우 실패 시 Slack/Discord 알림:

```yaml
- name: Notify failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: failure
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

이 설정을 통해 KRenamer 프로젝트는 완전히 자동화된 CI/CD 파이프라인을 가지게 됩니다. 코드 품질 유지, 자동 배포, 문서 업데이트가 모두 자동으로 처리됩니다!