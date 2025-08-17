# Chapter 3: CLI 기반 파일 이름 변경 도구

## 🎯 명령행에서 동작하는 실용적 도구 만들기

GUI를 배우기 전에 먼저 **명령행(CLI) 기반의 파일 이름 변경 도구**<!-- -->를 만들어봅시다! CLI 도구는 GUI보다 간단하지만 매우 실용적이고, 프로그래밍의 기본 개념들을 잘 보여줍니다.

**가장 간단한 기능부터 차근차근** 만들어서 점점 더 강력한 도구로 발전시켜보겠습니다.

## 🚀 이번 챕터의 목표

- **Step 1**: 기본 CLI 구조와 파일 목록 출력
- **Step 2**: 명령행 인자 처리와 옵션 파싱  
- **Step 3**: 접두사/접미사 추가 기능
- **Step 4**: 찾기/바꾸기 기능 구현
- **Step 5**: 완성된 CLI 도구와 고급 기능

Python의 `argparse`, `os`, `pathlib` 등을 사용해서 **실제로 유용한 CLI 도구**<!-- -->를 만들어봅시다!

## 🎨 우리가 만들 CLI 도구의 모습

```bash
# 기본 사용법
$ python renamer.py --prefix "new_" *.txt
발견된 파일: 3개
  example.txt → new_example.txt
  readme.txt → new_readme.txt  
  notes.txt → new_notes.txt
실행하시겠습니까? (y/n): y
✅ 3개 파일 이름 변경 완료!

# 고급 사용법
$ python renamer.py --find "old" --replace "new" --dry-run *.py
$ python renamer.py --suffix "_backup" --recursive ./documents/
```

*이번 챕터에서 만들 CLI 파일명 변경 도구입니다. 명령행에서 바로 사용할 수 있는 실용적인 도구예요!*

### Python 표준 라이브러리들이 어떻게 사용될까요?

- **argparse**: 명령행 인자와 옵션 처리
- **os/pathlib**: 파일 시스템 조작
- **glob**: 파일 패턴 매칭
- **sys**: 프로그램 종료와 입출력 제어
- **re**: 정규표현식을 이용한 고급 찾기/바꾸기

## Step 1: 기본 CLI 구조와 파일 목록 출력

가장 기본인 **명령행 인자를 받아서 파일 목록을 출력하기**<!-- -->부터 시작해봅시다.

### 기본 CLI 프로그램 구조 만들기

```python linenums="1" title="src/chapter3/step1_basic_cli.py"
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
```

### Step 1 실행해보기

위 코드를 실행하면 이런 기능들이 동작합니다:

```bash
# 기본 실행 (도움말 표시)
$ python step1_basic_cli.py
📁 CLI 파일명 변경 도구 v1.0
========================================
❌ 파일 패턴을 지정해주세요!

사용법: python step1_basic_cli.py [파일패턴...]
...

# 텍스트 파일 찾기
$ python step1_basic_cli.py *.txt
📁 CLI 파일명 변경 도구 v1.0
========================================
🔍 파일 검색 중... 패턴: *.txt
📋 발견된 파일: 3개
----------------------------------------
  1. readme.txt (2.1 KB)
  2. notes.txt (856 B)
  3. todo.txt (1.3 KB)
----------------------------------------

✅ Step 1 완료: 파일 목록을 성공적으로 찾았습니다!
💡 다음 단계에서는 이 파일들의 이름을 바꿔볼 예정입니다.
```

1. **명령행 인자 처리**: `sys.argv`로 사용자 입력 받기
2. **파일 패턴 매칭**: `glob` 모듈로 와일드카드 지원
3. **파일 정보 표시**: 크기와 개수 정보 제공
4. **도움말 시스템**: `-h` 옵션과 자동 도움말 표시

*Step 1에서는 Python의 기본 모듈들(`sys`, `os`, `glob`)을 사용해서 CLI 도구의 기초를 만들었습니다.*

## Step 2: 명령행 인자 처리와 옵션 파싱

이제 **전문적인 CLI 도구처럼 옵션을 처리하는 기능**<!-- -->을 추가해봅시다. Python의 `argparse` 모듈을 사용해서 전문적인 옵션 처리를 해보죠.

```python linenums="1" title="src/chapter3/step2_argparse.py"
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
```

### Step 2 실행해보기

이제 전문적인 CLI 옵션들을 사용해서 파일명을 바꿀 수 있습니다:

```bash
# 접두사 추가
$ python step2_argparse.py --prefix "new_" *.txt
📁 CLI 파일명 변경 도구 v2.0
========================================
📋 총 3개 파일 발견
✨ 작업: 접두사 'new_' 추가

👀 미리보기 (3개 파일):
============================================================
  readme.txt → new_readme.txt
  notes.txt → new_notes.txt
  todo.txt → new_todo.txt
============================================================
📊 바뀌는 파일: 3개 / 3개

실행하시겠습니까? (y/n): y

📊 결과:
  ✅ 성공: 3개

✨ 3개 파일의 이름이 성공적으로 변경되었습니다!

# Dry run 모드로 미리보기만
$ python step2_argparse.py --suffix "_backup" --dry-run *.py
👀 미리보기 (2개 파일):
============================================================
  script.py → script_backup.py
  test.py → test_backup.py
============================================================
🏃 Dry run 모드: 실제 변경은 수행되지 않았습니다.
```

**Step 2에서 배운 핵심 개념들:**

1. **argparse 모듈**: 전문적인 CLI 옵션 처리
2. **상호 배타적 그룹**: 하나의 작업만 선택 가능하도록
3. **Dry run 모드**: 안전한 미리보기 기능
4. **에러 핸들링**: 예외 상황 처리와 사용자 친화적 메시지
5. **사용자 확인**: 실제 변경 전 확인 절차

*Step 2에서는 argparse를 사용해서 진짜 CLI 도구처럼 동작하는 프로그램을 만들었습니다.*

## Step 3: 접두사/접미사 추가 기능

이제 **더 고급스러운 기능들**<!-- -->을 추가해봅시다. 백업 기능, 재귀적 검색, 그리고 더 안전한 파일 처리 기능들을 구현해보겠습니다.

