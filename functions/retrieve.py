import pyperclip
from algorithms.encryption import decrypt, generateKey
from prettytable import PrettyTable
from blessed import Terminal
from getpass import getpass


def retrieve(database):
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
        f'PASSPIN PASSWORD MANAGER - {str(plat_list[selection]).upper()} ACCOUNTS')))
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
    
    encrypted_password = database[plat_list[counter]][selection]["password"]
    password = decrypt(generateKey(database[plat_list[counter]][selection]["decryptkey"]), bytes(encrypted_password, 'utf-8'))
    pyperclip.copy(password)
    print(f"\nPassword has been copied to your clipboard.")
    getpass("\n\nPress [ENTER] to return to main menu.")
