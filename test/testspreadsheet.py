from unittest import TestCase
from spreadsheet import SpreadSheet


class TestSpreadSheet(TestCase):

    def test_is_integer_passed_as_string(self):
        spreadsheet = SpreadSheet()
        self.assertEqual(1, spreadsheet.evaluate('1'))

    def test_is_double_return_error_string(self):
        spreadsheet = SpreadSheet()
        self.assertEqual('#Error', spreadsheet.evaluate('1.5'))

    def test_is_string_return_error_string(self):
        spreadsheet = SpreadSheet()
        self.assertEqual('#Error', spreadsheet.evaluate("'Apple"))

    def test_is_correct_string(self):
        spreadsheet = SpreadSheet()
        self.assertEqual('Apple', spreadsheet.evaluate("'Apple'"))

    def test_is_simple_formula_string(self):
        spreadsheet = SpreadSheet()
        self.assertEqual('Apple', spreadsheet.evaluate("='Apple'"))

    def testis_simple_formula_int(self):
        spreadsheet = SpreadSheet()
        self.assertEqual(1, spreadsheet.evaluate("=1"))

    def test_is_simple_formula_error(self):
        spreadsheet = SpreadSheet()
        self.assertEqual('#Error', spreadsheet.evaluate("='Apple"))

    def test_cell_references_cell_int(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=B1")
        spreadsheet.set("B1", "42")
        self.assertEqual(42, spreadsheet.evaluate("A1"))

    def test_cell_references_cell_double(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=B1")
        spreadsheet.set("B1", "42.5")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_cell_references_cell_circular(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=B1")
        spreadsheet.set("B1", "=A1")
        self.assertEqual("#Circular", spreadsheet.evaluate("A1"))

    def test_is_arithmetic_operator_addition(self):
        spreadsheet = SpreadSheet()
        self.assertEqual(4, spreadsheet.evaluate("=1+3"))

    def test_is_arithmetic_operator_addition_double(self):
        spreadsheet = SpreadSheet()
        self.assertEqual("#Error", spreadsheet.evaluate("=1+3.5"))

    def test_is_arithmetic_operator_addition_multiplication(self):
        spreadsheet = SpreadSheet()
        self.assertEqual(7, spreadsheet.evaluate("=1+3*2"))

    def test_is_arithmetic_operator_division_by_zero(self):
        spreadsheet = SpreadSheet()
        self.assertEqual("#Error", spreadsheet.evaluate("=1/0"))

    def test_is_arithmetic_operator_reference_addition(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1+B1")
        spreadsheet.set("B1", "3")
        self.assertEqual(4, spreadsheet.evaluate("A1"))

    def test_is_arithmetic_operator_reference_addition_double(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1+B1")
        spreadsheet.set("B1", "3.1")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_is_arithmetic_operator_reference_addition_circular(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1+B1")
        spreadsheet.set("B1", "=A1")
        self.assertEqual("#Circular", spreadsheet.evaluate("A1"))

    def test_is_string_concatenation(self):
        spreadsheet = SpreadSheet()
        self.assertEqual("Hello World", spreadsheet.evaluate("='Hello'&' World'"))

    def test_is_string_concatenation_error(self):
        spreadsheet = SpreadSheet()
        self.assertEqual("#Error", spreadsheet.evaluate("='Hello'&' World"))

    def test_is_string_concatenation_reference(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "='Hello'&B1")
        spreadsheet.set("B1", "' World'")
        self.assertEqual("Hello World", spreadsheet.evaluate("A1"))

    def test_is_string_concatenation_reference_error(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "='Hello'&B1")
        spreadsheet.set("B1", " World'")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_is_string_concatenation_reference_circular(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "='Hello'&B1")
        spreadsheet.set("B1", "=A1")
        self.assertEqual("#Circular", spreadsheet.evaluate("A1"))

    def test_is_arithmetic_operator_reference_addition_multiplication_parentheses(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=2*(1+2)")
        self.assertEqual(6, spreadsheet.evaluate("A1"))

    def test_is_arithmetic_operator_addition_multiplication_spaces(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "= 2 * (1 + 2)")
        self.assertEqual(6, spreadsheet.evaluate("A1"))


    def test_is_arithmetic_operator_reference_addition_multiplication(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=2*(1+B1)")
        spreadsheet.set("B1", "2")
        self.assertEqual(6, spreadsheet.evaluate("A1"))

    def test_is_arithmetic_operator_reference_addition_multiplication_spaces(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "= 2 * (1 + B1)")
        spreadsheet.set("B1", "2")
        self.assertEqual(6, spreadsheet.evaluate("A1"))

    def test_is_arithmetic_operator_reference_addition_multiplication_double(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=2*(1+B1)")
        spreadsheet.set("B1", "2.1")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_is_arithmetic_operator_reference_addition_multiplication_circular(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=2*(1+B1)")
        spreadsheet.set("B1", "=A1")
        self.assertEqual("#Circular", spreadsheet.evaluate("A1"))
