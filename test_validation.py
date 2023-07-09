# Imports
# Python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import unittest
# Internal
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import validation


class TestValidation(unittest.TestCase):

    def test_validate_name(self):
        """
        Tests if validate_name function returns expected values.
        """
        self.assertTrue(validation.validate_name("Matthew"))
        self.assertFalse(validation.validate_name("M"))


if __name__ == '__main__':
    unittest.main()
