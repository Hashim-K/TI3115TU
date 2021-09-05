import unittest
from textwrap import dedent

import mock
from project.factorial_calc import ask_factorial, calc_factorial
from contextlib import redirect_stdout
from io import StringIO

# This class is used as a helper for the unit tests.
# It is needed since our program heavily depends on input/output behaviour.
# It iterates through the input.
class InputIter:
    def __init__(self, return_values, out):
        self.return_values_iter = iter(return_values)
        self.out = out

    def fake_input(self, prompt=''):
        self.out.write(prompt)
        return next(self.return_values_iter)

# The main test suite class.
# Note: These test are not exhaustive and nowhere near that.
# They should only serve as an example for testing user input
# and conducting unit tests in general.
class TestSuite(unittest.TestCase):

    # Test for behaviour with "normal" input
    # We mock console input and feed it using our InputIter class
    # The assertions we make: that the correct input '10' was fed and
    # that the program output the correct statement in the console.
    def test_ask_factorial(self):
        out = StringIO()
        with redirect_stdout(out), mock.patch('builtins.input', InputIter(['10'], out).fake_input):
            number = ask_factorial()
            self.assertEqual(10, number)
            self.assertEqual("Enter a number to find its factorial: \n", out.getvalue())

    # Test for behaviour with "abnormal" input and for loop behaviour.
    # We mock console input and feed it using our InputIter class
    # The assertions we make: that the correct input '12' was accepted at some point
    # and that the "1.1" input was not accepted
    # and the program output the correct statement in the console.
    def test_ask_factorial_number_float(self):
        out = StringIO()
        with redirect_stdout(out), mock.patch('builtins.input', InputIter(['1.1', '12'], out).fake_input):
            number = ask_factorial()
            self.assertEqual(12, number)
            self.assertEqual(dedent("""\
                Enter a number to find its factorial: 
                The number should be an integer.
                Enter a number to find its factorial: 
                """), out.getvalue())

    # Test for behaviour with "normal" input and correct factorial calculation.
    # We mock console input and feed it using our InputIter class
    # The assertions we make: that the correct input '3' was accepted
    # and that the correct answer of '6' was output.
    def test_get_factorial_correct(self):
        out = StringIO()
        with redirect_stdout(out), mock.patch('builtins.input', InputIter(['3'], out).fake_input):
            number = ask_factorial()
            self.assertEqual(3, number)
            calc_factorial(number)
            self.assertEqual(dedent("""\
                Enter a number to find its factorial: 
                result: 6\n"""), out.getvalue())

