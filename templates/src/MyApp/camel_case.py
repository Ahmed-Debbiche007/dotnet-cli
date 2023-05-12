import re

def to_camel_case(s):
    # Remove non-alphanumeric characters and split into words
    words = re.findall(r'\w+', s)
    
    # Capitalize first letter of each word except for the first word
    return words[0] + ''.join(word.capitalize() for word in words[1:])
