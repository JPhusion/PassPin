import csv

from blessed import Terminal
from getpass import getpass
from algorithms.verification_code import verif_code
from algorithms.encryption import encrypt, generateKey
from algorithms.hasher import secure_hash
from external.send_email import email_pwrs


def reset_master(old_key, master_password):
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
            while True:
                pw1 = getpass("\nEnter new master password:\n: ")
                pw2 = getpass("\nConfirm new master password:\n: ")
                pw3 = getpass("\nConfirm new master password:\n: ")
                if pw1 == pw2 and pw2 == pw3:
                    with open('./data/master.csv', mode='w', newline="") as file:
                        writer = csv.writer(file, delimiter=',',
                                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow(['HASH'])
                        writer.writerow([secure_hash(pw1)])
                    with open('./data/key.csv', mode='w', newline="") as file:
                        writer = csv.writer(file, delimiter=',',
                                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow(['KEY'])
                        writer.writerow(
                            [(encrypt(generateKey(pw1), old_key.decode('utf-8'))).decode('utf-8')])
                    print(term.clear)
                    print(term.lightgreen_on_green(term.center('')))
                    print(term.lightgreen_on_green(term.center(
                        'PASSPIN PASSWORD MANAGER - CHANGED MASTER PASSWORD')))
                    print(term.lightgreen_on_green(term.center('')))
                    print("\n")
                    print(term.center(term.green(
                        'Master password changed. You will need to sign in again. Press [ENTER] to continue.')))
                    getpass("")
                    break
                else:
                    print(term.red("Error: Passwords did not match. Please try again. Press [ENTER] to continue."))
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
