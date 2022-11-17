from functions.change_email import change_email
from functions.reset_master import reset_master
from functions.change_encryption_key import change_encryption_key
from functions.re_encryrypt_passwords import re_encryrypt_passwords
from blessed import Terminal
from getpass import getpass


def security(database, key, master_password):
    term = Terminal()
    while True:
        try:
            print(term.clear)
            print(term.black_on_red(term.center('')))
            print(term.black_on_red(term.center(
                'PASSPIN PASSWORD MANAGER - UPDATE SECURITY')))
            print(term.black_on_red(term.center('')))
            print("\n")
            print("Select an action from the list below:\n\n1. Change master password\n2. Change encryption key\n3. Re-encrypt all passwords\n4. Change verification email\n5. Cancel and return to main menu")
            selection = int(input("\n: "))
            if 1 <= selection <= 5:
                break
            print(term.red(
                "  Error: Invalid input. Please input the number which corresponds to your desired action. Press [ENTER] to continue."))
            getpass("  ")
        except ValueError:
            print(term.red(
                "  Error: Invalid input. Please input the number which corresponds to your desired action. Press [ENTER] to continue."))
            getpass("  ")

    if selection == 1:
        reset_master(key, master_password)
    elif selection == 2:
        change_encryption_key(database, master_password)
    elif selection == 3:
        re_encryrypt_passwords(database, key, master_password)
    elif selection == 4:
        change_email(master_password)
    elif selection == 5:
        pass
