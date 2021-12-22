import pyperclip

from algorithms.password_generator import generatePassword
from blessed import Terminal
from getpass import getpass


def password_generator():
    while True:
        term = Terminal()
        term.number_of_colors = 16
        print(term.clear)
        print(term.white_on_slategray(term.center('')))
        print(term.white_on_slategray(term.center(
            'PASSPIN PASSWORD MANAGER - PASSWORD GENERATOR')))
        print(term.white_on_slategray(term.center('')))
        print("\nEnter length of password (suggested min. length 12):")
        number = input(": ")
        try:
            length = int(number)
        except ValueError:
            print(term.red(
                "  Error: Invalid input. Input must be a positive integer. Press [ENTER] to continue."))
            getpass("  ")
        if length < 1:
            print(term.red(
                "  Error: Invalid input. Input must be a positive integer. Press [ENTER] to continue."))
            getpass("  ")
        else:
            break
    print(term.clear)
    print(term.white_on_slategray(term.center('')))
    print(term.white_on_slategray(term.center(
        'PASSPIN PASSWORD MANAGER - PASSWORD GENERATOR')))
    print(term.white_on_slategray(term.center('')))
    print("\n\n")
    password = generatePassword(length)
    print(term.green(term.center(password)))
    print("\n\n")
    pyperclip.copy(password)
    print(term.center(
        "Password copied to clipboard. Press [ENTER] to return to main menu."))
    getpass("  ")
