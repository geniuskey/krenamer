@echo off

REM KRenamer Build Script
REM Usage: make.bat [command]
REM
REM Available commands:
REM   exe       - Build standalone executable
REM   wheel     - Build wheel package
REM   sdist     - Build source distribution
REM   build     - Build both wheel and sdist
REM   install   - Install package in development mode
REM   docs      - Build documentation
REM   serve     - Serve documentation locally
REM   test      - Run tests
REM   clean     - Clean build artifacts
REM   publish   - Publish to PyPI (requires authentication)
REM   publish-test - Publish to TestPyPI
REM   help      - Show this help

setlocal EnableDelayedExpansion

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="exe" goto build_exe
if "%1"=="wheel" goto build_wheel
if "%1"=="sdist" goto build_sdist
if "%1"=="build" goto build_all
if "%1"=="install" goto install_dev
if "%1"=="docs" goto build_docs
if "%1"=="serve" goto serve_docs
if "%1"=="test" goto run_tests
if "%1"=="clean" goto clean
if "%1"=="publish" goto publish_pypi
if "%1"=="publish-test" goto publish_test
goto help

:build_exe
echo.
echo [BUILD] Building KRenamer executable...
echo =====================================
echo Installing PyInstaller if not available...
call pip install pyinstaller
if not exist "dist" mkdir dist
if not exist "build" mkdir build
echo.
echo Building executable with spec file...
call pyinstaller --clean krenamer.spec
if %errorlevel%==0 (
    echo.
    echo [SUCCESS] Executable built successfully!
    echo Location: dist\KRenamer.exe
    echo File size:
    for %%f in (dist\KRenamer.exe) do echo   %%~zf bytes
    echo.
) else (
    echo.
    echo [ERROR] Build failed!
    exit /b 1
)
goto end

:build_wheel
echo.
echo [BUILD] Building wheel package...
echo =================================
call pip install build
call python -m build --wheel
if %errorlevel%==0 (
    echo.
    echo [SUCCESS] Wheel built successfully!
    dir /b dist\*.whl
) else (
    echo [ERROR] Wheel build failed!
    exit /b 1
)
goto end

:build_sdist
echo.
echo [BUILD] Building source distribution...
echo ======================================
call pip install build
call python -m build --sdist
if %errorlevel%==0 (
    echo.
    echo [SUCCESS] Source distribution built successfully!
    dir /b dist\*.tar.gz
) else (
    echo [ERROR] Source distribution build failed!
    exit /b 1
)
goto end

:build_all
echo.
echo [BUILD] Building all packages...
echo ================================
call pip install build
call python -m build
if %errorlevel%==0 (
    echo.
    echo [SUCCESS] All packages built successfully!
    echo Contents of dist/:
    dir /b dist\
) else (
    echo [ERROR] Build failed!
    exit /b 1
)
goto end

:install_dev
echo.
echo [INSTALL] Installing in development mode...
echo ===========================================
call pip install -e .
if %errorlevel%==0 (
    echo.
    echo [SUCCESS] Package installed in development mode!
    echo You can now run: krenamer
) else (
    echo [ERROR] Installation failed!
    exit /b 1
)
goto end

:build_docs
echo.
echo [DOCS] Building documentation...
echo ===============================
call pip install mkdocs mkdocs-material mkdocs-minify-plugin pymdown-extensions sphinx sphinx-rtd-theme
echo.
echo Building API documentation with Sphinx...
cd docs\api-docs
call sphinx-build -b html . _build\html
if not %errorlevel%==0 (
    echo [ERROR] Sphinx API documentation build failed!
    cd ..\..
    exit /b 1
)
echo Copying API docs to main documentation...
if exist "..\api" rmdir /s /q "..\api"
xcopy /e /i /q "_build\html" "..\api"
cd ..\..
echo.
echo Building main documentation with MkDocs...
call mkdocs build --clean
if %errorlevel%==0 (
    echo.
    echo [SUCCESS] Documentation built successfully!
    echo Location: site/
    echo - Main docs: site\index.html
    echo - API docs: site\api\index.html
    echo Open site\index.html to view
) else (
    echo [ERROR] Documentation build failed!
    exit /b 1
)
goto end

