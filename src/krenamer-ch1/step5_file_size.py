def make_size_pretty(size_bytes):
    """파일 크기를 읽기 쉽게 바꿔주는 함수"""
    print(f"🔢 원래 크기: {size_bytes} 바이트")
    
    # 크기가 0이면 그냥 0B 반환
    if size_bytes == 0:
        return "0B"
    
    # 단위들: 바이트 → 킬로바이트 → 메가바이트 → 기가바이트
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    
    # 1024로 나누면서 적절한 단위 찾기
    for unit in units:
        if size_bytes < 1024.0:
            if unit == 'B':
                return f"{int(size_bytes)}{unit}"  # 바이트는 정수로
            else:
                return f"{size_bytes:.1f}{unit}"   # 나머지는 소수점 1자리
        size_bytes = size_bytes / 1024.0  # 1024로 나누기
    
    return f"{size_bytes:.1f}TB"  # 매우 큰 파일은 TB

# 테스트해보기
print("=== 파일 크기 예쁘게 만들기 ===")
test_sizes = [0, 512, 1024, 1536, 1048576, 1073741824]

for size in test_sizes:
    pretty_size = make_size_pretty(size)
    print(f"📊 {size:>10} 바이트 = {pretty_size}")
    print()