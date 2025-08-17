import sys
import os
import argparse
from pathlib import Path
import glob

class ArgumentParser:
    """명령행 인자 처리기"""
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='renamer',
            description='📁 CLI 기반 파일 이름 변경 도구',
            epilog='예시: python %(prog)s --prefix "new_" *.txt'
        )
        self.setup_arguments()
    
    def setup_arguments(self):
        """명령행 인자 설정"""
        
        # 파일 패턴 (위치 인자)
        self.parser.add_argument(
            'files',
            nargs='+',
            help='대상 파일 패턴들 (예: *.txt *.py)'
        )
        
        # 작업 유형 옵션
        action_group = self.parser.add_mutually_exclusive_group(required=True)
        action_group.add_argument(
            '--prefix', '-p',
            metavar='TEXT',
            help='파일명 앞에 추가할 텍스트'
        )
        action_group.add_argument(
            '--suffix', '-s', 
            metavar='TEXT',
            help='파일명 뒤에 추가할 텍스트'
        )
        action_group.add_argument(
            '--find-replace', '-fr',
            nargs=2,
            metavar=('FIND', 'REPLACE'),
            help='찾을 문자열과 바꿀 문자열'
        )
        
        # 기타 옵션
        self.parser.add_argument(
            '--dry-run', '-n',
            action='store_true',
            help='실제 변경 없이 미리보기만 표시'
        )
        self.parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='상세한 정보 출력'
        )
        self.parser.add_argument(
            '--force', '-f',
            action='store_true',
            help='확인 없이 바로 실행'
        )
    
    def parse_args(self, args=None):
        """인자 파싱"""
        return self.parser.parse_args(args)
    
    def print_help(self):
        """도움말 출력"""
        self.parser.print_help()

