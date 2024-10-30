from __future__ import annotations

class SpreadSheet:

    def __init__(self):
        self._cells = {}
        self._evaluating = set()

    def set(self, cell: str, value: str) -> None:
        self._cells[cell] = value

    def get(self, cell: str) -> str:
        return self._cells.get(cell, '')

    def evaluate(self, cell: str) -> int | str:
        try:
            if self.is_formula(cell):
                cell = cell.replace('=', '')

            # ========================================
            # Handle numbers
            # ========================================
            if cell.isnumeric():
                return int(cell)

            # ========================================
            # Handle strings
            # ========================================

            # Feature flags
            is_correctly_formatted = cell[0] == cell[-1] == "'"

            # Handle correct strings "'Apple'"
            if is_correctly_formatted:
                return cell.replace('"', '').replace("'", '')

            # Handle incorrect strings "'Apple"
            if not is_correctly_formatted:
                raise ValueError

            # ========================================
            # Handle formulas
            # ========================================

        except ValueError:
            return '#Error'

    def is_formula(self, cell: str) -> bool:
        return cell[0] == '='
