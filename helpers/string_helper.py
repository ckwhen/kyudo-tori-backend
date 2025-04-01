import unicodedata

def convert_full_to_half(input: str):
    return unicodedata.normalize('NFKC', input)