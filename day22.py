import functools
from enum import Enum


class Type(Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2


depth = 8112
target = (13, 743)


# depth = 510
# target = (10, 10)


@functools.cache
def erosion_level(x, y):
    return (geologic_index(x, y) + depth) % 20183


@functools.cache
def type(x, y):
    if erosion_level(x, y) % 3 == 0:
        return Type.ROCKY
    if erosion_level(x, y) % 3 == 1:
        return Type.WET
    if erosion_level(x, y) % 3 == 2:
        return Type.NARROW
    raise ValueError("Unknown erosion level")


@functools.cache
def geologic_index(x, y):
    if (x, y) == (0, 0):
        return 0
    elif (x, y) == target:
        return 0
    elif y == 0:
        return x * 16807
    elif x == 0:
        return y * 48271
    else:
        return erosion_level(x - 1, y) * erosion_level(x, y - 1)


def print_map():
    for row in range(target[1] + 1):
        for col in range(target[0] + 1):
            if (col, row) == target:
                print("T", end="")
            elif (col, row) == (0, 0):
                print("M", end="")
            else:
                t = type(col, row)
                if t == Type.ROCKY:
                    print(".", end="")
                if t == Type.WET:
                    print("=", end="")
                if t == Type.NARROW:
                    print("|", end="")
        print()
    print()


def risk():
    total = 0
    for row in range(target[1] + 1):
        for col in range(target[0] + 1):
            t = type(col, row)
            if t == Type.ROCKY:
                total += 0
            if t == Type.WET:
                total += 1
            if t == Type.NARROW:
                total += 2

    return total


def part1():
    print(risk())


part1()
