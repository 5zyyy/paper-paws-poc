import PyInstaller.__main__
import os
import streamlit
from PyInstaller.utils.hooks import collect_data_files, copy_metadata

# Get the streamlit package location
streamlit_path = os.path.dirname(streamlit.__file__)

# Ensure paths use correct separators
src_path = os.path.join(os.getcwd(), 'src')

PyInstaller.__main__.run([
    'run.py',
    '--name=paperpaws',
    '--onefile',
    '--clean',
    '--add-data', f'{streamlit_path}{os.pathsep}streamlit',
    # Add metadata
    '--copy-metadata', 'streamlit',
    '--copy-metadata', 'streamlit-extras',
    '--copy-metadata', 'altair',
    '--copy-metadata', 'pandas',
    '--copy-metadata', 'numpy',
    '--copy-metadata', 'pyyaml',
    '--copy-metadata', 'duckdb',
    # Hidden imports
    '--hidden-import', 'streamlit.runtime.scriptrunner.magic_funcs',
    '--hidden-import', 'streamlit.runtime.scriptrunner',
    '--hidden-import', 'streamlit.runtime',
    '--hidden-import', 'streamlit.commands.page_config',
    '--hidden-import', 'streamlit.elements.image',
    '--hidden-import', 'streamlit.elements.widgets',
    '--hidden-import', 'streamlit.elements.layouts',
    '--hidden-import', 'importlib_metadata',
    '--hidden-import', 'packaging',
    '--hidden-import', 'packaging.version',
    '--hidden-import', 'packaging.specifiers',
    '--hidden-import', 'packaging.requirements',
    '--hidden-import', 'streamlit_extras',
    '--hidden-import', 'streamlit_extras.stylable_container',
    # Collect all necessary data
    '--collect-data', 'streamlit',
    '--collect-data', 'streamlit_extras',
    '--collect-binaries', 'streamlit',
    '--collect-binaries', 'streamlit_extras',
    # Add src directory to the path
    '--add-data', f'{src_path}{os.pathsep}src',
    '--noconfirm'
]) 