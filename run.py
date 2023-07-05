# Imports
# Python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from time import time, sleep
from re import sub
import random
import termios
import sys
import tty
import pager
# Internal
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from validation import (
    validate_name,
    validate_menu_value,
    validate_vowels,
    check_profanity,
    check_dictionary,
    print_word_meaning,
    validate_user_word,
    validate_numbers,
    validate_user_numbers,
    validate_user_solution,
    validate_user_conundrum
)
from word_set import word_set
from nine_letter_word_set import nine_letter_word_set
# Third Party
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from inputimeout import inputimeout, TimeoutOccurred
from colorama import init
from colorama import Fore, Back, Style
from colorama.ansi import clear_screen
from art import text2art
from num2words import num2words
from anagram_solver.anagram_solver import find_possible, return_words
import countdown_numbers_solver

# Initialize colorama
init()

# Classes


class Player:
    """
    The Player class to contain all player attributes
    """
    def __init__(self,
                 name='Player',
                 score=0,
                 high_score=0,
                 round_time=0,
                 current_round=0,
                 chosen_letters=[],
                 chosen_numbers=[],
                 target_number=0,
                 guessed_words=[],
                 guessed_solutions=[],
                 guessed_conundrum=[]
                 ):
        self.name = name
        self.score = score
        self.high_score = high_score
        self.round_time = round_time
        self.current_round = current_round
        self.chosen_letters = chosen_letters
        self.chosen_numbers = chosen_numbers
        self.target_number = target_number
        self.guessed_words = guessed_words
        self.guessed_solutions = guessed_solutions
        self.guessed_conundrum = guessed_conundrum

    def update_score(self):
        """
        Update the Player score for the current
        round based on the player's guess and time
        remaining
        """
        if 1 <= Screen.round_number <= 3:
            round_score = (
                len(self.guessed_words[-1]) *
                self.round_time
            )
            self.score += round_score
        elif 4 <= Screen.round_number <= 5:
            round_score = 10 * self.round_time
            self.score += round_score

        return round_score


