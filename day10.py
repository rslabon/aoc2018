import re

lines = """
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
""".strip().splitlines()

with open("./resources/day10.txt") as f:
    lines = f.read().strip().splitlines()

points = set()
for line in lines:
    x, y, dx, dy = re.findall(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>", line)[0]
    point = (int(x), int(y), int(dx), int(dy))
    points.add(point)


def move(point, seconds):
    x, y, dx, dy = point
    while seconds > 0:
        x, y = x + dx, y + dy
        seconds -= 1
    return x, y, dx, dy


def find_seconds_with_min_x_width():
    moved_points = set(points)
    min_seconds = None
    min_x_width = float("inf")
    for second in range(20_000):
        moved_points = set(map(lambda p: move(p, 1), moved_points))
        xs = list(map(lambda p: p[0], moved_points))
        min_x = min(xs)
        max_x = max(xs)
        if max_x - min_x < min_x_width:
            min_x_width = max_x - min_x
            min_seconds = second
    return min_seconds + 1


def show(seconds):
    moved_points = set(map(lambda p: move(p, seconds), points))
    moved_points = set(map(lambda p: (p[0], p[1]), moved_points))
    xs = list(map(lambda p: p[0], moved_points))
    min_x = min(xs)
    max_x = max(xs)
    ys = list(map(lambda p: p[1], moved_points))
    min_y = min(ys)
    max_y = max(ys)
    margin = 5
    for y in range(min_y - margin, max_y + margin):
        for x in range(min_x - margin, max_x + margin):
            if (x, y) in moved_points:
                print("#", end="")
            else:
                print(".", end="")
        print()


seconds = find_seconds_with_min_x_width()


def part1():
    show(seconds)


def part2():
    print(seconds)


part1()
part2()
