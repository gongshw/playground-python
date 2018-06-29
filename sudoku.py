#!/usr/bin/env python3

"""
解数独
"""
 
import time
import curses
import random
from curses import wrapper


pazzle = '800000000003600000070090200050007000000045700000100030001000068008500010090000400'


class Sudoku:
    def __init__(self, pazzle):
        self.cells = [None] * 81
        self._version = 1
        self._candidate_version = [0] * 81
        self._candidate = [None] * 81
        i = 0
        for c in pazzle:
            if c.isspace() or c == ',':
                continue
            if c > '9' or c < '1':
                self.cells[i] = 0
                i += 1
            else:
                self.cells[i] = int(c)
                i += 1

    @staticmethod
    def _xy_to_i(x, y):
        return x*9+y

    @staticmethod
    def xy_to_str(x, y):
        return "%s%d" % ('ABCDEFGHI'[x], y+1)

    def cell(self, x, y):
        return self.cells[Sudoku._xy_to_i(x, y)]

    def set_cell(self, x, y, value):
        self.cells[Sudoku._xy_to_i(x, y)] = value
        self._version += 1

    def row(self, x):
        return self.cells[x*9:x*9+9]

    def collumn(self, y):
        return [self.cells[i*9+y] for i in range(0, 9)]

    def cell9(self, x, y):
        for i in range(int(x/3)*3, int(x/3+1)*3):
            for j in range(int(y/3)*3, int(y/3+1)*3):
                yield self.cell(i, j)

    def _number(self, x, y):
        v = self.cell(x, y)
        return ' ' if v == 0 else str(v)

    def candidate(self, x, y):
        i = Sudoku._xy_to_i(x, y)
        if self._candidate_version[i] != self._version:
            x = int(i/9)
            y = i % 9
            candidate = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
            row = [a for a in self.row(x) if a != 0]
            candidate -= set(row)
            collumn = [a for a in self.collumn(y) if a != 0]
            candidate -= set(collumn)
            cell9 = [a for a in self.cell9(x, y) if a != 0]
            candidate -= set(cell9)
            self._candidate[i] = candidate
            self._candidate_version[i] = self._version
        return self._candidate[i]

    def complete(self):
        for x in range(9):
            for y in range(9):
                c = self.cell(x, y)
                if c == 0:
                    return False
        return True

    def __str__(self):
        cell = self._number
        return '  1 2 3 4 5 6 7 8 9\n' \
            + ' ┌─────┬─────┬─────┐\n' \
            + 'A│' + cell(0, 0) + ' ' + cell(0, 1) + ' ' + cell(0, 2) \
            + '│' + cell(0, 3) + ' ' + cell(0, 4) + ' ' + cell(0, 5) \
            + '│' + cell(0, 6) + ' ' + cell(0, 7) + ' ' + cell(0, 8)+'│\n' \
            + 'B│' + cell(1, 0) + ' ' + cell(1, 1) + ' ' + cell(1, 2) \
            + '│' + cell(1, 3) + ' ' + cell(1, 4) + ' ' + cell(1, 5) \
            + '│' + cell(1, 6) + ' ' + cell(1, 7) + ' ' + cell(1, 8)+'│\n' \
            + 'C│' + cell(2, 0) + ' ' + cell(2, 1) + ' ' + cell(2, 2) \
            + '│' + cell(2, 3) + ' ' + cell(2, 4) + ' ' + cell(2, 5) \
            + '│' + cell(2, 6) + ' ' + cell(2, 7) + ' ' + cell(2, 8)+'│\n'  \
            + ' ├─────┼─────┼─────┤\n' \
            + 'D│' + cell(3, 0) + ' ' + cell(3, 1) + ' ' + cell(3, 2) \
            + '│' + cell(3, 3) + ' ' + cell(3, 4) + ' ' + cell(3, 5) \
            + '│' + cell(3, 6) + ' ' + cell(3, 7) + ' ' + cell(3, 8)+'│\n' \
            + 'E│' + cell(4, 0) + ' ' + cell(4, 1) + ' ' + cell(4, 2) \
            + '│' + cell(4, 3) + ' ' + cell(4, 4) + ' ' + cell(4, 5) \
            + '│' + cell(4, 6) + ' ' + cell(4, 7) + ' ' + cell(4, 8)+'│\n' \
            + 'F│' + cell(5, 0) + ' ' + cell(5, 1) + ' ' + cell(5, 2) \
            + '│' + cell(5, 3) + ' ' + cell(5, 4) + ' ' + cell(5, 5) \
            + '│' + cell(5, 6) + ' ' + cell(5, 7) + ' ' + cell(5, 8)+'│\n'  \
            + ' ├─────┼─────┼─────┤\n' \
            + 'G│' + cell(6, 0) + ' ' + cell(6, 1) + ' ' + cell(6, 2) \
            + '│' + cell(6, 3) + ' ' + cell(6, 4) + ' ' + cell(6, 5) \
            + '│' + cell(6, 6) + ' ' + cell(6, 7) + ' ' + cell(6, 8)+'│\n' \
            + 'H│' + cell(7, 0) + ' ' + cell(7, 1) + ' ' + cell(7, 2) \
            + '│' + cell(7, 3) + ' ' + cell(7, 4) + ' ' + cell(7, 5) \
            + '│' + cell(7, 6) + ' ' + cell(1, 7) + ' ' + cell(7, 8)+'│\n' \
            + 'I│' + cell(8, 0) + ' ' + cell(8, 1) + ' ' + cell(8, 2) \
            + '│' + cell(8, 3) + ' ' + cell(8, 4) + ' ' + cell(8, 5) \
            + '│' + cell(8, 6) + ' ' + cell(8, 7) + ' ' + cell(8, 8)+'│\n'  \
            + ' └─────┴─────┴─────┘\n'


