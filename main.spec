# main.spec
# THE FINAL JUDGEMENT
# Transcribed directly from forensic evidence. No guesswork remains.

import os
import sys
import sysconfig

# --- Step 1: Locate site-packages, the foundation of truth. ---
try:
    site_packages_path = sysconfig.get_path('purelib')
except (ImportError, AttributeError):
    sys.exit("FATAL: Cannot determine site-packages path. Python environment is corrupt.")

# --- Step 2: Define the EXACT SOURCE PATH, as revealed by the forensic log. ---
# The required data files are in the 'windows' subdirectory of 'tkinterDnD'.
tkdnd_source_path = os.path.join(site_packages_path, 'tkinterDnD', 'windows')

# --- Step 3: A final, absolute sanity check. ---
if not os.path.exists(tkdnd_source_path):
    sys.exit(
        f"CATASTROPHIC FAILURE: The proven source directory does not exist: {tkdnd_source_path}. "
        "The 'python-tkdnd' installation is fundamentally broken."
    )

# --- Analysis Block ---
# We now map the TRUE SOURCE to the EXPECTED DESTINATION.
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # THE ONE TRUE FIX:
        # Copy everything FROM the '.../tkinterDnD/windows' directory (source)
        # TO a directory named 'tkinterdnd2/tkdnd' inside the bundled app (destination).
        (tkdnd_source_path, 'tkinterdnd2/tkdnd'),
        
        # Do not forget your own assets.
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
    [], # Binaries are handled via datas for this library
    a.zipfiles,
    a.datas,
    name='MyAwesomeApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,
    icon='assets/hash.ico'
)
