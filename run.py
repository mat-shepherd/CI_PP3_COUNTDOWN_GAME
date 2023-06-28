# Imports
# Python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from time import sleep
from itertools import permutations
import os
# Internal
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from validation import (
    validate_name,
    validate_menu_value,
    validate_vowels,
    validate_consonants,
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
                 score=None,
                 high_score=None,
                 round_time=None,
                 current_round=None,
                 chosen_letters=None,
                 chosen_numbers=None):
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
        'game_round': 'game_screen_data.txt',
        'game_over': 'game_over_screen_data.txt'
    }

    round_number = 1

    def __init__(self, screen_data_file):
        self.screen_data_param = screen_data_file
        self.screen_data_file = Screen.screen_data[screen_data_file]

    def render(self, new_player=None):
        """
        Set screen bg to blue and render
        screen text and prompt in the terminal
        """
        print(Back.BLUE)
        print(clear_screen())
        self.display_text_art()
        self.display_text()
        user_prompt = self.display_prompt(new_player)

        return user_prompt

    def display_text_art(self):
        """
        Output text as ASCII art via Art library
        """
        if self.screen_data_param == 'intro':
            result = text2art('        COUNTDOWN', font='small')
            print(result)
        elif self.screen_data_param == 'rules':
            result = text2art('        COUNTDOWN RULES', font='small')
            print(result)
        elif self.screen_data_param == 'game_round':
            round_word = num2words(self.round_number, lang='en').upper()
            result = text2art(f'            ROUND {round_word}', font='small')
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

    def display_prompt(self, new_player=None):
        """
        Display relevant screen prompt
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
        elif self.screen_data_param == 'game_round':
            # Only update round number after first round
            if Screen.round_number > 1:
                Screen.round_number += 1
            # First 3 letter rounds
            if Screen.round_number <= 3:
                if Screen.round_number == 1:
                    while True:
                        user_prompt = input(
                            Fore.WHITE +
                            'Please enter your name\n'
                        )
                        if validate_name(user_prompt):
                            new_player = Player(user_prompt)
                            print(clear_screen())
                            self.display_text_art()
                            self.display_text()
                            print_centered(f"{new_player.name.upper()}, LET'S PLAY COUNTDOWN!\n")
                            break
                        else:
                            continue
                print(
                    f'Choose nine letters in total from the '
                    'following selection of Vowels and Consonants'
                    )
                while True:
                    user_prompt = input(
                        Fore.WHITE +
                        'How many vowels would you like for your word?'
                        '(Enter a value between 3 and 9)\n'
                    )
                    if validate_vowels(user_prompt):
                        break
                    else:
                        continue
            # Numbers round
            elif Screen.round_number == 4:
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
        # Return the user_prompt value and the player object
        # back to round_handler so we know which screen to
        # render next and so that player details can be
        # accessed when rendering new screens
        return user_prompt, new_player


class Letters:
    """
    The Letters class to contain all letters
    to choose from in the letters round
    """
    vowels = []
    consonants = []

    def __init__(self):
        self.vowels = populate_vowels()
        self.consonants = populate_consonants()
    
    def populate_vowels(self):
        """
        Add a selection of vowels with
        weighting used in Scrabble
        """
        vowel_counts = {
            'A': 9,
            'E': 12,
            'I': 9,
            'O': 8,
            'U': 4
        }
        
        for vowel, count in vowel_counts.items():
            vowels.extend([vowel] * count)
        
    def populate_consonants(self):
        """
        Add a selection of consonants with
        weighting used in Scrabble
        """
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
        
        for consonant, count in consonant_counts.items():
            consonants.extend([consonant] * count)


class Numbers:
    """
    The Numbers class to contain all numbers
    to choose from in the numbers round
    """
    big = []
    small = []
    target = 999

    def __init__(self, big, small, target):
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

def round_handler():
    """
    Load the initial game screen and
    create the next screen based on
    user input
    """
    intro_screen = Screen('intro')
    rules_screen = Screen('rules')
    game_screen = Screen('game_round')
    # Capture user input and player object
    # when screens are rendered
    user_response, new_player = intro_screen.render()
    # Render intro, rules and first round screens
    while True:
        if user_response[0] == '1':
            user_response = game_screen.render()
        elif user_response[0] == '2':
            user_response = rules_screen.render()
            # Inner loop to loop between intro screen
            # and rules screen until 1 selected
            # then continue to outer loop
            while True:
                if user_response[0] == '1':
                    break
                else:
                    user_response, new_player = intro_screen.render()
                    break

# Main game functions


def main():
    """
    Run all program functions
    """
    round_handler()
    # Player(name,score,high_score,round_time,current_round,chosen_letters,chosen_numbers)

# Call main game function

main()

