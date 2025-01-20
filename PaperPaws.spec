# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_dynamic_libs
from PyInstaller.utils.hooks import copy_metadata

datas = [('C:\\Users\\Ryan\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python312\\site-packages\\streamlit', 'streamlit'), ('C:\\project\\paper-paws-poc\\src', 'src')]
binaries = []
datas += collect_data_files('streamlit')
datas += collect_data_files('streamlit_extras')
datas += copy_metadata('streamlit')
datas += copy_metadata('streamlit-extras')
datas += copy_metadata('altair')
datas += copy_metadata('pandas')
datas += copy_metadata('numpy')
datas += copy_metadata('pyyaml')
datas += copy_metadata('duckdb')
binaries += collect_dynamic_libs('streamlit')
binaries += collect_dynamic_libs('streamlit_extras')


a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=['streamlit.runtime.scriptrunner.magic_funcs', 'streamlit.runtime.scriptrunner', 'streamlit.runtime', 'streamlit.commands.page_config', 'streamlit.elements.image', 'streamlit.elements.widgets', 'streamlit.elements.layouts', 'importlib_metadata', 'packaging', 'packaging.version', 'packaging.specifiers', 'packaging.requirements', 'streamlit_extras', 'streamlit_extras.stylable_container'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='paperpaws',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
