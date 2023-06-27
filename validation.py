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
    except TypeError as e:
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