# Imports
# Python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from time import time, sleep
from re import sub
import random
import termios
import sys
import tty
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
from nine_letter_word_list import nine_letter_word_list
# Third Party
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from inputimeout import inputimeout, TimeoutOccurred
from colorama import init
from colorama import Fore, Back, Style
from colorama.ansi import clear_screen
from art import text2art
from num2words import num2words
import pager
from anagram_solver.anagram_solver import find_possible, return_words
import countdown_numbers_solver
import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable

# Google drive and sheets scope
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('countdown_game')

# Initialise colorama
init()

# Classes


class Player:
    """
    Contains all player attributes.

    Keeps track of player name, score, letters,
    numbers, and words as the player progresses
    through rounds of the game. Contains method
    to update player score.

    Attributes
    -------
    screen_data : object
        Text file to render for each screen.
    name : string
        Player's name
    score : int
        Player's score
    high_score : int
        Player's high score from previous games
    leaderboard_score : int
        Score if playe'rs final score beats current
        top 10 leaderboard scores.
    round_time : int
        Player's time to complete last round.
    chosen_letters : list
        Player's assigned letters for letters round.
    chosen_numbers : list
        Player's assigned numbers for numbers round.
    target_number : int
        Player's assigned target number for numbers round.
    guessed_words : list
        Player's guessed words for each round.
    guessed_solutions : list
        Player's guessed solution for numbers round.
    guessed_conundrum : list
        Player's guessed word for conundrum round.

    Methods
    -------
    update_score()
        Update the Player score and high score.
    """
    def __init__(self,
                 name='',
                 score=0,
                 high_score=0,
                 leaderboard_score=0,
                 round_time=0,
                 chosen_letters=None,
                 chosen_numbers=None,
                 target_number=0,
                 guessed_words=None,
                 guessed_solutions=None,
                 guessed_conundrum=None
                 ):
        self.name = name
        self.score = score
        self.high_score = high_score
        self. leaderboard_score = leaderboard_score
        self.round_time = round_time
        self.chosen_letters = chosen_letters
        self.chosen_numbers = chosen_numbers
        self.target_number = target_number
        self.guessed_words = guessed_words
        self.guessed_solutions = guessed_solutions
        self.guessed_conundrum = guessed_conundrum

    def update_score(self):
        """
        Update the Player score and high score.

        Update player's score for the current
        round based on the player's guess and time
        remaining. If the player's score is now
        higher than their high score update the
        high score.

        Returns
        -------
        round_score : int
            Calculated score for round
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

        # If score is now higher than previous high
        # score update player's high score
        if self.score > self.high_score:
            self.high_score = self.score

        return round_score


class Screen:
    """
    Contains the attributes and methods of all game screen
    elements to be rendered.

    Called by round_handler to create Screen object instances
    to render the correct screen elements depending on the
    screen_data_param and/or round_number.

    Attributes
    -------
    screen_data_param : string
        Shortened keyword to represent screen data file to use
        when rendering. Passed via parameter when creating
        object instance of Screen.
    screen_data_file : string
        Screen data file to use when creating object
        instance of Screen.
    screen_data : object
        Stores the text file to render for each screen.
    letter_tiles : string
        Stores an ASCII string to represent letter tiles.
        Used to populate letters and numbers into tile
        string.
    round_number : int
        Keeps track of the round number.

    Methods
    -------
    render(
        new_player=None,
        new_letters=None,
        new_numbers=None,
        new_conundrum=None
    )
        Render screen elements to the terminal.
    display_text_art()
        Output text as ASCII art via Art library.
    display_text()
        Retrieve screen text from data files.
    timed_input(
        new_player=None,
        timer_prompt=None,
        new_conundrum=None
    )
        Display timed input for 30 or 60 seconds.
    display_score(new_player=None)
        Display the user score
    update_tiles(
        new_player=None,
        new_conundrum=None,
        screen_param=None
    )
        Update letters tiles with chosen letters.
    display_prompt(
        new_player=None,
        new_letters=None,
        new_numbers=None,
        new_conundrum=None
    )
        Display relevant user prompt for screen.
    """
    screen_data = {
        'intro': 'intro_screen_data.txt',
        'rules': 'rules_screen_data.txt',
        'scores': 'game_screen_data.txt',
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
        print(Style.BRIGHT + Back.BLUE + Fore.WHITE)
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
            self.update_tiles(
                new_player,
                new_conundrum,
                self.screen_data_param
            )
        # Only print tiles and score during
        # enter name, rounds, and feedback screens
        if self.screen_data_param not in [
            'intro',
            'rules',
            'scores',
            'game_over'
        ]:
            self.display_score(new_player)
            print_centered(
                Style.BRIGHT + Fore.YELLOW +
                self.letter_tiles +
                Fore.RESET
            )
        elif self.screen_data_param in [
            'scores'
        ]:
            print_rainbow(
                'HALL OF FAME!\n',
                'center'
            )
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
            print('\n')
            print_rainbow(
                f"CONGRATULATIONS {new_player.name.upper()}!\n",
                "center"
            )
            print_centered(
                Style.BRIGHT + Fore. WHITE +
                f"          YOUR FINAL SCORE IS {new_player.score}!\n"
            )
        # Render high scores table
        if self.screen_data_param == 'scores':
            print_high_scores()
        # Render user prompt
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
        if self.screen_data_param in [
            'intro',
            'rules',
            'scores',
            'enter_name'
        ]:
            result = text2art(
                '        COUNTDOWN', font='small'
                )
            print(Style.BRIGHT + result)
        elif self.screen_data_param not in [
            'intro',
            'rules',
            'scores',
            'enter_name'
        ]:
            round_word = num2words(
                self.round_number, lang='en'
                ).upper()
            # Add varying amount of spaces
            # based on length of round number string
            if Screen.round_number == 1:
                spaces_num = len(round_word) * (5 // Screen.round_number)
            else:
                spaces_num = (
                    5 + len(round_word)
                    * (5 // Screen.round_number) + 2
                )
            spaces_str = ' ' * int(spaces_num)
            if self.screen_data_param == 'scores':
                result = text2art(
                    f'{spaces_str}HIGH SCORES', font='small'
                    )
            elif self.screen_data_param == 'game_over':
                # Add additional space to center
                spaces_str += '  '
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

    def timed_input(
        self,
        new_player=None,
        timer_prompt=None,
        new_conundrum=None
    ):
        """
        Display timed input for 30 or 60 seconds

        Display a user prompt for 30 or 60 seconds
        depening on round number. Validates user's
        input and stores valid input in player object
        attributes. Returns time remaining when the
        user enters input. Displays timeout message
        and removes prompt if time has elapsed.

        Parameters
        ----------
        new_player : object
            Current Player Object.
        timer_prompt : string
            String to print as input prompt.
        new_conundrum : object
            Current Conundrum Object.

        Returns
        -------
         user_prompt : string or boolean
            Users input or False if no input
            entered.
         time_remaining : int
            Time reamining when user enters
            their input.
        """
        countdown = 60 if Screen.round_number == 4 else 30
        start_time = time()
        # Initialise player guess attributes as lists if
        # not yet created
        if new_player.guessed_words is None:
            new_player.guessed_words = []
        if new_player.guessed_solutions is None:
            new_player.guessed_solutions = []
        if new_player.guessed_conundrum is None:
            new_player.guessed_conundrum = []

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
                    if validate_user_conundrum(
                        user_prompt,
                        new_player,
                        new_conundrum
                    ):
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
                # Store empty word during letter's rounds to not
                # throw off looking up player's last guessed word
                if 1 <= Screen.round_number <= 3:
                    new_player.guessed_words.insert(
                        Screen.round_number - 1,
                        ' '
                    )
                sleep(2)
                break

            time_remaining = int(countdown - (time() - start_time))
            if time_remaining > 0:
                print('You have :', time_remaining, 'seconds remaining!')

        return user_prompt, time_remaining

    def display_score(self, new_player=None):
        """
        Display the user score and previous
        high score if known

        Parameters
        ----------
        new_player : object
            Current Player Object.
        """
        print_centered(
            f'Your Score: {new_player.score}   '
            f'Previous High Score: {new_player.high_score}'
        )

    def update_tiles(
        self,
        new_player=None,
        new_conundrum=None,
        screen_param=None
    ):
        """
        Update letters tiles with chosen letters

        Parameters
        ----------
        new_player : object
            Current Player Object.
        new_conundrum : object
            Current Conundrum Object.
        screen_param : string
            Keyword to represent current screen rendered.
        """
        # If enter_name screen populate letters with Ready?
        if (new_player.chosen_letters is None or
                len(new_player.chosen_letters) == 0):
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
        # Start testing for which screen
        # to render
        if self.screen_data_param == 'intro':
            while True:
                user_prompt = input(
                    Fore.WHITE +
                    'Enter 1 to Start the Game, 2 '
                    'to See the Game Rules,\n'
                    'or 3 to See the Scores '
                    'Leaderboard\n'
                )
                if validate_menu_value(
                    user_prompt,
                    self.screen_data_param
                ):
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
                if validate_menu_value(
                    user_prompt,
                    self.screen_data_param
                ):
                    break
                else:
                    continue
        elif self.screen_data_param == 'scores':
            while True:
                user_prompt = input(
                    Fore.WHITE +
                    'Enter 1 to Start the Game or 2'
                    ' to Return to the Intro Screen\n'
                )
                if validate_menu_value(
                    user_prompt,
                    self.screen_data_param
                ):
                    break
                else:
                    continue
        elif self.screen_data_param == 'enter_name':
            # Add additional vertical spacing
            print('\n\n\n\n')
            while True:
                # Check if player name exists from
                # previous round
                if new_player.name == '':
                    user_prompt = input(
                        Fore.WHITE +
                        'Please enter your name...\n'
                        '(must be 2 to 10 letter characters long)\n'
                    )
                else:
                    # If player name already exists ask if they want
                    # to keep it or change it
                    while True:
                        user_prompt = input(
                            Fore.WHITE +
                            f'Type 1 to keep the name '
                            + Fore.YELLOW +
                            f'{new_player.name} '
                            + Fore.WHITE +
                            f'or 2 to enter a new name\n'
                        )
                        if validate_menu_value(
                            user_prompt,
                            self.screen_data_param
                        ):
                            if user_prompt == '1':
                                user_prompt = new_player.name
                                break
                            elif user_prompt == '2':
                                user_prompt = input(
                                    Fore.WHITE +
                                    'Please enter your name\n'
                                    '(must be 2 to 10 letter characters long) '
                                    '...\n'
                                )
                                if validate_name(user_prompt):
                                    break
                        else:
                            continue
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
            if len(new_player.guessed_words[-1]) > 0:
                # Get player's last guessed word
                user_word = new_player.guessed_words[-1]
            else:
                user_word = ''
            if user_word == '' or user_word == ' ':
                print(
                    Fore.WHITE +
                    f"\n{new_player.name}, you didn't guess a word "
                    f"within the time limit. Better luck next round!\n"
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
                        f"{len(user_word)} letter word with "
                        f"{new_player.round_time} seconds remaining. \n"
                        f"{new_player.name}, you scored {round_score} points "
                        f"for round {Screen.round_number}!"
                    )
                elif valid_word is None:
                    print(
                        f"It appears '{user_word}' is NOT a word "
                        "found in our dictionary.\n"
                        f"Better luck next time!"
                    )
            # Pause execution for key press to progress
            wait_for_keypress(
                Fore.YELLOW +
                '\nPress any key to see what our dictionary corner '
                'found...'
                + Fore.RESET
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
                    Fore.WHITE +
                    f"\n{new_player.name}, you didn't provide a solution "
                    f"within the time limit. Better luck next round!\n"
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
                        Fore.WHITE +
                        f"\n{user_solution} is a "
                        f"valid solution for reaching "
                        f"{new_player.target_number}!\n"
                        f"You had {new_player.round_time} seconds "
                        f"remaining. \n"
                        f"{new_player.name}, you scored {round_score} points "
                        f"for round {Screen.round_number}!\n"
                    )
                # If solution is close still congratulate player!
                elif valid_solution is False and target_difference <= 50:
                    print(
                        Fore.WHITE +
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
                        Fore.WHITE +
                        f"Sorry you didn't reach the target number of "
                        f"{new_player.target_number}!\n"
                        f"Your solution of {user_solution} = "
                        f"{solution_result}.\n"
                        f"Better luck next time!\n"
                    )
            # Pause to give the user time to read
            wait_for_keypress(
                Fore.YELLOW +
                '\nHit any key to see the solutions we found...'
                + Fore.RESET
            )
            print(
                Fore.LIGHTGREEN_EX +
                f"Here's what our maths wiz came up with...\n"
                + Fore.RESET
                )
            # Provide solutions to round
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
                    Fore.WHITE +
                    f"\n{new_player.name}, you didn't guess a word "
                    f"within the time limit. Better luck next time!\n"
                )
            # Check if word matches target
            # Convert to upper to avoid case mismatch
            elif user_word.upper() == new_conundrum.target.upper():
                round_score = new_player.update_score()
                print(
                    Style.BRIGHT + Fore.WHITE +
                    f"\n{new_player.name}, that's correct!\n"
                    f"You guessed our conundrum is {new_conundrum.target}.\n"
                    f"You solved it with {new_player.round_time} "
                    f"seconds remaining. \n"
                    f"\n{new_player.name}, you scored {round_score} points "
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
                        f"You got it with {new_player.round_time} "
                        f"seconds remaining. \n"
                        f"{new_player.name}, you scored {round_score} points "
                        f"for round {Screen.round_number}!\n"
                    )
                elif valid_word is None:
                    print(
                        f"It appears '{user_word.lower().capitalize()}' is "
                        f"NOT a word found in our dictionary.\n"
                        f"Better luck next time!"
                    )
            # Check player score against
            # leaderboard and insert if in
            # top 10. Doing before game over
            # to give time to update
            new_player.leaderboard_score = store_high_scores(new_player)
            # Pause before end game screen
            wait_for_keypress(
                Fore.YELLOW +
                'Press any key to continue...'
                + Fore.RESET
            )
            user_prompt = 'game_over'
        # Game Over
        elif self.screen_data_param == 'game_over':
            if new_player.leaderboard_score > 0:
                # Output the high scores and a congrats
                # message for the game over screen
                print_rainbow(
                    "THAT'S A NEW HIGH SCORE!\n",
                    'center'
                )
                # Add delay so user can read top of terminal
                sleep(4)
                # Print leaderboard
                print_high_scores()
            # Let user choose to start new game
            # or end game
            wait_for_keypress(
                Fore.YELLOW +
                'Press any key to start a new game or ESC to end game...'
                + Fore.RESET,
                allow_escape=True
            )
            user_prompt = ''
            # If the user pressed any key other
            # than escape start a new game
            # and pass existing name and high score
            existing_name = new_player.name
            existing_high_score = new_player.high_score
            main(existing_name, existing_high_score)
        # Else game is over

        # Return the user_prompt value back to round_handler
        # so we know which screen to render next
        return user_prompt


class Letters:
    """
    Contains all letter types and letters to
    choose from in the letters round and letter
    generation methods.

    Attributes
    ----------
    vowels : list
        List of vowels populated to player's specification.
    consonants : list
        List of consonants populated to player's specification.

    Methods
    -------
    populate_vowels()
        Populate a requested number of vowels to player
        object attribute.
    populate_consonants()
        Populate a requested number of consonants to player
        object attribute.
    random_letters(type, count)
        Return the requested count of letters from the
        requested type of letters.
    longest_word(anagram)
        Return the longest anagaram solution we can find.
    """

    def __init__(self):
        self.vowels = self.populate_vowels()
        self.consonants = self.populate_consonants()

    def populate_vowels(self):
        """
        Populate vowels to player object attribute.

        Populate a requested number of vowels to player
        object attribute using a selection of vowels with
        weighting used in Scrabble.

        Returns
        ----------
        vowels : list
            List of vowels of size requested by the
            player.
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
        Populate consonants to player object attribute.

        Populate a requested number of consonants to player
        object attribute using a selection of consonants
        with weighting used in Scrabble.

        Returns
        -------
        consonants : list
            List of consonants of size requested by the
            player.
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
        from the requested type of letters.

        Parameters
        ----------
        type : string
            Type of letters to generate.
        count : int
            Size of letter list to generate.

        Returns
        -------
        random.sample(letter_set, count) : list
            List of letters of type and count requested
            by the player.
        """
        letter_set = self.vowels if type == 'vowels' else self.consonants
        return random.sample(letter_set, count)

    def longest_word(self, anagram):
        """
        Return the longest anagaram solution we can find.

        Create some random variations of the letter
        list and loop through the anagram solver.
        Less time consuming than creating all
        permutations of a set of 9 letters, but
        also not highly effective at finding words.
        Code adapted from
        https://github.com/patrickleweryharris/anagram-solver

        Parameters
        ----------
        anagram : list
            List of letters representing the anagram in the
            conundrum round.

        Returns
        -------
        actual_words : list
            List of words generated from the anagram.

        len_word : int
            Length of words generated from the anagram.

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
            # Check the shuffled list hasn't already been
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
    Contains all types of numbers to choose from
    and solve for in the numbers round and numbers
    generation methods.

    Attributes
    ----------
    big : list
        List of big numbers for the numbers round.
    small : list
        List of small numbers for the numbers round.
    target : int
        Three digit random;ly generated target number
        for the numbers round.

    Methods
    -------
    random_numbers(count)
        Return the requested count of numbers
        from big and small numbers lists.
    random_target()
        Generate a three digit target number
        for the numbers round.
    """

    def __init__(self):
        self.big = [25, 50, 75, 100]
        self.small = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.target = 999

    def random_numbers(self, count):
        """
        Return the requested count of numbers
        from big and small numbers lists.

        Parameters
        ----------
        count : int
            Number of small numbers selected by the
            player.

        Returns
        -------
        big_numbers : list
            List of big numbers of size requested by the
            player.
        small_numbers : list
            List of small numbers of size requested by the
            player.
        """
        big_numbers = random.sample(self.big, count)
        small_numbers = random.sample(self.small, 6 - count)
        return big_numbers, small_numbers

    def random_target(self):
        """
        Generate a three digit target number for the
        numbers round.

        Returns
        -------
        target_number : int
            Three digit target number for numbers round.
        """
        target_number = random.randint(100, 999)
        return target_number


class Conundrum:
    """
    Contains the Conundrum word attributes for the
    Conundrum round and methods to populate and
    solve the conundrum.

    Attributes
    ----------
    target : list
        Randomly sampled word from nine letter
        word list.
    scrambled : string
        Scambled version of the chosen conundrum
        word.

    Methods
    -------
    populate_conundrum()
        Generates conundrum word and scrambled word.
    """
    def __init__(self, target=[], scrambled=[]):
        self.target = target
        self.scrambled = scrambled

    def populate_conundrum(self):
        """
        Generates conundrum word and scrambled word.

        Chooses a word from the 9 letter word list
        and scrambles the word. Stores the target and
        scrambled words in Conundrum attributes.
        """
        while True:
            random_conundrum = random.sample(
                nine_letter_word_list, 1
            )[0].upper()
            # Make sure word isn't on profanity list
            # to avoid validated user conundrum not
            # matching generated conundrum
            # stop looping if valid word found
            if check_profanity(random_conundrum) < 0.9:
                break
        scrambled_conundrum = ''.join(
            random.sample(random_conundrum, len(random_conundrum))
        )
        self.target = random_conundrum
        self.scrambled = scrambled_conundrum


# Helper Functions


def print_centered(text):
    """
    Print text centered in terminal.

    Parameters
    ----------
    text : string
        Text to print centered.
    """
    terminal_width = 80
    centered_text = text.center(terminal_width)
    print(centered_text)


def print_rainbow(text, alignment=None):
    """
    Print text characters in range of
    rainbow colours
    Adapted from answer by ChatGPT
    by openai.com

    Parameters
    ----------
    alignment : string
        Flag to indicate if text should be
        centered or not.
    """
    colors = [
        Fore.RED,
        Fore.YELLOW,
        Fore.GREEN,
        Fore.CYAN,
        Fore.MAGENTA
    ]

    # Store text letters as a list
    characters = list(text)
    color_text = ''

    # Loop through characters and colors
    # to build colorful string
    for i in range(len(characters)):
        char = characters[i]
        color = colors[i % len(colors)]
        color_text += (color + char)

    color_text += (Fore.RESET)

    # Check if we need to center align text
    if alignment == 'center':
        # Calculate how many Fore characters
        # add to string length to adjust center
        # calculation
        string_diff = len(color_text) - len(text)
        adj_terminal_width = 80 + string_diff
        print(color_text.center(adj_terminal_width))
    else:
        print(color_text)


def wait_for_keypress(text, allow_escape=False):
    """
    Block code execution and wait for keypress
    Code from answer by ChatGPT by openai.com

    Parameters
    ----------
    allow_escape : boolean
        Flag to indicate if keypress should
        listen for ESC key and exit program.
    """
    print(text)
    sys.stdin.flush()
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        if allow_escape:
            char = sys.stdin.read(1)
            if char == '\x1b':
                # Exit the program if Escape
                # key is pressed
                sys.exit()
        else:
            sys.stdin.read(1)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def solve_numbers_round(new_player):
    """
    Solve for the target in the numbers round

    Provide the user with solutions to reach
    the target number using the chosen numbers.
    Uses pypi.org/project/countdown-numbers-solver/

    Parameters
    ----------
    new_player : object
        Current Player Object
    """
    countdown_numbers_solver.solve(
        new_player.chosen_numbers,
        new_player.target_number
    )


def print_high_scores():
    """
    Print high score from Scores Google Sheet.

    Look up top 10 high scores in Countdown
    Game Google Sheet and print.

    Based on code from the Code Institute's
    Love Sandwiches project and PrettyTable
    suggestions from ChatGPT by Openai.com.
    """
    scores_worksheet = SHEET.worksheet('scores')
    high_scores = scores_worksheet.get_all_values()

    # Create a PrettyTable
    table = PrettyTable()

    # Add column headings with color
    # to the table
    color_headings = [
        f"{Fore.YELLOW}{heading}{Fore.WHITE}"
        for heading in high_scores[0]
    ]
    table.field_names = color_headings

    # Iterate through high score rows,
    # excluding header row and add rows
    # to the table
    for rows in high_scores[1:]:
        table.add_row(rows)

    # Center align table and print
    table.align = "c"

    # Output the table to the terminal
    table_string = table.get_string()
    terminal_width = 80
    padding = (terminal_width - len(table_string.split("\n")[0])) // 2

    # Apply padding to each line of the table
    centered_table = "\n".join([
        " " * padding + line
        for line in table_string.split("\n")
    ])

    print(f'{centered_table}\n')


def store_high_scores(new_player):
    """
    Store high scores in Google Sheet

    Look up top 10 high scores in Countdown
    Game Google Sheet and update if player's
    score is in top ten.

    Based on code from the Code Institute's
    Love Sandwiches project.

    Parameters
    ----------
    new_player : object
        Current Player Object

    Returns
    -------
    new_high_score : int
        Player score if higher than leaderboard
        score. 0 if not higher.
    """
    scores_worksheet = SHEET.worksheet('scores')
    # Get high scores from second column
    high_score_numbers = scores_worksheet.col_values(2)
    # get player's name and score from their player object
    player_name = new_player.name
    player_score = new_player.score
    # Loop through column values ignoring
    # heading cell
    new_high_score = 0
    for ind in range(1, 11):
        # If player's score is higher than an existing
        # entry in the top 10 add it to the table
        if player_score >= int(high_score_numbers[ind]):
            # Set row where new score will be inserted
            row_index = ind + 1
            # Set flag that player achieved new
            # leaderboard high score
            new_high_score = player_score
            # Break once next highest score found
            break
    if new_high_score:
        # Insert new score row
        scores_worksheet.insert_row([player_name, player_score], row_index)
        # Delete last row to remove lowest score to keep to 10 scores
        scores_worksheet.delete_rows(12)

    return new_high_score


def round_handler(new_player, new_letters, new_numbers, new_conundrum):
    """
    Handles game flow by determing which screen
    to render next.

    Load the initial game intro screen and
    then create render subsequnet screens based
    on user input.

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
    """
    intro_screen = Screen('intro')
    rules_screen = Screen('rules')
    scores_screen = Screen('scores')
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
    # Render intro, rules, scores
    # and first round screens
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
        # High scores screen
        elif user_response == '3':
            user_response = scores_screen.render(
                new_player,
                new_letters,
                new_numbers,
                new_conundrum
            )
            # Inner loop to loop between scores screen
            # and intro screen until 1 selected
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
            break


# Main game functions


def main(existing_name='', existing_high_score=0):
    """
    Create game objects
    Run all program functions
    """
    # Reset round number and previous inputs
    # in case this is a repeat game
    Screen.round_number = 0
    user_word = ''
    user_solution = ''
    user_response = ''
    user_prompt = ''
    # Create new game object instances and pass to round
    # handler
    new_player = Player()
    new_letters = Letters()
    new_numbers = Numbers()
    new_conundrum = Conundrum()
    # Retrieve existing player name and high score
    if existing_name:
        new_player.name = existing_name
    if existing_high_score:
        new_player.high_score = existing_high_score
    round_handler(new_player, new_letters, new_numbers, new_conundrum)


# Call main game function

main()
# End of code...phew...thanks for reading!
