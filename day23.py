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


def count_in_range(nanobots, x, y, z):
    in_range = 0
    for nano in nanobots:
        distance = manhatan_distance(nano, (x, y, z))
        if distance <= nano[3]:
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


def part2():
    xs = list(map(lambda x: x[0], nanobots))
    ys = list(map(lambda x: x[1], nanobots))
    zs = list(map(lambda x: x[2], nanobots))
    minx = min(xs)
    maxx = max(xs)
    miny = min(ys)
    maxy = max(ys)
    minz = min(zs)
    maxz = max(zs)
    max_range = max(maxx - minx, maxy - miny, maxz - minz)
    step = 1
    while step < max_range:
        step *= 2

    max_in_range = float('-inf')
    best_position = None
    best_distance = None

    while step > 1:
        for x in range(minx, maxx + 1, step):
            for y in range(miny, maxy + 1, step):
                for z in range(minz, maxz + 1, step):
                    in_range = count_in_range(nanobots, x, y, z)
                    distance = manhatan_distance((x, y, z), (0, 0, 0))
                    if in_range > max_in_range or (in_range == max_in_range and distance < best_distance):
                        max_in_range = in_range
                        best_position = (x, y, z)
                        best_distance = distance

        minx = best_position[0] - step
        maxx = best_position[0] + step
        miny = best_position[1] - step
        maxy = best_position[1] + step
        minz = best_position[2] - step
        maxz = best_position[2] + step
        step //= 2

    print(best_distance)


part1()
part2()
