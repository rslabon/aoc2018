import functools
import re

lines = """
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
""".strip().splitlines()

lines = """
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
""".strip().splitlines()

with open('./resources/day23.txt') as f:
    lines = f.read().strip().splitlines()

nanobots = []
for line in lines:
    x, y, z, r = re.findall(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)', line)[0]
    x = int(x)
    y = int(y)
    z = int(z)
    r = int(r)
    nanobots.append((x, y, z, r))


def manhatan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def intersection(ranges):
    ranges = sorted(ranges)
    stack = []
    for r in ranges:
        if not stack:
            stack.append(r)
        elif r[0] > stack[-1][1]:
            stack.append(r)
        else:
            if r[0] <= stack[-1][1]:
                stack[-1][0] = r[0]
            if r[1] <= stack[-1][1]:
                stack[-1][1] = r[1]

    return stack


@functools.cache
def number_in_range(pos):
    in_range = 0
    for nanobot in set(nanobots):
        if manhatan_distance(pos, nanobot) <= nanobot[3]:
            in_range += 1
    return in_range


def part1():
    largest_signal_radius = sorted(nanobots, key=lambda x: x[3], reverse=True)[0]
    in_range = 0
    r = largest_signal_radius[3]
    for nanobot in set(nanobots):
        if manhatan_distance(largest_signal_radius, nanobot) <= r:
            in_range += 1
    print(in_range)


def xxx(nanobots, x, y, z, r):
    in_range = 0
    for other_nanobot in nanobots:
        distance = manhatan_distance(other_nanobot, (x, y, z))
        if distance <= other_nanobot[3] + r:
            in_range += 1
    return in_range


def part2(nanobots):
    nanobots = set(nanobots)
    ranges = dict()
    for nanobot in nanobots:
        in_range = 0
        for other_nanobot in nanobots - {nanobot}:
            distance = manhatan_distance(other_nanobot, nanobot)
            if distance <= other_nanobot[3] + nanobot[3]:
                in_range += 1
        ranges[nanobot] = in_range

    nano_in_ranges, _, (x, y, z, r) = list(sorted(map(lambda x: (-x[1], x[0][-1], x[0]), ranges.items())))[0]
    nano_in_ranges = - nano_in_ranges
    nanobots -= {(x, y, z, r)}
    rr = r
    while True:
        k = xxx(nanobots, x, y, z, r)
        if k < nano_in_ranges:
            r += 1
            break
        r -= 1
    print(rr, r)

# print(xranges)
# print(intersection(xranges))
#
# print(yranges)
# print(intersection(yranges))
#
# print(zranges)
# print(intersection(zranges))


# part1()
part2(nanobots)
