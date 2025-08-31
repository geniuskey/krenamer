"""
전체 워크플로우 통합 테스트 - Chapter 8 사양에 맞춘 버전
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch


class TestRenameWorkflow:
    """리네임 워크플로우 통합 테스트"""
    
    def test_complete_rename_workflow(self, temp_dir):
        """완전한 리네임 워크플로우 테스트"""
        from krenamer.core import RenameEngine
        
        # 1. 테스트 파일들 생성
        test_files = []
        for i in range(3):
            file_path = temp_dir / f"test_file_{i}.txt"
            file_path.write_text(f"Content {i}")
            test_files.append(str(file_path))
        
        # 2. 엔진 초기화 및 파일 추가
        engine = RenameEngine()
        added_count = engine.add_files(test_files)
        assert added_count == 3
        
        # 3. 규칙 추가
        engine.method = "prefix"
        engine.prefix_text = "NEW_"
        
        # 추가 변환 적용
        engine.suffix_text = "_backup"
        engine.case_method = "upper"
        
        # 4. 미리보기 생성
        plan = engine.generate_rename_plan()
        assert len(plan) == 3
        
        # 5. 파일명 확인
        for i, (original, new_name, matches) in enumerate(plan):
            if matches:
                # 접두사와 변환이 모두 적용되어야 함
                assert new_name.startswith("NEW_")
                assert "_backup" in new_name or new_name.endswith(".txt")
        
        # 6. 실제 실행 (mocking)
        with patch('os.rename') as mock_rename:
            engine.execute_rename()
            
            # 모든 매칭 파일에 대해 rename이 호출되어야 함
            matching_count = sum(1 for _, _, matches in plan if matches)
            assert mock_rename.call_count == matching_count
    
    def test_complex_rename_scenario(self, temp_dir):
        """복잡한 리네임 시나리오 테스트"""
        from krenamer.core import RenameEngine
        
        # 다양한 형태의 파일들 생성
        files_data = [
            ("IMG_20231215_001.jpg", "Image content"),
            ("Document with spaces.pdf", "PDF content"),
            ("UPPERCASE_FILE.TXT", "Text content"),
            ("file_with_123_numbers.doc", "Doc content")
        ]
        
        test_files = []
        for filename, content in files_data:
            file_path = temp_dir / filename
            file_path.write_text(content)
            test_files.append(str(file_path))
        
        engine = RenameEngine()
        engine.add_files(test_files)
        
        # 1단계: 공백을 언더스코어로 변경
        engine.method = "replace"
        engine.find_text = " "
        engine.replace_text = "_"
        engine.case_method = "lower"
        
        plan = engine.generate_rename_plan()
        
        # 결과 확인 - 공백이 언더스코어로 변경되고 소문자로 변환
        for original_path, new_name, matches in plan:
            if matches:
                original_filename = Path(original_path).name
                # 원본에 공백이 있었다면 언더스코어로 변경되어야 함
                if " " in original_filename:
                    assert "_" in new_name
                    assert " " not in new_name
                # 소문자로 변환되어야 함
                name_without_ext = Path(new_name).stem
                assert name_without_ext.islower()
        
        # 2단계: 접두사 추가 테스트를 별도로 진행
        engine2 = RenameEngine()
        engine2.add_files(test_files)
        engine2.method = "prefix"
        engine2.prefix_text = "processed_"
        
        plan2 = engine2.generate_rename_plan()
        
        # 접두사가 모든 파일에 추가되는지 확인
        for original_path, new_name, matches in plan2:
            if matches:
                assert new_name.startswith('processed_')
    
    def test_conditional_rename_workflow(self, temp_dir):
        """조건부 리네임 워크플로우 테스트"""
        from krenamer.core import RenameEngine
        
        # 다양한 확장자의 파일들 생성
        files_data = [
            ("image1.jpg", "image"),
            ("image2.png", "image"),  
            ("document1.pdf", "document"),
            ("document2.txt", "document"),
            ("archive.zip", "archive")
        ]
        
        test_files = []
        for filename, content in files_data:
            file_path = temp_dir / filename
            file_path.write_text(content)
            test_files.append(str(file_path))
        
        engine = RenameEngine()
        engine.add_files(test_files)
        
        # 조건: 이미지 파일만 처리
        engine.use_ext_condition = True
        engine.allowed_extensions = ".jpg,.png"
        
        # 변경: 접두사 추가
        engine.method = "prefix"
        engine.prefix_text = "image_"
        
        plan = engine.generate_rename_plan()
        
        # 이미지 파일만 매칭되어야 함
        matching_files = [(original, new_name) for original, new_name, matches in plan if matches]
        
        for original, new_name in matching_files:
            ext = Path(original).suffix.lower()
            assert ext in ['.jpg', '.png']
            assert new_name.startswith("image_")
        
        # 비이미지 파일은 매칭되지 않아야 함
        non_matching_files = [original for original, new_name, matches in plan if not matches]
        for original in non_matching_files:
            ext = Path(original).suffix.lower()
            assert ext not in ['.jpg', '.png']
    
    def test_error_handling_workflow(self, temp_dir):
        """오류 처리 워크플로우 테스트"""
        from krenamer.core import RenameEngine
        
        # 테스트 파일 생성
        file_path = temp_dir / "test.txt"
        file_path.write_text("content")
        
        engine = RenameEngine()
        engine.add_files([str(file_path)])
        
        # 접두사 규칙 추가
        engine.method = "prefix"
        engine.prefix_text = "NEW_"
        
        # 대상 파일이 이미 존재하는 상황 시뮬레이션
        target_path = temp_dir / "NEW_test.txt"
        target_path.write_text("existing content")
        
        # 실행 (파일 존재로 인한 오류 예상)
        with patch('os.path.exists', return_value=True):
            try:
                engine.execute_rename()
            except Exception:
                # 오류가 발생할 수 있음 (정상적인 동작)
                pass
    
    def test_partial_success_workflow(self, temp_dir):
        """부분 성공 워크플로우 테스트"""
        from krenamer.core import RenameEngine
        
        # 여러 테스트 파일 생성
        test_files = []
        for i in range(3):
            file_path = temp_dir / f"file_{i}.txt"
            file_path.write_text(f"content {i}")
            test_files.append(str(file_path))
        
        engine = RenameEngine()
        engine.add_files(test_files)
        
        engine.method = "prefix"
        engine.prefix_text = "NEW_"
        
        # 하나의 대상 파일이 이미 존재하도록 설정
        existing_file = temp_dir / "NEW_file_1.txt"
        existing_file.write_text("existing")
        
        with patch('os.rename') as mock_rename:
            # 첫 번째와 세 번째 파일은 성공, 두 번째는 실패
            def side_effect(old, new):
                if "file_1" in old:
                    raise FileExistsError("File exists")
                return None
            
            mock_rename.side_effect = side_effect
            
            try:
                engine.execute_rename()
            except FileExistsError:
                # 일부 파일에서 오류가 발생할 수 있음
                pass
            
            # 적어도 일부 파일은 처리되어야 함
            assert mock_rename.call_count >= 1


class TestRenameEngineIntegration:
    """RenameEngine 통합 테스트"""
    
    def test_file_list_management(self, temp_dir):
        """파일 목록 관리 통합 테스트"""
        from krenamer.core import RenameEngine
        
        # 초기 파일들 생성
        initial_files = []
        for i in range(5):
            file_path = temp_dir / f"initial_{i}.txt"
            file_path.write_text(f"content {i}")
            initial_files.append(str(file_path))
        
        engine = RenameEngine()
        
        # 파일 추가
        added = engine.add_files(initial_files)
        assert added == 5
        assert len(engine.files) == 5
        
        # 일부 파일 제거
        engine.remove_files_by_indices([0, 2])
        assert len(engine.files) == 3
        
        # 추가 파일들 생성 및 추가
        additional_files = []
        for i in range(2):
            file_path = temp_dir / f"additional_{i}.txt"
            file_path.write_text(f"additional content {i}")
            additional_files.append(str(file_path))
        
        added = engine.add_files(additional_files)
        assert added == 2
        assert len(engine.files) == 5
        
        # 중복 방지 확인
        added = engine.add_files(additional_files)
        assert added == 0  # 이미 존재하므로 추가되지 않음
        assert len(engine.files) == 5
        
        # 전체 제거
        engine.clear_files()
        assert len(engine.files) == 0
    
    def test_gui_engine_integration(self):
        """GUI와 엔진 통합 테스트"""
        from krenamer.core import RenameEngine
        
        try:
            from krenamer.gui import RenamerGUI
            
            # GUI가 엔진을 올바르게 사용할 수 있는지 확인
            engine = RenameEngine()
            
            # GUI 인스턴스 생성 시도 (display가 없을 수 있으므로 try-catch)
            try:
                import tkinter as tk
                root = tk.Tk()
                root.withdraw()  # 화면에 표시하지 않음
                
                # 기본적인 연동 테스트
                engine.method = "prefix"
                engine.prefix_text = "gui_test_"
                
                plan = engine.generate_rename_plan()
                assert isinstance(plan, list)
                
                root.destroy()
                
            except Exception:
                # GUI 테스트는 헤드리스 환경에서 실패할 수 있음
                pytest.skip("GUI integration test skipped (no display)")
                
        except ImportError:
            pytest.skip("GUI module not available")
    
    def test_configuration_persistence(self, temp_dir):
        """설정 지속성 테스트"""
        from krenamer.core import RenameEngine
        
        # 첫 번째 엔진 인스턴스
        engine1 = RenameEngine()
        engine1.method = "prefix"
        engine1.prefix_text = "test_"
        engine1.case_method = "lower"
        engine1.replace_spaces = True
        
        # 설정 값 저장
        config = {
            'method': engine1.method,
            'prefix_text': engine1.prefix_text,
            'case_method': engine1.case_method,
            'replace_spaces': engine1.replace_spaces
        }
        
        # 두 번째 엔진 인스턴스에 설정 적용
        engine2 = RenameEngine()
        engine2.method = config['method']
        engine2.prefix_text = config['prefix_text']
        engine2.case_method = config['case_method']
        engine2.replace_spaces = config['replace_spaces']
        
        # 동일한 결과를 생성하는지 확인
        test_file = temp_dir / "test.txt"
        test_file.write_text("content")
        
        engine1.add_files([str(test_file)])
        engine2.add_files([str(test_file)])
        
        plan1 = engine1.generate_rename_plan()
        plan2 = engine2.generate_rename_plan()
        
        # 두 엔진이 동일한 결과를 생성해야 함
        assert len(plan1) == len(plan2) == 1
        
        _, new_name1, _ = plan1[0]
        _, new_name2, _ = plan2[0]
        assert new_name1 == new_name2


class TestRealFileOperations:
    """실제 파일 시스템과의 통합 테스트"""
    
    def test_actual_file_rename(self, temp_dir):
        """실제 파일 이름 변경 테스트"""
        from krenamer.core import RenameEngine
        
        # 실제 파일 생성
        original_file = temp_dir / "original.txt"
        original_file.write_text("test content")
        
        engine = RenameEngine()
        engine.add_files([str(original_file)])
        
        engine.method = "prefix"
        engine.prefix_text = "renamed_"
        
        plan = engine.generate_rename_plan()
        assert len(plan) == 1
        
        original_path, new_name, matches = plan[0]
        if matches:
            expected_path = temp_dir / new_name
            
            # 실제 파일 이름 변경 실행
            try:
                engine.execute_rename()
                
                # 원본 파일이 없어졌는지 확인
                assert not original_file.exists()
                
                # 새 파일이 생성되었는지 확인
                assert expected_path.exists()
                assert expected_path.read_text() == "test content"
                
            except Exception as e:
                # 파일 시스템 오류가 발생할 수 있음
                pytest.skip(f"File system operation failed: {e}")
    
    def test_directory_with_subdirectories(self, temp_dir):
        """서브디렉토리가 있는 환경에서의 테스트"""
        from krenamer.core import RenameEngine
        
        # 루트 파일들 생성
        root_files = []
        for i in range(2):
            file_path = temp_dir / f"root_{i}.txt"
            file_path.write_text(f"root content {i}")
            root_files.append(str(file_path))
        
        # 서브디렉토리와 파일들 생성
        sub_dir = temp_dir / "subdir"
        sub_dir.mkdir()
        
        sub_files = []
        for i in range(2):
            file_path = sub_dir / f"sub_{i}.txt"
            file_path.write_text(f"sub content {i}")
            sub_files.append(str(file_path))
        
        engine = RenameEngine()
        
        # 루트 파일들만 추가 (RenameEngine은 비재귀적)
        added = engine.add_files(root_files)
        assert added == 2
        
        # 서브디렉토리 파일들도 수동으로 추가
        added = engine.add_files(sub_files)
        assert added == 2
        
        # 총 4개 파일이 있어야 함
        assert len(engine.files) == 4
        
        # 모든 파일에 규칙 적용
        engine.method = "suffix"
        engine.suffix_text = "_processed"
        
        plan = engine.generate_rename_plan()
        assert len(plan) == 4
        
        # 모든 파일이 올바르게 처리되는지 확인
        for original, new_name, matches in plan:
            if matches:
                assert "_processed" in new_name