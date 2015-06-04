import sys
import os.path
import os
from fcs_format import run

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("Usage: main.py <path>")
        sys.exit(0)

    path = os.path.abspath(args[1])
    file_path = []
    if os.path.isdir(path):
        for fname in os.listdir(path):
            if os.path.splitext(fname)[1] == ".fcs":
                file_path.append(os.path.join(path, fname))
    else:
        file_path.append(path)

    for fpath in file_path:
        run(fpath)
