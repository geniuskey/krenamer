class MyFileManager:
    """내가 만든 파일 관리자"""
    
    def __init__(self):
        """파일 관리자를 처음 만들 때 실행되는 함수"""
        print("🎉 새로운 파일 관리자가 만들어졌어요!")
        self.my_files = []  # 내 파일들을 저장할 리스트
        self.total_renamed = 0  # 지금까지 바꾼 파일 개수
    
    def add_file(self, file_path):
        """파일을 관리 목록에 추가하기"""
        if file_path not in self.my_files:
            self.my_files.append(file_path)
            print(f"📁 '{file_path}' 파일을 추가했어요!")
        else:
            print(f"⚠️  '{file_path}' 파일은 이미 있어요!")
    
    def show_files(self):
        """현재 관리 중인 파일들 보여주기"""
        print(f"\n📋 현재 관리 중인 파일: {len(self.my_files)}개")
        for i, file_path in enumerate(self.my_files, 1):
            print(f"   {i}. {file_path}")
    
    def add_prefix_to_all(self, prefix):
        """모든 파일에 접두사 추가하기"""
        print(f"\n✨ 모든 파일에 '{prefix}' 접두사 추가 결과:")
        new_names = []
        
        for file_path in self.my_files:
            from pathlib import Path
            file_info = Path(file_path)
            new_name = prefix + file_info.name
            new_full_path = file_info.parent / new_name
            new_names.append(str(new_full_path))
            print(f"   📄 {file_info.name} → {new_name}")
        
        return new_names
    
    def add_numbers_to_all(self, start_number=1):
        """모든 파일에 순서대로 번호 매기기"""
        print(f"\n🔢 {start_number}번부터 순서대로 번호 매기기:")
        new_names = []
        
        for i, file_path in enumerate(self.my_files):
            from pathlib import Path
            file_info = Path(file_path)
            number = start_number + i
            new_name = f"{number:03d}_{file_info.name}"  # 001, 002, 003...
            new_full_path = file_info.parent / new_name
            new_names.append(str(new_full_path))
            print(f"   📄 {file_info.name} → {new_name}")
        
        return new_names