#!/usr/bin/env python3

"""
算24点
"""
from decimal import Decimal
import sys


class BiOperator:
    def __init__(self, symbol, operation):
        self.symbol = symbol
        self.operation = operation

    def __str__(self):
        return self.symbol

    def calc(self, n1, n2):
        return self.operation(n1, n2)


class Express:
    def __init__(self, e1, op, e2):
        self.e1 = e1
        self.op = op
        self.e2 = e2

    def __str__(self):
        return "(%s%s%s)" % (self.e1, self.op, self.e2)

    def value(self):
        return self.op.calc(self.e1.value(), self.e2.value())


class Num:
    def __init__(self, n):
        self.num = Decimal(n)

    def __str__(self):
        return str(self.num)

    def value(self):
        return self.num


OPS = [
    BiOperator('+', lambda n1, n2: (n1 + n2)),
    BiOperator('-', lambda n1, n2: (n1 - n2)),
    BiOperator('*', lambda n1, n2: (n1 * n2)),
    BiOperator('-', lambda n1, n2: (n1 / n2))
]

GAME_TARGET = 24


def solve(nums):
    for expression in generate(nums):
        try:
            value = expression.value()
            if value == GAME_TARGET:
                return expression
        except ZeroDivisionError:
            pass
    return None


def generate(nums):
    if len(nums) == 0:
        return
    if len(nums) == 1:
        yield Num(nums[0])
        return
    for d in divide_nums(nums):
        for op in OPS:
            for e1 in generate(d[0]):
                for e2 in generate(d[1]):
                    yield Express(e1, op, e2)


def divide_nums(nums):
    for d in divide0(nums):
        if len(d[0]) > 0 and len(d[1]) > 0:
            yield d


def divide0(nums):
    if len(nums) == 0:
        yield [[], []]
        return
    for d in divide0(nums[1:]):
        yield [d[0]+[nums[0]], d[1]]
        yield [d[0], d[1]+[nums[0]]]


if __name__ == '__main__':
    nums_to_solve = sys.argv[1:]
    print(solve(nums_to_solve), '=', GAME_TARGET)
