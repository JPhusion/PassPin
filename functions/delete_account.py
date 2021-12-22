import re

from prettytable import PrettyTable
from blessed import Terminal
from getpass import getpass
from algorithms.encryption import encrypt
from algorithms.hasher import secure_hash


def deleteAccount(database, key, master_password):
    encryption_key = key
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

    print(term.clear)
    print(term.white_on_slategray(term.center('')))
    print(term.white_on_slategray(term.center(
        f'PASSPIN PASSWORD MANAGER - DELETE {str(plat_list[selection]).upper()} ACCOUNTS')))
    print(term.white_on_slategray(term.center('')))
    print("\n")

    x = PrettyTable()
    titles = ["*"]
    for key in database[plat_list[selection]]['1'].keys():
        if key != "password" and key != "decryptkey":
            titles.append(key.title())
    x.field_names = titles
    number = 0
    for account in database[plat_list[selection]].values():
        number += 1
        new_entry = [number]
        for key, attribute in account.items():
            if key != "password" and key != "decryptkey":
                new_entry.append(attribute)
        x.add_row(new_entry)

    while True:
        print(term.clear)
        print(term.white_on_slategray(term.center('')))
        print(term.white_on_slategray(term.center(
            f'PASSPIN PASSWORD MANAGER - DELETE {str(plat_list[selection]).upper()} ACCOUNTS')))
        print(term.white_on_slategray(term.center('')))
        print("\n")
        print("Select an account from the list below:")
        print(x)
        account = input(": ")
        if account in database[plat_list[selection]]:
            if input("Confirm irreversible account deletion? (y/n):\n: ") == "y":
                if secure_hash(getpass("Enter master password to delete the account:\n: ")) == master_password:
                    if len(database[plat_list[selection]]) == 1:
                        del database[plat_list[selection]]
                    else:
                        del database[plat_list[selection]][account]
                        database[plat_list[selection]] = {str(int(k) - 1) if int(k) > int(
                            account) else k: v for k, v in database[plat_list[selection]].items()}
                    database = encrypt(encryption_key, str(
                        database)).decode('utf-8')
                    with open("./data/database.txt", "r+") as f:
                        data = f.read()
                        f.seek(0)
                        f.write(re.sub(data, database, data))
                        f.truncate()
                    print(f"\nAccount has been permanently deleted.")
                    getpass("\n\nPress [ENTER] to return to main menu.")
                    break
                else:
                    print(term.red(
                        "  Error: Password incorrect. Press [ENTER] to continue."))
                    getpass("  ")
            else:
                print(
                    "\nAccount deletion cancelled. Press [ENTER] to continue")
                getpass("  ")
                break
            break
        print(term.red(
            "  Error: Invalid input. Please input the number which corresponds to your desired action. Press [ENTER] to continue."))
        getpass("  ")
    
