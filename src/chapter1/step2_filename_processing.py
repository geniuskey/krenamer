print("=== 파일명 바꾸기 연습 ===")

# 원본 파일명
filename = "내 사진 (복사본).jpg"
print(f"🔤 원본 파일명: {filename}")

# 1) 파일명과 확장자 나누기
import os
name_part, extension = os.path.splitext(filename)
print(f"📄 파일명 부분: '{name_part}'")
print(f"📎 확장자 부분: '{extension}'")

# 2) 특별한 문자들 제거하기
cleaned_name = filename.replace("(복사본)", "")  # (복사본) 제거
cleaned_name = cleaned_name.replace("  ", " ")   # 두 번 띄어쓰기를 한 번으로
print(f"🧹 정리된 파일명: '{cleaned_name}'")

# 3) 공백을 밑줄로 바꾸기
underscore_name = cleaned_name.replace(" ", "_")
print(f"🔗 밑줄로 연결: '{underscore_name}'")

# 4) 대소문자 바꾸기
print(f"🔤 소문자로: '{filename.lower()}'")
print(f"🔠 대문자로: '{filename.upper()}'")

# 5) 앞뒤에 글자 추가하기
prefix = "NEW_"
suffix = "_BACKUP"
new_filename = prefix + name_part + suffix + extension
print(f"✨ 최종 결과: '{new_filename}'")