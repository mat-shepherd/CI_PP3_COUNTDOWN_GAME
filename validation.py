# Imports
# Third Party
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from colorama import Fore
from profanity_check import predict_prob
from PyDictionary import PyDictionary
from collections import Counter
import countdown_numbers_solver

# Create instance of PyDictionary
dictionary = PyDictionary()


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


def validate_numbers(number):
    """
    Check player has selected no less than 0 and no
    more than 4 big numbers
    """
    try:
        if 0 <= int(number) <= 4:
            return True
        else:
            raise ValueError
    except ValueError:
        print(Fore.RED + 'Please enter only numbers between 0 and 4')
        return False


def check_profanity(word):
    """
    Check if word uses profanity
    """
    return predict_prob([word])


def check_dictionary(word):
    """
    Check if word is used in PyDictionary
    """
    try:
        word_meaning = dictionary.meaning(word)
    except IndexError:
        return None
    else:
        return word_meaning


def print_word_meaning(word, new_player):
    """
    Check if word is used in PyDictionary
    and print the word length and meaning
    """
    word_meaning_found = check_dictionary(word)
    if word_meaning_found is None:
        print(
            f"It appears '{word}' is NOT a word "
            "found in our  dictionary. Better luck "
            "next time!"
        )
        valid_word = False
    else:
        valid_word = True
        formatted_word = word.lower().capitalize()
        print(
            f"\nAccording to our dictionary the top "
            f"definitions of '{formatted_word}' are:\n"
            )
        count = 0
        for part_of_speech, meanings in word_meaning_found.items():
            for meaning in meanings:
                print(f"{part_of_speech} - {meaning}")
                # Only print the first 3 meanings
                count += 1
                if count >= 2:
                    break
    return valid_word


def check_letters_used(word, new_player):
    """
    Check if the player's word uses only
    the letters chosen for this round.
    Code adapted from answer by ChatGPT by
    https://openai.com.
    """
    # Convert chosen_letters and word to counter
    # dictionaries in lowercase
    chosen_counter = Counter(
        char.lower() for char in new_player.chosen_letters
    )
    word_counter = Counter(word.lower())

    for char, count in word_counter.items():
        if char not in chosen_counter or count > chosen_counter[char]:
            return False
    return True


def validate_user_word(user_word, new_player):
    """
    Check user letters round word is valid,
    using only the letters provided
    """
    try:
        # Check if word is profane
        if check_letters_used(user_word, new_player) is False:
            raise ValueError("You can only user the letters above!")
        elif check_profanity(user_word) >= 0.9:
            raise ValueError(
                "That word is on our profanity list and is not allowed."
            )
        elif user_word == '':
            raise ValueError('Please enter a word!')
        elif user_word.isalpha() is False:
            raise ValueError('Please enter letters only')
        elif len(user_word) < 2:
            raise ValueError('Your word must be longer than 2 letters!')
        elif (len(user_word) > 2 and user_word.isalpha()):
            return True
        else:
            raise ValueError("Your word isn't valid!")
    except ValueError as e:
        print(Fore.LIGHTRED_EX + str(e))
        return False


def validate_user_conundrum(user_word):
    """
    Check user conundrum word is valid,
    using only the letters provided
    """
    pass
