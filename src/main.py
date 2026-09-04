import re
import os

# ALU Regex Data Extraction - main.py
# I'm writing this to extract data from raw text using regex

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, "..")
input_path = os.path.join(project_root, "input", "raw-text.txt")

with open(input_path, "r") as f:
    text = f.read()

print("Read the input file. It has", len(text), "characters.")
print()


# --- Extract emails ---

email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
raw_emails = re.findall(email_pattern, text)

emails = []
for email in raw_emails:
    if email.count("@") != 1:
        continue
    parts = email.split("@")
    username = parts[0]
    domain = parts[1]
    if len(username) == 0:
        continue
    if "." not in domain:
        continue
    if domain.endswith("."):
        continue
    emails.append(email)

print("Valid emails found:", len(emails))
for e in emails:
    print(" ", e)
print()


# --- Extract phone numbers ---

phone_pattern = r'(?:\+250[\s-]*[0-9]{3}[\s-]*[0-9]{3}[\s-]*[0-9]{3})|(?:0[0-9]{3}[\s-]*[0-9]{3}[\s-]*[0-9]{3})'
raw_phones = re.findall(phone_pattern, text)

phones = []
for phone in raw_phones:
    digits = phone.replace(" ", "").replace("-", "")
    if digits.startswith("0"):
        digits = "+250" + digits[1:]
    phones.append(digits)

print("Phone numbers found:", len(phones))
for p in phones:
    print(" ", p)
print()


# --- Extract URLs ---

# I use this regex to find HTTP and HTTPS URLs.
# I only accept http and https because I don't want javascript: or data: URLs
url_pattern = r'https?://[A-Za-z0-9._~:/?#\[\]@!$&\'()*+,;=-]+'

raw_urls = re.findall(url_pattern, text)

# I clean up the URLs a bit
urls = []
for url in raw_urls:
    # I remove trailing punctuation that might have been captured
    url = url.rstrip(".,;:!?)")
    urls.append(url)

print("URLs found:", len(urls))
for u in urls:
    print(" ", u)