class CLIRenamer:
    """개선된 CLI 파일명 변경 도구"""
    
    def __init__(self):
        self.files = []
        self.arg_parser = ArgumentParser()
    
    def find_files(self, patterns, verbose=False):
        """파일 패턴으로 파일 찾기"""
        self.files = []
        
        if verbose:
            print("🔍 파일 검색 시작...")
        
        for pattern in patterns:
            matched_files = glob.glob(pattern)
            
            if verbose:
                print(f"  패턴 '{pattern}': {len(matched_files)}개 발견")
            
            for file_path in matched_files:
                if os.path.isfile(file_path):
                    abs_path = os.path.abspath(file_path)
                    if abs_path not in self.files:
                        self.files.append(abs_path)
        
        if verbose:
            print(f"📋 총 {len(self.files)}개 파일 발견")
        
        return len(self.files)
    
    def generate_new_names(self, operation, value1, value2=None):
        """새로운 파일명 생성"""
        new_names = []
        
        for file_path in self.files:
            directory = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            
            if operation == 'prefix':
                new_name = f"{value1}{name}{ext}"
            elif operation == 'suffix':
                new_name = f"{name}{value1}{ext}"
            elif operation == 'find_replace':
                new_name = filename.replace(value1, value2)
            else:
                new_name = filename
            
            new_path = os.path.join(directory, new_name)
            new_names.append((file_path, new_path))
        
        return new_names
    
    def show_preview(self, rename_plan):
        """미리보기 표시"""
        if not rename_plan:
            print("❌ 변경할 파일이 없습니다.")
            return
        
        print(f"\n👀 미리보기 ({len(rename_plan)}개 파일):")
        print("=" * 60)
        
        changes = 0
        for old_path, new_path in rename_plan:
            old_name = os.path.basename(old_path)
            new_name = os.path.basename(new_path)
            
            if old_name != new_name:
                print(f"  {old_name} → {new_name}")
                changes += 1
            else:
                print(f"  {old_name} (변경없음)")
        
        print("=" * 60)
        print(f"📊 바뀌는 파일: {changes}개 / {len(rename_plan)}개")
    
    def confirm_execution(self):
        """실행 확인"""
        try:
            response = input("\n실행하시겠습니까? (y/n): ").strip().lower()
            return response in ['y', 'yes', '예']
        except KeyboardInterrupt:
            print("\n❌ 사용자가 취소했습니다.")
            return False
    
    def execute_rename(self, rename_plan, verbose=False):
        """파일명 변경 실행"""
        if not rename_plan:
            print("❌ 변경할 파일이 없습니다.")
            return 0, []
        
        success_count = 0
        errors = []
        
        if verbose:
            print("\n⚙️ 파일명 변경 시작...")
        
        for old_path, new_path in rename_plan:
            if old_path == new_path:
                if verbose:
                    print(f"  건너뛰기: {os.path.basename(old_path)}")
                continue
            
            try:
                # 동일한 이름의 파일이 이미 있는지 확인
                if os.path.exists(new_path):
                    errors.append(f"{os.path.basename(old_path)}: 대상 파일이 이미 존재함")
                    continue
                
                os.rename(old_path, new_path)
                success_count += 1
                
                if verbose:
                    print(f"  ✅ {os.path.basename(old_path)} → {os.path.basename(new_path)}")
                
            except Exception as e:
                error_msg = f"{os.path.basename(old_path)}: {str(e)}"
                errors.append(error_msg)
                
                if verbose:
                    print(f"  ❌ {error_msg}")
        
        return success_count, errors
    
    def run(self, args=None):
        """프로그램 실행"""
        try:
            # 인자 파싱
            parsed_args = self.arg_parser.parse_args(args)
            
            print("📁 CLI 파일명 변경 도구 v2.0")
            print("=" * 40)
            
            # 파일 찾기
            file_count = self.find_files(parsed_args.files, parsed_args.verbose)
            
            if file_count == 0:
                print("❌ 패턴에 맞는 파일이 없습니다.")
                return 1
            
            # 작업 유형 결정
            if parsed_args.prefix:
                operation = 'prefix'
                value1 = parsed_args.prefix
                value2 = None
                print(f"✨ 작업: 접두사 '{value1}' 추가")
            elif parsed_args.suffix:
                operation = 'suffix'
                value1 = parsed_args.suffix
                value2 = None
                print(f"✨ 작업: 접미사 '{value1}' 추가")
            elif parsed_args.find_replace:
                operation = 'find_replace'
                value1, value2 = parsed_args.find_replace
                print(f"✨ 작업: '{value1}' → '{value2}' 바꾸기")
            
            # 변경 계획 생성
            rename_plan = self.generate_new_names(operation, value1, value2)
            
            # 미리보기 표시
            self.show_preview(rename_plan)
            
            # Dry run 모드인 경우 여기서 종료
            if parsed_args.dry_run:
                print("\n🏃 Dry run 모드: 실제 변경은 수행되지 않았습니다.")
                return 0
            
            # 확인 요청 (포스 모드가 아닌 경우)
            if not parsed_args.force:
                if not self.confirm_execution():
                    print("❌ 사용자가 취소했습니다.")
                    return 0
            
            # 실제 변경 실행
            success_count, errors = self.execute_rename(rename_plan, parsed_args.verbose)
            
            # 결과 보고
            print(f"\n📊 결과:")
            print(f"  ✅ 성공: {success_count}개")
            if errors:
                print(f"  ❌ 실패: {len(errors)}개")
                if parsed_args.verbose:
                    for error in errors:
                        print(f"    - {error}")
            
            if success_count > 0:
                print(f"\n✨ {success_count}개 파일의 이름이 성공적으로 변경되었습니다!")
                return 0
            else:
                print("\n❌ 성공적으로 변경된 파일이 없습니다.")
                return 1
                
        except KeyboardInterrupt:
            print("\n\n❌ 사용자가 중단했습니다.")
            return 130
        except Exception as e:
            print(f"\n❌ 오류가 발생했습니다: {e}")
            return 1

def main():
    """메인 함수"""
    renamer = CLIRenamer()
    exit_code = renamer.run()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()