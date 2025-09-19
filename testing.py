import string

ALPHABET = string.ascii_letters + string.digits  # base62
BASE = len(ALPHABET)

def encode_string_to_number(s):
    num = 0
    for i, c in enumerate(s):
        num = num * BASE + ALPHABET.index(c)
    return num

def decode_number_to_string(num):
    chars = []
    while num > 0:
        num, rem = divmod(num, BASE)
        chars.append(ALPHABET[rem])
    return ''.join(reversed(chars))

# Example usage:
original = "Ab1qwerwerttrrZ"  # Max 4 characters
token = encode_string_to_number(original)
print("Encoded to:", token)  # e.g. 44710657

recovered = decode_number_to_string(token)
print("Decoded back:", recovered)
