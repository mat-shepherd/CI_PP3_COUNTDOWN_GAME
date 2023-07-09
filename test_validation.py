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


class TestValidation(unittest.TestCase):

    def test_validate_name(self):
        """
        Tests if validate_name function returns
        expected values. Should only accept
        2 to 10 letter characters from user input.
        """
        self.assertEqual(validate_name("Matthew"), True)
        self.assertEqual(validate_name("Will"), True)
        self.assertEqual(validate_name("MS"), True)
        self.assertEqual(validate_name("MatShep"), True)
        self.assertEqual(validate_name("M"), False)
        self.assertEqual(validate_name("123"), False)
        self.assertEqual(validate_name("@#'"), False)
        self.assertEqual(validate_name("Mat123"), False)
        self.assertEqual(validate_name(""), False)
        self.assertEqual(validate_name(" Mat"), False)
        self.assertEqual(validate_name("   "), False)
        self.assertEqual(validate_name("Mat Shep"), False)
        self.assertEqual(validate_name("M@t"), False)
        self.assertEqual(validate_name("MatShepherd"), False)

    def test_validate_menu_value(self):
        """
        Tests if validate_menu_value function
        returns expected values. Should only
        accept number values in user input bewteen
        1 and 3 on intro screen and between 1 and 2
        rules screen.
        """
        self.assertEqual(validate_menu_value(1, "intro"), True)
        self.assertEqual(validate_menu_value(2, "intro"), True)
        self.assertEqual(validate_menu_value(3, "intro"), True)
        self.assertEqual(validate_menu_value('a', "intro"), False)
        self.assertEqual(validate_menu_value(0, "intro"), False)
        self.assertEqual(validate_menu_value(4, "intro"), False)
        self.assertEqual(validate_menu_value(1, "rules"), True)
        self.assertEqual(validate_menu_value(2, "rules"), True)
        self.assertEqual(validate_menu_value('b', "rules"), False)
        self.assertEqual(validate_menu_value(0, "rules"), False)
        self.assertEqual(validate_menu_value(3, "rules"), False)

    def test_validate_vowels(self):
        """
        Tests if validate_vowels function
        returns expected values. Should only
        accept a user input of 3 to 9 for number
        of vowels - input is string.
        """
        self.assertEqual(validate_vowels('3'), True)
        self.assertEqual(validate_vowels('7'), True)
        self.assertEqual(validate_vowels('2'), False)
        self.assertEqual(validate_vowels('10'), False)
        self.assertEqual(validate_vowels('a'), False)
        self.assertEqual(validate_vowels(' '), False)
        self.assertEqual(validate_vowels('0'), False)


if __name__ == '__main__':
    unittest.main()
