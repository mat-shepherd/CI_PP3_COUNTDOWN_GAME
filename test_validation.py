# Imports
# Python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import unittest
# Internal
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from validation import (
    validate_name,
    validate_menu_value,
    validate_vowels,
    check_profanity,
    check_dictionary,
    print_word_meaning,
    check_letters_used,
    validate_numbers,
    validate_user_word,
    check_numbers_used,
    validate_user_numbers,
    validate_user_solution,
    validate_user_conundrum
)
from run import Player, Letters, Numbers, Conundrum
# Third Party
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from profanity_check import predict_prob
from PyDictionary import PyDictionary
import numexpr as ne


class TestValidation(unittest.TestCase):

    def test_validate_name(self):
        '''
        Tests if validate_name function returns
        expected values. Should only accept
        2 to 10 letter characters from user input.
        '''
        self.assertEqual(validate_name('Matthew'), True)
        self.assertEqual(validate_name('Will'), True)
        self.assertEqual(validate_name('MS'), True)
        self.assertEqual(validate_name('MatShep'), True)
        self.assertEqual(validate_name('M'), False)
        self.assertEqual(validate_name('123'), False)
        self.assertEqual(validate_name("@#'"), False)
        self.assertEqual(validate_name('Mat123'), False)
        self.assertEqual(validate_name(''), False)
        self.assertEqual(validate_name(' Mat'), False)
        self.assertEqual(validate_name('   '), False)
        self.assertEqual(validate_name('Mat Shep'), False)
        self.assertEqual(validate_name('M@t'), False)
        self.assertEqual(validate_name('MatShepherd'), False)

    def test_validate_menu_value(self):
        '''
        Tests if validate_menu_value function
        returns expected values. Should only
        accept number values in user input bewteen
        1 and 3 on intro screen and between 1 and 2
        rules screen.
        '''
        self.assertEqual(validate_menu_value(1, 'intro'), True)
        self.assertEqual(validate_menu_value(2, 'intro'), True)
        self.assertEqual(validate_menu_value(3, 'intro'), True)
        self.assertEqual(validate_menu_value('a', 'intro'), False)
        self.assertEqual(validate_menu_value(0, 'intro'), False)
        self.assertEqual(validate_menu_value(4, 'intro'), False)
        self.assertEqual(validate_menu_value(1, 'rules'), True)
        self.assertEqual(validate_menu_value(2, 'rules'), True)
        self.assertEqual(validate_menu_value('b', 'rules'), False)
        self.assertEqual(validate_menu_value(0, 'rules'), False)
        self.assertEqual(validate_menu_value(3, 'rules'), False)

    def test_validate_vowels(self):
        '''
        Tests if validate_vowels function
        returns expected values. Should only
        accept a user input of 3 to 9 for number
        of vowels - input is string.
        '''
        self.assertEqual(validate_vowels('3'), True)
        self.assertEqual(validate_vowels('7'), True)
        self.assertEqual(validate_vowels('2'), False)
        self.assertEqual(validate_vowels('10'), False)
        self.assertEqual(validate_vowels('a'), False)
        self.assertEqual(validate_vowels(' '), False)
        self.assertEqual(validate_vowels('0'), False)

    def test_check_profanity(self):
        '''
        Tests if check_profanity function
        returns expected values. Should return a value
        less than 0.9 for safe words and greater than 0.9
        for profane words.
        '''
        self.assertLess(check_profanity('hello'), 0.9)
        self.assertLess(check_profanity('pythonic'), 0.9)
        self.assertLess(check_profanity('dictionary'), 0.9)
        self.assertGreater(check_profanity('shit'), 0.9)
        self.assertGreater(check_profanity('bastard'), 0.9)

    def test_check_dictionary(self):
        '''
        Tests if check_dictionary function
        returns expected values. Should return None if
        word not found otherwise retruns word meaning.
        '''
        self.assertIsNotNone(check_dictionary('dictionary'))
        self.assertIsNotNone(check_dictionary('philanthropy'))
        self.assertIsNotNone(check_dictionary('testing'))
        self.assertIsNotNone(check_dictionary('jig'))
        self.assertIsNone(check_dictionary('snozzberry'))
        self.assertIsNone(check_dictionary('flibbidyflobbedy'))

    def test_print_word_meaning(self):
        '''
        Tests if print_word_meaning function
        returns expected values. Should return False if
        word not found otherwise prints word meaning and returns
        True.
        '''
        self.assertEqual(print_word_meaning('dictionary'), True)
        self.assertEqual(print_word_meaning('philanthropy'), True)
        self.assertEqual(print_word_meaning('testing'), True)
        self.assertEqual(print_word_meaning('jig'), True)
        self.assertEqual(print_word_meaning('snozzberry'), False)
        self.assertEqual(print_word_meaning('flibbidyflobbedy'), False)

    def test_check_letters_used(self):
        '''
        Tests if check_letters_used function
        returns expected values. Should return False if
        word uses letters not found in Player chosen
        letters or conundrum target letters list else
        returns True.
        '''
        new_player = Player()
        new_conundrum = Conundrum()
        new_player.chosen_letters = [
            'r', 'a', 'p', 'r', 'm', 'e', 'm', 'o', 'g'
        ]
        new_conundrum.target = [
            'v', 'a', 'l', 'i', 'd', 'a', 't', 'e', 'd'
        ]
        self.assertEqual(check_letters_used("programme", new_player), True)
        self.assertEqual(check_letters_used("gamer", new_player), True)
        self.assertEqual(check_letters_used("party", new_player), False)
        self.assertEqual(check_letters_used("excellent", new_player), False)
        self.assertEqual(check_letters_used("000", new_player), False)
        self.assertEqual(check_letters_used(" ", new_player), False)         
        self.assertEqual(
            check_letters_used("validated", new_player, new_conundrum),
            True
        )
        self.assertEqual(
            check_letters_used("dilate", new_player, new_conundrum),
            True
        )
        self.assertEqual(
            check_letters_used("bodacious", new_player, new_conundrum),
            False
        )
        self.assertEqual(
            check_letters_used("partyon", new_player, new_conundrum),
            False
        )
        self.assertEqual(
            check_letters_used("000", new_player, new_conundrum),
            False
        )
        self.assertEqual(
            check_letters_used(" ", new_player, new_conundrum),
            False
        )

    def test_validate_numbers(self):
        '''
        Tests if validate_numbers function
        returns expected values. Should only
        accept number values in user input of
        no less than 0 and no more than 4.
        '''
        self.assertEqual(validate_numbers('0'), True)
        self.assertEqual(validate_numbers('2'), True)
        self.assertEqual(validate_numbers('4'), True)
        self.assertEqual(validate_numbers('a'), False)
        self.assertEqual(validate_numbers('-1'), False)
        self.assertEqual(validate_numbers('-1'), False)
        self.assertEqual(validate_numbers('5'), False)

    def test_validate_user_word(self):
        '''
        Tests if validate_user_word function
        returns expected values. Returns True if
        letters round word is valid and uses only
        the letters provided else retruns False.
        '''
        new_player = Player()
        new_player.chosen_letters = [
            'r', 'a', 'p', 'r', 'm', 'e', 'm', 'o', 'g'
        ]
        self.assertEqual(check_letters_used("programme", new_player), True)
        self.assertEqual(check_letters_used("gamer", new_player), True)
        self.assertEqual(check_letters_used("000", new_player), False)
        self.assertEqual(check_letters_used(" ", new_player), False)           
        self.assertEqual(check_letters_used("party", new_player), False)
        self.assertEqual(check_letters_used("excellent", new_player), False)

    def test_check_numbers_used(self):
        '''
        Tests if check_numbers_used function
        returns expected values. Should return False if
        solution string uses numbers not found in Player
        chosen numbers list, or uses numbers more than shown,
        else returns True.
        '''
        new_player = Player()
        new_player.chosen_numbers = [25, 75, 100, 3, 7, 2]
        self.assertEqual(check_numbers_used("25 + 75 + 100", new_player), True)
        self.assertEqual(
            check_numbers_used("(7 - 3) + 100 *  2", new_player), True
        )
        self.assertEqual(
            check_numbers_used("25 * 75 + 3 / 100 + 7 - 2", new_player), True
        )
        self.assertEqual(
            check_numbers_used("4 + 25 + 100", new_player), False
        )
        self.assertEqual(
            check_numbers_used("25 + 25 + 100", new_player), False
        )


if __name__ == '__main__':
    unittest.main()
