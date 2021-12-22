import re

from getpass import getpass
from blessed import Terminal

from algorithms.hasher import secure_hash
from external.send_email import email_pwrs
from algorithms.verification_code import verif_code
from algorithms.password_generator import generatePassword
from algorithms.encryption import encrypt, decrypt, generateKey, generateRandomKey

"""
1. for each platform
2. for each account
3. decrypt passwords
4. generate random decryptkey
5. encrypt password with decryptkey
6. write decryptkey and password to database
7. write database to file
"""

def re_encryrypt_passwords(database, key, master_password):
    term = Terminal()
    print(term.clear)
    print(term.black_on_red(term.center('')))
    print(term.black_on_red(term.center(
        'PASSPIN PASSWORD MANAGER - CHANGE MASTER PASSWORD')))
    print(term.black_on_red(term.center('')))
    pw = getpass("\nEnter master password:\n: ")
    if secure_hash(pw) == master_password:
        # TODO ASK FOR CURRENT PASSWORD AND ADD SECURITY QUESTIONS
        print("\nSending verification code...")
        code = verif_code()
        email_pwrs(code)
        input_code = input(
            "\nPlease enter the verification code sent to you\n: ")
        if input_code == code:
            for platform in database.values():
                for account in platform.values():
                    password = decrypt(generateKey(account["decryptkey"]), bytes(account["password"], 'utf-8'))
                    account["decryptkey"] = generatePassword(50)
                    account["password"] = encrypt(generateKey(account["decryptkey"]), password).decode('utf-8')
            database = encrypt(key, str(database)).decode('utf-8')
            with open("./data/email.txt", "r+") as f:
                data = f.read()
                f.seek(0)
                f.write(re.sub(data, database, data))
                f.truncate()
            print(term.clear)
            print(term.lightgreen_on_green(term.center('')))
            print(term.lightgreen_on_green(term.center(
                'PASSPIN PASSWORD MANAGER - RE-ENCRYPTED ALL PASSWORDS')))
            print(term.lightgreen_on_green(term.center('')))
            print("\n")
            print(term.center(term.green(
                'All passwords re-encrypted. You will need to sign in again. Press [ENTER] to continue.')))
            getpass("")
        else:
            print("\n")
            print(term.center(term.red(
                'The verification code was incorrect. The owner has been alerted to your failed attempt with your details.')))
            print("")
            print(term.center(term.red('Press [ENTER] to continue.')))
            getpass("")
    else:
        print("\n")
        print(term.center(term.red(
            'The password was incorrect. The owner has been alerted to your failed attempt with your details.')))
        print("")
        print(term.center(term.red('Press [ENTER] to continue.')))
        getpass("")
