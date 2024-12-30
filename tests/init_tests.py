import sys
import os

def append_to_path():
    current_dir = os.getcwd()
    parent_dir = current_dir.replace("/tests", '')
    sys.path.append(parent_dir)
