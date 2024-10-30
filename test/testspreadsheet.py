from unittest import TestCase
from spreadsheet import SpreadSheet


class TestSpreadSheet(TestCase):

    def test_cell_content_is_integer_passed_as_string(self):
        spreadsheet = SpreadSheet()
        self.assertEqual(1, spreadsheet.evaluate('1'))

    def test_cell_content_is_double_return_error_string(self):
        spreadsheet = SpreadSheet()
        self.assertEqual('#Error', spreadsheet.evaluate('1.5'))

    def test_cell_content_is_string_return_error_string(self):
        spreadsheet = SpreadSheet()
        self.assertEqual('#Error', spreadsheet.evaluate("'Apple"))

    def test_cell_content_is_correct_string(self):
        spreadsheet = SpreadSheet()
        self.assertEqual('Apple', spreadsheet.evaluate("'Apple'"))

    def test_cell_content_is_simple_formula_string(self):
        spreadsheet = SpreadSheet()
        self.assertEqual('Apple', spreadsheet.evaluate("='Apple'"))

    def test_cell_content_is_simple_formula_int(self):
        spreadsheet = SpreadSheet()
        self.assertEqual(1, spreadsheet.evaluate("=1"))

    def test_cell_content_is_simple_formula_error(self):
        spreadsheet = SpreadSheet()
        self.assertEqual('#Error', spreadsheet.evaluate("='Apple"))

    def test_cell_references_simple_formula(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=B1")
        spreadsheet.set("B1", "42")
        self.assertEqual(42, spreadsheet.evaluate("A1"))
