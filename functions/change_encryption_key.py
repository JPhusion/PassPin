import re
import csv

from getpass import getpass
from blessed import Terminal

from algorithms.hasher import secure_hash
from external.send_email import email_pwrs
from algorithms.verification_code import verif_code
from algorithms.encryption import encrypt, generateKey, generateRandomKey

"""
1. generate new key
2. encrypt database with new key
3. encrypt key with password
4. write database and key to files
"""


def change_encryption_key(database, master_password):
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
            new_key = generateRandomKey()
            encrypted_database = encrypt(
                new_key, str(database)).decode('utf-8')
            encrypted_key = encrypt(generateKey(pw), new_key).decode('utf-8')
            with open("./data/database.txt", "r+") as f:
                data = f.read()
                f.seek(0)
                f.write(re.sub(data, encrypted_database, data))
                f.truncate()
            with open('./data/key.csv', mode='w', newline="") as file:
                writer = csv.writer(file, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['KEY'])
                writer.writerow([encrypted_key])
            print(term.clear)
            print(term.lightgreen_on_green(term.center('')))
            print(term.lightgreen_on_green(term.center(
                'PASSPIN PASSWORD MANAGER - CHANGED ENCRYPTION KEY')))
            print(term.lightgreen_on_green(term.center('')))
            print("\n")
            print(term.center(term.green(
                'Master password changed. You will need to sign in again. Press [ENTER] to continue.')))
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
