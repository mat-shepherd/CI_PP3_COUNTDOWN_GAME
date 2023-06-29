# Imports
# Third Party
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from colorama import Fore

# Validation functions


def validate_name(name):
    try:
        if (len(name) > 2 and name.isalpha()):
            return True
        elif name == '':
            raise ValueError('Please enter some text')
        elif len(name) < 2:
            raise ValueError('Please enter a name more than 2 characters long')
        else:
            raise ValueError('Please enter letters only')
    except ValueError as e:
        print(Fore.RED + str(e))
        return False


def validate_menu_value(number):
    """
    Check menu values are 1 or 2
    """
    try:
        if 1 <= int(number) <= 2:
            return True
        else:
            raise ValueError
    except ValueError:
        print(Fore.RED + 'Please enter only 1 or 2')
        return False


def validate_vowels(number):
    """
    Check player has selected no more than 9 vowels
    """
    try:
        if 1 <= int(number) <= 9:
            return True
        else:
            raise ValueError
    except ValueError:
        print(Fore.RED + 'Please enter only numbers between 3 and 9')
        return False


def validate_consonants(user_value):
    """
    Check player has selected correct number of
    consonant letters
    """
    pass


def validate_user_word(user_word):
    """
    Check user letters round word is valid,
    using only the letters provided
    """
    pass


def validate_user_conundrum(user_word):
    """
    Check user conundrum word is valid,
    using only the letters provided
    """
    pass
