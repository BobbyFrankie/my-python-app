# main.spec
# FINAL, CORRECTED, AND ROBUST VERSION
# This spec file uses PyInstaller's internal hooks to reliably find package data.

import os
from PyInstaller.utils.hooks import get_package_paths

# --- The Core Fix: Using PyInstaller's Own Tools ---
# Instead of a fragile 'import', we use the official hook to find the package path.
# This is guaranteed to work if the package is in the environment PyInstaller knows about.
try:
    # get_package_paths returns the path to the package's code.
    package_path = get_package_paths('tkinterdnd2')[0]
    # We then construct the path to its data directory.
    tkdnd_data_path = os.path.join(package_path, 'tkdnd')
except IndexError:
    # This error will trigger if 'python-tkdnd' is not installed at all.
    import sys
    sys.exit("CRITICAL ERROR: PyInstaller's hooks could not find the 'tkinterdnd2' package. Please ensure 'python-tkdnd' is installed in the build environment.")


# --- Analysis Block ---
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        (tkdnd_data_path, 'tkinterdnd2/tkdnd'), # The reliable path to the data.
        ('assets', 'assets')                   # Your assets folder.
    ],
    hiddenimports=['tkinterdnd2'], # Kept as a safeguard.
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# --- EXE Block (Correctly configured for a one-file build) ---
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MyAwesomeApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,
    icon='assets/hash.ico'
)