```python linenums="1" title="src/chapter3/step3_prefix_suffix.py"
import sys
import os
import argparse
import shutil
from pathlib import Path
import glob
from datetime import datetime

class AdvancedCLIRenamer:
    """고급 CLI 파일명 변경 도구"""
    
    def __init__(self):
        self.files = []
        self.backup_dir = None
        self.setup_argparse()
    
    def setup_argparse(self):
        """argparse 설정"""
        self.parser = argparse.ArgumentParser(
            prog='renamer-advanced',
            description='🚀 고급 CLI 파일명 변경 도구',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
사용 예시:
  %(prog)s --prefix "new_" *.txt                    # 접두사 추가
  %(prog)s --suffix "_backup" --recursive src/      # 재귀적 접미사 추가
  %(prog)s --prefix "photo_" --backup ./backups/ *.jpg  # 백업과 함께
  %(prog)s --case upper *.py                        # 대소문자 변경
            """
        )
        
        # 파일 패턴
        self.parser.add_argument(
            'files', nargs='+',
            help='대상 파일 패턴들'
        )
        
        # 작업 유형
        action_group = self.parser.add_mutually_exclusive_group(required=True)
        action_group.add_argument('--prefix', '-p', help='접두사 추가')
        action_group.add_argument('--suffix', '-s', help='접미사 추가') 
        action_group.add_argument('--case', choices=['upper', 'lower', 'title'], 
                                 help='대소문자 변경')
        
        # 고급 옵션
        self.parser.add_argument('--recursive', '-r', action='store_true',
                               help='하위 디렉토리까지 재귀적 검색')
        self.parser.add_argument('--backup', metavar='DIR',
                               help='변경 전 백업 디렉토리')
        self.parser.add_argument('--dry-run', '-n', action='store_true',
                               help='미리보기만 표시')
        self.parser.add_argument('--force', '-f', action='store_true',
                               help='확인 없이 실행')
        self.parser.add_argument('--verbose', '-v', action='store_true',
                               help='상세 정보 출력')
        self.parser.add_argument('--extension', '-e', action='append',
                               help='특정 확장자만 처리 (예: -e .txt -e .py)')
    
    def find_files(self, patterns, recursive=False, extensions=None, verbose=False):
        """파일 찾기 (재귀적 옵션 포함)"""
        self.files = []
        
        if verbose:
            print(f"🔍 파일 검색 {'(재귀적)' if recursive else '(현재 디렉토리만)'}...")
        
        for pattern in patterns:
            if recursive:
                # 재귀적 검색을 위해 **/ 패턴 사용
                if not pattern.startswith('**/'):
                    pattern = f"**/{pattern}"
                matched_files = glob.glob(pattern, recursive=True)
            else:
                matched_files = glob.glob(pattern)
            
            for file_path in matched_files:
                if os.path.isfile(file_path):
                    abs_path = os.path.abspath(file_path)
                    
                    # 확장자 필터 적용
                    if extensions:
                        file_ext = os.path.splitext(abs_path)[1].lower()
                        if file_ext not in extensions:
                            continue
                    
                    if abs_path not in self.files:
                        self.files.append(abs_path)
        
        if verbose:
            print(f"📋 총 {len(self.files)}개 파일 발견")
            if extensions:
                print(f"🔧 필터링된 확장자: {', '.join(extensions)}")
        
        return len(self.files)
    
    def create_backup(self, file_path, backup_dir, verbose=False):
        """파일 백업 생성"""
        if not backup_dir:
            return True
        
        try:
            # 백업 디렉토리 생성
            os.makedirs(backup_dir, exist_ok=True)
            
            # 백업 파일명 (타임스탬프 포함)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            backup_filename = f"{name}_{timestamp}{ext}"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # 파일 복사
            shutil.copy2(file_path, backup_path)
            
            if verbose:
                print(f"  💾 백업: {backup_filename}")
            
            return True
            
        except Exception as e:
            print(f"❌ 백업 실패 {filename}: {e}")
            return False
    
    def generate_new_names(self, operation, value):
        """새로운 파일명 생성"""
        rename_plan = []
        
        for file_path in self.files:
            directory = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            
            if operation == 'prefix':
                new_name = f"{value}{filename}"
            elif operation == 'suffix':
                new_name = f"{name}{value}{ext}"
            elif operation == 'case':
                if value == 'upper':
                    new_name = filename.upper()
                elif value == 'lower':
                    new_name = filename.lower()
                elif value == 'title':
                    new_name = f"{name.title()}{ext}"
            else:
                new_name = filename
            
            new_path = os.path.join(directory, new_name)
            rename_plan.append((file_path, new_path))
        
        return rename_plan
    
    def show_preview(self, rename_plan, verbose=False):
        """미리보기 표시"""
        if not rename_plan:
            print("❌ 변경할 파일이 없습니다.")
            return
        
        print(f"\n👀 변경 미리보기 ({len(rename_plan)}개 파일):")
        print("=" * 70)
        
        changes = 0
        unchanged = 0
        
        for old_path, new_path in rename_plan:
            old_name = os.path.basename(old_path)
            new_name = os.path.basename(new_path)
            
            if old_name != new_name:
                if verbose:
                    # 전체 경로 표시
                    print(f"  📂 {old_path}")
                    print(f"  ➡️  {new_path}")
                    print()
                else:
                    print(f"  {old_name} → {new_name}")
                changes += 1
            else:
                if verbose:
                    print(f"  ➖ {old_name} (변경없음)")
                unchanged += 1
        
        print("=" * 70)
        print(f"📊 변경: {changes}개, 변경없음: {unchanged}개")
        
        if self.backup_dir:
            print(f"💾 백업 위치: {os.path.abspath(self.backup_dir)}")
    
    def execute_rename(self, rename_plan, backup_dir=None, verbose=False):
        """파일명 변경 실행"""
        if not rename_plan:
            return 0, []
        
        success_count = 0
        errors = []
        
        print("\n⚙️ 파일명 변경 실행 중...")
        
        for i, (old_path, new_path) in enumerate(rename_plan, 1):
            if old_path == new_path:
                continue
            
            try:
                # 진행률 표시
                if verbose:
                    print(f"  [{i}/{len(rename_plan)}] {os.path.basename(old_path)}")
                
                # 백업 생성
                if backup_dir:
                    if not self.create_backup(old_path, backup_dir, verbose):
                        errors.append(f"{os.path.basename(old_path)}: 백업 실패")
                        continue
                
                # 대상 파일 존재 확인
                if os.path.exists(new_path):
                    errors.append(f"{os.path.basename(old_path)}: 대상 파일이 이미 존재")
                    continue
                
                # 파일명 변경
                os.rename(old_path, new_path)
                success_count += 1
                
                if verbose:
                    print(f"    ✅ → {os.path.basename(new_path)}")
                
            except Exception as e:
                error_msg = f"{os.path.basename(old_path)}: {e}"
                errors.append(error_msg)
                
                if verbose:
                    print(f"    ❌ {error_msg}")
        
        return success_count, errors
    
    def run(self, args=None):
        """프로그램 실행"""
        try:
            parsed_args = self.parser.parse_args(args)
            
            print("🚀 고급 CLI 파일명 변경 도구 v3.0")
            print("=" * 50)
            
            # 확장자 처리
            extensions = None
            if parsed_args.extension:
                extensions = [ext if ext.startswith('.') else f'.{ext}' 
                             for ext in parsed_args.extension]
            
            # 파일 찾기
            file_count = self.find_files(
                parsed_args.files, 
                parsed_args.recursive,
                extensions,
                parsed_args.verbose
            )
            
            if file_count == 0:
                print("❌ 조건에 맞는 파일이 없습니다.")
                return 1
            
            # 백업 디렉토리 설정
            self.backup_dir = parsed_args.backup
            
            # 작업 유형 결정
            if parsed_args.prefix:
                operation, value = 'prefix', parsed_args.prefix
                print(f"✨ 작업: 접두사 '{value}' 추가")
            elif parsed_args.suffix:
                operation, value = 'suffix', parsed_args.suffix
                print(f"✨ 작업: 접미사 '{value}' 추가")
            elif parsed_args.case:
                operation, value = 'case', parsed_args.case
                print(f"✨ 작업: 대소문자를 {value}로 변경")
            
            # 변경 계획 생성
            rename_plan = self.generate_new_names(operation, value)
            
            # 미리보기
            self.show_preview(rename_plan, parsed_args.verbose)
            
            # Dry run 모드
            if parsed_args.dry_run:
                print("\n🏃 Dry run 모드: 실제 변경은 수행되지 않았습니다.")
                return 0
            
            # 사용자 확인
            if not parsed_args.force:
                try:
                    response = input("\n실행하시겠습니까? (y/n): ").strip().lower()
                    if response not in ['y', 'yes', '예']:
                        print("❌ 사용자가 취소했습니다.")
                        return 0
                except KeyboardInterrupt:
                    print("\n❌ 사용자가 중단했습니다.")
                    return 130
            
            # 실행
            success_count, errors = self.execute_rename(
                rename_plan, self.backup_dir, parsed_args.verbose
            )
            
            # 결과 보고
            print(f"\n📊 실행 결과:")
            print(f"  ✅ 성공: {success_count}개")
            if errors:
                print(f"  ❌ 실패: {len(errors)}개")
                if parsed_args.verbose:
                    for error in errors:
                        print(f"    - {error}")
            
            if success_count > 0:
                print(f"\n🎉 {success_count}개 파일의 이름이 성공적으로 변경되었습니다!")
                if self.backup_dir:
                    print(f"💾 백업이 {self.backup_dir}에 저장되었습니다.")
                return 0
            else:
                return 1
                
        except KeyboardInterrupt:
            print("\n❌ 사용자가 중단했습니다.")
            return 130
        except Exception as e:
            print(f"❌ 오류: {e}")
            return 1

def main():
    renamer = AdvancedCLIRenamer()
    exit_code = renamer.run()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
```

