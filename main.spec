# main.spec
# FINAL, ROBUST, AND DIRECT PATH VERSION
# This spec file abandons all auto-discovery hooks and builds the path manually.

import os
import site
import sys

# --- The Ultimate Fix: Direct Path Construction ---
# We use Python's standard 'site' library to find the site-packages directory.
# This is the most reliable way to locate installed packages.
try:
    # Find the primary site-packages directory.
    site_packages_path = next(p for p in site.getsitepackages() if 'site-packages' in p)
except StopIteration:
    sys.exit("CRITICAL ERROR: Could not find the site-packages directory. The Python environment seems broken.")

# We now construct the absolute path to the data directory we need.
# This bypasses all of PyInstaller's faulty name recognition.
tkdnd_data_path = os.path.join(site_packages_path, 'tkinterdnd2', 'tkdnd')

# A crucial sanity check to ensure the path actually exists before we proceed.
if not os.path.exists(tkdnd_data_path):
    sys.exit(
        f"CRITICAL ERROR: The tkinterdnd2 data directory was not found at the expected path: {tkdnd_data_path}. "
        f"This indicates a problem with the 'python-tkdnd' installation."
    )


# --- Analysis Block ---
# This configuration is now based on a guaranteed, existing file path.
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        (tkdnd_data_path, 'tkinterdnd2/tkdnd'), # Using the direct, verified path.
        ('assets', 'assets')                   # Your assets folder.
    ],
    hiddenimports=['tkinterdnd2'], # Kept as a final safeguard.
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# --- EXE Block (Correct for one-file build) ---
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
