# THE FINAL AND CORRECT VERSION
# Based on irrefutable file system reconnaissance.

import os
import sys
import sysconfig

# --- The Ultimate Fix: Using the CORRECT Directory Name ---
try:
    # Step 1: Reliably find the site-packages directory.
    site_packages_path = sysconfig.get_path('purelib')
    if not site_packages_path or not os.path.exists(site_packages_path):
        raise FileNotFoundError
except (ImportError, FileNotFoundError):
    sys.exit("CRITICAL ERROR: Could not determine the site-packages path. Your Python environment appears to be broken.")

# Step 2: Construct the path using the PROVEN, CORRECT directory name: "tkinterDnD".
# THE CRITICAL FIX IS HERE.
tkdnd_source_path = os.path.join(site_packages_path, 'tkinterDnD', 'tkdnd')

# Step 3: A final sanity check. If this fails, the package installation itself is corrupted.
if not os.path.exists(tkdnd_source_path):
    sys.exit(
        f"CRITICAL ERROR: The data directory was not found at the correct path: {tkdnd_source_path}. "
        f"This means the 'python-tkdnd' package is installed incorrectly or is a corrupted version."
    )

# --- Analysis Block ---
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    # The source is the CORRECT path, the destination is what the library code expects internally.
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

# --- EXE Block ---
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
