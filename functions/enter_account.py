import re
import json

from blessed import Terminal
from getpass import getpass
from prettytable import PrettyTable
from algorithms.encryption import encrypt, decrypt, generateKey
from algorithms.password_generator import generatePassword

"""
1. choose platform and convert to lowercase
2. check if platform already exists
3. if exists, go through each attribute and ask for input, else, ask for attributes
4. generate a 50 char decryptkey
5. generate an encryption key based off 50 char decryptkey
6. encrypt password input using encryption key
7. store new values in database
8. recrypt database and write to database file
"""


def newAccount(database, key):
    term = Terminal()
    term.number_of_colors = 16

    def clear(title):
        print(term.clear)
        print(term.white_on_slategray(term.center('')))
        print(term.white_on_slategray(term.center(title)))
        print(term.white_on_slategray(term.center('')))
    while True:
        try:
            clear('PASSPIN PASSWORD MANAGER - ADD ACCOUNT')
            print(
                "\nSelect a platform from the list below or enter the name of the platform:\n")
            counter = 0
            plat_list = {}
            temp = []
            for platform in database:
                temp.append(platform)
            temp.sort()
            print(f"1. New platform")
            plat_list.update({1: "New platform"})
            for platform in temp:
                counter += 1
                print(f"{counter + 1}. {platform.title()}")
                plat_list.update({counter + 1: platform})
            print("")
            selection = input(": ").lower()
            selection = int(selection)
            if 1 <= selection <= len(database) + 1:
                platform = plat_list[selection]
                break
            print(term.red(
                "  Error: Invalid input. Please input the number which corresponds to your desired action. Press [ENTER] to continue."))
            getpass("  ")
        except ValueError:
            if selection in database:
                confirmation = input(
                    f"  Platform already exists. Add new account to {selection}? (y/n)")
            else:
                confirmation = input(
                    f"  Confirm creation of new platform as {selection} (y/n)\n: ")
            if confirmation == "y" or confirmation == "yes":
                platform = selection
                break
            else:
                print(term.red(
                    "  Creation canclled. Press [ENTER] to continue."))
                getpass("  ")

    if platform.lower() == "new platform":
        platform = input("\nEnter platform name:\n: ")
    new_entry = {}
    if platform in database:
        for attribute in database[platform]["1"].keys():
            clear(f'PASSPIN PASSWORD MANAGER - ADD {platform.upper()} ACCOUNT')
            if attribute == "decryptkey":
                decryptkey = generatePassword(50)
                new_entry.update({attribute: decryptkey})
            elif attribute == "password":
                while True:
                    print(f"\nEnter {attribute.title()}:")
                    pw1 = getpass(": ")
                    print("Confirm password")
                    if getpass(": ") == pw1:
                        new_entry.update(
                            {attribute: encrypt(generateKey(decryptkey), pw1).decode('utf-8')})
                        break
                    else:
                        print(
                            term.red("Error: Passwords did not match. Please try again"))
            else:
                print(f"\nEnter {attribute.title()}:")
                new_entry.update({attribute: input(": ")})
    else:
        database.update({platform: {}})
        possible_attributes = ["decryptkey", "username", "first name",
                               "last name", "email", "recovery email", "phone number", "birthday"]
        for attribute in possible_attributes:
            clear(f'PASSPIN PASSWORD MANAGER - ADD {platform.upper()} ACCOUNT')
            if attribute == "decryptkey":
                decryptkey = generatePassword(50)
                new_entry.update({attribute: decryptkey})
            else:
                print(f"\nEnter {attribute.title()} (Press [ENTER] to skip):")
                entry_value = input(": ")
                if entry_value != "":
                    new_entry.update({attribute: entry_value})
        while True:
            clear("PASSPIN PASSWORD MANAGER - ADDITIONAL ATTRIBUTES")
            if input("\nAre there any other attributes you could like to add? (y/n): ") == "y":
                attribute = input(
                    "Enter the name of the attribute (Press [ENTER] to cancel):\n: ").lower()
                if attribute != "":
                    print(
                        f"\nEnter {attribute.title()} (Press [ENTER] to cancel):")
                    entry_value = input(": ")
                    if entry_value != "":
                        new_entry.update({attribute: entry_value})
            else:
                break
        while True:
            print(f"\nEnter Password:")
            pw1 = getpass(": ")
            print("Confirm Password")
            if getpass(": ") == pw1:
                new_entry.update(
                    {"password": encrypt(generateKey(decryptkey), pw1).decode('utf-8')})
                break
            else:
                print(
                    term.red("Error: Passwords did not match. Please try again"))

    while True:
        clear("PASSPIN PASSWORD MANAGER - CONFIRM NEW ACCOUNT")
        print("\nConfirm the following account details:\n")
        x = PrettyTable()
        fields = []
        values = []
        for attribute, value in new_entry.items():
            if attribute != "decryptkey":
                fields.append(attribute.title())
                if attribute == "password":
                    values.append(
                        decrypt(generateKey(new_entry["decryptkey"]), bytes(value, 'utf-8')))
                else:
                    values.append(value)
        x.field_names = fields
        x.add_row(values)
        print(x)
        print("\nSelect an action from the list below:\n\n1. Edit an attribute\n2. Cancel account creation\n3. Confirm and write account to database\n")
        action = input(": ")
        if action == "1":
            while True:
                clear("PASSPIN PASSWORD MANAGER - EDIT ATTRIBUTE")
                print("\nSelect an attribute to edit:\n")
                for i, attribute in enumerate(fields):
                    print(f"{i + 1}. {attribute}")
                edit_no = input("\n: ")
                try:
                    if 1 <= int(edit_no) <= len(fields):
                        attribute = fields[int(edit_no) - 1]
                        break
                    else:
                        print(term.red(
                            "  Error: Invalid input. Please input the number which corresponds to your desired action. Press [ENTER] to continue."))
                        getpass("  ")
                except ValueError:
                    print(term.red(
                        "  Error: Invalid input. Please input the number which corresponds to your desired action. Press [ENTER] to continue."))
                    getpass("  ")
            clear(f"PASSPIN PASSWORD MANAGER - EDIT {attribute.upper()}")
            if attribute.lower() == "password":
                while True:
                    password = getpass(
                        "\nEnter new password (press [ENTER] to cancel):\n: ")
                    if password == "":
                        break
                    passtest = getpass(
                        "\nConfirm new password (press [ENTER] to cancel):\n: ")
                    if passtest == "":
                        break
                    if password == passtest:
                        new_entry["password"] = encrypt(
                            generateKey(decryptkey), password).decode('utf-8')
                        break
                    else:
                        print(
                            term.red("Error: Passwords did not match. Please try again"))
            else:
                changed_attribute = input(
                    f"\nEnter new {attribute} (press [ENTER] to cancel):\n: ")
                if changed_attribute != "":
                    new_entry[attribute.lower()] = (changed_attribute)
        
        elif action == "2":
            if input("\nConfirm account creation cancellation? (y/n):\n: ") == "y":
                return
        elif action == "3":
            database[platform].update(
                {str(len(database[platform]) + 1): new_entry})
            database = encrypt(key, str(database)).decode('utf-8')
            with open("./data/database.txt", "r+") as f:
                data = f.read()
                f.seek(0)
                f.write(re.sub(data, database, data))
                f.truncate()
            print(f"\nNew {platform.title()} account has been added to the database.")
            getpass("\n\nPress [ENTER] to return to main menu.")
            return
        else:
            print(term.red(
                "  Error: Invalid input. Please input the number which corresponds to your desired action. Press [ENTER] to continue."))
            getpass("  ")
