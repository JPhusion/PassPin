import re
import csv
import json

from tqdm import tqdm
from blessed import Terminal
from getpass import getpass

from functions.delete_account import deleteAccount
from functions.enter_account import newAccount
from functions.edit_account import editAccount
from functions.retrieve import retrieve
from functions.password_generator import password_generator
from functions.security import security
from algorithms.hasher import secure_hash
from algorithms.encryption import generateKey, decrypt

while True:
    term = Terminal()
    term.number_of_colors = 16

    reader = csv.DictReader(open("./data/master.csv"))
    for raw in reader:
        master_password = raw.get('HASH')

    print(term.clear)
    print(term.white_on_slategray(term.center('')))
    print(term.white_on_slategray(term.center(
        'PASSPIN PASSWORD MANAGER - IDENTITY VERIFICATION: ENTER MASTER PASSWORD')))
    print(term.white_on_slategray(term.center('')))
    print("\n")
    input_password = getpass(': ')

    print(term.center('Verifying your identity\n'))

    if secure_hash(input_password, True) == master_password:
        print(term.clear)
        print(term.lightgreen_on_green(term.center('')))
        print(term.lightgreen_on_green(term.center('ACCESS GRANTED')))
        print(term.lightgreen_on_green(term.center('')))
        print(term.center('\n\n'))
        print(term.green(term.center('Your identity was successfully verified.\n')))

    else:
        print(term.clear)
        print(term.black_on_red(term.center('')))
        print(term.black_on_red(term.center('ACCESS DENIED')))
        print(term.black_on_red(term.center('')))
        print(term.center('\n\n'))
        print(term.center(term.red(
            'Your identity could not be verified. The owner has been alerted to your failed attempt with your details.\n')))
        pbar2 = tqdm(total=1, bar_format='  |{bar}|  ', colour='red')
        pbar2.update(n=1)
        exit()

    reader = csv.DictReader(open("./data/key.csv"))
    for raw in reader:
        encrypted_key = raw.get('KEY')

    key = bytes(decrypt(generateKey(input_password),
                bytes(encrypted_key, 'utf8')), 'utf8')
    encrypted_database = open('./data/database.txt', 'r')
    encrypted_file = encrypted_database.read()
    encrypted_database.close
    # print((decrypt(key, bytes(encrypted_file, 'utf8'))))
    database = json.loads(decrypt(key, bytes(encrypted_file, 'utf8')).strip(
        "'<>() ").replace('\'', '\"'))

    reader = csv.DictReader(open("./data/email.csv"))
    for raw in reader:
        email = raw.get('EMAIL')

    if email == "invalid_email@invalid_address.com":
        print(term.clear)
        print(term.white_on_slategray(term.center('')))
        print(term.white_on_slategray(term.center(
            'PASSPIN PASSWORD MANAGER - ENTER EMAIL')))
        print(term.white_on_slategray(term.center('')))
        print("\n")
        new_email = input(
            "Enter your email. This will be used to verify your identity when updating security.\n: ")
        with open('./data/email.csv', mode='w', newline="") as file:
            writer = csv.writer(file, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['EMAIL'])
            writer.writerow([new_email])
    while True:
        while True:
            try:
                print(term.clear)
                print(term.white_on_slategray(term.center('')))
                print(term.white_on_slategray(term.center(
                    'PASSPIN PASSWORD MANAGER - IDENTITY VERIFIED')))
                print(term.white_on_slategray(term.center('')))
                print("\n")
                print("Select an action from the list below:\n\n1. Retrieve a password\n2. Enter a new account\n3. Edit an account\n4. Delete an account\n5. Generate a secure password\n6. Update security\n7. Exit")
                selection = int(input("\n: "))
                if 1 <= selection <= 7:
                    break
                print(term.red(
                    "  Error: Invalid input. Please input the number which corresponds to your desired action. Press [ENTER] to continue."))
                getpass("  ")
            except ValueError:
                print(term.red(
                    "  Error: Invalid input. Please input the number which corresponds to your desired action. Press [ENTER] to continue."))
                getpass("  ")

        if selection == 1:
            retrieve(database)
        elif selection == 2:
            newAccount(database, key)
        elif selection == 3:
            editAccount(database, key)
        elif selection == 4:
            deleteAccount(database, key, master_password)
        elif selection == 5:
            password_generator()
        elif selection == 6:
            security(database, key, master_password)
            break
        elif selection == 7:
            exit()
