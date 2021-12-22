import secrets
import string

def generatePassword(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    while "'" in password or "\"" in password:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password
