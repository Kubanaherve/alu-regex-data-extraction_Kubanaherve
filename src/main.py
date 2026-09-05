import re
import json
import os

# ALU Regex Data Extraction - main.py
# I'm writing this to extract data from raw text using regex

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, "..")
input_path = os.path.join(project_root, "input", "raw-text.txt")
output_path = os.path.join(project_root, "output", "sample-output.json")

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


# --- Extract phone numbers ---

phone_pattern = r'(?:\+250[\s-]*[0-9]{3}[\s-]*[0-9]{3}[\s-]*[0-9]{3})|(?:0[0-9]{3}[\s-]*[0-9]{3}[\s-]*[0-9]{3})'
raw_phones = re.findall(phone_pattern, text)

phones = []
for phone in raw_phones:
    digits = phone.replace(" ", "").replace("-", "")
    if digits.startswith("0"):
        digits = "+250" + digits[1:]
    phones.append(digits)


# --- Extract URLs ---

url_pattern = r'https?://[A-Za-z0-9._~:/?#\[\]@!$&\'()*+,;=-]+'
raw_urls = re.findall(url_pattern, text)

urls = []
for url in raw_urls:
    url = url.rstrip(".,;:!?)")
    urls.append(url)


# --- Extract credit card numbers ---

card_pattern = r'\b(\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{1,4})\b'
raw_cards = re.findall(card_pattern, text)

def luhn_check(number):
    digits = number.replace(" ", "").replace("-", "")
    if not digits.isdigit():
        return False
    if len(digits) < 13 or len(digits) > 19:
        return False
    total = 0
    reverse_digits = digits[::-1]
    for i in range(len(reverse_digits)):
        n = int(reverse_digits[i])
        if i % 2 == 1:
            n = n * 2
            if n > 9:
                n = n - 9
        total = total + n
    return total % 10 == 0

cards = []
for card in raw_cards:
    if luhn_check(card):
        digits = card.replace(" ", "").replace("-", "")
        masked = "*" * (len(digits) - 4) + digits[-4:]
        cards.append(masked)


# --- Build the output ---

result = {
    "emails": emails,
    "phone_numbers": phones,
    "urls": urls,
    "credit_cards": cards,
    "summary": {
        "total_emails": len(emails),
        "total_phones": len(phones),
        "total_urls": len(urls),
        "total_cards": len(cards)
    }
}

# I make sure the output folder exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# I save the results to a JSON file
with open(output_path, "w") as f:
    json.dump(result, f, indent=2)


# --- Print a summary ---

print("I found:")
print("  Emails:", len(emails))
print("  Phones:", len(phones))
print("  URLs:  ", len(urls))
print("  Cards: ", len(cards))
print()
print("Done. I saved the results in output/sample-output.json")
