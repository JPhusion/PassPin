import re
import copy

from blessed import Terminal
from getpass import getpass
from prettytable import PrettyTable
from algorithms.encryption import generateKey, encrypt, decrypt


def editAccount(database, key):
    encryption_key = key
    old_database = copy.deepcopy(database)
    term = Terminal()
    term.number_of_colors = 16
    if len(database) == 0:
        print(term.clear)
        print(term.white_on_slategray(term.center('')))
        print(term.white_on_slategray(term.center(
            'PASSPIN PASSWORD MANAGER - NO ACCOUNTS')))
        print(term.white_on_slategray(term.center('')))
        print("\n")
        print(term.center(term.red(
            'There are no registered accounts. Enter a new one to begin. Press [ENTER] to continue.')))
        getpass("")
        return

    def clear(title):
        print(term.clear)
        print(term.white_on_slategray(term.center('')))
        print(term.white_on_slategray(term.center(title)))
        print(term.white_on_slategray(term.center('')))

    while True:
        try:
            print(term.clear)
            print(term.white_on_slategray(term.center('')))
            print(term.white_on_slategray(term.center(
                'PASSPIN PASSWORD MANAGER - SELECT PLATFORM')))
            print(term.white_on_slategray(term.center('')))
            print("\nSelect a platform from the list below:\n")
            counter = 0
            plat_list = {}
            temp = []
            for platform in database:
                temp.append(platform)
            temp.sort()
            for platform in temp:
                counter += 1
                print(f"{counter}. {platform.title()}")
                plat_list.update({counter: platform})
            print("")
            selection = int(input(": "))
            if 1 <= selection <= len(database):
                break
            print(term.red(
                "  Error: Invalid input. Please input the number which corresponds to your desired action. Press [ENTER] to continue."))
            getpass("  ")
        except ValueError:
            print(term.red(
                "  Error: Invalid input. Please input the number which corresponds to your desired action. Press [ENTER] to continue."))
            getpass("  ")

    x = PrettyTable()
    titles = ["*"]
    for key in database[plat_list[counter]]['1'].keys():
        if key != "password" and key != "decryptkey":
            titles.append(key.title())
    x.field_names = titles
    for number, account in enumerate(database[plat_list[counter]].values()):
        number += 1
        row = [number]
        for key, attribute in account.items():
            if key != "password" and key != "decryptkey":
                row.append(attribute)
        x.add_row(row)

    while True:
        print(term.clear)
        print(term.white_on_slategray(term.center('')))
        print(term.white_on_slategray(term.center(
            f'PASSPIN PASSWORD MANAGER - {str(plat_list[counter]).upper()} ACCOUNTS')))
        print(term.white_on_slategray(term.center('')))
        print("\n")
        print("Select an account from the list below:")
        print(x)
        selection = input(": ")
        if selection in database[plat_list[counter]]:
            break
        print(term.red(
            "  Error: Invalid input. Please input the number which corresponds to your desired action. Press [ENTER] to continue."))
        getpass("  ")

    fields = []
    for attribute in database[plat_list[counter]][selection].keys():
        if attribute != "decryptkey":
            fields.append(attribute)

    def edit():
        while True:
            clear("PASSPIN PASSWORD MANAGER - EDIT ATTRIBUTE")
            print("\nSelect an attribute to edit:\n")
            for i, attribute in enumerate(fields):
                print(f"{i + 1}. {attribute.title()}")
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
                    database[plat_list[counter]][selection]["password"] = encrypt(
                        generateKey(database[plat_list[counter]][selection]["decryptkey"]), password).decode('utf-8')
                    break
                else:
                    print(
                        term.red("Error: Passwords did not match. Please try again"))
        else:
            changed_attribute = input(
                f"\nEnter new {attribute} (press [ENTER] to cancel):\n: ")
            if changed_attribute != "":
                database[plat_list[counter]][selection][attribute.lower()] = (
                    changed_attribute)
    edit()

    while True:
        clear("PASSPIN PASSWORD MANAGER - CONFIRM EDIT ACCOUNT")
        print("\nConfirm the following account details:\n")
        x = PrettyTable()
        fields = []
        values = []
        for attribute, value in database[plat_list[counter]][selection].items():
            if attribute != "decryptkey":
                fields.append(attribute.title())
                if attribute == "password":
                    values.append(
                        decrypt(generateKey(database[plat_list[counter]][selection]["decryptkey"]), bytes(value, 'utf-8')))
                else:
                    values.append(value)
        x.field_names = fields
        x.add_row(values)
        print(x)
        print("\nSelect an action from the list below:\n\n1. Edit another attribute\n2. Cancel account edit\n3. Confirm and write account to database\n")
        action = input(": ")
        if action == "1":
            edit()
        elif action == "2":
            if input("\nConfirm account creation cancellation? (y/n):\n: ") == "y":
                database = copy.deepcopy(old_database)
        elif action == "3":
            database = encrypt(encryption_key, str(database)).decode('utf-8')
            with open("./data/database.txt", "r+") as f:
                data = f.read()
                f.seek(0)
                f.write(re.sub(data, database, data))
                f.truncate()
            print(
                f"\nNew {platform.title()} account has been added to the database.")
            getpass("\n\nPress [ENTER] to return to main menu.")
            return
        else:
            print(term.red(
                "  Error: Invalid input. Please input the number which corresponds to your desired action. Press [ENTER] to continue."))
            getpass("  ")
