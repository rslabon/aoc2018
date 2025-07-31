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


def part1():
    largest_signal_radius = sorted(nanobots, key=lambda x: x[3], reverse=True)[0]
    in_range = 0
    r = largest_signal_radius[3]
    for nanobot in set(nanobots):
        if manhatan_distance(largest_signal_radius, nanobot) <= r:
            in_range += 1
    print(in_range)


part1()
