# -*- mode: python ; coding: utf-8 -*-
import os

a = Analysis(
    [os.path.join('src', 'psw', '__main__.py')],
    pathex=['src'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='psw',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    # macOS: set codesign_identity and entitlements_file before publishing
    # signed binaries. Unsigned executables will be blocked by Gatekeeper;
    # users can work around with: xattr -dr com.apple.quarantine psw
    codesign_identity=None,
    entitlements_file=None,
)
