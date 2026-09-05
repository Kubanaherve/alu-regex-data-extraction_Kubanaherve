import re
import json
import os

# ============================================================
# ALU Regex Data Extraction - main.py
# I wrote this program to extract emails, phone numbers, URLs,
# and credit card numbers from raw text using regex.
# ============================================================

# I treat the input as untrusted because it comes from an outside source.
# I never execute anything from the text — I only look for patterns.

# --- Step 1: Read the input file ---

# I figure out where the project root is so I can find the input file
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, "..")
input_path = os.path.join(project_root, "input", "raw-text.txt")
output_path = os.path.join(project_root, "output", "sample-output.json")

# I read the raw text file
with open(input_path, "r") as f:
    text = f.read()

# I do a simple size check because I don't want to process something huge
if len(text) > 1_000_000:
    print("The input file is too large. I'm not going to process it.")
    exit()

print("Read the input file. It has", len(text), "characters.")
print()


# --- Step 2: Extract emails ---

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

    # I don't want domains that have too many parts — that looks suspicious
    # like test@alueducation.com.evil.com (someone faking the domain)
    domain_parts = domain.split(".")
    if len(domain_parts) > 3:
        continue

    emails.append(email)

# Now I classify each email by its ALU domain type
email_results = []
for email in emails:
    domain = email.split("@")[1].lower()

    # I check the domain to see if it's an ALU email
    if domain == "alueducation.com":
        email_type = "ALU official"
    elif domain == "alumni.alueducation.com":
        email_type = "ALU alumni"
    elif domain == "si.alueducation.com":
        email_type = "ALU SI"
    elif domain == "alustudent.com":
        email_type = "ALU student"
    else:
        email_type = "other"

    # I mask the email because I don't want to show the full address in the output.
    # I keep the first letter and the domain so you can still tell what it is.
    username = email.split("@")[0]
    masked_username = username[0] + "****"
    masked_email = masked_username + "@" + email.split("@")[1]

    email_results.append({
        "email": masked_email,
        "type": email_type
    })


# --- Step 3: Extract phone numbers ---

# I use this regex to find Rwandan phone numbers.
# I allow spaces and dashes because people write phone numbers differently.
# \+250 matches the country code for Rwanda.
# 0[0-9]{3} matches the local format starting with 0 like 0788.
# Then I expect two more groups of 3 digits separated by spaces or dashes.
phone_pattern = r'(?:\+250[\s-]*[0-9]{3}[\s-]*[0-9]{3}[\s-]*[0-9]{3})|(?:0[0-9]{3}[\s-]*[0-9]{3}[\s-]*[0-9]{3})'

raw_phones = re.findall(phone_pattern, text)

# I normalize each phone number to the +250 format
phones = []
for phone in raw_phones:
    # I remove all spaces and dashes to get just the digits
    digits = phone.replace(" ", "").replace("-", "")

    # If it starts with 0, I replace that with +250
    if digits.startswith("0"):
        digits = "+250" + digits[1:]

    # I make sure the final number is the right length for Rwanda
    # A Rwanda number should be +250 followed by 9 digits = 13 characters total
    if not digits.startswith("+250"):
        continue
    # I remove the + to count just the digits
    just_digits = digits.replace("+", "")
    if len(just_digits) != 12:
        continue

    phones.append(digits)


# --- Step 4: Extract URLs ---

# I use this regex to find HTTP and HTTPS URLs.
# https? allows both http and https.
# I only accept http and https because I don't want to treat things like
# javascript: or data: as normal URLs. Those could be dangerous.
url_pattern = r'https?://[A-Za-z0-9._~:/?#\[\]@!$&\'()*+,;=-]+'

raw_urls = re.findall(url_pattern, text)

# I clean up the URLs a bit
urls = []
for url in raw_urls:
    # I remove trailing punctuation that might have been captured from the text
    url = url.rstrip(".,;:!?)")

    # I don't trust URLs from the text — I don't execute them or open them.
    # I just store them in my results.
    urls.append(url)


# --- Step 5: Extract credit card numbers ---

# I use this regex to find things that look like credit card numbers.
# Cards are usually 13-19 digits, but I look for 13-16 digit patterns
# with optional spaces or dashes between groups of 4.
# \d{4} matches four digits, and [\s-]? allows an optional space or dash.
card_pattern = r'\b(\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{1,4})\b'

raw_cards = re.findall(card_pattern, text)

# I use the Luhn algorithm to check if a card number is valid.
# I use this because a regex alone cannot tell me if a card number is real.
# The Luhn check is a simple math check that most real card numbers pass.
def luhn_check(number):
    # I remove spaces and dashes to get just the digits
    digits = number.replace(" ", "").replace("-", "")

    # I make sure it's all digits
    if not digits.isdigit():
        return False

    # I need at least 13 digits for a card number
    if len(digits) < 13 or len(digits) > 19:
        return False

    # I reject all zeros because that's obviously not a real card
    if all(d == "0" for d in digits):
        return False

    # I do the Luhn algorithm here
    # I start from the right and double every second digit
    total = 0
    reverse_digits = digits[::-1]
    for i in range(len(reverse_digits)):
        n = int(reverse_digits[i])
        if i % 2 == 1:
            n = n * 2
            if n > 9:
                n = n - 9
        total = total + n

    # If the total is divisible by 10, the number passes the Luhn check
    return total % 10 == 0

cards = []
for card in raw_cards:
    if luhn_check(card):
        # I hide most of the card number because I don't want sensitive data in my output.
        # I only keep the last 4 digits so you can tell which card it is.
        digits = card.replace(" ", "").replace("-", "")
        masked = "*" * (len(digits) - 4) + digits[-4:]
        cards.append(masked)


# --- Step 6: Build the output ---

result = {
    "emails": email_results,
    "phone_numbers": phones,
    "urls": urls,
    "credit_cards": cards,
    "summary": {
        "total_emails": len(email_results),
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


# --- Step 7: Print a summary ---

print("I found:")
print("  Emails:", len(email_results))
print("  Phones:", len(phones))
print("  URLs:  ", len(urls))
print("  Cards: ", len(cards))
print()
print("Done. I saved the results in output/sample-output.json")
