# Imports
# Python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from time import sleep
from itertools import permutations
import os
import random
import sys
# Internal
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from validation import (
    validate_name,
    validate_menu_value,
    validate_vowels,
    validate_user_word,
    validate_user_conundrum
)
# Third Party
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from PyDictionary import PyDictionary
from profanity_check import predict, predict_prob
import countdown_numbers_solver
from colorama import init
from colorama import Fore, Back
from colorama.ansi import clear_screen
from art import text2art
from num2words import num2words


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
                 chosen_numbers=[]
                 ):
        self.name = name
        self.score = score
        self.high_score = high_score
        self.round_time = round_time
        self.current_round = current_round
        self.chosen_letters = chosen_letters
        self.chosen_numbers = chosen_numbers


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
        'numbers_round': 'game_screen_data.txt',
        'conundrum_round': 'game_screen_data.txt',                        
        'game_over': 'game_over_screen_data.txt'
    }

    letter_tiles = """
                     +---+---+---+---+---+---+---+---+---+ 
                     | * | * | * | * | * | * | * | * | * | 
                     +---+---+---+---+---+---+---+---+---+  
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
        print(Back.BLUE)
        print(clear_screen())
        self.display_text_art()
        if self.screen_data_param in [
            'intro',
            'rules',
            'game_over'
        ]:
            self.display_text()
        # Update tiles for enter_name screen
        if self.screen_data_param in ['enter_name']:
            self.update_tiles(new_player)
        # Only print tiles and score during rounds
        if self.screen_data_param in [
            'enter_name'
            'letters_round',
            'numbers_round',
            'conundrum_round'
        ]:
            print_centered(self.letter_tiles)
            self.display_score(new_player)
        # Only print on first round
        if Screen.round_number == 1:
            print_centered(
                f"{new_player.name.upper()}, "
                "LET'S PLAY COUNTDOWN!\n"
            )
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
            print(result)
        elif self.screen_data_param in [
            'letters_round',
            'numbers_round',
            'conundrum_round'
        ]:
            round_word = num2words(
                self.round_number, lang='en'
                ).upper()
            result = text2art(
                f'               ROUND {round_word}', font='small'
                )
            print(result)

    def display_text(self):
        """
        Retrieve screen text from data files
        """
        try:
            with open(self.screen_data_file) as f:
                text = f.read()
                print(text)
        except OSError as e:
            errno, strerror = e.args
            print(f'There is an I/O error number, {errno}: {strerror}.')

    def display_timer(self, new_player=None):
        """
        Display round timer function that runs for 30 seconds
        """
        for i in range(30, 0, -1):
            sys.stdout.write("\rTime remaining: " + str(i) + "seconds")
            sys.stdout.flush()
            sleep(1)
        sys.stdout.write("\rTime's up!                             \n")
        sys.stdout.flush()

    def display_score(self, new_player=None):
        """
        Display the user score
        """
        print_centered(f'Your Score: {new_player.score}\n')

    def update_tiles(self, new_player=None):
        """
        Update letters tiles with chosen letters
        """
        # If enter_name screen populate letters with Ready? 
        if len(new_player.chosen_letters) == 0:
            new_player.chosen_letters = ['R', 'e', 'a', 'd', 'y', '?']
        for char in new_player.chosen_letters:
            # Loop through player chosen letters and use
            # each letter to repalce letter tile
            self.letter_tiles = self.letter_tiles.replace('*', char, 1)

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
                )
                if validate_name(user_prompt):
                    new_player.name = user_prompt
                    # Return start_ga,e flag to 
                    # round_handler to break out of 
                    # first loop
                    user_prompt = 'start_rounds'
                    print(f'Prompt being returned: {user_prompt}')
                    break
                else:
                    continue
        # Letters round
        elif self.screen_data_param == 'letters_round':
            print(
                Fore.YELLOW +
                f'Choose 9 letters in total from '
                'a selection of Vowels and Consonants\n'
                '(Once you choose a number of vowels, the '
                'remaining letters will be made up '
                'of consonants)\n'
                )
            # Get number of vowels and validate number
            while True:
                user_prompt = input(
                    Fore.WHITE +
                    'How many vowels would you like for your word?\n'
                    '(Enter a value between 3 and 9)'
                )
                if validate_vowels(user_prompt):
                    # Pick vowels and store in Player attribute
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
                    print(clear_screen())
                    self.display_text_art()
                    self.update_tiles(new_player)
                    print_centered(self.letter_tiles)
                    self.display_score(new_player)
                    print(
                        f'{new_player.name}, '
                        'Your letters are displayed above. '
                        'Ready to play?\n'
                    )
                    # round_timer()
                    break
                else:
                    continue
        # Numbers round
        elif self.screen_data_param == 'numbers_round':
            print(
                f'Choose six numbers in total from the '
                'following selection of Big Numbers and Small'
                'Numbers'
            )
            while True:
                user_prompt = input(
                    Fore.WHITE +
                    'How many big numbers (25, 50, 75, 100) '
                    'would you like to select?'
                    '(Enter a value between 0 and 4)\n'
                )
                if validate_user_word(user_prompt):
                    break
                else:
                    continue
        # Conundrum round
        elif self.screen_data_param == 'conundrum_round':
            pass
        # Else game is over
        else:
            while True:
                user_prompt = input(
                    Fore.WHITE +
                    'Using the letters above, please enter'
                    'your solution to the conundrum\n'
                )
                if validate_user_conundrum(user_prompt):
                    break
                else:
                    continue
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


class Numbers:
    """
    The Numbers class to contain all numbers
    to choose from in the numbers round
    """
    big = []
    small = []
    target = 999

    def __init__(self,
                 big=None,
                 small=None,
                 target=None
                 ):
        self.big = Numbers.big
        self.small = Numbers.small
        self.target = Numbers.target


class Conundrum:
    """
    The Conundrum class to contain the
    Conundrum word attributes for the
    Conundrum round
    """
    target = "Conundrum"
    scrambled = []

    def __init__(self):
        self.target = Conundrum.target
        self.scrambled = Conundrum.scrambled

# Helper Functions


def print_centered(text):
    """
    Print text centered in terminal
    """
    terminal_width = 80
    centered_text = text.center(terminal_width)
    print(centered_text)


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
    numbers_screen = Screen('numbers_round')
    conundrum_screen = Screen('conundrum_round')
    game_over_screen = Screen('game_over')
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
        elif user_response == 'start_rounds':
            # Update round number in Screen
            Screen.round_number += 1
            user_response = letters_screen.render(
                new_player,
                new_letters,
                new_numbers,
                new_conundrum
            )
        else:
            print('Break out of round handler')
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
    # print(new_numbers.numbers)
    # sleep(5)
    new_conundrum = Conundrum()
    round_handler(new_player, new_letters, new_numbers, new_conundrum)
    print('Back in main')

# Call main game function

main()