class Solver:

    def __init__(self, sudoku, scr):
        self.sudoku = sudoku
        self.scr = scr
        self.count = 0
        self.max_depth = len([a for a in self.sudoku.cells if a == 0])

    def _next0(self):
        x = None
        y = None
        candidate = None
        for i in range(9*9):
            x0 = int(i / 9)
            y0 = i % 9
            c0 = self.sudoku.cell(x0, y0)
            if c0 == 0:
                candidate0 = self.sudoku.candidate(x0, y0)
                if candidate == None or len(candidate0) < len(candidate):
                    x = x0
                    y = y0
                    candidate = candidate0
                    if len(candidate) == 1:
                        return [{"x": x, "y": y, "value": next(iter(candidate))}]
                    if len(candidate) == 0:
                        return []

        return [{"x": x, "y": y, "value": v} for v in candidate]

    def _next1_by(self, matrix_x, matrix_y):
        candidate1 = None
        for i in range(9):
            row = {}
            for j in range(9):
                x = matrix_x(i, j)
                y = matrix_y(i, j)
                if self.sudoku.cell(x, y) == 0:
                    for value in self.sudoku.candidate(x, y):
                        row.setdefault(value, []).append((x, y))
            for k, v in row.items():
                if candidate1 is None or len(candidate1) > len(v):
                    candidate1 = [{"x": xy[0], "y": xy[1], "value": k}
                                  for xy in v]
                    if len(candidate1) == 1:
                        return candidate1
        return candidate1

    def _next_by_row(self):
        return self._next1_by(lambda i, j: i, lambda i, j: j)

    def _next_by_collumn(self):
        return self._next1_by(lambda i, j: j, lambda i, j: i)

    def _next_by_cell9(self):
        def x_func(i, j): return (int(i/3)*3 + int(j/3))

        def y_func(i, j): return ((i % 3)*3 + j % 3)
        return self._next1_by(x_func, y_func)

    def _next1(self):
        candidate_row = self._next_by_row()
        if(len(candidate_row) <= 1):
            return candidate_row
        candidate_collumn = self._next_by_collumn()
        if(len(candidate_collumn) <= 1):
            return candidate_collumn
        candidate_cell9 = self._next_by_cell9()
        tmp = candidate_row if len(candidate_row) < len(
            candidate_collumn) else candidate_collumn
        return tmp if len(tmp) < len(candidate_cell9) else candidate_cell9

    def _next(self):
        candidate0 = self._next0()
        if len(candidate0) <= 1:
            return candidate0
        candidate1 = self._next1()
        return candidate1 if len(candidate1) < len(candidate0) else candidate0

    def _show(self, depth, guess):
        process = (depth+1)/self.max_depth*100
        process_bar = '=' * depth + '-'*(self.max_depth-depth-1)
        self.scr.addstr(0, 0, 'Guess count: %08d' % (self.count))
        self.scr.addstr(1, 0, 'Process: %03d%%[%s]' % (process, process_bar))
        self.scr.addstr(2, 0, 'try set ({}) to {}'.format(
            Sudoku.xy_to_str(guess["x"], guess["y"]), guess["value"]))
        self.scr.addstr(3, 0, 'time: %.3fs' % (time.clock() - self.start))
        self.scr.addstr(4, 0, str(self.sudoku))
        self.scr.refresh()

    def _solve(self, depth):
        if self.sudoku.complete():
            return True
        candidate = self._next()
        random.shuffle(candidate)
        for guess in candidate:
            self.sudoku.set_cell(guess["x"], guess["y"], guess["value"])
            self.count += 1
            self._show(depth, guess)
            if(self._solve(depth+1)):
                return True
            self.sudoku.set_cell(guess["x"], guess["y"], 0)
        return False

    def solve(self):
        self.start = time.clock()
        self._solve(0)


def main(stdscr):
    sudoku = Sudoku(pazzle)
    solver = Solver(sudoku, stdscr)
    solver.solve()
    stdscr.getch()


if __name__ == '__main__':
    from curses import wrapper
    wrapper(main)

