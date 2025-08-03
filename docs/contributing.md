# 기여하기

KRenamer 프로젝트에 관심을 가져주셔서 감사합니다! 이 문서는 프로젝트에 기여하는 간단한 방법을 설명합니다.

## 🚀 빠른 시작

### 1. 이슈 리포트

버그를 발견했거나 개선사항이 있다면:

1. [Issues 페이지](https://github.com/geniuskey/krenamer/issues)에서 기존 이슈 확인
2. 새로운 이슈 생성
3. 다음 정보 포함:
   - 운영체제 및 Python 버전
   - 문제 상황 설명
   - 재현 방법
   - 기대했던 결과

### 2. 기능 제안

새로운 기능을 제안하고 싶다면:

1. [Discussions 페이지](https://github.com/geniuskey/krenamer/discussions)에서 먼저 논의
2. 커뮤니티 피드백 수집
3. 필요시 이슈로 등록

### 3. 코드 기여

간단한 기여 과정:

```bash
# 1. 저장소 Fork 및 클론
git clone https://github.com/[your-username]/krenamer.git
cd krenamer

# 2. 개발 환경 설정
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .

# 3. 새 브랜치 생성
git checkout -b your-feature-branch

# 4. 코드 수정 및 테스트
# ... 작업 ...

# 5. 커밋 및 푸시
git add .
git commit -m "설명적인 커밋 메시지"
git push origin your-feature-branch

# 6. Pull Request 생성
```

## 🎯 기여 가능한 영역

### 초보자 친화적
- 문서 오타 수정
- 번역 개선
- 예제 코드 추가
- 테스트 케이스 추가

### 중급자용
- 버그 수정
- 새로운 파일 필터 추가
- UI/UX 개선
- 성능 최적화

### 고급자용
- 새로운 핵심 기능
- 아키텍처 개선
- 플러그인 시스템
- 크로스 플랫폼 호환성

## 📋 간단한 가이드라인

### 코드 스타일
- Python PEP 8 스타일 준수
- 의미 있는 변수명 사용
- 주석으로 복잡한 로직 설명

### 커밋 메시지
```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
test: 테스트 추가
```

### 테스트
- 새로운 기능에는 테스트 추가
- 기존 테스트가 깨지지 않도록 확인
- `python -m pytest` 로 테스트 실행

## 💬 소통하기

- **질문**: GitHub Discussions 사용
- **버그 리포트**: GitHub Issues 사용
- **실시간 채팅**: Discord 채널 (준비 중)

## 🙏 기여 인정

모든 기여자는 다음과 같이 인정받습니다:

- README.md의 기여자 목록에 이름 추가
- 릴리스 노트에 기여 내용 기록
- GitHub 프로필에 기여 뱃지 표시

---

**함께 만들어가는 오픈소스 프로젝트에 참여해주셔서 감사합니다!** 🎉
