def safe_rename_file(old_name, new_name):
    """안전하게 파일명을 바꾸는 함수"""
    print(f"🔄 '{old_name}'을 '{new_name}'으로 바꾸려고 해요...")
    
    try:
        # 1단계: 원본 파일이 정말 있는지 확인
        import os
        if not os.path.exists(old_name):
            print(f"❌ 앗! '{old_name}' 파일을 찾을 수 없어요!")
            return False
        
        # 2단계: 새 이름으로 된 파일이 이미 있는지 확인  
        if os.path.exists(new_name):
            print(f"⚠️  '{new_name}' 파일이 이미 있어요!")
            print("   같은 이름의 파일이 있으면 덮어써질 수 있어요.")
            return False
        
        # 3단계: 실제로는 파일명을 바꾸지 않고 시뮬레이션만
        print(f"✅ 성공! '{old_name}' → '{new_name}'으로 바뀔 예정이에요")
        return True
        
    except PermissionError:
        print("🚫 권한이 없어서 파일을 바꿀 수 없어요!")
        print("   (파일이 다른 프로그램에서 사용 중일 수도 있어요)")
        return False
    
    except Exception as e:
        print(f"😵 예상치 못한 문제가 생겼어요: {e}")
        print("   개발자에게 문의해주세요!")
        return False

# 테스트해보기
print("=== 안전한 파일명 변경 테스트 ===")

# 존재하지 않는 파일 테스트
safe_rename_file("없는파일.txt", "새파일.txt")
print()

# 실제 존재할 만한 파일 테스트  
safe_rename_file("C:/Windows/System32/notepad.exe", "새이름.exe")
print()