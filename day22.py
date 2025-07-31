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


def manhatan_distance(current, destination):
    return abs(current[0] - destination[0]) + abs(current[1] - destination[1])


def part1():
    print(risk())


def part2():
    type_cache = dict()
    maxx = target[0] * 2
    maxy = target[1] * 2

    for y in range(maxy):
        for x in range(maxx):
            type_cache[(x, y)] = type(x, y)

    steps = {(0, 0, Gear.Torch): Step()}
    for y in range(maxy):
        for x in range(maxx):
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                xx = x + dx
                yy = y + dy
                if xx < 0 or yy < 0 or xx >= maxx or yy >= maxy:
                    continue
                from_type = type_cache[(x, y)]
                to_type = type_cache[(xx, yy)]
                common_gear = possible_gear[from_type] & possible_gear[to_type]
                if not common_gear:
                    continue

                if (x, y) == (0, 0):
                    from_possible_gear = [Gear.Torch]
                else:
                    from_possible_gear = possible_gear[from_type]

                for from_gear in from_possible_gear:
                    from_step = steps.get((x, y, from_gear), Step())
                    steps[(x, y, from_gear)] = from_step
                    for to_gear in common_gear:
                        to_step_min = 1 if to_gear == from_gear else 7 + 1
                        to_step = steps.get((xx, yy, to_gear), Step())
                        steps[(xx, yy, to_gear)] = to_step
                        from_step.adj[(xx, yy, to_gear)] = to_step_min

    q = []
    heapq.heapify(q)
    heapq.heappush(q, (0, 0, 0, Gear.Torch))
    cost = {(0, 0, Gear.Torch): 0}
    min_minutes = float("inf")
    seen = set()

    while q:
        _, x, y, gear = heapq.heappop(q)
        if (x, y, gear) in seen:
            continue
        seen.add((x, y, gear))

        if (x, y) == target:
            took_minutes = cost[(x, y, gear)] + (0 if gear == Gear.Torch else 7)
            min_minutes = min(min_minutes, took_minutes)
            continue

        step = steps[(x, y, gear)]
        for nx, ny, ng in step.adj.keys():
            new_cost = cost[(x, y, gear)] + step.adj[(nx, ny, ng)]
            if (nx, ny, ng) not in cost or new_cost < cost[(nx, ny, ng)]:
                cost[(nx, ny, ng)] = new_cost
                heapq.heappush(q, (new_cost, nx, ny, ng))

    print(min_minutes)



# part1()
part2()
# too high 1035