:serve_docs
echo.
echo [DOCS] Serving documentation locally...
echo ======================================
call pip install mkdocs mkdocs-material mkdocs-minify-plugin pymdown-extensions sphinx sphinx-rtd-theme
echo.
echo Building latest API documentation...
cd docs\api-docs
call sphinx-build -b html . _build\html
if exist "..\api" rmdir /s /q "..\api"
xcopy /e /i /q "_build\html" "..\api"
cd ..\..
echo Starting local server at http://localhost:8000
echo Press Ctrl+C to stop
call mkdocs serve
goto end

:run_tests
echo.
echo [TEST] Running KRenamer tests...
echo =================================

REM Check if pytest is available
call pytest tests -v
goto end

:clean
echo.
echo [CLEAN] Cleaning build artifacts...
echo ==================================
if exist "build" (
    echo Removing build/
    rmdir /s /q build
)
if exist "dist" (
    echo Removing dist/
    rmdir /s /q dist
)
if exist "*.egg-info" (
    echo Removing *.egg-info
    for /d %%d in (*.egg-info) do rmdir /s /q "%%d"
)
if exist "__pycache__" (
    echo Removing __pycache__
    for /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
)
if exist "*.pyc" (
    echo Removing *.pyc files
    del /s /q *.pyc
)
if exist "site" (
    echo Removing site/
    rmdir /s /q site
)
echo [SUCCESS] Clean completed!
goto end

:publish_test
echo.
echo [PUBLISH] Publishing to TestPyPI...
echo ===================================
call pip install twine
if not exist "dist\*.whl" (
    echo No wheel found. Building first...
    call :build_wheel
)
echo.
echo Uploading to TestPyPI...
call twine upload --repository testpypi dist/*
if %errorlevel%==0 (
    echo.
    echo [SUCCESS] Published to TestPyPI!
    echo Install with: pip install -i https://test.pypi.org/simple/ krenamer
) else (
    echo [ERROR] Upload failed!
    exit /b 1
)
goto end

:publish_pypi
echo.
echo [PUBLISH] Publishing to PyPI...
echo ===============================
echo WARNING: This will publish to the official PyPI!
set /p confirm="Are you sure? (y/N): "
if /i not "%confirm%"=="y" (
    echo Cancelled.
    goto end
)
call pip install twine
if not exist "dist\*.whl" (
    echo No wheel found. Building first...
    call :build_wheel
)
echo.
echo Uploading to PyPI...
call twine upload dist/*
if %errorlevel%==0 (
    echo.
    echo [SUCCESS] Published to PyPI!
    echo Install with: pip install krenamer
) else (
    echo [ERROR] Upload failed!
    exit /b 1
)
goto end

:help
echo.
echo KRenamer Build System
echo ====================
echo.
echo Usage: make.bat [command]
echo.
echo Available commands:
echo.
echo   BUILD COMMANDS:
echo     exe          Build standalone executable (.exe)
echo     wheel        Build wheel package (.whl)
echo     sdist        Build source distribution (.tar.gz)
echo     build        Build both wheel and sdist
echo     install      Install package in development mode
echo.
echo   DOCUMENTATION:
echo     docs         Build documentation (Sphinx API + MkDocs)
echo     serve        Serve documentation locally (http://localhost:8000)
echo.
echo   TESTING:
echo     test         Run tests
echo.
echo   DEPLOYMENT:
echo     publish-test Publish to TestPyPI
echo     publish      Publish to PyPI (production)
echo.
echo   UTILITIES:
echo     clean        Clean build artifacts
echo     help         Show this help
echo.
echo Examples:
echo   make exe           # Build KRenamer.exe
echo   make build         # Build wheel and sdist
echo   make docs          # Build documentation
echo   make serve         # Preview docs locally
echo   make clean         # Clean up build files
echo.

:end
echo.
