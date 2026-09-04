import re
import os

# ALU Regex Data Extraction - main.py
# I'm writing this to extract data from raw text using regex

# I figure out where the project root is so I can find the input file
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, "..")
input_path = os.path.join(project_root, "input", "raw-text.txt")

# I read the raw text file
with open(input_path, "r") as f:
    text = f.read()

print("Read the input file. It has", len(text), "characters.")
print()
