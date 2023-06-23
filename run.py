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
from colorama import Fore

# Initialize colorama
init(autoreset=True)

# Classes
class Player:
    def __init__(self,
                 name,
                 score,
                 high_score,
                 round_time,
                 current_round,
                 chosen_letters,
                 chosen_numbers):
        self.name = name
        self.score = score
        self.high_score = high_score
        self.round_time = round_time
        self.current_round = current_round
        self.chosen_letters = chosen_letters
        self.chosen_numbers = chosen_numbers        

class Screen:
    def __init__(self, name, content):
        self.name = name
        self.content = content

class Letters:
    def __init__(self, vowels, consonants):
        self.vowels = vowels
        self.consonants = consonants

class Numbers:
    def __init__(self, big, small, target):
        self.big = big
        self.small = small
        self.target = target

class Conundrum:
    def __init__(self, target, scrambled):
        self.target = target
        self.scrambled = scrambled 

# Game

