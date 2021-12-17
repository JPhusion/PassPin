# resets the master password

from algorithms.verification_code import verif_code
from external.send_email import email_pwrs

def reset_master():
    # TODO ASK FOR CURRENT PASSWORD AND ADD SECURITY QUESTIONS
    code = verif_code()
    email_pwrs(code)
    input_code = input("Please enter the verification code sent to you\n: ")
    if input_code == code:
        print("reset password")
    else:
        print("The verification code was incorrect. The owner has been alerted to your failed attempt.")
