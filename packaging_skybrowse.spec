# Run with: pyinstaller packaging_skybrowse.spec
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

hiddenimports = ["PySide6.QtWebEngineCore", "PySide6.QtWebEngineWidgets"]
datas = collect_data_files("PySide6")
binaries = collect_dynamic_libs("PySide6")

a = Analysis(["main.py"], pathex=["."], binaries=binaries, datas=datas, hiddenimports=hiddenimports, hookspath=[], runtime_hooks=[], excludes=[], noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name="SkyBrowse", debug=False, bootloader_ignore_signals=False, strip=False, upx=False, console=False)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="SkyBrowse")
