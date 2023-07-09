# Imports
# Python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from re import search, findall
from collections import Counter
# Third Party
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from colorama import Fore
from profanity_check import predict_prob
from PyDictionary import PyDictionary
import numexpr as ne

# Create instance of PyDictionary
dictionary = PyDictionary()


def validate_name(name):
    """
    Check name input is valid.

    Check name input is between 2 and 10
    alphabet characters only and that name passes
    profanity filter.

    Parameters
    ----------
    name : string
        Name string input by player.

    Returns
    -------
    boolean
        Returns False on ValueError.
    """
    try:
        if check_profanity(name) >= 0.9:
            raise ValueError(
                "That name doesn't pass our profanity check"
            )
        elif (2 <= len(name) <= 10 and name.isalpha()):
            return True
        elif name == '':
            raise ValueError('Please enter some text')
        elif not name.isalpha():
            raise ValueError(
                'Please enter letters only. '
                'No spaces or other characters.'
            )
        elif not 2 <= len(name) <= 10:
            raise ValueError(
                'Please enter a name more than 2 characters '
                'and less than 10 characters long'
            )
        else:
            raise ValueError(
                'Please enter a name more than 2 characters '
                'and less than 10 characters long'
            )
    except ValueError as e:
        print(Fore.RED + str(e))
        return False


def validate_menu_value(number, current_screen):
    """
    Check menu values are 1, 2 or 3.

    Check values are 1, 2 or 3 in intro screen
    else check values are 1 or 2.

    Parameters
    ----------
    number : string
        Number string input by player.
    current_screen : string
        Keyword indicating current screen
        player is viewing.

    Returns
    -------
    boolean
        Returns False on ValueError.
    """
    try:
        if current_screen in ['intro']:
            if 1 <= int(number) <= 3:
                return True
            else:
                raise ValueError
        else:
            if 1 <= int(number) <= 2:
                return True
            else:
                raise ValueError
    except ValueError:
        if current_screen in ['intro']:
            print(Fore.RED + 'Please enter only 1, 2 or 3')
        else:
            print(Fore.RED + 'Please enter only 1 or 2')
        return False


def validate_vowels(number):
    """
    Check player has selected no less than 3 and no
    more than 9 vowels.

    Parameters
    ----------
    number : string
        Number string input by player.

    Returns
    -------
    boolean
        Returns False on ValueError.
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

    Parameters
    ----------
    word : string
        String input by player.

    Returns
    -------
    return predict_prob([word]) : float
        Probablity that a string contains profanity.
    """
    return predict_prob([word])


def check_dictionary(word):
    """
    Check if word is used in PyDictionary

    Parameters
    ----------
    word : string
        String input by player.

    Returns
    -------
    word_meaning : list or None
        Word meaning if found in PyDictionary.
    """
    try:
        word_meaning = dictionary.meaning(word, disable_errors=True)
    except IndexError:
        return None
    else:
        return word_meaning


def print_word_meaning(word, new_player=None):
    """
    Check if word is used in PyDictionary
    and print the word length and meaning

    Parameters
    ----------
    word : string
        String input by player.
    new_player : object
        Current Player Object.

    Returns
    -------
    valid_word: boolean
        True if word found in PyDictionary
        and false if not.
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
            f"definition(s) of '{formatted_word}' is/are:\n"
            )
        count = 0
        for part_of_speech, meanings in word_meaning_found.items():
            # Only print the first 2 meanings
            if count > 1:
                break
            for meaning in meanings:
                print(f"{part_of_speech} - {meaning}\n")
                count += 1
                if count > 1:
                    break
    return valid_word


def check_letters_used(word, new_player=None, new_conundrum=None):
    """
    Check if the player's word uses only
    the letters chosen for this round.
    Code adapted from answer by ChatGPT by
    https://openai.com.

    Parameters
    ----------
    word : string
        String input by player.
    new_player : object
        Current Player Object.
    new_conundrum : object
        Current Conundrum Object.

    Returns
    -------
    boolean
        True if word only users letters in
        conundrum and false if not.
    """
    # Convert user input word and conundrum letters
    # or chosen letters to counter dictionaries
    # in lowercase. Check if this is conundrum
    # or letters round by checking if new_condrum
    # object was passed to function
    if new_conundrum:
        chosen_counter = Counter(
            char.lower() for char in new_conundrum.target
        )
    else:
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
    more than 4 big numbers.

    Parameters
    ----------
    number : string
        Number string input by player.

    Returns
    -------
    boolean
        True if number is 0 to 4 and
        False if not.
    """
    try:
        if 0 <= int(number) <= 4:
            return True
        else:
            raise ValueError
    except ValueError:
        print(Fore.RED + 'Please enter only numbers between 0 and 4')
        return False


