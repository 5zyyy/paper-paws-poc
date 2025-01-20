import streamlit
import streamlit.web.cli as stcli
import os
import sys


def resolve_path(path):
    # Get the directory where the executable is located
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        bundle_dir = os.getcwd()
    
    resolved_path = os.path.abspath(os.path.join(bundle_dir, path))
    return resolved_path


if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        resolve_path(os.path.join("src", "app.py")),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main()) 