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
        self.adj = dict()


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

    for from_y in range(maxy):
        for from_x in range(maxx):
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                to_x = from_x + dx
                to_y = from_y + dy
                if to_x < 0 or to_y < 0 or to_x >= maxx or to_y >= maxy:
                    continue
                from_type = type(from_x, from_y)
                to_type = type(to_x, to_y)

                from_possible_gear = possible_gear[from_type]

                for from_gear in from_possible_gear:
                    from_step = steps.get((from_x, from_y, from_gear), Step())
                    steps[(from_x, from_y, from_gear)] = from_step
                    for other_gear in from_possible_gear - {from_gear}:
                        change_step = steps.get((to_x, to_y, other_gear), Step())
                        steps[(to_x, to_y, other_gear)] = change_step
                        from_step.adj[(from_x, from_y, other_gear)] = 7

                for from_gear in from_possible_gear:
                    if from_gear in possible_gear[to_type]:
                        to_step = steps.get((to_x, to_y, from_gear), Step())
                        steps[(to_x, to_y, from_gear)] = to_step
                        from_step = steps[(from_x, from_y, from_gear)]
                        from_step.adj[(to_x, to_y, from_gear)] = 1

    q = []
    heapq.heapify(q)
    heapq.heappush(q, (0, 0, 0, Gear.Torch))
    cost = {(0, 0, Gear.Torch): 0}
    min_minutes = float("inf")
    prev = {(0, 0, Gear.Torch): None}
    seen = set()

    while q:
        _, from_x, from_y, gear = heapq.heappop(q)
        if (from_x, from_y, gear) in seen:
            continue
        seen.add((from_x, from_y, gear))

        if (from_x, from_y) == target and gear == Gear.Torch:
            took_minutes = cost[(from_x, from_y, gear)]
            min_minutes = min(min_minutes, took_minutes)
            break

        step = steps[(from_x, from_y, gear)]
        for nx, ny, ng in step.adj.keys():
            new_cost = cost[(from_x, from_y, gear)] + step.adj[(nx, ny, ng)]
            if (nx, ny, ng) not in cost or new_cost < cost[(nx, ny, ng)]:
                cost[(nx, ny, ng)] = new_cost
                prev[(nx, ny, ng)] = (from_x, from_y, gear)
                heapq.heappush(q, (new_cost, nx, ny, ng))

    print(min_minutes)


part1()
part2()