def validate_user_word(user_word, new_player=None):
    """
    Check user letters round word is valid,
    using only the letters provided.

    Parameters
    ----------
    user_word : string
        String input by player.
    new_player : object
        Current Player Object.

    Returns
    -------
    boolean
        True if word is valid and only users
        chosen letters and False if not.
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


def check_numbers_used(solution, new_player=None):
    """
    Check if the player's solution uses only
    the numbers chosen for this round.
    Code adapted from answer by ChatGPT by
    https://openai.com.

    Parameters
    ----------
    solution : string
        Solution string input by player.
    new_player : object
        Current Player Object.

    Returns
    -------
    boolean
        True if only uses numbers from chosen
        numbers and False if not.
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
        if num not in chosen_counter or count > chosen_counter[num]:
            return False
    return True


def validate_user_numbers(user_solution, new_player=None):
    """
    Check user's numbers round solution is valid
    Check only numbers and operators are used

    Parameters
    ----------
    user_solution : string
        Solution string input by player.
    new_player : object
        Current Player Object.

    Returns
    -------
    boolean
        True if only uses numbers from chosen
        numbers, only uses numbers, and only uses
        allowed operators and False if not.
    """
    try:
        # Check solution only uses chosen numbers
        if check_numbers_used(user_solution, new_player) is False:
            raise ValueError('You can only use the chosen numbers above!')
        # Look for non-allowable characters,
        # empty value, or just spaces in
        # user_solution
        illegal_regex = r'[^0-9\(\)\*\+\/\-\s]'
        match = search(illegal_regex, user_solution)
        if user_solution == '' or user_solution.isspace():
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


def validate_user_solution(solution, new_player=None):
    """
    Evaluate user's solution is correct.

    Evaluate user solution string and compare
    to target number.

    Parameters
    ----------
    solution : string
        Solution string input by player.
    new_player : object
        Current Player Object.

    Returns
    -------
    result_valid : boolean
        True if solution achieves target number
        and False if not.
    solution_result : int
        Evaluated number result of solution string.
    target_difference : int
        Difference, if any, between evaluated number
        result of solution string and target number.
    """
    target = new_player.target_number
    solution_result = int(ne.evaluate(solution))
    result_valid = True if solution_result == target else False
    # Check is the solution close?
    target_difference = abs(target - solution_result)

    return result_valid, solution_result, target_difference


def validate_user_conundrum(user_word, new_player=None, new_conundrum=None):
    """
    Check user conundrum word is valid,
    using only the letters provided.

    Check conundrum input passes profanity
    filter, only uses letters, and is exactly
    9 letters long.

    Parameters
    ----------
    user_word : string
        Solution string input by player.
    new_player : object
        Current Player Object.
    new_conundrum : object
        Current Conundrum Object.

    Returns
    -------
    boolean
        True if valid and False if ValueError.
    """
    try:
        # Check if word is profane
        if check_letters_used(user_word, new_player, new_conundrum) is False:
            raise ValueError("You can only user the letters above!")
        elif check_profanity(user_word) >= 0.9:
            raise ValueError(
                "That word is on our profanity list and is not allowed."
            )
        elif user_word == '':
            raise ValueError('Please enter a word!')
        elif user_word.isalpha() is False:
            raise ValueError('Please enter letters only')
        elif len(user_word) < 9:
            raise ValueError('Your word must be 9 letters long!')
        elif (len(user_word) == 9 and user_word.isalpha()):
            return True
        else:
            raise ValueError("Your word isn't valid!")
    except ValueError as e:
        print(Fore.LIGHTRED_EX + str(e))
        return False
