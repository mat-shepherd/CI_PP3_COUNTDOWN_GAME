# Imports
# Third Party
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from colorama import Fore
from profanity_check import predict
from PyDictionary import PyDictionary
import countdown_numbers_solver

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
    Check player has selected no less than 3 and no
    more than 9 vowels
    """
    try:
        if 3 <= int(number) <= 9:
            return True
        else:
            raise ValueError
    except ValueError:
        print(Fore.RED + 'Please enter only numbers between 3 and 9')
        return False


def check_profanity(word):
    """
    Check if word uses profanity
    """
    return predict([word])


def check_dictionary(word):
    """
    Check if word is used in PyDictionary
    """
    dictionary = PyDictionary()
    word_meaning = dictionary.meaning(word)
    return word_meaning


def print_word_meaning(word):
    """
    Check if word is used in PyDictionary
    and print the word meaning
    """
    word_meaning_found = check_dictionary(word)
    if word_meaning_found is None:
        print(f"It appears '{word}' is NOT a word found in the dictionary.")
    else:
        print(f"You're in luck, '{word}' IS found in the dictionary!")
        print(f"The definition of '{word}' is:")
        for part_of_speech, meanings in word_meaning_found.items():
            for meaning in meanings:
                print(f"{part_of_speech} - {meaning}")


def validate_user_word(user_word):
    """
    Check user letters round word is valid,
    using only the letters provided
    """
    try:
        if (len(user_word) > 2 and user_word.isalpha()):
            return True
        # Check if word is profane
        if check_profanity(user_word) == 1:
            print(f"That word is not allowed")
        elif user_word == '':
            raise ValueError('Please enter a word!')
        elif user_word.isalpha() is False:
            raise ValueError('Please enter letters only')
        elif len(user_word) < 2:
            raise ValueError('Your word must be longer than 2 letters!')
        else:
            raise ValueError("Your word isn't valid!")
    except ValueError as e:
        print(Fore.RED + str(e))
        return False


def validate_user_conundrum(user_word):
    """
    Check user conundrum word is valid,
    using only the letters provided
    """
    pass
