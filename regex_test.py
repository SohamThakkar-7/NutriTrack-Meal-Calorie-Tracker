import re

text1 = "Glycosylated Haemoglobin (HbA1c) 5.9%"

patterns = [
    r"(?:ha?e?moglobin|hb|hgb).*?((?:[2-9]|\d{2,})\.?\d*)\s*g\s*/?\s*d\s*l?",
    r"(?:ha?e?moglobin).{0,50}?((?:[2-9]|\d{2,})\.?\d*)",
    r"\b(?:hb|hgb)\b.{0,25}?((?:[2-9]|\d{2,})\.?\d*)",
]

for p in patterns:
    m = re.search(p, text1, re.IGNORECASE)
    if m:
        print(f"Pattern: {p} -> Matched: {m.group(1)}")
    else:
        print(f"Pattern: {p} -> No match")
