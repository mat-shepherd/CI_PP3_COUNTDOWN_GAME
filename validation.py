# Imports
# Python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from re import search, findall
# Third Party
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from colorama import Fore
from profanity_check import predict_prob
from PyDictionary import PyDictionary
from collections import Counter
import numexpr as ne

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
        word_meaning = dictionary.meaning(word, disable_errors=True)
    except IndexError:
        return None
    else:
        return word_meaning


def print_word_meaning(word, new_player):
    """
    Check if word is used in PyDictionary
    and print the word length and meaning
    """
    word_meaning_found = check_dictionary(word.lower())
    if word_meaning_found is None:
        # Return false so calling function can handle
        # printing no meaning found message
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
            # Only print the first 2 meanings
            if count >= 1:
                break
            for meaning in meanings:
                print(f"{part_of_speech} - {meaning}\n")
                count += 1
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


def check_numbers_used(solution, new_player):
    """
    Check if the player's solution uses only
    the numbers chosen for this round.
    Code adapted from answer by ChatGPT by
    https://openai.com.
    """
    chosen_counter = Counter(
        num for num in new_player.chosen_numbers
    )
    # Find numbers in solution string
    find_nums = r'\b\d+\b'
    solution_nums = findall(find_nums, solution)
    # Convert froms strings to numbers
    solution_nums = [int(num) for num in solution_nums]
    number_counter = Counter(solution_nums)

    for num, count in number_counter.items():
        print(num)
        if num not in chosen_counter or count > chosen_counter[num]:
            return False
    return True


def validate_user_numbers(user_solution, new_player):
    """
    Check user's numbers round solution is valid
    Check only numbers and operators are used
    """
    try:
        # Check solution only uses chosen numbers
        if check_numbers_used(user_solution, new_player) is False:
            raise ValueError('You can only use the chosen numbers above!')
        # Look for non-allowable characters
        # or empty value in user_solution
        illegal_regex = r'[^0-9\(\)\*\+\/\-\s]'
        match = search(illegal_regex, user_solution)
        if user_solution == '':
            raise ValueError('Please enter a solution!')
        elif match is not None:
            raise ValueError(
                'Please use only numbers or the '
                'operators + - / * ()'
            )
        else:
            return True
    except ValueError as e:
        print(Fore.LIGHTRED_EX + str(e))
        return False


def validate_user_solution(solution, new_player):
    """
    Evaluate user's solution is correct

    Evaluate user solution string and compare
    to target number
    """
    target = new_player.target_number
    solution_result = int(ne.evaluate(solution))
    result_valid = True if solution_result == target else False
    # Check is the solution close?
    target_difference = abs(target - solution_result)

    return result_valid, solution_result, target_difference


def validate_user_conundrum(user_word):
    """
    Check user conundrum word is valid,
    using only the letters provided
    """
    pass
