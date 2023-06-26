# Imports
# Third Party
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from colorama import Fore

# Validation functions

def validate_name(name):
    try:
        if (len(name) > 2 and name.isalpha()):
            return True
        else:
            raise Exception
    except TypeError:
        print(Fore.RED + 'Please enter letters only')
        return False
    except EOFError:
        print(Fore.RED + 'Please enter your name')
        return False

def validate_menu_value(name):
    """
    Check menu values are 1 or 2
    """
    try:
        if 1 <= int(name) <= 2:
            return True
        else:
            raise ValueError
    except ValueError:
        print(Fore.RED + 'Please enter only 1 or 2')
        return False