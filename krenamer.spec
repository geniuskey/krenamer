# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, 'src')

block_cipher = None

a = Analysis(
    ['src/krenamer/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include tkinterdnd2 DLL files if they exist
        ('.venv/Lib/site-packages/tkinterdnd2/tkdnd', 'tkinterdnd2/tkdnd'),
    ],
    hiddenimports=[
        'tkinterdnd2',
        'krenamer.core',
        'krenamer.gui',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='KRenamer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/krenamer.ico' if os.path.exists('assets/krenamer.ico') else None,
    version_file='version_info.txt' if os.path.exists('version_info.txt') else None,
)