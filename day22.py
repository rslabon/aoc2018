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

depth = 8112
target = (13, 743)

depth = 510
target = (10, 10)


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


def move_to(current, gear, destination):
    if destination[0] < 0 or destination[1] < 0:
        return []

    cx, cy = current
    ctype = type(cx, cy)
    dx, dy = destination
    dtype = type(dx, dy)

    common_gear = possible_gear[ctype] & possible_gear[dtype]
    if not common_gear:
        return []

    if destination == target:
        return [(7 + 1 if gear != Gear.Torch else 1, Gear.Torch, (dx, dy))]
    else:
        return [(7 if new_gear != gear else 1, new_gear, (dx, dy)) for new_gear in common_gear]


def manhatan_distance(current, destination):
    return abs(current[0] - destination[0]) + abs(current[1] - destination[1])


def part1():
    print(risk())


def part2():
    maxx = target[0] + 100
    maxy = target[1] + 100
    q = []
    heapq.heapify(q)
    heapq.heappush(q, (0, 0, 0, Gear.Torch, (0, 0), set(), []))
    min_minutes = float('inf')

    while q:
        _, minutes, changes, gear, (x, y), seen, path = heapq.heappop(q)

        if (x, y) in seen:
            continue
        if minutes >= min_minutes:
            continue

        seen.add((x, y))
        path.append(((x, y), minutes, gear, type(x, y)))
        if (x, y) == target:
            if minutes < min_minutes:
                min_minutes = minutes
            print("BUM!", minutes, changes)
            print_map(dict(map(lambda x: (x[0], x[2]), path)))
            continue

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            xx = x + dx
            yy = y + dy
            if (xx, yy) in seen:
                continue
            if xx < 0 or yy < 0:
                continue
            for next_minutes, next_gear, next_position in move_to((x, y), gear, (xx, yy)):
                if minutes + next_minutes < min_minutes:
                    heapq.heappush(q, (manhatan_distance(next_position, target),
                                       minutes + next_minutes,
                                       changes + (1 if next_gear != gear else 0),
                                       next_gear,
                                       next_position,
                                       set(seen),
                                       path[:]))


# def part2():
#     maxx = target[0] + 1000
#     maxy = target[1] + 1000
#     q = []
#     heapq.heapify(q)
#     heapq.heappush(q, (0, Gear.Torch, (0, 0)))
#     min_minutes = float('inf')
#     cost = {(0, 0): 0}
#     prev = {(0, 0): None}
#     xxx = {(0,0): Gear.Torch}
#
#     while q:
#         minutes, gear, (x, y) = heapq.heappop(q)
#
#         if (x, y) == target:
#             min_minutes = minutes
#             print(min_minutes)
#             c = (x, y)
#             path = [(x, y)]
#             cpath = [cost[c]]
#             while c:
#                 c = prev[c]
#                 if c:
#                     cpath.append(cost[c])
#                     path.append(c)
#             path.reverse()
#             cpath.reverse()
#             print(path)
#             print(cpath)
#             print_map(path)
#             break
#
#         for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
#             xx = x + dx
#             yy = y + dy
#             if xx < 0 or yy < 0:
#                 continue
#             for next_minutes, next_gear, next_position in move_to((x, y), gear, (xx, yy)):
#                 new_cost = cost[(x, y)] + next_minutes
#                 if next_position not in cost or new_cost < cost[next_position]:
#                     cost[next_position] = new_cost
#                     prev[next_position] = (x, y)
#                     heapq.heappush(q, (new_cost, next_gear, next_position))
#
#     print(min_minutes)


# part1()
part2()
# too high 1035
