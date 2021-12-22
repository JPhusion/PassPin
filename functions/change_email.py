import csv

from blessed import Terminal
from getpass import getpass

from algorithms.hasher import secure_hash
from external.send_email import email_pwrs
from algorithms.verification_code import verif_code


def change_email(master_password):
    term = Terminal()
    print(term.clear)
    print(term.black_on_red(term.center('')))
    print(term.black_on_red(term.center(
        'PASSPIN PASSWORD MANAGER - CHANGE MASTER PASSWORD')))
    print(term.black_on_red(term.center('')))
    if secure_hash(getpass("\nEnter master password:\n: ")) == master_password:
        # TODO ASK FOR CURRENT PASSWORD AND ADD SECURITY QUESTIONS
        print("\nSending verification code...")
        code = verif_code()
        email_pwrs(code)
        input_code = input(
            "\nPlease enter the verification code sent to you\n: ")
        if input_code == code:
            term = Terminal()
            print(term.clear)
            print(term.black_on_red(term.center('')))
            print(term.black_on_red(term.center(
                'PASSPIN PASSWORD MANAGER - ENTER EMAIL')))
            print(term.black_on_red(term.center('')))
            print("\n")
            new_email = input(
                "Enter your new email. This will be used to verify your identity when updating security.\n: ")
            with open('./data/email.csv', mode='w', newline="") as file:
                writer = csv.writer(file, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['EMAIL'])
                writer.writerow([new_email])
            print(term.clear)
            print(term.lightgreen_on_green(term.center('')))
            print(term.lightgreen_on_green(term.center(
                'PASSPIN PASSWORD MANAGER - CHANGED EMAIL')))
            print(term.lightgreen_on_green(term.center('')))
            print("\n")
            print(term.center(term.green(
                f'Successfully changed email to {new_email}.')))
            print("\n")
            print(term.center(term.green(
                'You will need to sign in again. Press [ENTER] to continue.')))
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
