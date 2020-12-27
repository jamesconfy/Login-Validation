import re

pattern = "^([0][7-9][0-1]\d{8}$)"
pattern1 = "(^[0][7-9][0-1]\d{8}$)|(^[+]?[234][7-9][0-1]\d{8}$)"
pattern2 = "^((\+234|0)[7-9][0-1]\d{8}$)|^([])"

number = "+2349149795370"
matched = re.match(pattern2, number)

print(matched)