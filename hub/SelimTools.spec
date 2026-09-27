# -*- mode: python ; coding: utf-8 -*-
# 빌드는 build.ps1로 한다: 테스트 → 이 spec으로 폴더형 빌드 → NSIS 설치 파일
import re
from pathlib import Path

from PyInstaller.utils.win32.versioninfo import (
    FixedFileInfo,
    StringFileInfo,
    StringStruct,
    StringTable,
    VarFileInfo,
    VarStruct,
    VSVersionInfo,
)

# exe 파일 속성은 작업지도서·CTQ 앱과 같은 문구로 쓴다. 버전은 main.py의 APP_VERSION에서 읽는다
version_text = re.search(
    r'^APP_VERSION = "(\d+\.\d+\.\d+)"$', Path(SPECPATH, 'main.py').read_text(encoding='utf-8'), re.M
).group(1)
version_numbers = tuple(int(part) for part in version_text.split('.')) + (0,)
version = VSVersionInfo(
    ffi=FixedFileInfo(filevers=version_numbers, prodvers=version_numbers),
    kids=[
        StringFileInfo([StringTable('041204B0', [
            StringStruct('CompanyName', '세림전자'),
            StringStruct('FileDescription', 'Selim Tools'),
            StringStruct('FileVersion', version_text),
            StringStruct('InternalName', 'SelimTools'),
            StringStruct('LegalCopyright', '© 2026 세림전자 개발팀 오민상P'),
            StringStruct('OriginalFilename', 'SelimTools.exe'),
            StringStruct('ProductName', 'Selim Tools'),
            StringStruct('ProductVersion', version_text),
        ])]),
        VarFileInfo([VarStruct('Translation', [0x0412, 1200])]),
    ],
)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/icon.ico', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
# QtCore는 Windows의 ICU를 쓴다. 빌드 PC의 다른 ICU DLL이 섞이면 시작할 때 깨진다 (작업지도서 앱과 같은 처리).
# 위젯만 쓰므로 OpenGL 소프트웨어 렌더러(약 20MB)도 뺀다.
a.binaries = [entry for entry in a.binaries if Path(entry[0]).name.casefold() not in ('icuuc.dll', 'opengl32sw.dll')]
pyz = PYZ(a.pure)

# 폴더형: 한 파일형과 달리 실행할 때마다 임시 폴더에 풀지 않아 창이 바로 뜬다
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SelimTools',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # UPX로 압축한 exe는 백신 오탐이 잦다
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
    version=version,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='SelimTools',
)