### Step 3에서 추가된 고급 기능들

```bash
# 백업과 함께 접두사 추가
$ python step3_prefix_suffix.py --prefix "new_" --backup ./backups/ *.txt

# 재귀적으로 모든 하위 폴더의 파일 처리
$ python step3_prefix_suffix.py --suffix "_old" --recursive src/

# 특정 확장자만 처리
$ python step3_prefix_suffix.py --prefix "img_" -e .jpg -e .png photos/

# 대소문자 변경
$ python step3_prefix_suffix.py --case upper *.py
```

**Step 3의 핵심 개념들:**

1. **백업 시스템**: 변경 전 파일을 안전하게 보관
2. **재귀적 검색**: 하위 디렉토리까지 처리
3. **확장자 필터링**: 특정 파일 타입만 선택적 처리
4. **진행률 표시**: 사용자 경험 개선
5. **에러 수집**: 실패한 파일들을 추적하고 보고

## Step 4: 찾기/바꾸기 기능 구현

이제 **정규표현식을 지원하는 강력한 찾기/바꾸기 기능**<!-- -->과 **연번 매기기 기능**<!-- -->을 추가해봅시다.

```python linenums="1" title="src/chapter3/step4_find_replace.py"
import sys
import os
import argparse
import re
import shutil
from pathlib import Path
import glob
from datetime import datetime

class PowerfulCLIRenamer:
    """강력한 찾기/바꾸기 기능을 가진 CLI 도구"""
    
    def __init__(self):
        self.files = []
        self.backup_dir = None
        self.setup_argparse()
    
    def setup_argparse(self):
        """argparse 설정"""
        self.parser = argparse.ArgumentParser(
            prog='renamer-powerful',
            description='💪 강력한 CLI 파일명 변경 도구',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
고급 사용 예시:
  %(prog)s --find "IMG" --replace "Photo" *.jpg           # 단순 찾기/바꾸기
  %(prog)s --regex "(\d+)" --replace "pic_\\1" *.jpg      # 정규식 사용
  %(prog)s --number --start 1 --digits 3 *.mp3           # 연번 매기기
  %(prog)s --remove-spaces *.txt                         # 공백 제거
  %(prog)s --find "old" --replace "new" --ignore-case *.* # 대소문자 무시
            """
        )
        
        # 파일 패턴
        self.parser.add_argument('files', nargs='+', help='대상 파일 패턴들')
        
        # 작업 유형 (상호 배타적)
        action_group = self.parser.add_mutually_exclusive_group(required=True)
        action_group.add_argument('--find', help='찾을 문자열')
        action_group.add_argument('--regex', help='찾을 정규표현식 패턴')
        action_group.add_argument('--number', action='store_true', help='연번 매기기')
        action_group.add_argument('--remove-spaces', action='store_true', 
                                help='공백을 언더스코어로 변경')
        action_group.add_argument('--prefix', help='접두사 추가')
        action_group.add_argument('--suffix', help='접미사 추가')
        
        # 찾기/바꾸기 관련 옵션
        self.parser.add_argument('--replace', help='바꿀 문자열')
        self.parser.add_argument('--ignore-case', '-i', action='store_true',
                               help='대소문자 구분 안함')
        
        # 연번 매기기 옵션
        self.parser.add_argument('--start', type=int, default=1,
                               help='연번 시작 숫자 (기본값: 1)')
        self.parser.add_argument('--digits', type=int, default=2,
                               help='연번 자릿수 (기본값: 2)')
        self.parser.add_argument('--number-format', default='{number}_{name}',
                               help='연번 형식 (기본값: {number}_{name})')
        
        # 기타 옵션
        self.parser.add_argument('--recursive', '-r', action='store_true')
        self.parser.add_argument('--backup', metavar='DIR', help='백업 디렉토리')
        self.parser.add_argument('--dry-run', '-n', action='store_true')
        self.parser.add_argument('--force', '-f', action='store_true')
        self.parser.add_argument('--verbose', '-v', action='store_true')
        self.parser.add_argument('--extension', '-e', action='append')
    
    def find_files(self, patterns, recursive=False, extensions=None, verbose=False):
        """파일 찾기"""
        self.files = []
        
        for pattern in patterns:
            if recursive:
                pattern = f"**/{pattern}" if not pattern.startswith('**/') else pattern
                matched_files = glob.glob(pattern, recursive=True)
            else:
                matched_files = glob.glob(pattern)
            
            for file_path in matched_files:
                if os.path.isfile(file_path):
                    abs_path = os.path.abspath(file_path)
                    
                    if extensions:
                        file_ext = os.path.splitext(abs_path)[1].lower()
                        if file_ext not in extensions:
                            continue
                    
                    if abs_path not in self.files:
                        self.files.append(abs_path)
        
        # 파일명으로 정렬 (연번 매기기를 위해)
        self.files.sort(key=lambda x: os.path.basename(x).lower())
        
        if verbose:
            print(f"📋 총 {len(self.files)}개 파일 발견 (정렬됨)")
        
        return len(self.files)
    
    def generate_new_names(self, args):
        """새로운 파일명 생성"""
        rename_plan = []
        
        for index, file_path in enumerate(self.files):
            directory = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            
            new_name = filename
            
            if args.find or args.regex:
                # 찾기/바꾸기 또는 정규식
                replace_text = args.replace or ""
                
                if args.regex:
                    # 정규표현식 모드
                    flags = re.IGNORECASE if args.ignore_case else 0
                    try:
                        new_name = re.sub(args.regex, replace_text, filename, flags=flags)
                    except re.error as e:
                        print(f"❌ 정규식 오류: {e}")
                        new_name = filename
                
                elif args.find:
                    # 단순 찾기/바꾸기
                    if args.ignore_case:
                        # 대소문자 무시 찾기/바꾸기
                        pattern = re.escape(args.find)
                        new_name = re.sub(pattern, replace_text, filename, flags=re.IGNORECASE)
                    else:
                        new_name = filename.replace(args.find, replace_text)
            
            elif args.number:
                # 연번 매기기
                number = args.start + index
                number_str = f"{number:0{args.digits}d}"
                
                # 연번 형식 적용
                format_vars = {
                    'number': number_str,
                    'name': name,
                    'ext': ext[1:] if ext else '',  # 점 제거
                    'original': filename
                }
                
                try:
                    new_name = args.number_format.format(**format_vars)
                    if not new_name.endswith(ext) and ext:
                        new_name += ext
                except KeyError as e:
                    print(f"❌ 형식 오류: {e}")
                    new_name = f"{number_str}_{filename}"
            
            elif args.remove_spaces:
                # 공백 제거
                new_name = filename.replace(' ', '_')
                # 연속된 언더스코어 정리
                new_name = re.sub(r'_+', '_', new_name)
            
            elif args.prefix:
                new_name = f"{args.prefix}{filename}"
            
            elif args.suffix:
                new_name = f"{name}{args.suffix}{ext}"
            
            new_path = os.path.join(directory, new_name)
            rename_plan.append((file_path, new_path))
        
        return rename_plan
    
    def validate_rename_plan(self, rename_plan):
        """변경 계획 검증"""
        issues = []
        new_names = []
        
        for old_path, new_path in rename_plan:
            new_name = os.path.basename(new_path)
            
            # 빈 파일명 체크
            if not new_name or new_name in ['.', '..']:
                issues.append(f"{os.path.basename(old_path)}: 잘못된 파일명")
                continue
            
            # 중복 파일명 체크
            if new_name in new_names:
                issues.append(f"{new_name}: 중복 파일명")
            else:
                new_names.append(new_name)
            
            # 파일명 길이 체크 (Windows 기준)
            if len(new_name) > 255:
                issues.append(f"{new_name}: 파일명이 너무 김")
            
            # 금지된 문자 체크 (Windows)
            forbidden_chars = r'<>:"/\|?*'
            if any(char in new_name for char in forbidden_chars):
                issues.append(f"{new_name}: 금지된 문자 포함")
        
        return issues
    
    def show_preview(self, rename_plan, verbose=False):
        """미리보기 표시"""
        if not rename_plan:
            print("❌ 변경할 파일이 없습니다.")
            return
        
        print(f"\n👀 변경 미리보기 ({len(rename_plan)}개 파일):")
        print("=" * 80)
        
        changes = 0
        for i, (old_path, new_path) in enumerate(rename_plan):
            old_name = os.path.basename(old_path)
            new_name = os.path.basename(new_path)
            
            if old_name != new_name:
                if verbose:
                    print(f"  {i+1:3d}. {old_name}")
                    print(f"       ➡️  {new_name}")
                else:
                    print(f"  {i+1:3d}. {old_name} → {new_name}")
                changes += 1
            else:
                if verbose:
                    print(f"  {i+1:3d}. {old_name} (변경없음)")
        
        print("=" * 80)
        print(f"📊 변경될 파일: {changes}개 / {len(rename_plan)}개")
    
    def execute_rename(self, rename_plan, backup_dir=None, verbose=False):
        """파일명 변경 실행"""
        if not rename_plan:
            return 0, []
        
        success_count = 0
        errors = []
        
        print("\n⚙️ 파일명 변경 실행 중...")
        
        for i, (old_path, new_path) in enumerate(rename_plan, 1):
            if old_path == new_path:
                continue
            
            try:
                if verbose:
                    print(f"  [{i}/{len(rename_plan)}] {os.path.basename(old_path)}")
                
                # 백업 생성
                if backup_dir:
                    os.makedirs(backup_dir, exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_name = f"{os.path.basename(old_path)}_{timestamp}"
                    backup_path = os.path.join(backup_dir, backup_name)
                    shutil.copy2(old_path, backup_path)
                
                # 대상 파일 존재 확인
                if os.path.exists(new_path):
                    errors.append(f"{os.path.basename(old_path)}: 대상 파일이 이미 존재")
                    continue
                
                # 파일명 변경
                os.rename(old_path, new_path)
                success_count += 1
                
                if verbose:
                    print(f"    ✅ → {os.path.basename(new_path)}")
                
            except Exception as e:
                error_msg = f"{os.path.basename(old_path)}: {e}"
                errors.append(error_msg)
                if verbose:
                    print(f"    ❌ {error_msg}")
        
        return success_count, errors
    
    def run(self, args=None):
        """프로그램 실행"""
        try:
            parsed_args = self.parser.parse_args(args)
            
            print("💪 강력한 CLI 파일명 변경 도구 v4.0")
            print("=" * 50)
            
            # 인자 검증
            if (parsed_args.find or parsed_args.regex) and not parsed_args.replace:
                print("❌ --find 또는 --regex 사용 시 --replace가 필요합니다.")
                return 1
            
            # 확장자 처리
            extensions = None
            if parsed_args.extension:
                extensions = [ext if ext.startswith('.') else f'.{ext}' 
                             for ext in parsed_args.extension]
            
            # 파일 찾기
            file_count = self.find_files(
                parsed_args.files,
                parsed_args.recursive,
                extensions,
                parsed_args.verbose
            )
            
            if file_count == 0:
                print("❌ 조건에 맞는 파일이 없습니다.")
                return 1
            
            # 작업 설명
            if parsed_args.find:
                print(f"✨ 작업: '{parsed_args.find}' → '{parsed_args.replace}' 바꾸기")
                if parsed_args.ignore_case:
                    print("  (대소문자 구분 안함)")
            elif parsed_args.regex:
                print(f"✨ 작업: 정규식 '{parsed_args.regex}' → '{parsed_args.replace}'")
            elif parsed_args.number:
                print(f"✨ 작업: 연번 매기기 (시작: {parsed_args.start}, 자릿수: {parsed_args.digits})")
                print(f"  형식: {parsed_args.number_format}")
            elif parsed_args.remove_spaces:
                print("✨ 작업: 공백을 언더스코어로 변경")
            elif parsed_args.prefix:
                print(f"✨ 작업: 접두사 '{parsed_args.prefix}' 추가")
            elif parsed_args.suffix:
                print(f"✨ 작업: 접미사 '{parsed_args.suffix}' 추가")
            
            # 변경 계획 생성
            rename_plan = self.generate_new_names(parsed_args)
            
            # 변경 계획 검증
            issues = self.validate_rename_plan(rename_plan)
            if issues:
                print(f"\n⚠️ 검증 실패 ({len(issues)}개 문제):")
                for issue in issues[:5]:  # 최대 5개만 표시
                    print(f"  - {issue}")
                if len(issues) > 5:
                    print(f"  ... 및 {len(issues)-5}개 추가 문제")
                return 1
            
            # 미리보기
            self.show_preview(rename_plan, parsed_args.verbose)
            
            # Dry run 모드
            if parsed_args.dry_run:
                print("\n🏃 Dry run 모드: 실제 변경은 수행되지 않았습니다.")
                return 0
            
            # 사용자 확인
            if not parsed_args.force:
                try:
                    response = input("\n실행하시겠습니까? (y/n): ").strip().lower()
                    if response not in ['y', 'yes', '예']:
                        print("❌ 사용자가 취소했습니다.")
                        return 0
                except KeyboardInterrupt:
                    print("\n❌ 사용자가 중단했습니다.")
                    return 130
            
            # 실행
            success_count, errors = self.execute_rename(
                rename_plan, parsed_args.backup, parsed_args.verbose
            )
            
            # 결과 보고
            print(f"\n📊 실행 결과:")
            print(f"  ✅ 성공: {success_count}개")
            if errors:
                print(f"  ❌ 실패: {len(errors)}개")
                if parsed_args.verbose:
                    for error in errors:
                        print(f"    - {error}")
            
            if success_count > 0:
                print(f"\n🎉 {success_count}개 파일의 이름이 성공적으로 변경되었습니다!")
                return 0
            else:
                return 1
                
        except KeyboardInterrupt:
            print("\n❌ 사용자가 중단했습니다.")
            return 130
        except Exception as e:
            print(f"❌ 오류: {e}")
            return 1

def main():
    renamer = PowerfulCLIRenamer()
    exit_code = renamer.run()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
```

