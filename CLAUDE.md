# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

KRenamer is a Korean Windows GUI file renaming tool built with Python tkinter. It supports drag & drop functionality, batch file renaming with various methods (prefix/suffix, numbering, find/replace, regex), conditional filtering, and real-time preview.

## Architecture

### Core Components

- `src/krenamer/core.py` - `RenameEngine` class containing all file processing logic, conditions, and renaming operations
- `src/krenamer/gui.py` - `RenameGUI` class managing the tkinter interface, drag & drop, and user interactions  
- `src/krenamer/main.py` - Application entry point and error handling

### Key Design Patterns

- Separation of Concerns: GUI logic is completely separate from file processing logic
- Engine-View Pattern: `RenameEngine` handles all business logic while `RenamerGUI` only manages UI
- Conditional Processing: Files are filtered through conditions before renaming operations

### Chapter-based Development Structure

This is an educational project with incremental development examples:
- `src/chapter1/` - Basic GUI structure
- `src/chapter2/` - Drag & drop functionality  
- `src/chapter3/` - File renaming logic
- `src/chapter4/` - Advanced conditional features
- `src/krenamer/` - Final complete version

## Development Commands

### Running the Application

```bash
# Run final version
cd src/krenamer && python main.py

# Run specific chapter version  
cd src/chapter1 && python main.py

# Run as installed package
python -m krenamer.main
```

### Installation & Setup

```bash
# Install dependencies
pip install tkinterdnd2

# Install package in development mode
pip install -e .

# Install for documentation building
pip install mkdocs mkdocs-material
```

### Testing

```bash
# Test basic functionality
python simple_test.py

# Test GUI with debugging
python test_gui.py

# Test package installation
python test_install.py
```

### Documentation

```bash
# Serve documentation locally
mkdocs serve
# Access at http://localhost:8000

# Build documentation
mkdocs build
```

## Important Implementation Details

### Drag & Drop Handling

The application uses `tkinterdnd2` for drag & drop functionality. The `setup_drag_drop()` method registers multiple targets (drop label, file tree, main window) for better reliability. File path parsing handles various formats including brace-wrapped paths.

### File Processing Pipeline

1. Files added to `RenameEngine.files` list
2. Conditions applied via `matches_conditions()` 
3. Rename plan generated with `generate_rename_plan()`
4. Duplicate handling and path updates in `execute_rename()`

### GUI State Management

The GUI uses tkinter StringVars and traces for real-time updates. The `refresh_file_list()` method rebuilds the file tree display whenever files are added/removed or conditions change.

### Error Handling

- Graceful degradation when `tkinterdnd2` is not available
- File operation errors are collected and reported to user
- GUI exceptions are caught with user-friendly messages

## Common Issues

- Filter mismatch: Ensure `display_filter` StringVar matches combo box values exactly
- Path updates: After renaming, file paths in `engine.files` must be updated to new locations
- Multiple windows: Avoid creating extra Tk instances; use single root window
- Korean fonts: Application uses "맑은 고딕" font; fallback handling may be needed

## Dependencies

- tkinter - Standard library GUI framework
- tkinterdnd2>=0.3.0 - Drag & drop functionality (optional but recommended)
- Python>=3.8 - Required version

## Build & Distribution

```bash
# Build package
python -m build

# Install from wheel
pip install dist/krenamer-1.0.0-py3-none-any.whl
```

The package installs a `renamer` command-line entry point that launches the GUI application.

## markdown 작성 시 주의 사항

- **Bold** 처리 직후 한국어 조사가 붙을 시 <!-- --> 빈 주석을 추가하여 Bold 가 깨지는 것을 방지합니다. 예를 들어 **볼드**<!-- -->는 주석이 수반되어야 해요.
- bullet list 혹은 number list 를 사용할 시 줄넘김이 직전 라인에 적용되어야 해요. 안 그러면 mkdocs 가 list 형태로 인식하지 못 합니다. 
- 삽화를 만들 때 필요한 코드들은 "src\chapter*" 에 넣어둡니다.
- .md 파일에서 markdown 코드를 삽입해야할 때는 4개의 backtick(````)으로 작성해줘. 