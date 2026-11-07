import unittest
from unittest.mock import patch

from src.validation import ask_integer, ask_option


class TestValidation(unittest.TestCase):

    def test_valid_integer(self):
        with patch("builtins.input", return_value="80000"):
            result = ask_integer("Mileage: ")

        self.assertEqual(result, 80000)

    def test_invalid_integer(self):
        with patch("builtins.input", side_effect=["abc", "-100", "80000"]):
            result = ask_integer("Mileage: ")

        self.assertEqual(result, 80000)

    def test_valid_option(self):
        options = ["Automatic", "Manual", "Semi-automatic"]

        with patch("builtins.input", return_value="2"):
            result = ask_option("Transmission", options)

        self.assertEqual(result, "Manual")

    def test_invalid_option(self):
        options = ["Automatic", "Manual", "Semi-automatic"]

        with patch("builtins.input", side_effect=["99", "abc", "1"]):
            result = ask_option("Transmission", options)

        self.assertEqual(result, "Automatic")


if __name__ == "__main__":
    unittest.main()
