# main.spec
# THE ATONEMENT
# Restoring the vital binaries that were wrongfully removed.

import os
import sys
import sysconfig

# --- The tkinterdnd2 fix, which was correct, remains untouched. ---
try:
    site_packages_path = sysconfig.get_path('purelib')
except (ImportError, AttributeError):
    sys.exit("FATAL: Cannot determine site-packages path. Python environment is corrupt.")

tkdnd_source_path = os.path.join(site_packages_path, 'tkinterDnD', 'windows')

if not os.path.exists(tkdnd_source_path):
    sys.exit(
        f"CATASTROPHIC FAILURE: The proven source directory does not exist: {tkdnd_source_path}. "
        "The 'python-tkdnd' installation is fundamentally broken."
    )

# --- Analysis Block (Correct and Unchanged) ---
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        (tkdnd_source_path, 'tkinterdnd2/tkdnd'),
        ('assets', 'assets')
    ],
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

# --- EXE Block (THE CRITICAL CORRECTION) ---
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,  # <<< THE LIFELINE, RESTORED.
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
