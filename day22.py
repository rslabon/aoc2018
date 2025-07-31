import functools
import heapq
from enum import Enum


class Type(Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2

    def __repr__(self):
        if self.value == 0:
            return '.'
        elif self.value == 1:
            return '='
        elif self.value == 2:
            return '|'


class Gear(Enum):
    Torch = 0
    Climbing = 1
    Neither = 2

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        if self.value == 0:
            return 'T'
        elif self.value == 1:
            return 'C'
        elif self.value == 2:
            return 'N'


possible_gear = {
    Type.ROCKY: {Gear.Climbing, Gear.Torch},
    Type.WET: {Gear.Neither, Gear.Climbing},
    Type.NARROW: {Gear.Torch, Gear.Neither},
}


class Step:
    def __init__(self):
        self.minutes = dict()


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


def print_map(path):
    for row in range(target[1] + 10):
        for col in range(target[0] + 10):
            if (col, row) in path:
                print(path[(col, row)].__repr__(), end="")
            elif (col, row) == target:
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


def part2():
    maxx = target[0] * 5
    maxy = target[1] * 2
    steps = dict()

    for y in range(maxy):
        for x in range(maxx):
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                to_x = x + dx
                to_y = y + dy
                if to_x < 0 or to_y < 0 or to_x >= maxx or to_y >= maxy:
                    continue
                from_type = type(x, y)
                to_type = type(to_x, to_y)

                from_possible_gear = possible_gear[from_type]

                for gear in from_possible_gear:
                    from_step = steps.get((x, y, gear), Step())
                    steps[(x, y, gear)] = from_step
                    for other_gear in from_possible_gear - {gear}:
                        change_gear = steps.get((to_x, to_y, other_gear), Step())
                        steps[(to_x, to_y, other_gear)] = change_gear
                        from_step.minutes[(x, y, other_gear)] = 7

                for gear in from_possible_gear:
                    if gear in possible_gear[to_type]:
                        to_step = steps.get((to_x, to_y, gear), Step())
                        steps[(to_x, to_y, gear)] = to_step
                        from_step = steps[(x, y, gear)]
                        from_step.minutes[(to_x, to_y, gear)] = 1

    q = []
    heapq.heapify(q)
    heapq.heappush(q, (0, 0, 0, Gear.Torch))
    cost = {(0, 0, Gear.Torch): 0}
    min_minutes = float("inf")
    prev = {(0, 0, Gear.Torch): None}
    seen = set()

    while q:
        _, x, y, gear = heapq.heappop(q)
        if (x, y, gear) in seen:
            continue
        seen.add((x, y, gear))

        if (x, y) == target and gear == Gear.Torch:
            took_minutes = cost[(x, y, gear)]
            min_minutes = min(min_minutes, took_minutes)
            break

        step = steps[(x, y, gear)]
        for next_x, next_y, next_gear in step.minutes.keys():
            new_cost = cost[(x, y, gear)] + step.minutes[(next_x, next_y, next_gear)]
            if (next_x, next_y, next_gear) not in cost or new_cost < cost[(next_x, next_y, next_gear)]:
                cost[(next_x, next_y, next_gear)] = new_cost
                prev[(next_x, next_y, next_gear)] = (x, y, gear)
                heapq.heappush(q, (new_cost, next_x, next_y, next_gear))

    print(min_minutes)


part1()
part2()
