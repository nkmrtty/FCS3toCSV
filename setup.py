from distutils.core import setup
import py2exe
import sys

sys.argv.append("py2exe")
setup(name="FCS3 Parser",
      console=[dict(script="main.py", dest_base="FCS3toCSV")],
      options={"py2exe": {"bundle_files":1, "compressed":1, "optimize":2}},
      zipfile=None)
