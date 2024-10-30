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
            # Handle formula cases
            if self.isformula(cell):
                cell = self.handle_simple_formula(cell)

            # Handle reference cases
            if self.isreference(cell):
                return self.evaluate(self.get(cell))

            # Handle calculation cases
            if self.iscalculation(cell):
                return self.handle_simple_calculation(cell)

            # Handle simple int cases
            if cell.isnumeric():
                return self.handle_simple_int(cell)

            # Handle simple string cases
            return self.handle_simple_strings(cell)

        except ValueError:
            return '#Error'

        except RecursionError:
            return '#Circular'

    def iscalculation(self, cell: str) -> bool:
        if '+' in cell:
            return True

        if '-' in cell:
            return True

        if '*' in cell:
            return True

        if '/' in cell:
            return True

        return False

    def isformula(self, cell: str) -> bool:
        return cell[0] == '='

    def isreference(self, cell: str) -> bool:
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return cell[0] in letters and cell[1:].isnumeric()

    def handle_simple_formula(self, cell: str) -> int | str:
        return cell.replace('=', '')

    def handle_simple_strings(self, cell: str) -> str:
        # Feature flags
        is_correctly_formatted = cell[0] == cell[-1] == "'"

        # Handle correct strings "'Apple'"
        if is_correctly_formatted:
            return cell.replace('"', '').replace("'", '')

        # Handle incorrect strings "'Apple"
        if not is_correctly_formatted:
            raise ValueError

    def handle_simple_int(self, cell: str) -> int:
        return int(cell)

    def handle_simple_calculation(self, cell: str) -> int | str:
        cell = eval(cell.replace('=', ''))

        if isinstance(cell, float):
            return '#Error'

        return self.handle_simple_int(cell)