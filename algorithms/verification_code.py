import random
import string

def verif_code():
    characters = string.ascii_uppercase + string.digits
    code = random.sample(characters, 24)
    formatted_code = ""
    counter = 0
    for char in code:
        if counter % 4 == 0 and counter != 0:
            formatted_code += "-"
        formatted_code += char
        counter += 1
    return formatted_code
