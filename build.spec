# build.spec
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
import os

# Coleta submódulos da pasta 'tabs'
hiddenimports = collect_submodules("tabs")

# Detecta plataforma
is_windows = os.name == "nt"
icon_path = "assets/icon.ico" if is_windows else "assets/icon.icns"

# Análise
a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('assets/icon.png', 'assets'),
        ('ffmpeg/ffmpeg.exe', 'ffmpeg') if is_windows else ('ffmpeg/ffmpeg', 'ffmpeg')
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ConversorDeAudio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=icon_path
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ConversorDeAudio'
)
