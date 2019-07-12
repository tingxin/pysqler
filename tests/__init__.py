import os
import sys

file_path = os.path.join(os.path.dirname(__file__), '..')
abs_path = os.path.abspath(file_path)
sys.path.insert(0, abs_path)
