# 문제 해결 가이드

Renamer 사용 중 발생할 수 있는 문제들과 해결 방법을 정리했습니다.

## 🚨 자주 발생하는 오류

### 1. AttributeError: 'RenamerGUI' object has no attribute 'pattern_var'

**원인**: GUI 초기화 순서 문제로 일부 변수들이 아직 생성되지 않았을 때 접근하려 했습니다.

**해결책**: 
- v1.0.1에서 수정됨
- GUI 변수들의 존재 여부를 확인하는 `hasattr()` 체크 추가
- 안전한 초기화 순서 보장

```python
# 수정된 코드 예시
if hasattr(self, 'pattern_var') and self.pattern_var.get():
    # 패턴 변수가 존재할 때만 실행
```

### 2. ModuleNotFoundError: No module named 'tkinterdnd2'

**원인**: 드래그 앤 드롭 기능에 필요한 라이브러리가 설치되지 않았습니다.

**해결책**:
```bash
pip install tkinterdnd2
```

**대안**: tkinterdnd2 없이도 기본 기능은 사용 가능합니다.
- "파일 추가" 버튼으로 파일 선택
- 드래그 앤 드롭 기능만 비활성화됨

### 3. UnicodeEncodeError: 'cp949' codec can't encode character

**원인**: Windows 콘솔에서 한글 또는 특수 문자 출력 시 인코딩 문제

**해결책**:
```bash
# 환경 변수 설정
set PYTHONIOENCODING=utf-8

# 또는 파이썬 실행 시
python -X utf8 main.py
```

### 4. tkinter 관련 오류들

#### "No module named 'tkinter'"
**해결책**:
- **Windows**: Python 재설치 시 tkinter 포함 옵션 선택
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **CentOS/RHEL**: `sudo yum install tkinter`

#### 한글 폰트가 깨져 보임
**해결책**:
```python
# 시스템별 폰트 설정
# Windows
font=("맑은 고딕", 12)
# macOS  
font=("AppleGothic", 12)
# Linux
font=("DejaVu Sans", 12)
```

## 🔧 성능 관련 문제

### 1. 대용량 파일 목록 처리 시 느림

**현상**: 수백 개 이상의 파일 처리 시 UI가 멈춤

**해결책**:
- 파일 개수를 200개 이하로 제한
- 또는 배치 처리로 나누어 실행

### 2. 정규식 패턴이 복잡할 때 응답 없음

**현상**: 복잡한 정규식 사용 시 프로그램이 멈춤

**해결책**:
- 간단한 패턴부터 테스트
- "조건 테스트" 기능으로 미리 확인
- 타임아웃 기능 추가 예정

## 🛠️ 설치 관련 문제

### 1. pip 설치가 안 됨

**해결책**:
```bash
# 개발 모드로 설치
pip install -e .

# 캐시 삭제 후 재시도
pip cache purge
pip install --no-cache-dir tkinterdnd2

# 권한 문제 시
pip install --user tkinterdnd2
```

### 2. Windows에서 실행 파일이 안 만들어짐

**해결책**:
```bash
# PyInstaller 사용
pip install pyinstaller
pyinstaller --onefile --windowed src/krenamer/main.py
```

## 🐛 버그 신고

### 신고 전 체크리스트

- [ ] 최신 버전 사용 중인가?
- [ ] 필요한 의존성이 모두 설치되었나?
- [ ] 오류 메시지를 정확히 복사했나?
- [ ] 재현 가능한 단계를 정리했나?

### 신고 방법

1. **GitHub Issues**: https://github.com/geniuskey/krenamer/issues
2. **이메일**: contact@geniuskey.com

### 포함할 정보

```
환경 정보:
- OS: Windows 10/11, macOS, Linux
- Python 버전: python --version
- 패키지 버전: pip show krenamer
- 에러 메시지: 전체 트레이스백 포함

재현 단계:
1. 애플리케이션 실행
2. 파일 10개 추가
3. 정규식 패턴 "..." 입력
4. 실행 버튼 클릭
5. 오류 발생

기대 결과:
파일명이 정상적으로 변경되어야 함

실제 결과:
AttributeError: ... 오류 발생
```

## 📚 추가 도움말

### 1. 정규식 패턴 도움

**유용한 정규식 리소스**:
- https://regexr.com/ - 정규식 테스트
- https://regex101.com/ - 정규식 설명
- https://regexone.com/ - 정규식 학습

### 2. Python GUI 학습 자료

- **tkinter 공식 문서**: https://docs.python.org/3/library/tkinter.html
- **Real Python tkinter**: https://realpython.com/python-gui-tkinter/

### 3. 파일 시스템 관련

- **pathlib 문서**: https://docs.python.org/3/library/pathlib.html
- **os.path 문서**: https://docs.python.org/3/library/os.path.html

## 🔄 버전별 변경사항

### v1.0.1 (현재)
- GUI 초기화 순서 문제 수정
- 변수 존재 여부 확인 로직 추가
- 안정성 개선

### v1.0.0 (초기 릴리스)
- 기본 GUI 기능
- 드래그 앤 드롭 지원
- 다양한 리네임 방식
- 조건부 필터링
- 정규식 패턴 매칭

---

!!! tip "도움이 더 필요하다면"
    이 가이드에서 해결되지 않는 문제가 있다면 GitHub Issues에 신고해주세요.
    커뮤니티와 함께 해결책을 찾아보겠습니다!