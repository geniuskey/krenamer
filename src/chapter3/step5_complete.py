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