class Screen:
    """
    The Screen class to contain all screen
    definitions and attributes
    """
    screen_data = {
        'intro': 'intro_screen_data.txt',
        'rules': 'rules_screen_data.txt',
        'enter_name': 'game_screen_data.txt',
        'letters_round': 'game_screen_data.txt',
        'show_letters': 'game_screen_data.txt',
        'letters_guess': 'game_screen_data.txt',
        'letters_feedback': 'game_screen_data.txt',
        'numbers_round': 'game_screen_data.txt',
        'show_numbers': 'game_screen_data.txt',
        'numbers_guess': 'game_screen_data.txt',
        'numbers_feedback': 'game_screen_data.txt',
        'show_conundrum': 'game_screen_data.txt',
        'conundrum_guess': 'game_screen_data.txt',
        'conundrum_feedback': 'game_screen_data.txt',
        'game_over': 'game_screen_data.txt'
    }

    letter_tiles = """
            +-----+-----+-----+-----+-----+-----+-----+-----+-----+  
            |  *  |  *  |  *  |  *  |  *  |  *  |  *  |  *  |  *  |  
            +-----+-----+-----+-----+-----+-----+-----+-----+-----+  
    """

    round_number = 0

    def __init__(self, screen_data_file):
        self.screen_data_param = screen_data_file
        self.screen_data_file = Screen.screen_data[screen_data_file]

    def render(self,
               new_player=None,
               new_letters=None,
               new_numbers=None,
               new_conundrum=None
               ):
        """
        Render screen elements to the terminal.

        Set screen bg to blue and render
        screen text, score, timer,  and prompt
        in the terminal.

        Parameters
        ----------
        new_player : object
            Current Player Object
        new_letters : object
            Current Letters Object
        new_numbers : object
            Current Numbers Object
        new_conundrum : object
            Current Conundrum Object

        Returns
        -------
        user_prompt : string
            User inputted string
        """
        print(Style.BRIGHT + Back.BLUE)
        print(clear_screen())
        self.display_text_art()
        if self.screen_data_param in [
            'intro',
            'rules',
            'game_over'
        ]:
            self.display_text()
        # Update tiles on enter_name,
        # show and feedback screens
        if self.screen_data_param in [
            'enter_name',
            'show_letters',
            'letters_guess',
            'letters_feedback',
            'show_numbers',
            'numbers_guess',
            'numbers_feedback',
            'show_conundrum',
            'conundrum_guess',
            'conundrum_feedback'
        ]:
            self.update_tiles(new_player, new_conundrum, self.screen_data_param)
        # Only print tiles and score during
        # enter name, rounds, and feedback screens
        if self.screen_data_param not in [
            'intro',
            'rules',
            'game_over'
        ]:
            self.display_score(new_player)
            print_centered(
                Style.BRIGHT + Fore.YELLOW +
                self.letter_tiles +
                Fore.RESET
            )
        # Only print subheading on certain rounds
        if (
            Screen.round_number == 1
            and new_player.chosen_letters == [
                ' ', ' ', 'R', 'E', 'A', 'D', 'Y', '?', ' '
            ]
        ):
            print_centered(
                Fore.WHITE +
                f"{new_player.name.upper()}, "
                "LET'S PLAY COUNTDOWN!\n"
            )
        elif (
            Screen.round_number == 4
            and self.screen_data_param not in [
                'show_numbers',
                'numbers_guess',
                'numbers_feedback'
                ]
        ):
            print_centered(
                Style.BRIGHT + Fore.WHITE +
                f"     {new_player.name.upper()}, "
                "WELCOME TO THE NUMBERS ROUND!\n"
            )
        # Print Target Number in numbers round
        elif (
            Screen.round_number == 4
            and self.screen_data_param in [
                'show_numbers',
                'numbers_guess',
                'numbers_feedback'
                ]
        ):
            print_centered(
                Style.BRIGHT + Fore.YELLOW +
                f'          TARGET: {new_player.target_number}\n'
                + Fore.RESET
            )
        elif self.screen_data_param == 'show_conundrum':
            print_centered(
                Style.BRIGHT + Fore.WHITE +
                f"       {new_player.name.upper()}, "
                "WELCOME TO THE FINAL CONUNDRUM ROUND!\n"
            )
        elif self.screen_data_param == 'game_over':
            print_centered(
                f"\n{new_player.name.upper()}!\n"
            )
            print_centered(f"YOUR FINAL SCORE IS {new_player.score}!\n")
            print_centered(f"CONGRATULATIONS!\n")
        user_prompt = self.display_prompt(
            new_player,
            new_letters,
            new_numbers,
            new_conundrum
        )

        return user_prompt

    def display_text_art(self):
        """
        Output text as ASCII art via Art library
        """
        if self.screen_data_param in ['intro', 'rules', 'enter_name']:
            result = text2art(
                '        COUNTDOWN', font='small'
                )
            print(Style.BRIGHT + result)
        elif self.screen_data_param not in ['intro', 'rules', 'enter_name']:
            round_word = num2words(
                self.round_number, lang='en'
                ).upper()
            # Add varying amount of spaceds
            # based on length of round number string
            if Screen.round_number == 1:
                spaces_num = len(round_word) * (5 // Screen.round_number)
            else:
                spaces_num = (
                    5 + len(round_word)
                    * (5 // Screen.round_number) + 2
                )
            spaces_str = ' ' * int(spaces_num)
            if self.screen_data_param == 'game_over':
                # Add extra spacing to center
                spaces_str += spaces_str + ' '
                result = text2art(
                    f'{spaces_str}GAME OVER', font='small'
                    )
            else:
                result = text2art(
                    f'{spaces_str}ROUND {round_word}', font='small'
                    )
            print(Style.BRIGHT + Fore.WHITE + result)

    def display_text(self):
        """
        Retrieve screen text from data files
        """
        try:
            with open(self.screen_data_file) as f:
                # Paginate text if on rules
                if self.screen_data_file == 'rules_screen_data.txt':
                    pager.page(f)
                else:
                    text = f.read()
                    print(Style.BRIGHT + text)
        except OSError as e:
            errno, strerror = e.args
            print(f'There is an I/O error number, {errno}: {strerror}.')

    def timed_input(self, new_player=None, timer_prompt=None, new_conundrum=None):
        """
        Display timed input for 30 seconds
        """
        countdown = 60 if Screen.round_number == 4 else 30
        start_time = time()

        while True:
            try:
                user_prompt = inputimeout(
                    prompt=timer_prompt,
                    timeout=countdown
                )
                time_remaining = int(countdown - (time() - start_time))
                # Had to add additional timeout check
                # and raise error to work on Heroku
                if time_remaining == 0:
                    raise TimeoutOccurred("Time's Up!")
                # Check round number so we know which
                # validations to use
                if 1 <= Screen.round_number <= 3:
                    if validate_user_word(user_prompt, new_player):
                        # Store guessed words in Player attribute
                        # at index one less than round number
                        new_player.guessed_words.insert(
                            Screen.round_number - 1,
                            user_prompt
                        )
                        time_remaining = int(countdown - (time() - start_time))
                        break
                elif Screen.round_number == 4:
                    if validate_user_numbers(user_prompt, new_player):
                        # Store guessed solutions in Player attribute
                        # at index one less than round number
                        new_player.guessed_solutions.insert(
                            Screen.round_number - 1,
                            user_prompt
                        )
                        time_remaining = int(countdown - (time() - start_time))
                        break
                elif Screen.round_number == 5:
                    if validate_user_conundrum(user_prompt, new_player, new_conundrum):
                        # Store guessed solutions in Player attribute
                        # at index one less than round number
                        new_player.guessed_conundrum.insert(
                            Screen.round_number - 1,
                            user_prompt
                        )
                        time_remaining = int(countdown - (time() - start_time))
                        break
            except TimeoutOccurred:
                print("Time's Up!")
                user_prompt = False
                time_remaining = 0
                break

            time_remaining = int(countdown - (time() - start_time))
            if time_remaining > 0:
                print('You have :', time_remaining, 'seconds remaining!')

        return user_prompt, time_remaining

    def display_score(self, new_player=None):
        """
        Display the user score
        """
        print_centered(f'Your Score: {new_player.score}')

    def update_tiles(self, new_player=None, new_conundrum=None, screen_param=None):
        """
        Update letters tiles with chosen letters
        """
        # If enter_name screen populate letters with Ready?
        if len(new_player.chosen_letters) == 0:
            new_player.chosen_letters = [
                ' ',
                ' ',
                'R',
                'E',
                'A',
                'D',
                'Y',
                '?',
                ' '
            ]
        # Reset letter tiles
        self.letter_tiles = sub(r'[a-zA-Z0-9]', '*', self.letter_tiles)
        if Screen.round_number != 4:
            # Check if this is conundrum round and whether
            # to show target or scrambled conundrum
            # otherwist show player chosen letters
            if screen_param in ['show_conundrum', 'conundrum_guess']:
                letters_object = list(new_conundrum.scrambled)
                print(f'Target: {new_conundrum.target}')
            elif screen_param == 'conundrum_feedback':
                letters_object = list(new_conundrum.target)
            else:
                letters_object = new_player.chosen_letters

            for char in letters_object:
                # Loop through player chosen letters and use
                # each letter to replace existing tile characters
                self.letter_tiles = sub(
                    r'[*]', char, self.letter_tiles,
                    count=1
                )
        elif Screen.round_number == 4:
            # Replace 1,2 and last characters with spaces
            self.letter_tiles = sub(r'\*', ' ', self.letter_tiles, count=1)
            self.letter_tiles = sub(r'\*', ' ', self.letter_tiles, count=1)
            self.letter_tiles = sub(r'\*(?!.*\*)', ' ', self.letter_tiles)
            for char in new_player.chosen_numbers:
                # Loop through player chosen numbers and convert
                # each number to a string character to replace
                # existing tile characters
                # Calculate how many spaces to keep number
                # centered
                char = str(char)
                char_length = len(char)
                spaces_left = 1
                spaces_right = 1
                if char_length == 1:
                    spaces_left = 2
                if 1 <= char_length <= 2:
                    spaces_right = 2
                if char_length == 3:
                    spaces_right = 1
                centered_char = ' ' * spaces_left + char + ' ' * spaces_right
                self.letter_tiles = sub(
                    r'(\s*)\*(\s*)', centered_char,
                    self.letter_tiles,
                    count=1
                )

    def display_prompt(self,
                       new_player=None,
                       new_letters=None,
                       new_numbers=None,
                       new_conundrum=None
                       ):
        """
        Display relevant user prompt for screen.

        Checks which screen is being rendered and
        provides the relevant set of prompts. Passes
        input to be validated, updates relevant
        objects with user input and then returns
        user_prompt to round_handler.

        Parameters
        ----------
        new_player : object
            Current Player Object
        new_letters : object
            Current Letters Object
        new_numbers : object
            Current Numbers Object
        new_conundrum : object
            Current Conundrum Object

        Returns
        -------
        user_prompt : string
            User inputted string
        """
        if self.screen_data_param == 'intro':
            while True:
                user_prompt = input(
                    Fore.WHITE +
                    'Enter 1 to Start the Game or 2'
                    ' to See the Game Rules\n'
                )
                if validate_menu_value(user_prompt):
                    break
                else:
                    continue
        elif self.screen_data_param == 'rules':
            while True:
                user_prompt = input(
                    Fore.WHITE +
                    'Enter 1 to Start the Game or 2'
                    ' to Return to the Intro Screen\n'
                )
                if validate_menu_value(user_prompt):
                    break
                else:
                    continue
        elif self.screen_data_param == 'enter_name':
            while True:
                user_prompt = input(
                    Fore.WHITE +
                    'Please enter your name\n'
                    '(must be 2 to 10 letter characters long)...\n'
                )
                if validate_name(user_prompt):
                    new_player.name = user_prompt.lower().capitalize()
                    # Return start_game flag to
                    # round_handler to break out of
                    # first loop
                    user_prompt = 'start_rounds'
                    break
                else:
                    continue
        # Letters round
        elif self.screen_data_param == 'letters_round':
            print(
                Style.BRIGHT + Fore.LIGHTGREEN_EX +
                f'Choose 9 letters in total from '
                'a selection of Vowels and Consonants\n'
                '(Once you choose a number of vowels, the '
                'remaining letters will be \n'
                'made up of consonants)\n'
                + Fore.RESET
                )
            # Get number of vowels and validate number
            while True:
                user_prompt = input(
                    Fore.WHITE +
                    'How many vowels would you like for your word?\n'
                    '(Enter a value between 3 and 9)\n'
                )
                if validate_vowels(user_prompt):
                    # Empty player chosen letters then
                    # pick vowels and store in Player attribute
                    new_player.chosen_letters = []
                    new_player.chosen_letters.extend(
                        new_letters.random_letters(
                            'vowels', int(user_prompt)
                            )
                    )
                    # Select remaining letters as random consonants
                    # and store in Player attribute
                    max_consonants = 9 - int(user_prompt)
                    new_player.chosen_letters.extend(
                        new_letters.random_letters(
                            'consonants', max_consonants
                            )
                        )
                    # return flag to move to show letters
                    user_prompt = 'show_letters'
                    break
                else:
                    continue
        # Show letters and check if ready
        elif self.screen_data_param == 'show_letters':
            print(
                Fore.LIGHTGREEN_EX +
                f'Make the longest word possible using only '
                'the letters in the tiles above!\n'
                'The word must be longer than 2 letters long.\n'
                'You can only use the letters as often as they are '
                'shown above!\n'
            )
            # Pause execution and wait for keypress
            wait_for_keypress(
                Fore.YELLOW +
                'Ready to play? Press any key to start the timer...'
                + Fore.RESET
            )
            user_prompt = 'letters_guess'
        # Letters round guessing prompt
        elif self.screen_data_param == 'letters_guess':
            print(
                Fore.WHITE +
                f'You have 30 seconds...\n'
                )
            # Get word guess
            timer_prompt = (
                Fore.WHITE + 'Enter your longest word...'
            )
            user_prompt, time_remaining = self.timed_input(
                new_player,
                timer_prompt
            )
            # If valid word store player's round time
            if user_prompt:
                new_player.round_time = time_remaining
            user_prompt = 'letters_feedback'
        # Letters round feedback
        elif self.screen_data_param == 'letters_feedback':
            # Check if user entered a word
            if len(new_player.guessed_words) > 0:
                # Get player's last guessed word
                user_word = new_player.guessed_words[-1]
            else:
                user_word = ''
            if user_word == '':
                print(
                    f"\n{new_player.name}, you didn't guess a word "
                    f"within the time limit. Better luck next round!"
                )
            else:
                # Check if word in pydictionary
                print(
                    Style.BRIGHT + Fore.WHITE +
                    f'Checking your word in the dictionary...\n'
                    )
                valid_word = check_dictionary(user_word)
                if valid_word:
                    round_score = new_player.update_score()
                    print(
                        f"{user_word.lower().capitalize()}, that's a "
                        f"{len(user_word)} letter word in "
                        f"{new_player.round_time} seconds. \n"
                        f"{new_player.name}, you scored {round_score} points "
                        f"for round {Screen.round_number}!"
                    )
                elif valid_word is None:
                    print(
                        f"It appears '{user_word}' is NOT a word "
                        "found in our dictionary.\n"
                        f"Better luck next time!"
                    )
            # Print longest word if anagram solver can find one
            print(
                Fore.LIGHTGREEN_EX +
                f"\nChecking what our 'limited' dictionary corner found...\n"
                f"This might take 5 to 10 seconds...\n"
                + Fore.RESET
                )
            longest_words, word_len = new_letters.longest_word(
                new_player.chosen_letters
            )
            if longest_words:
                if len(longest_words) == 1:
                    print(
                        Fore.WHITE +
                        f"\nHere's a {word_len} letter word that our "
                        f"dictionary corner found!\n"
                        )
                else:
                    print(
                        Fore.WHITE +
                        f"\nHere are some {word_len} letter words that our "
                        f"dictionary corner found!\n"
                    )
                for item in set(longest_words):
                    # Running through in set form prevents duplicates
                    print(
                        Fore.YELLOW +
                        f'{item}'
                        + Fore.RESET
                        )
                    # Don't print meaning message if none found
                    if check_dictionary(item):
                        print_word_meaning(item, new_player)
            else:
                print(
                    Style.BRIGHT + Fore.WHITE +
                    "Our dictionary corner couldn't find any "
                    "better words either!"
                )
            # Pause execution for key press to progress
            wait_for_keypress(
                Fore.YELLOW +
                '\nReady for the next round? Press any key to '
                'continue...'
                + Fore.RESET
            )
            # If still in first 3 rounds set user response
            # to loop back to start next round
            if Screen.round_number <= 2:
                user_prompt = 'start_rounds'
            else:
                user_prompt = 'numbers_screen'
        # Numbers round
        elif self.screen_data_param == 'numbers_round':
            print(
                Style.BRIGHT + Fore.LIGHTGREEN_EX +
                f'Choose six numbers in total from the '
                'following selection of Big\n'
                'Numbers and Small Numbers...\n'
                + Fore.RESET
            )
            while True:
                user_prompt = input(
                    Fore.WHITE +
                    'How many big numbers (25, 50, 75, 100) '
                    'would you like to select?\n'
                    '(Enter a value between 0 and 4)\n'
                )
                if validate_numbers(user_prompt):
                    # Empty player chosen numbers then
                    # pick requested number of random big and small
                    # numbers and store in Player attribute
                    big_numbers, small_numbers = new_numbers.random_numbers(
                        int(user_prompt)
                    )
                    new_player.chosen_numbers = []
                    new_player.chosen_numbers.extend(
                        big_numbers + small_numbers
                    )
                    # Generate target number and store in Player
                    # attribute
                    target_number = new_numbers.random_target()
                    new_player.target_number = target_number

                    # return flag to move to show letters
                    user_prompt = 'show_numbers'
                    break
        # Show numbers and check if ready
        elif self.screen_data_param == 'show_numbers':
            print(
                Fore.LIGHTGREEN_EX +
                f'Use any of the 6 numbers in the tiles above and basic\n'
                'mathematical operators + - * / ( ) '
                'to reach the target number.\n'
                'You can only use numbers as often as they are '
                'shown above!\n'
                'Remember order of operations!\n'
            )
            # Pause execution and wait for keypress
            wait_for_keypress(
                Fore.YELLOW +
                'Ready to play? Press any key to start the timer...'
                + Fore.RESET
            )
            user_prompt = 'numbers_guess'
        # Numbers round guessing prompt
        elif self.screen_data_param == 'numbers_guess':
            print('You have 60 seconds...\n')
            # Get numbers solution guess
            timer_prompt = (
                Fore.WHITE +
                'Enter your solution to reach the '
                'target number...'
            )
            user_prompt, time_remaining = self.timed_input(
                new_player,
                timer_prompt
            )
            # If valid solution store player's round time
            if user_prompt:
                new_player.round_time = time_remaining
            user_prompt = 'numbers_feedback'
        # Numbers round feedback
        elif self.screen_data_param == 'numbers_feedback':
            # Get player's last guessed solution and evaluate
            # string to check if solution matches target number
            print(
                Style.BRIGHT + Fore.WHITE +
                f'Checking your solution...\n'
                )
            user_solution = new_player.guessed_solutions[0]
            if user_solution == '':
                print(
                    f"\n{new_player.name}, you didn't provide a solution "
                    f"within the time limit. Better luck next round!"
                )
            else:
                valid_solution, solution_result, target_difference =\
                    validate_user_solution(
                        user_solution,
                        new_player
                    )
                if valid_solution:
                    round_score = new_player.update_score()
                    print(
                        f"\n{user_solution} is a "
                        f"valid solution for reaching "
                        f"{new_player.target_number}!\n"
                        f"You solved it in {new_player.round_time} seconds. \n"
                        f"{new_player.name}, you scored {round_score} points "
                        f"for round {Screen.round_number}!\n"
                    )
                # If solution is close still congratulate player!
                elif valid_solution is False and target_difference <= 50:
                    print(
                        f"Sorry you didn't reach the target number of "
                        f"{new_player.target_number}!\n"
                        f"\nYour solution of {user_solution} = "
                        f"{solution_result}.\n"
                        f"\nBut you were within {target_difference} of "
                        f"the target!\n"
                        f"That's amazing! Well done!\n"
                    )
                elif valid_solution is False:
                    print(
                        f"Sorry you didn't reach the target number of "
                        f"{new_player.target_number}!\n"
                        f"Your solution of {user_solution} = "
                        f"{solution_result}.\n"
                        f"Better luck next time!"
                    )
            print(
                Fore.LIGHTGREEN_EX +
                f"Let's see what solutions our maths wiz came up with...\n"
                + Fore.RESET
                )
            # Provide solutions to round
            # add 4 seconds of delay to give the user time to read
            sleep(4)                
            solve_numbers_round(new_player)
            # Pause execution for key press to progress
            wait_for_keypress(
                Fore.YELLOW +
                '\nReady for the next round? Press any key to '
                'continue...'
                + Fore.RESET
            )
            user_prompt = 'show_conundrum'
        # Show conundrum screen
        elif self.screen_data_param == 'show_conundrum':
            print(
                Style.BRIGHT + Fore.LIGHTGREEN_EX +
                f'A scrambled 9 letter word is shown above.\n'
                f'Solve this anagram within 30 seconds!\n'
                + Fore.RESET
            )
            # Pause execution and wait for keypress
            wait_for_keypress(
                Fore.YELLOW +
                'Ready to play? Press any key to start the timer...'
                + Fore.RESET
            )
            user_prompt = 'conundrum_guess'
        # Numbers round guessing prompt
        elif self.screen_data_param == 'conundrum_guess':
            print('You have 30 seconds...\n')
            # Get conundrum guess
            timer_prompt = (
                Fore.WHITE +
                'Enter your solution to the conundrum... '
            )
            user_prompt, time_remaining = self.timed_input(
                new_player,
                timer_prompt,
                new_conundrum
            )
            # If valid solution store player's round time
            if user_prompt:
                new_player.round_time = time_remaining
            user_prompt = 'conundrum_feedback'
        # Conundrum round feedback
        elif self.screen_data_param == 'conundrum_feedback':
            # Check if user entered a word
            if len(new_player.guessed_conundrum) > 0:
                # Get player's last guessed word
                user_word = new_player.guessed_conundrum[0]
            else:
                user_word = ''
            if user_word == '':
                print(
                    f"\n{new_player.name}, you didn't guess a word "
                    f"within the time limit. Better luck next round!"
                )
            # Check if word matches target
            # Convert to upper to avoid case mismatch
            elif user_word.upper() == new_conundrum.target.upper():
                round_score = new_player.update_score()
                print(
                    f"\n{new_player.name}, that's correct!\n"
                    f"You guessed our conundrum is {new_conundrum.target}.\n"
                    f"You solved it in {new_player.round_time} seconds. \n"
                    f"{new_player.name}, you scored {round_score} points "
                    f"for round {Screen.round_number}!\n"
                )
            else:
                # Check if word in pydictionary
                print(
                    Style.BRIGHT + Fore.WHITE +
                    f"That isn't our target word, but let's "
                    f'check your word in the dictionary...\n'
                    )
                valid_word = check_dictionary(user_word)
                if valid_word:
                    round_score = new_player.update_score()
                    print(
                        f"{user_word.lower().capitalize()}, that's wasn't "
                        f"our target word above, but it's still a valid "
                        f"{len(user_word)} letter word!\n"
                        f"You got it in {new_player.round_time} seconds. \n"
                        f"{new_player.name}, you scored {round_score} points "
                        f"for round {Screen.round_number}\n!"
                    )
                elif valid_word is None:
                    print(
                        f"It appears '{user_word.lower().capitalize()}' is "
                        f"NOT a word found in our dictionary.\n"
                        f"Better luck next time!"
                    )
            # Pause before end game screen
            wait_for_keypress(
                Fore.YELLOW +
                'Press any key to continue...'
                + Fore.RESET
            )
            user_prompt = 'game_over'
        # Game Over
        elif self.screen_data_param == 'game_over':
            wait_for_keypress(
                Fore.YELLOW +
                'Press any key to end game...'
                + Fore.RESET
            )
            user_prompt = ''
        # Else game is over

        # Return the user_prompt value back to round_handler
        # so we know which screen to render next
        return user_prompt


class Letters:
    """
    The Letters class to contain all letters
    to choose from in the letters round
    """

    def __init__(self):
        self.vowels = self.populate_vowels()
        self.consonants = self.populate_consonants()

    def populate_vowels(self):
        """
        Add a selection of vowels with
        weighting used in Scrabble
        """
        vowels = []
        vowel_counts = {
            'A': 9,
            'E': 12,
            'I': 9,
            'O': 8,
            'U': 4
        }
        # Populate vowels  with letters from dictionary
        for vowel, count in vowel_counts.items():
            vowels.extend([vowel] * count)
        # Shuffle letters in new list
        random.shuffle(vowels)
        return vowels

    def populate_consonants(self):
        """
        Add a selection of consonants with
        weighting used in Scrabble
        """
        consonants = []
        consonant_counts = {
            'B': 2,
            'C': 2,
            'D': 4,
            'F': 2,
            'G': 3,
            'H': 2,
            'J': 1,
            'K': 1,
            'L': 4,
            'M': 2,
            'N': 6,
            'P': 2,
            'Q': 1,
            'R': 6,
            'S': 4,
            'T': 6,
            'V': 2,
            'W': 2,
            'X': 1,
            'Y': 2,
            'Z': 1
        }
        # Populate consonants with letters from dictionary
        for consonant, count in consonant_counts.items():
            consonants.extend([consonant] * count)
        # Shuffle letters in new list
        random.shuffle(consonants)
        return consonants

    def random_letters(self, type, count):
        """
        Return the requested count of letters
        from the requested set of letters
        """
        letter_set = self.vowels if type == 'vowels' else self.consonants
        return random.sample(letter_set, count)

    def longest_word(self, anagram):
        """
        Return the longest word we can find
        Create some random variations of the letter
        list and loop through the anagram solver.
        Less time consuming than creating all
        permutations of a set of 9 letters, but
        also not highly effective at finding words.
        Code adapted from
        https://github.com/patrickleweryharris/anagram-solver
        """
        anagram_lst = []
        anagram_variations = []
        # Create list of characters
        for char in anagram:
            anagram_lst.append(char)

        # Add initial list to variations list
        anagram_variations.append(list(anagram_lst))
        # Generate 2 additional mixed lists of anagrams
        # and add to a list
        for ind in range(1, 2):
            random.shuffle(anagram_lst)
            shuffled_lst = list(anagram_lst)
            # Check the suffled list hasn't already been
            # generated before adding
            if not any(lst == shuffled_lst for lst in anagram_variations):
                anagram_variations.append(shuffled_lst)

        # Loop through variations until some words are found
        for ind in range(len(anagram_variations)):
            words = find_possible(anagram_variations[ind])
            # Importing custom scrabble word_set from file
            # instead of importing word_set from
            # the anagram_solver module
            actual_words = return_words(words, word_set)

            # Break out of the check if words are found
            if len(actual_words) > 0:
                actual_words = list(set(actual_words))
                return actual_words, len(actual_words[0])

            # Recurse the function by popping one letter off
            # to see if we can quickly find a 4 letter words
            # or longer without creating all permutations
            if len(actual_words) == 0 and len(anagram) >= 4:
                anagram_variations[ind].pop(-1)
                smaller_anagram = ''.join(anagram_variations[ind])
                new_actual_words, len_word = self.longest_word(smaller_anagram)
                actual_words = new_actual_words

                # Break out of the check if words are found
                if len(actual_words) > 0:
                    actual_words = list(set(actual_words))
                    return actual_words, len(actual_words[0])

            else:
                len_word = len(anagram)
        # Remove any duplicates by creating a set and then
        # convert back to a list
        actual_words = list(set(actual_words))
        return actual_words, len_word


class Numbers:
    """
    The Numbers class to contain all numbers
    to choose from in the numbers round
    """

    def __init__(self):
        self.big = [25, 50, 75, 100]
        self.small = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.target = 999

    def random_numbers(self, count):
        """
        Return the requested count of letters
        from the requested set of letters
        """
        big_numbers = random.sample(self.big, count)
        small_numbers = random.sample(self.small, 6 - count)
        return big_numbers, small_numbers

    def random_target(self):
        """
        Generate a 3 digit target number
        """
        target_number = random.randint(100, 999)
        return target_number


class Conundrum:
    """
    The Conundrum class to contain the
    Conundrum word attributes for the
    Conundrum round
    """
    def __init__(self, target=[], scrambled=[]):
        self.target = target
        self.scrambled = scrambled

    def populate_conundrum(self):
        """
        Generate conundrum word and scrambled word
        Choose a word from the 9 letter word list
        and scramble the word.
        """
        # while True:
        random_conundrum = random.sample(nine_letter_word_set, 1)[0].upper()
        # Make sure word isn't on profanity list
        # if check_profanity(random_conundrum) >= 0.9:
        #    break
        scrambled_conundrum = ''.join(
            random.sample(random_conundrum, len(random_conundrum))
        )
        self.target = random_conundrum
        self.scrambled = scrambled_conundrum


# Helper Functions


def print_centered(text):
    """
    Print text centered in terminal
    """
    terminal_width = 80
    centered_text = text.center(terminal_width)
    print(centered_text)


def wait_for_keypress(text):
    """
    Block code execution and wait for keypress
    Code from answer by ChatGPT by openai.com
    """
    print(text)
    sys.stdin.flush()
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        sys.stdin.read(1)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def solve_numbers_round(new_player):
    """
    Solve for the target in the numbers round

    Provide the user with solutions to reach
    the target number using the chosen numbers.
    Uses pypi.org/project/countdown-numbers-solver/
    """
    countdown_numbers_solver.solve(
        new_player.chosen_numbers,
        new_player.target_number
    )


def round_handler(new_player, new_letters, new_numbers, new_conundrum):
    """
    Load the initial game screen and
    create the next screen based on
    user input
    """
    intro_screen = Screen('intro')
    rules_screen = Screen('rules')
    name_screen = Screen('enter_name')
    letters_screen = Screen('letters_round')
    show_letters = Screen('show_letters')
    letters_guess = Screen('letters_guess')
    letters_feedback = Screen('letters_feedback')
    numbers_screen = Screen('numbers_round')
    show_numbers = Screen('show_numbers')
    numbers_guess = Screen('numbers_guess')
    numbers_feedback = Screen('numbers_feedback')
    show_conundrum = Screen('show_conundrum')
    conundrum_guess = Screen('conundrum_guess')
    conundrum_feedback = Screen('conundrum_feedback')
    game_over = Screen('game_over')
    # Capture user input and player object
    # when screens are rendered
    user_response = intro_screen.render(
        new_player,
        new_letters,
        new_numbers,
        new_conundrum
    )
    # Render intro, rules and first round screens
    while True:
        if user_response == '1':
            user_response = name_screen.render(
                new_player,
                new_letters,
                new_numbers,
                new_conundrum
            )
            break
        elif user_response == '2':
            user_response = rules_screen.render(
                new_player,
                new_letters,
                new_numbers,
                new_conundrum
            )
            # Inner loop to loop between intro screen
            # and rules screen until 1 selected
            # then continue to outer loop
            while True:
                if user_response == '1':
                    break
                else:
                    user_response = intro_screen.render(
                        new_player,
                        new_letters,
                        new_numbers,
                        new_conundrum
                    )
                    break
    # If still in first 3 letter rounds
    # loop again
    while True:
        if Screen.round_number <= 3:
            if user_response == 'start_rounds':
                # Update round number in Screen
                Screen.round_number += 1
                user_response = letters_screen.render(
                    new_player,
                    new_letters,
                    new_numbers,
                    new_conundrum
                )
            elif user_response == 'show_letters':
                user_response = show_letters.render(
                    new_player,
                    new_letters,
                    new_numbers,
                    new_conundrum
                )
            elif user_response == 'letters_guess':
                user_response = letters_guess.render(
                    new_player,
                    new_letters,
                    new_numbers,
                    new_conundrum
                )
            elif user_response == 'letters_feedback':
                user_response = letters_feedback.render(
                    new_player,
                    new_letters,
                    new_numbers,
                    new_conundrum
                )
                if user_response == 'numbers_screen':
                    break
    # Render Numbers and Conundrum round screens
    while True:
        if user_response == 'numbers_screen':
            Screen.round_number += 1
            user_response = numbers_screen.render(
                new_player,
                new_letters,
                new_numbers,
                new_conundrum
            )
        elif user_response == 'show_numbers':
            user_response = show_numbers.render(
                new_player,
                new_letters,
                new_numbers,
                new_conundrum
            )
        elif user_response == 'numbers_guess':
            user_response = numbers_guess.render(
                new_player,
                new_letters,
                new_numbers,
                new_conundrum
            )
        elif user_response == 'numbers_feedback':
            user_response = numbers_feedback.render(
                new_player,
                new_letters,
                new_numbers,
                new_conundrum
            )
        # Conundrum round
        elif user_response == 'show_conundrum':
            Screen.round_number += 1
            # Generate target conundrum
            new_conundrum.populate_conundrum()
            user_response = show_conundrum.render(
                new_player,
                new_letters,
                new_numbers,
                new_conundrum
            )
        elif user_response == 'conundrum_guess':
            user_response = conundrum_guess.render(
                new_player,
                new_letters,
                new_numbers,
                new_conundrum
            )
        elif user_response == 'conundrum_feedback':
            user_response = conundrum_feedback.render(
                new_player,
                new_letters,
                new_numbers,
                new_conundrum
            )
        elif user_response == 'game_over':
            user_response = game_over.render(
                new_player,
                new_letters,
                new_numbers,
                new_conundrum
            )            
        else:
            print('No more screens')
            break


# Main game functions


def main():
    """
    Create game objects
    Run all program functions
    """
    new_player = Player()
    new_letters = Letters()
    new_numbers = Numbers()
    new_conundrum = Conundrum()
    round_handler(new_player, new_letters, new_numbers, new_conundrum)
    print('Back in main')

# Call main game function

main()