### Step 4의 강력한 기능들 사용하기

```bash
# 정규표현식으로 복잡한 패턴 변경
$ python step4_find_replace.py --regex "IMG_(\d+)" --replace "photo_\1" *.jpg
✨ 작업: 정규식 'IMG_(\d+)' → 'photo_\1'
  IMG_001.jpg → photo_001.jpg
  IMG_055.jpg → photo_055.jpg

# 연번 매기기
$ python step4_find_replace.py --number --start 1 --digits 3 *.mp3
✨ 작업: 연번 매기기 (시작: 1, 자릿수: 3)
  song1.mp3 → 001_song1.mp3
  song2.mp3 → 002_song2.mp3

# 커스텀 연번 형식
$ python step4_find_replace.py --number --number-format "Track_{number}_{name}" *.mp3

# 공백 제거
$ python step4_find_replace.py --remove-spaces "My Document.txt"
  My Document.txt → My_Document.txt
```

**Step 4의 핵심 개념들:**

1. **정규표현식**: 복잡한 패턴 매칭과 그룹 참조
2. **연번 매기기**: 파일들에 순서대로 번호 부여
3. **파일명 검증**: 잘못된 파일명과 중복 방지
4. **커스텀 형식**: 사용자 정의 파일명 패턴
5. **고급 옵션**: 대소문자 무시, 특수문자 처리

