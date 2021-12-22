import hashlib
from tqdm import tqdm


def secure_hash(text, bar=False):
    if bar:
        pbar = tqdm(total=10000, bar_format='  |{bar}|  ', colour='CYAN')
    alphabet = 'm!n@b#v$c^x&z(l]k)j[h}g{f\d"s;a>p<o/i;u>y<t:r+e=w_q'
    salt = ""
    changed_salt = alphabet[len(text) % 26]
    for letter in text:
        if letter in alphabet:
            salt += alphabet[(alphabet.index(letter) + len(text)) % 26]
    salt = salt[::-1]
    for i in range(100000):
        text = hashlib.sha512(str(text + salt).encode("utf-8")).hexdigest()
        if i % 10 == 0:
            if bar:
                pbar.update(n=1)
            try:
                index = int(text[0])
            except ValueError:
                try:
                    index = alphabet.index(changed_salt[0])
                except IndexError:
                    index = 2
            changed_salt = ""
            for letter in salt:
                if letter in alphabet:
                    changed_salt += alphabet[(alphabet.index(letter) +
                                              len(text)*index) % 26]
                    salt = changed_salt
    return text
