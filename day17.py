import random
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

# with open("./resources/day17.txt") as f:
#     lines = f.read().strip().splitlines()

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

grid = {}
for scan in scans:
    x_range, y_range = scan
    for y in range(y_range[0], y_range[1] + 1):
        for x in range(x_range[0], x_range[1] + 1):
            grid[(x, y)] = "#"


def print_scans(grid, drops):
    for y in range(min_y - 1, max_y + 1):
        for x in range(min_x - 5, max_x + 5):
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


def clear(reserves, id):
    if id in reserves:
        for p in reserves[id]:
            if p in grid:
                del grid[p]
        del reserves[id]


total = set()
while True:
    id = random.random()
    drops = deque([(water_source[0], water_source[1], id)])
    seen = set()
    reserves = {id: set()}
    before_reserves = set([k for k, v in grid.items() if v == "~"])
    while drops:
        x, y, id = drops.popleft()
        if (x, y) in seen:
            continue
        if y > max_y:
            clear(reserves, id)
            continue

        seen.add((x, y))
        total.add((x, y))

        moved = False
        if can_move(grid, x, y + 1) and (x, y + 1):
            seen.remove((x, y))
            if id in reserves:
                seen -= reserves[id]
            clear(reserves, id)
            id = random.random()
            if id not in reserves:
                reserves[id] = {(x, y + 1)}
            drops.appendleft((x, y + 1, id))
            moved = True
        else:
            if can_move(grid, x - 1, y) and (x - 1, y) not in seen:
                if id in reserves:
                    reserves[id].add((x - 1, y))
                drops.appendleft((x - 1, y, id))
                moved = True
            if can_move(grid, x + 1, y) and (x + 1, y) not in seen:
                if id in reserves:
                    reserves[id].add((x + 1, y))
                drops.appendleft((x + 1, y, id))
                moved = True

        if not moved:
            if id in reserves:
                for p in reserves[id]:
                    grid[p] = "~"

    after_reserves = set([k for k, v in grid.items() if v == "~"])
    if before_reserves == after_reserves:
        break

print_scans(grid, total)
total = [(x, y) for (x, y) in total if min_y <= y <= max_y]
print("part1", len(total))  # 31788
print("part2", len(after_reserves))  # 25800
