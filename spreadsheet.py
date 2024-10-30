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
            if self.isstrconcatenation(cell):
                return self.handle_string_concatenation(cell)

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

        except ZeroDivisionError:
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

    def isstrconcatenation(self, cell: str) -> bool:
        if "&" in cell:
            return True

    def handle_string_concatenation(self, cell: str) -> str:
        cells = cell.split('&')
        result = ''
        for c in cells:
            value = self.evaluate(c)
            self.handle_cell_errors(value)
            result += value

        return result

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

    def handle_cell_errors(self, value: str | int) -> None:
        if value == '#Error':
            raise ValueError

        if value == '#Circular':
            raise RecursionError

        if value == '.':
            raise ValueError

        if isinstance(value, float):
            raise ValueError

    def handle_simple_calculation(self, cell: str) -> int | str:
        calc_array = []
        has_references = False
        index = 0

        while index < len(cell):
            if cell[index].isalpha():
                value = self.evaluate(self.get(cell[index] + cell[index + 1]))
                self.handle_cell_errors(value)
                calc_array.append(value)
                has_references = True
                index += 2
            else:
                calc_array.append(cell[index])
                index += 1

        if has_references:
            cell = ''.join(map(str, calc_array))

        cell = eval(cell.replace('=', ''))

        if isinstance(cell, float):
            return '#Error'

        return self.handle_simple_int(cell)
