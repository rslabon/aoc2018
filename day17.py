from collections import deque
from enum import Enum

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
# x=480, y=2..10
# x=520, y=2..10
# y=10, x=480..520
# x=495, y=5..7
# x=505, y=5..7
# y=7, x=495..505
# """.strip().splitlines()


with open("./resources/day17.txt") as f:
    lines = f.read().strip().splitlines()


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    DOWN = 3


def can_move(grid, seen, x, y):
    return (x, y) not in grid and (x, y) not in seen


class WaterDrop:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def move(self, grid, seen):
        if self.direction == Direction.DOWN:
            if can_move(grid, seen, self.x, self.y + 1):
                return [WaterDrop(self.x, self.y + 1, Direction.DOWN)]
            else:
                r = []
                if can_move(grid, seen, self.x - 1, self.y):
                    r.append(WaterDrop(self.x - 1, self.y, Direction.LEFT))
                if can_move(grid, seen, self.x + 1, self.y):
                    r.append(WaterDrop(self.x + 1, self.y, Direction.RIGHT))
                if len(r) == 0:
                    grid[(self.x, self.y)] = "@"

                return r
        elif self.direction == Direction.LEFT:
            if can_move(grid, seen, self.x, self.y + 1):
                return [WaterDrop(self.x, self.y + 1, Direction.DOWN)]
            elif can_move(grid, seen, self.x - 1, self.y):
                return [WaterDrop(self.x - 1, self.y, Direction.LEFT)]
            else:
                grid[(self.x, self.y)] = "@"

        elif self.direction == Direction.RIGHT:
            if can_move(grid, seen, self.x, self.y + 1):
                return [WaterDrop(self.x, self.y + 1, Direction.DOWN)]
            elif can_move(grid, seen, self.x + 1, self.y):
                return [WaterDrop(self.x + 1, self.y, Direction.RIGHT)]
            else:
                grid[(self.x, self.y)] = "@"

        return []

    def __repr__(self):
        return f"WaterDrop({self.x}, {self.y}, {self.direction})"


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
    for y in range(min_y - y_margin, max_y + 1 + y_margin):
        for x in range(min_x - x_margin, max_x + 1 + x_margin):
            if (x, y) == water_source:
                print("+", end="")
            elif (x, y) in grid:
                print(grid[(x, y)], end="")
            elif (x, y) in drops:
                print("|", end="")
            else:
                print(".", end="")
        print()


# print_scans(grid)
total = set()
last_seen = set()
while True:
    drops = deque([WaterDrop(500, 1, Direction.DOWN)])
    seen = set()
    while drops:
        drop = drops.popleft()
        if (drop.x, drop.y) in seen:
            continue
        if min_x < drop.x > max_x + 1 or min_y < drop.y > max_y:
            continue
        seen.add((drop.x, drop.y))
        move = drop.move(grid, seen)
        drops += move

    if seen == last_seen:
        break

    last_seen = seen
    total |= seen
    print(len(total))

print_scans(grid, total)

# zle too low 685
# zle too high 175737
print(len(total))
