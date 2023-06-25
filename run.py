# Imports
# Python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from time import sleep
from itertools import permutations
import os
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Third Party
from PyDictionary import PyDictionary
from profanity_check import predict, predict_prob
import countdown_numbers_solver
from colorama import init
from colorama import Fore, Back
from colorama.ansi import clear_screen
from art import text2art


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
    def __init__(self, screen_data_file):
        self.screen_data_file = screen_data_file

    def render(self):
        # Set screen bg to blue and render screen elements in the terminal
        print(Back.BLUE)
        print(clear_screen())
        self.display_art_text()
        self.display_text()
        user_prompt = self.display_prompt()

        return user_prompt

    def display_art_text(self):
        # Output text as ASCII art via Figlet library
        if self.screen_data_file == 'intro_screen_data.txt':
            result = text2art("        COUNTDOWN", font='small')
            print(result)
        elif self.screen_data_file == 'rules_screen_data.txt':
            result = text2art("        COUNTDOWN RULES", font='small')
            print(result)
        elif self.screen_data_file == 'start_game_screen_data.txt':
            result = text2art("        ROUND ONE", font='small')
            print(result)

    def display_text(self):
        # Retrieve screen text from data files
        try:
            with open(self.screen_data_file) as f:
                text = f.read()
                print(text)
        except OSError as e:
            errno, strerror = e.args
            print(f'There is an I/O error number, {errno}: {strerror}.')

    def display_prompt(self):
        # Display relevant screen prompt
        if self.screen_data_file == 'intro_screen_data.txt':
            try:
                user_prompt = input(
                    'Enter 1 to Start the Game or 2'
                    ' to Read the Game Rules\n'
                    )
                if not (1 <= int(user_prompt) <= 2):
                    raise ValueError
            except ValueError:
                print(Fore.RED + 'Please enter only 1 or 2')
        elif self.screen_data_file == 'rules_screen_data.txt':
            try:
                user_prompt = input(
                    'Enter 1 to Start the Game or 2'
                    ' to Return to the Intro Screen\n'
                    )
                if not (1 <= int(user_prompt) <= 2):
                    raise ValueError
            except ValueError:
                print(Fore.RED + 'Please enter only 1 or 2')
        elif self.screen_data_file == 'start_game_screen_data.txt':
            while True:
                try:
                    user_prompt = input('Please Enter Your Name\n')
                    if (len(user_prompt) > 2 AND user_prompt.isalpha()):
                    break
                else:
                    raise Exception
                except TypeError:
                    print(Fore.RED + 'Please enter letters only')
                    continue
                except EOFError:
                    print(Fore.RED + 'Please enter your name')
                    continue

        return user_prompt


class Letters:
    """
    The Letters class to contain all letters
    to choose from in the letters round
    """
    def __init__(self, vowels, consonants):
        self.vowels = vowels
        self.consonants = consonants


class Numbers:
    """
    The Numbers class to contain all numbers
    to choose from in the numbers round
    """
    def __init__(self, big, small, target):
        self.big = big
        self.small = small
        self.target = target


class Conundrum:
    """
    The Conundrum class to contain the
    Conundrum word attributes for the
    Conundrum round
    """
    def __init__(self, target, scrambled):
        self.target = target
        self.scrambled = scrambled


# Main game functions
def main():
    """
    Run all program functions
    """
    intro_screen = Screen('intro_screen_data.txt')
    user_response = intro_screen.render()
    print(user_response)
    # Player(name,score,high_score,round_time,current_round,chosen_letters,chosen_numbers)

# Call main game function
main()

