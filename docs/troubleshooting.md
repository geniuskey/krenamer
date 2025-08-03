# 문제 해결 가이드

KRenamer 사용 중 발생할 수 있는 문제들과 해결 방법을 안내합니다.

## 🐛 일반적인 문제들

### 1. tkinter 관련 오류

#### ModuleNotFoundError: No module named 'tkinter'

**증상:**
```
ModuleNotFoundError: No module named 'tkinter'
```

**해결 방법:**
- **Windows**: Python 재설치 시 "tcl/tk and IDLE" 옵션 체크
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **CentOS/RHEL**: `sudo yum install tkinter` 또는 `sudo dnf install python3-tkinter`
- **macOS**: `brew install python-tk`

### 2. tkinterdnd2 관련 오류

#### 드래그 앤 드롭이 작동하지 않음

**증상:**
- 파일을 드래그해도 반응이 없음
- 드롭 영역이 활성화되지 않음

**해결 방법:**
```bash
pip install --upgrade tkinterdnd2
```

**대안:**
- tkinterdnd2가 설치되지 않은 경우 기본 파일 선택 다이얼로그 사용
- "파일 추가" 버튼으로 파일 선택

### 3. 한글 폰트 문제

#### 한글이 깨져서 표시됨

**증상:**
- GUI에서 한글이 □□□로 표시
- 파일명의 한글이 제대로 표시되지 않음

**해결 방법:**
```python
# Windows
font=("맑은 고딕", 12)

# macOS
font=("AppleGothic", 12)

# Linux
font=("DejaVu Sans", 12)
```

## 🔧 설치 문제

### 1. pip 설치 실패

#### SSL 인증서 오류

**해결 방법:**
```bash
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org tkinterdnd2
```

#### 권한 오류 (Windows)

**해결 방법:**
- 관리자 권한으로 명령 프롬프트 실행
- 또는 사용자 디렉토리에 설치: `pip install --user tkinterdnd2`

### 2. Python 버전 호환성

#### Python 버전이 너무 낮음

**요구사항:**
- Python 3.8 이상 권장
- Python 3.6 이상에서 동작

**확인 방법:**
```bash
python --version
```

## 🏃‍♂️ 실행 문제

### 1. 파일 권한 오류

#### PermissionError: [Errno 13] Permission denied

**원인:**
- 파일이 다른 프로그램에서 사용 중
- 읽기 전용 파일
- 관리자 권한 필요

**해결 방법:**
1. 파일을 사용 중인 프로그램 종료
2. 파일 속성에서 읽기 전용 해제
3. 관리자 권한으로 실행

### 2. 파일명 인코딩 문제

#### UnicodeDecodeError 또는 UnicodeEncodeError

**해결 방법:**
```python
# 파일 읽기 시
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 파일 쓰기 시
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
```

### 3. 긴 파일 경로 문제 (Windows)

#### 파일 경로가 260자를 초과

**해결 방법:**
1. Windows 10 1607 이상에서 긴 경로 활성화:
   - `gpedit.msc` → 컴퓨터 구성 → 관리 템플릿 → 시스템 → 파일 시스템
   - "Win32 긴 경로 사용" 정책 활성화

2. 레지스트리 수정:
   ```
   HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem
   LongPathsEnabled = 1
   ```

## 💾 데이터 문제

### 1. 설정 파일 손상

#### 설정이 저장되지 않거나 로드되지 않음

**해결 방법:**
```bash
# 설정 파일 위치 (Windows)
%APPDATA%\KRenamer\settings.json

# 설정 파일 위치 (macOS)
~/Library/Application Support/KRenamer/settings.json

# 설정 파일 위치 (Linux)
~/.config/KRenamer/settings.json
```

**재설정 방법:**
1. 설정 파일 삭제
2. KRenamer 재시작
3. 기본 설정으로 복구됨

### 2. 히스토리 데이터베이스 오류

#### 작업 히스토리를 불러올 수 없음

**해결 방법:**
1. 히스토리 데이터베이스 파일 삭제:
   ```bash
   # 데이터베이스 위치
   [설정폴더]/history.db
   ```
2. 애플리케이션 재시작

## 🖥️ 성능 문제

### 1. 대량 파일 처리 시 느려짐

#### 수천 개의 파일 처리 시 응답 없음

**해결 방법:**
- 배치 크기 조정 (한 번에 100-500개씩 처리)
- 필터링을 활용하여 처리할 파일 수 줄이기
- 백그라운드 스레드 활용

### 2. 메모리 사용량 증가

#### 장시간 사용 시 메모리 누수

**해결 방법:**
- 주기적으로 파일 목록 초기화
- 캐시 클리어
- 애플리케이션 재시작

## 🔍 디버깅 방법

### 1. 로그 활성화

```python
import logging

# 로그 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('krenamer.log'),
        logging.StreamHandler()
    ]
)
```

### 2. 테스트 모드 실행

```bash
# 실제 파일 변경 없이 시뮬레이션만 실행
python main.py --test-mode
```

### 3. 상세 오류 정보 확인

```python
import traceback

try:
    # 문제가 되는 코드
    pass
except Exception as e:
    print(f"오류 발생: {e}")
    print("상세 정보:")
    traceback.print_exc()
```

## 📞 지원 받기

### 1. 이슈 리포트

문제가 해결되지 않으면 다음 정보와 함께 이슈를 등록해주세요:

- **운영체제**: Windows 10/11, macOS, Ubuntu 등
- **Python 버전**: `python --version` 결과
- **패키지 버전**: `pip list | grep tkinter` 결과
- **오류 메시지**: 전체 오류 메시지와 스택 트레이스
- **재현 방법**: 문제를 재현할 수 있는 단계별 설명

### 2. 로그 파일 첨부

문제 발생 시 다음 파일들을 첨부해주세요:
- `krenamer.log` (로그 파일)
- `settings.json` (설정 파일)
- 문제가 된 파일들의 목록

### 3. 임시 해결책

문제가 해결될 때까지 사용할 수 있는 대안:
- 더 작은 단위로 파일 처리
- 기본 기능만 사용
- 수동으로 백업 후 진행

## 🛡️ 예방 방법

### 1. 백업 습관

- 중요한 파일은 항상 백업 후 진행
- 테스트 폴더에서 먼저 실행
- 미리보기 기능 적극 활용

### 2. 안전한 사용

- 시스템 파일이 있는 폴더는 피하기
- 파일이 사용 중일 때는 작업 피하기
- 네트워크 드라이브에서는 신중하게 사용

### 3. 정기적인 유지보수

- 설정 파일 정기적으로 백업
- 히스토리 데이터베이스 정리
- 최신 버전으로 업데이트

---

이 가이드로 해결되지 않는 문제가 있다면 [이슈 트래커](https://github.com/geniuskey/krenamer/issues)에 문의해주세요.