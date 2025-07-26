from collections import Counter

lines = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
""".strip().splitlines()

with open('./resources/day18.txt', 'r') as f:
    lines = f.read().strip().splitlines()


def parse_grid(lines):
    grid = dict()
    for row, line in enumerate(lines):
        for column, c in enumerate(line):
            grid[(row, column)] = c

    return grid


def adjacent(grid, x, y):
    result = []
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)):
        xx = x + dx
        yy = y + dy
        if (xx, yy) in grid:
            result.append(grid[(xx, yy)])

    return result


def print_grid(grid):
    for row in range(50):
        for col in range(50):
            if (row, col) in grid:
                print(grid[(row, col)], end="")
        print()
    print()


def score(grid):
    counter = Counter(grid.values())
    return counter["#"] * counter["|"]


def change(grid):
    new_grid = dict(grid)
    for k, v in grid.items():
        adj = adjacent(grid, *k)
        counter = Counter(adj)
        if v == "." and counter["|"] >= 3:
            new_grid[k] = "|"
        elif v == "|" and counter["#"] >= 3:
            new_grid[k] = "#"
        elif v == "#":
            if counter["|"] >= 1 and counter["#"] >= 1:
                new_grid[k] = "#"
            else:
                new_grid[k] = "."

    return new_grid


def part1():
    grid = parse_grid(lines)
    for _ in range(10):
        grid = change(grid)
    print(score(grid))


def part2():
    grid = parse_grid(lines)
    seen = []
    minute = 0
    while True:
        grid = change(grid)
        minute += 1
        if grid in seen:
            cycle = seen.index(grid)
            seen = seen[cycle:]
            break
        seen.append(grid)

    offset = (1000000000 - minute) % len(seen)
    print(score(seen[offset]))


part1()
part2()
