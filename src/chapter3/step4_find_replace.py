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
