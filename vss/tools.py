"""
A set of tools related to Visual SourceSafe.
"""

import os

def get_ss_path():
    """
    Get the Microsoft Visual SourceSafe executable path.

    Checks for the VSS_PYTHON_SS_PATH environment variable if specified and for the usual default installation path otherwise.

    SS_PATH may contains files or folders. When folders are specified, an executable named 'ss.exe' is looked for.

    If the executable is not found, None is returned.
    """

    paths = os.environ.get('VSS_PYTHON_SS_PATH', r'C:\Program Files\Microsoft Visual SourceSafe\ss.exe').split(';')

    for path in paths:
        if os.path.isfile(path):
            return path
        elif os.path.isdir(path):
            fname = os.path.join(path, 'ss.exe')
            if os.path.isfile(fname):
                return fname
