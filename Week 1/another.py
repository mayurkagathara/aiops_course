# from W01_python_basics import *
# import W01_python_basics
# import math, csv, json, datetime, re
# from math import pi

# add_all(2,3,4,5)

import os

module_path = os.path.dirname(os.path.realpath(__file__))
print(module_path)

log_path = os.path.join(module_path, "..", "Week2", "app.log")
print(log_path)

file_path = os.path.join(module_path, 'a.txt')

with open(file_path, "w") as f:
    f.write("This document contains the word 'Python' and 'regex'.\n")
    f.write("It's a simple test file for pattern matching.\n")
    