## Step 5: 완성된 CLI 도구와 고급 기능

마지막으로 **프로페셔널한 CLI 도구의 모든 기능**<!-- -->을 포함한 완성된 버전을 만들어봅시다.

```python linenums="1" title="src/chapter3/step5_complete.py"
#!/usr/bin/env python3
"""
완성된 CLI 파일명 변경 도구
모든 기능을 포함한 최종 버전
"""

import sys
import os
import argparse
import re
import shutil
import json
import logging
from pathlib import Path
import glob
from datetime import datetime
from typing import List, Tuple, Dict, Optional

class CompleteRenamer:
    """완성된 CLI 파일명 변경 도구"""
    
    def __init__(self):
        self.files = []
        self.config = self.load_config()
        self.setup_logging()
        self.setup_argparse()
    
    def load_config(self):
        """설정 파일 로드"""
        config_file = Path.home() / '.renamer_config.json'
        default_config = {
            'backup_dir': None,
            'default_extensions': [],
            'verbose': False,
            'confirm_threshold': 10,
            'max_filename_length': 255
        }
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except Exception:
                pass
        
        return default_config
    
    def setup_logging(self):
        """로깅 설정"""
        log_level = logging.DEBUG if self.config.get('verbose') else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('renamer.log'),
                logging.StreamHandler() if self.config.get('verbose') else logging.NullHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_argparse(self):
        """argparse 설정"""
        self.parser = argparse.ArgumentParser(
            prog='renamer',
            description='🚀 완성된 CLI 파일명 변경 도구',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
완성된 기능들:
  기본 작업:
    --prefix TEXT                     접두사 추가
    --suffix TEXT                     접미사 추가
    --find TEXT --replace TEXT        찾기/바꾸기
    --regex PATTERN --replace TEXT    정규식 찾기/바꾸기
    --number                          연번 매기기
    --remove-spaces                   공백 제거
    --case {upper,lower,title}        대소문자 변경
  
  고급 작업:
    --template TEMPLATE               템플릿 기반 이름 변경
    --sanitize                        파일명 정리 (특수문자 제거)
    --truncate LENGTH                 파일명 길이 제한
  
  필터 옵션:
    --extension EXT                   특정 확장자만 처리
    --min-size SIZE                   최소 파일 크기
    --max-size SIZE                   최대 파일 크기
    --modified-after DATE             수정 날짜 이후
    --modified-before DATE            수정 날짜 이전
  
  안전 옵션:
    --backup DIR                      백업 디렉토리
    --dry-run                         미리보기만
    --interactive                     각 파일마다 확인
    --undo BACKUP_DIR                 변경 취소
  
사용 예시:
  renamer --prefix "img_" *.jpg                          # 기본 사용
  renamer --regex "(\d+)" --replace "pic_\\1" *.jpg      # 정규식
  renamer --number --template "{number:03d}_{name}" *    # 템플릿
  renamer --sanitize --max-size 10MB documents/         # 필터링
  renamer --undo ./backups/20231201_143022/             # 취소
            """
        )
        
        # 파일 패턴
        self.parser.add_argument('files', nargs='*', 
                               help='대상 파일 패턴들 (미지정시 현재 디렉토리)')
        
        # 기본 작업 (상호 배타적)
        action_group = self.parser.add_mutually_exclusive_group()
        action_group.add_argument('--prefix', help='접두사 추가')
        action_group.add_argument('--suffix', help='접미사 추가')
        action_group.add_argument('--find', help='찾을 문자열')
        action_group.add_argument('--regex', help='정규식 패턴')
        action_group.add_argument('--number', action='store_true', help='연번 매기기')
        action_group.add_argument('--remove-spaces', action='store_true', help='공백 제거')
        action_group.add_argument('--case', choices=['upper', 'lower', 'title'], help='대소문자 변경')
        action_group.add_argument('--template', help='템플릿 형식 (예: {number:03d}_{name})')
        action_group.add_argument('--sanitize', action='store_true', help='파일명 정리')
        action_group.add_argument('--undo', metavar='BACKUP_DIR', help='변경 취소')
        
        # 관련 옵션
        self.parser.add_argument('--replace', help='바꿀 문자열')
        self.parser.add_argument('--ignore-case', '-i', action='store_true')
        self.parser.add_argument('--truncate', type=int, help='파일명 최대 길이')
        
        # 연번 옵션
        self.parser.add_argument('--start', type=int, default=1, help='연번 시작')
        self.parser.add_argument('--step', type=int, default=1, help='연번 증가폭')
        self.parser.add_argument('--digits', type=int, default=3, help='연번 자릿수')
        
        # 필터 옵션
        self.parser.add_argument('--extension', '-e', action='append', help='처리할 확장자')
        self.parser.add_argument('--min-size', help='최소 파일 크기 (예: 1MB)')
        self.parser.add_argument('--max-size', help='최대 파일 크기 (예: 10MB)')
        self.parser.add_argument('--modified-after', help='수정 날짜 이후 (YYYY-MM-DD)')
        self.parser.add_argument('--modified-before', help='수정 날짜 이전 (YYYY-MM-DD)')
        
        # 기타 옵션
        self.parser.add_argument('--recursive', '-r', action='store_true')
        self.parser.add_argument('--backup', help='백업 디렉토리')
        self.parser.add_argument('--dry-run', '-n', action='store_true')
        self.parser.add_argument('--force', '-f', action='store_true')
        self.parser.add_argument('--interactive', action='store_true')
        self.parser.add_argument('--verbose', '-v', action='store_true')
        self.parser.add_argument('--quiet', '-q', action='store_true')
        self.parser.add_argument('--config', action='store_true', help='설정 정보 표시')
    
    def parse_size(self, size_str: str) -> int:
        """크기 문자열을 바이트로 변환"""
        if not size_str:
            return 0
        
        size_str = size_str.upper()
        multipliers = {
            'B': 1, 'K': 1024, 'KB': 1024,
            'M': 1024**2, 'MB': 1024**2,
            'G': 1024**3, 'GB': 1024**3
        }
        
        for suffix, multiplier in multipliers.items():
            if size_str.endswith(suffix):
                try:
                    number = float(size_str[:-len(suffix)])
                    return int(number * multiplier)
                except ValueError:
                    break
        
        try:
            return int(size_str)
        except ValueError:
            raise ValueError(f"잘못된 크기 형식: {size_str}")
    
    def parse_date(self, date_str: str) -> datetime:
        """날짜 문자열을 datetime으로 변환"""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"잘못된 날짜 형식: {date_str} (YYYY-MM-DD 형식 사용)")
    
    def matches_filters(self, file_path: str, args) -> bool:
        """파일이 필터 조건에 맞는지 확인"""
        try:
            stat = os.stat(file_path)
            
            # 크기 필터
            if args.min_size:
                min_bytes = self.parse_size(args.min_size)
                if stat.st_size < min_bytes:
                    return False
            
            if args.max_size:
                max_bytes = self.parse_size(args.max_size)
                if stat.st_size > max_bytes:
                    return False
            
            # 날짜 필터
            file_time = datetime.fromtimestamp(stat.st_mtime)
            
            if args.modified_after:
                after_date = self.parse_date(args.modified_after)
                if file_time < after_date:
                    return False
            
            if args.modified_before:
                before_date = self.parse_date(args.modified_before)
                if file_time > before_date:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.warning(f"필터 검사 실패 {file_path}: {e}")
            return False
    
    def find_files(self, patterns: List[str], args) -> int:
        """파일 찾기 (필터 적용)"""
        self.files = []
        
        # 패턴이 없으면 현재 디렉토리의 모든 파일
        if not patterns:
            patterns = ['*']
        
        for pattern in patterns:
            if args.recursive:
                pattern = f"**/{pattern}" if not pattern.startswith('**/') else pattern
                matched_files = glob.glob(pattern, recursive=True)
            else:
                matched_files = glob.glob(pattern)
            
            for file_path in matched_files:
                if not os.path.isfile(file_path):
                    continue
                
                abs_path = os.path.abspath(file_path)
                
                # 확장자 필터
                if args.extension:
                    file_ext = os.path.splitext(abs_path)[1].lower()
                    extensions = [ext if ext.startswith('.') else f'.{ext}' 
                                 for ext in args.extension]
                    if file_ext not in extensions:
                        continue
                
                # 기타 필터들
                if not self.matches_filters(abs_path, args):
                    continue
                
                if abs_path not in self.files:
                    self.files.append(abs_path)
        
        # 정렬
        self.files.sort(key=lambda x: os.path.basename(x).lower())
        return len(self.files)
    
    def generate_new_names(self, args) -> List[Tuple[str, str]]:
        """새로운 파일명 생성"""
        rename_plan = []
        
        for index, file_path in enumerate(self.files):
            directory = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            
            new_name = filename
            
            # 각 작업 유형별 처리
            if args.template:
                # 템플릿 기반
                variables = {
                    'name': name,
                    'ext': ext[1:] if ext else '',
                    'filename': filename,
                    'number': args.start + (index * args.step),
                    'index': index,
                    'dir': os.path.basename(directory)
                }
                try:
                    new_name = args.template.format(**variables)
                    if not new_name.endswith(ext) and ext:
                        new_name += ext
                except (KeyError, ValueError) as e:
                    self.logger.error(f"템플릿 오류: {e}")
                    continue
            
            elif args.sanitize:
                # 파일명 정리
                new_name = self.sanitize_filename(filename)
            
            elif args.find or args.regex:
                # 찾기/바꾸기
                replace_text = args.replace or ""
                if args.regex:
                    flags = re.IGNORECASE if args.ignore_case else 0
                    try:
                        new_name = re.sub(args.regex, replace_text, filename, flags=flags)
                    except re.error as e:
                        self.logger.error(f"정규식 오류: {e}")
                        continue
                else:
                    if args.ignore_case:
                        pattern = re.escape(args.find)
                        new_name = re.sub(pattern, replace_text, filename, flags=re.IGNORECASE)
                    else:
                        new_name = filename.replace(args.find, replace_text)
            
            elif args.number:
                # 연번 매기기
                number = args.start + (index * args.step)
                number_str = f"{number:0{args.digits}d}"
                new_name = f"{number_str}_{filename}"
            
            elif args.remove_spaces:
                new_name = re.sub(r'\s+', '_', filename)
            
            elif args.case:
                if args.case == 'upper':
                    new_name = filename.upper()
                elif args.case == 'lower':
                    new_name = filename.lower()
                elif args.case == 'title':
                    new_name = f"{name.title()}{ext}"
            
            elif args.prefix:
                new_name = f"{args.prefix}{filename}"
            
            elif args.suffix:
                new_name = f"{name}{args.suffix}{ext}"
            
            # 길이 제한
            if args.truncate:
                new_name = self.truncate_filename(new_name, args.truncate)
            
            new_path = os.path.join(directory, new_name)
            rename_plan.append((file_path, new_path))
        
        return rename_plan
    
    def sanitize_filename(self, filename: str) -> str:
        """파일명 정리 (특수문자 제거)"""
        # Windows 금지 문자 제거
        forbidden = r'<>:"/\|?*'
        for char in forbidden:
            filename = filename.replace(char, '_')
        
        # 연속된 공백/언더스코어 정리
        filename = re.sub(r'[\s_]+', '_', filename)
        
        # 앞뒤 공백/언더스코어 제거
        filename = filename.strip('_. ')
        
        return filename
    
    def truncate_filename(self, filename: str, max_length: int) -> str:
        """파일명 길이 제한"""
        if len(filename) <= max_length:
            return filename
        
        name, ext = os.path.splitext(filename)
        available_length = max_length - len(ext)
        
        if available_length <= 0:
            return filename[:max_length]
        
        return name[:available_length] + ext
    
    def create_backup(self, rename_plan: List[Tuple[str, str]], backup_dir: str) -> str:
        """변경 전 백업 생성"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, timestamp)
        os.makedirs(backup_path, exist_ok=True)
        
        # 변경 정보 저장
        backup_info = {
            'timestamp': timestamp,
            'changes': [(old, new) for old, new in rename_plan if old != new]
        }
        
        info_file = os.path.join(backup_path, 'backup_info.json')
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, ensure_ascii=False, indent=2)
        
        # 파일들 백업
        for old_path, new_path in rename_plan:
            if old_path != new_path:
                backup_file = os.path.join(backup_path, os.path.basename(old_path))
                shutil.copy2(old_path, backup_file)
        
        return backup_path
    
    def execute_undo(self, backup_dir: str) -> bool:
        """변경 취소"""
        info_file = os.path.join(backup_dir, 'backup_info.json')
        
        if not os.path.exists(info_file):
            print(f"❌ 백업 정보를 찾을 수 없습니다: {info_file}")
            return False
        
        try:
            with open(info_file, 'r', encoding='utf-8') as f:
                backup_info = json.load(f)
            
            print(f"🔄 변경 취소 중... (백업: {backup_info['timestamp']})")
            
            success_count = 0
            errors = []
            
            for old_path, new_path in backup_info['changes']:
                try:
                    if os.path.exists(new_path):
                        backup_file = os.path.join(backup_dir, os.path.basename(old_path))
                        if os.path.exists(backup_file):
                            os.rename(new_path, old_path)
                            success_count += 1
                        else:
                            errors.append(f"백업 파일 없음: {os.path.basename(old_path)}")
                    else:
                        errors.append(f"대상 파일 없음: {os.path.basename(new_path)}")
                        
                except Exception as e:
                    errors.append(f"{os.path.basename(old_path)}: {e}")
            
            print(f"📊 취소 결과: 성공 {success_count}개, 실패 {len(errors)}개")
            if errors:
                for error in errors[:5]:
                    print(f"  ❌ {error}")
            
            return success_count > 0
            
        except Exception as e:
            print(f"❌ 취소 실패: {e}")
            return False
    
    def show_config(self):
        """설정 정보 표시"""
        print("⚙️ 현재 설정:")
        print("=" * 40)
        for key, value in self.config.items():
            print(f"  {key}: {value}")
        print("=" * 40)
        print(f"설정 파일: {Path.home() / '.renamer_config.json'}")
        print(f"로그 파일: renamer.log")
    
    def run(self, args=None):
        """프로그램 실행"""
        try:
            parsed_args = self.parser.parse_args(args)
            
            # 설정 표시
            if parsed_args.config:
                self.show_config()
                return 0
            
            # 취소 작업
            if parsed_args.undo:
                return 0 if self.execute_undo(parsed_args.undo) else 1
            
            # 작업 검증
            needs_replace = parsed_args.find or parsed_args.regex
            if needs_replace and not parsed_args.replace:
                print("❌ --find 또는 --regex 사용 시 --replace가 필요합니다.")
                return 1
            
            if not any([parsed_args.prefix, parsed_args.suffix, parsed_args.find, 
                       parsed_args.regex, parsed_args.number, parsed_args.remove_spaces,
                       parsed_args.case, parsed_args.template, parsed_args.sanitize]):
                print("❌ 작업 유형을 지정해주세요.")
                self.parser.print_help()
                return 1
            
            # 출력 레벨 설정
            if not parsed_args.quiet:
                print("🚀 완성된 CLI 파일명 변경 도구 v5.0")
                print("=" * 50)
            
            # 파일 찾기
            file_count = self.find_files(parsed_args.files or [], parsed_args)
            
            if file_count == 0:
                if not parsed_args.quiet:
                    print("❌ 조건에 맞는 파일이 없습니다.")
                return 1
            
            if not parsed_args.quiet:
                print(f"📋 {file_count}개 파일 발견")
            
            # 변경 계획 생성
            rename_plan = self.generate_new_names(parsed_args)
            
            # 미리보기
            changes = sum(1 for old, new in rename_plan if old != new)
            if not parsed_args.quiet:
                print(f"📊 변경될 파일: {changes}개")
                
                # 상세 미리보기 (일부만)
                if changes > 0:
                    print("\n👀 미리보기:")
                    for i, (old_path, new_path) in enumerate(rename_plan[:10]):
                        if old_path != new_path:
                            old_name = os.path.basename(old_path)
                            new_name = os.path.basename(new_path)
                            print(f"  {old_name} → {new_name}")
                    
                    if changes > 10:
                        print(f"  ... 및 {changes-10}개 추가 변경")
            
            if changes == 0:
                if not parsed_args.quiet:
                    print("✅ 변경할 파일이 없습니다.")
                return 0
            
            # Dry run
            if parsed_args.dry_run:
                if not parsed_args.quiet:
                    print("\n🏃 Dry run 모드: 실제 변경은 수행되지 않았습니다.")
                return 0
            
            # 확인 (대화형 모드가 아닌 경우)
            if not parsed_args.force and not parsed_args.interactive:
                if changes >= self.config.get('confirm_threshold', 10):
                    try:
                        response = input(f"\n{changes}개 파일을 변경합니다. 계속하시겠습니까? (y/n): ")
                        if response.lower() not in ['y', 'yes', '예']:
                            print("❌ 사용자가 취소했습니다.")
                            return 0
                    except KeyboardInterrupt:
                        print("\n❌ 사용자가 중단했습니다.")
                        return 130
            
            # 백업 생성
            backup_path = None
            if parsed_args.backup or self.config.get('backup_dir'):
                backup_dir = parsed_args.backup or self.config['backup_dir']
                backup_path = self.create_backup(rename_plan, backup_dir)
                if not parsed_args.quiet:
                    print(f"💾 백업 생성: {backup_path}")
            
            # 실행
            success_count = 0
            errors = []
            
            if not parsed_args.quiet:
                print("\n⚙️ 파일명 변경 실행 중...")
            
            for old_path, new_path in rename_plan:
                if old_path == new_path:
                    continue
                
                # 대화형 확인
                if parsed_args.interactive:
                    old_name = os.path.basename(old_path)
                    new_name = os.path.basename(new_path)
                    try:
                        response = input(f"{old_name} → {new_name} 변경하시겠습니까? (y/n/q): ")
                        if response.lower() == 'q':
                            break
                        elif response.lower() not in ['y', 'yes', '예']:
                            continue
                    except KeyboardInterrupt:
                        break
                
                try:
                    if os.path.exists(new_path):
                        errors.append(f"{os.path.basename(old_path)}: 대상 파일이 이미 존재")
                        continue
                    
                    os.rename(old_path, new_path)
                    success_count += 1
                    
                    if parsed_args.verbose:
                        print(f"  ✅ {os.path.basename(old_path)} → {os.path.basename(new_path)}")
                    
                except Exception as e:
                    error_msg = f"{os.path.basename(old_path)}: {e}"
                    errors.append(error_msg)
                    self.logger.error(error_msg)
            
            # 결과 보고
            if not parsed_args.quiet:
                print(f"\n📊 실행 결과:")
                print(f"  ✅ 성공: {success_count}개")
                if errors:
                    print(f"  ❌ 실패: {len(errors)}개")
                    if parsed_args.verbose:
                        for error in errors:
                            print(f"    - {error}")
                
                if success_count > 0:
                    print(f"\n🎉 {success_count}개 파일의 이름이 성공적으로 변경되었습니다!")
                    if backup_path:
                        print(f"💾 백업: {backup_path}")
                        print(f"🔄 취소하려면: renamer --undo {backup_path}")
            
            return 0 if success_count > 0 else 1
            
        except KeyboardInterrupt:
            print("\n❌ 사용자가 중단했습니다.")
            return 130
        except Exception as e:
            print(f"❌ 오류: {e}")
            self.logger.error(f"Unexpected error: {e}", exc_info=True)
            return 1

def main():
    """메인 함수"""
    renamer = CompleteRenamer()
    exit_code = renamer.run()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
```

