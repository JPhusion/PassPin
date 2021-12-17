import hashlib

def secure_hash(text):
    alphabet = 'mnbvcxzlkjhgfdsapoiuytrewq'
    salt = ""
    for letter in text:
        if letter in alphabet:
            salt += alphabet[(alphabet.index(letter) + len(text)) % 26]
    salt = salt[::-1]
    for i in range (1000000):
        text = hashlib.sha512(str(text + salt).encode("utf-8")).hexdigest()
    return text
