import sys
import os
from pathlib import Path
import glob

class BasicCLIRenamer:
    """기본 CLI 파일명 변경 도구"""
    
    def __init__(self):
        self.files = []  # 발견된 파일들을 저장할 리스트
        print("📁 CLI 파일명 변경 도구 v1.0")
        print("=" * 40)
    
    def find_files(self, patterns):
        """파일 패턴으로 파일 찾기"""
        self.files = []
        
        for pattern in patterns:
            # glob을 사용해서 패턴에 맞는 파일들 찾기
            matched_files = glob.glob(pattern)
            
            for file_path in matched_files:
                # 파일인지 확인하고 절대경로로 변환
                if os.path.isfile(file_path):
                    abs_path = os.path.abspath(file_path)
                    if abs_path not in self.files:  # 중복 방지
                        self.files.append(abs_path)
        
        return len(self.files)
    
    def list_files(self):
        """발견된 파일들 목록 출력"""
        if not self.files:
            print("❌ 패턴에 맞는 파일이 없습니다.")
            return
        
        print(f"📋 발견된 파일: {len(self.files)}개")
        print("-" * 40)
        
        for i, file_path in enumerate(self.files, 1):
            # 파일명만 표시 (경로는 너무 길어서)
            filename = os.path.basename(file_path)
            file_size = self.get_file_size(file_path)
            print(f"{i:3d}. {filename} ({file_size})")
        
        print("-" * 40)
    
    def get_file_size(self, file_path):
        """파일 크기를 읽기 쉬운 형태로 반환"""
        try:
            size = os.path.getsize(file_path)
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size/1024:.1f} KB"
            else:
                return f"{size/(1024*1024):.1f} MB"
        except OSError:
            return "알 수 없음"
    
    def show_help(self):
        """도움말 출력"""
        help_text = """
사용법: python step1_basic_cli.py [파일패턴...]

예시:
  python step1_basic_cli.py *.txt        # 모든 txt 파일
  python step1_basic_cli.py *.py *.js    # py와 js 파일들
  python step1_basic_cli.py "test*.log"  # test로 시작하는 log 파일들
  python step1_basic_cli.py photo_*.jpg  # photo_로 시작하는 jpg 파일들

기능:
  - 파일 패턴 매칭으로 파일 찾기
  - 파일 목록과 크기 정보 표시
  - 중복 파일 자동 제거
"""
        print(help_text)
    
    def run(self, args):
        """프로그램 실행"""
        # 명령행 인자 확인
        if len(args) < 2:
            print("❌ 파일 패턴을 지정해주세요!")
            self.show_help()
            return 1
        
        # 도움말 요청 확인
        if args[1] in ["-h", "--help", "help"]:
            self.show_help()
            return 0
        
        # 파일 패턴들 (첫 번째 인자부터)
        file_patterns = args[1:]
        
        print(f"🔍 파일 검색 중... 패턴: {', '.join(file_patterns)}")
        
        # 파일 찾기
        file_count = self.find_files(file_patterns)
        
        if file_count == 0:
            print("\n💡 팁: 파일이 없을 때 확인사항:")
            print("  - 파일 패턴이 올바른지 확인")
            print("  - 현재 디렉토리에 해당 파일들이 있는지 확인")
            print("  - 따옴표로 패턴을 감싸보세요: \"*.txt\"")
            return 1
        
        # 파일 목록 출력
        self.list_files()
        
        print("\n✅ Step 1 완료: 파일 목록을 성공적으로 찾았습니다!")
        print("💡 다음 단계에서는 이 파일들의 이름을 바꿔볼 예정입니다.")
        
        return 0

def main():
    """메인 함수"""
    renamer = BasicCLIRenamer()
    exit_code = renamer.run(sys.argv)
    sys.exit(exit_code)

# 프로그램 실행
if __name__ == "__main__":
    main()