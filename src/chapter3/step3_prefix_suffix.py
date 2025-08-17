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