### Step 5 완성된 도구의 강력한 기능들

```bash
# 설정 확인
$ python step5_complete.py --config

# 템플릿 기반 이름 변경
$ python step5_complete.py --template "Photo_{number:04d}_{name}" *.jpg

# 고급 필터링
$ python step5_complete.py --sanitize --min-size 1MB --max-size 10MB photos/

# 대화형 모드
$ python step5_complete.py --prefix "backup_" --interactive *.txt

# 백업과 함께 변경
$ python step5_complete.py --find "old" --replace "new" --backup ./backups/ *

# 변경 취소
$ python step5_complete.py --undo ./backups/20231201_143022/
```

## 🎓 Chapter 3에서 배운 것들

### 핵심 Python 모듈들

1. **argparse**: 전문적인 CLI 인터페이스 구축
2. **glob**: 파일 패턴 매칭과 와일드카드 지원
3. **re**: 정규표현식을 통한 강력한 문자열 처리
4. **os/pathlib**: 파일 시스템 조작
5. **json**: 설정과 데이터 저장
6. **logging**: 전문적인 로깅 시스템

### CLI 도구 설계 원칙

1. **UNIX 철학**: 한 가지 일을 잘하는 도구
2. **사용자 경험**: 직관적인 옵션과 명확한 피드백
3. **안전성**: Dry run, 백업, 확인 절차
4. **확장성**: 설정 파일과 플러그인 구조
5. **에러 처리**: 친화적인 에러 메시지와 복구 방법

### 실용적인 프로그래밍 패턴

- **점진적 개발**: 간단한 기능부터 복잡한 기능까지
- **모듈화**: 각 기능을 독립적인 메서드로 분리
- **검증과 피드백**: 사용자 입력 검증과 명확한 결과 표시
- **설정 관리**: 사용자 설정과 기본값 처리

*Chapter 3에서는 Python 표준 라이브러리만으로 전문적인 CLI 도구를 만드는 방법을 배웠습니다. 다음 Chapter 4에서는 이 CLI 기능에 tkinter GUI를 추가해서 더욱 사용하기 쉬운 도구로 발전시켜보겠습니다!*