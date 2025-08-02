"""
Pytest configuration file for KRenamer tests
"""

import sys
from pathlib import Path

# Add src to path for all tests
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# pytest fixtures and configuration
import pytest


@pytest.fixture
def temp_files():
    """Fixture to provide temporary test files"""
    import tempfile
    import shutil
    
    temp_dir = Path(tempfile.mkdtemp())
    test_files = []
    
    # Create some test files
    for i in range(3):
        test_file = temp_dir / f"test_{i}.txt"
        test_file.write_text(f"Test content {i}")
        test_files.append(str(test_file))
    
    yield test_files, temp_dir
    
    # Cleanup
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


@pytest.fixture
def krenamer_engine():
    """Fixture to provide a clean RenameEngine instance"""
    from krenamer.core import RenameEngine
    return RenameEngine()