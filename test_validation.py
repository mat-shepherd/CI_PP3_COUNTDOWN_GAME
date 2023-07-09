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
        Tests if validate_name function returns expected values.
        """
        self.assertTrue(validate_name("Matthew"))
        self.assertTrue(validate_name("Will"))
        self.assertTrue(validate_name("MS"))
        self.assertTrue(validate_name("MatShep"))
        self.assertFalse(validate_name("M"))
        self.assertFalse(validate_name("123"))
        self.assertFalse(validate_name("@#'"))
        self.assertFalse(validate_name("Mat123"))
        self.assertFalse(validate_name(""))
        self.assertFalse(validate_name(" Mat"))
        self.assertFalse(validate_name("   "))
        self.assertFalse(validate_name("Mat Shep"))
        self.assertFalse(validate_name("M@t"))
        self.assertFalse(validate_name("MatShepherd"))


if __name__ == '__main__':
    unittest.main()
