# main.spec
# FINAL & CORRECTED VERSION
# This spec file is self-contained and configured for a ONE-FILE build.

import os
import sys

# --- Dynamic Path Discovery for tkinterdnd2 (The Core Fix) ---
try:
    import tkinterdnd2
    dnd_path = os.path.dirname(tkinterdnd2.__file__)
    tkdnd_data_path = os.path.join(dnd_path, 'tkdnd')
except ImportError as e:
    sys.exit(f"CRITICAL ERROR: Cannot find 'tkinterdnd2' module. Please ensure 'python-tkdnd' is installed in your build environment. Details: {e}")


# --- Analysis Block ---
# Defines all inputs for your application.
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    # Data files: Combines the tkinterdnd2 fix and your 'assets' folder.
    datas=[
        (tkdnd_data_path, 'tkinterdnd2/tkdnd'),
        ('assets', 'assets')
    ],
    # Hidden import for double insurance.
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
# This block now solely defines the final output as a single executable.
# All your previous options are correctly placed here.
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas, # All data is bundled directly into the EXE
    [],
    name='MyAwesomeApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False, # Creates a windowed (non-console) application
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/hash.ico'
)

# DELETED: The `coll = COLLECT(...)` block has been completely removed.
# Its absence is what enables the one-file build mode.
