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
    
    print(f"\n📁 파일 경로: {file_path}")
    print(f"   📄 파일명만: {file_info.name}")
    print(f"   📂 폴더 경로: {file_info.parent}")
    print(f"   📎 확장자: {file_info.suffix}")
    print(f"   📝 이름(확장자 제외): {file_info.stem}")