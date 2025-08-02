print("=== 여러 파일 한 번에 처리하기 ===")

# 여러 파일명을 리스트에 저장
my_files = [
    "휴가사진_001.jpg",
    "휴가사진_002.jpg", 
    "중요문서_v1.2.pdf",
    "백업파일_2023_12_15.zip"
]

print("📋 원본 파일들:")
for file in my_files:
    print(f"  - {file}")

# 모든 파일에 접두사 "정리된_" 추가하기
print("\n✨ 접두사 '정리된_' 추가 결과:")
renamed_files = []
for file in my_files:
    new_name = "정리된_" + file
    renamed_files.append(new_name)
    print(f"  📄 {file} → {new_name}")

# 더 간단한 방법: 리스트 컴프리헨션 (고급 기법)
print("\n🚀 더 간단한 방법으로 해보기:")
quick_renamed = ["NEW_" + file for file in my_files]
for i, file in enumerate(my_files):
    print(f"  📄 {file} → {quick_renamed[i]}")