"""
Pure Python Loader for Windows Application Control environments.
Prioritizes pure Python source files (.py) over compiled C-extension (.pyd) binaries
when loading packages like SQLAlchemy in environments where unsigned .pyd files may be restricted.
"""
import sys
import os
import importlib.util

class PurePythonFinder:
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith('sqlalchemy'):
            for p in (path or []):
                py_file = os.path.join(p, fullname.split('.')[-1] + '.py')
                if os.path.isfile(py_file):
                    return importlib.util.spec_from_file_location(fullname, py_file)
        return None

if not any(isinstance(f, PurePythonFinder) for f in sys.meta_path):
    sys.meta_path.insert(0, PurePythonFinder())
