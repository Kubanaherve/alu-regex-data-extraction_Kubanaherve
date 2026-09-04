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


# --- Extract emails ---

# I use this regex to find emails in the text.
# [A-Za-z0-9._%+-]+ matches the part before the @
# [A-Za-z0-9.-]+ matches the domain name
# \.[A-Za-z]{2,} matches the dot and the extension like .com or .org
email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

raw_emails = re.findall(email_pattern, text)

# I check each email before adding it to make sure it's actually valid
emails = []
for email in raw_emails:
    # I check there is exactly one @ sign
    if email.count("@") != 1:
        continue

    parts = email.split("@")
    username = parts[0]
    domain = parts[1]

    # I check there is something before the @
    if len(username) == 0:
        continue

    # I check the domain has at least one dot
    if "." not in domain:
        continue

    # I check the domain doesn't end with a dot
    if domain.endswith("."):
        continue

    emails.append(email)

print("Valid emails found:", len(emails))
for e in emails:
    print(" ", e)
