# main.spec
# This file is the ultimate configuration for PyInstaller.
# It perfectly merges your requirements with the fix for tkinterdnd2.

import os
import sys

# --- Dynamic Path Discovery for tkinterdnd2 ---
# This block is the core fix. It finds where the essential Tcl/Tk scripts
# for tkinterdnd2 are located, so we can tell PyInstaller to pack them.
try:
    import tkinterdnd2
    dnd_path = os.path.dirname(tkinterdnd2.__file__)
    tkdnd_data_path = os.path.join(dnd_path, 'tkdnd')
except ImportError as e:
    sys.exit(f"CRITICAL ERROR: Cannot find 'tkinterdnd2' module. Please ensure 'python-tkdnd' is installed in your build environment before running PyInstaller. Details: {e}")


# --- Analysis Block ---
# This block defines all inputs for your application.
a = Analysis(
    ['main.py'],  # YOUR SCRIPT: Changed from hasy.py to main.py
    pathex=[],
    binaries=[],
    # --- The CRITICAL 'datas' section ---
    # This combines MY fix with YOUR requirement.
    # 1. Adds the tkinterdnd2 data files.
    # 2. Adds your entire 'assets' folder, just like '--add-data "assets;assets"'.
    datas=[
        (tkdnd_data_path, 'tkinterdnd2/tkdnd'),
        ('assets', 'assets')
    ],
    # Double insurance for the import.
    hiddenimports=['tkinterdnd2'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# --- EXE Block ---
# This block configures the final .exe file, mirroring all your command-line options.
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MyAwesomeApp',         # YOUR NAME: as per --name "MyAwesomeApp"
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,              # YOUR WINDOWS SETTING: as per --windowed
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/hash.ico'      # YOUR ICON: as per --icon "assets/hash.ico"
)

# --- COLLECT Block (for one-file builds, this structure is correct) ---
# This ensures all the analyzed parts are collected into the final bundle.
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MyAwesomeApp' # The name of the temporary build folder
)
