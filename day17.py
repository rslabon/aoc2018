from collections import deque

lines = """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
""".strip().splitlines()

# lines = """
# x=480, y=4..10
# x=520, y=2..10
# y=10, x=480..520
# x=495, y=5..7
# x=505, y=5..7
# y=7, x=495..505
# """.strip().splitlines()

with open("./resources/day17.txt") as f:
    lines = f.read().strip().splitlines()

scans = []
water_source = (500, 0)
x_margin = 50
y_margin = 5
min_x, max_x = float("inf"), float("-inf")
min_y, max_y = float("inf"), float("-inf")
for line in lines:
    parts = line.split(", ")
    x = None
    y = None
    for p in parts:
        if p.startswith("x="):
            if ".." in p:
                start, end = map(int, p[2:].split(".."))
                x = (start, end)
            else:
                x = (int(p[2:]), int(p[2:]))
        else:
            if ".." in p:
                start, end = map(int, p[2:].split(".."))
                y = (start, end)
            else:
                y = (int(p[2:]), int(p[2:]))

    min_x = min(min_x, x[0])
    max_x = max(max_x, x[1])
    min_y = min(min_y, y[0])
    max_y = max(max_y, y[1])

    scans.append((x, y))

print(min_x, max_x, min_y, max_y)

grid = {}
for scan in scans:
    x_range, y_range = scan
    for y in range(y_range[0], y_range[1] + 1):
        for x in range(x_range[0], x_range[1] + 1):
            grid[(x, y)] = "#"


def print_scans(grid, drops):
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) == water_source:
                print("+", end="")
            elif (x, y) in grid:
                print(grid[(x, y)], end="")
            elif (x, y) in drops:
                print("|", end="")
            else:
                print(".", end="")
        print()


def can_move(grid, x, y):
    return (x, y) not in grid


# print_scans(grid, set())
total = set()
last_seen = set()
while True:
    drops = deque([(500, 0)])
    seen = set()
    while drops:
        x, y = drops.popleft()
        if (x, y) in seen:
            continue
        if y > max_y:
            continue

        seen.add((x, y))

        if can_move(grid, x, y + 1):
            drops.appendleft((x, y + 1))
        else:
            if can_move(grid, x - 1, y):
                drops.appendleft((x - 1, y))
            if can_move(grid, x + 1, y):
                drops.appendleft((x + 1, y))

    if seen:
        seen_y = sorted(set(map(lambda x: x[1], seen)))
        seen_y = filter(lambda y: y < max_y, seen_y)
        for y in seen_y:
            level = filter(lambda x: x[1] == y, seen)
            level = sorted(level, key=lambda x: x[0])
            levels = []
            if level:
                clevel = []
                prev_x = None
                for x, y in level:
                    if prev_x is None or prev_x + 1 == x:
                        clevel.append((x, y))
                        prev_x = x
                    elif prev_x + 1 != x:
                        levels.append(clevel)
                        clevel = [(x, y)]
                        prev_x = x
                if clevel:
                    levels.append(clevel)

            for level in levels:
                has_level_bellow = False
                for (x, y) in level:
                    if (x, y + 1) in seen:
                        has_level_bellow = True
                        break
                if has_level_bellow:
                    continue
                for (x, y) in level:
                    grid[(x, y)] = "@"

    if last_seen == seen:
        break

    last_seen = seen
    total |= seen
    print(len(total))

# zle too low 685
# zle too high 175737
# zle too high 75261
print_scans(grid, total)
total |= set([k for k, v in grid.items() if v == "@"])
total = [(x, y) for (x, y) in total if min_y <= y <= max_y]
print(len(total))
# 31788
