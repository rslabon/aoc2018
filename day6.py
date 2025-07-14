from collections import deque

lines = """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""".strip().splitlines()

with open('./resources/day6.txt', 'r') as f:
    lines = f.read().strip().splitlines()

points = []
max_x = float("-inf")
max_y = float("-inf")
for line in lines:
    y, x = map(int, line.split(", "))
    points.append((x, y))
    max_x = max(max_x, x)
    max_y = max(max_y, y)


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def area(grid, p):
    seen = set()
    q = deque()
    q.append(p)

    while q:
        x, y = q.popleft()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_x = x + dx
            new_y = y + dy
            if not (0 <= new_x <= max_x and 0 <= new_y <= max_y):
                continue
            if grid[new_x, new_y][1] == p:
                q.append((new_x, new_y))

    return len(seen)


def part1():
    grid = dict()
    for i in range(0, max_x + 1):
        for j in range(0, max_y + 1):
            for p in points:
                d = manhattan_distance(p, (i, j))
                if (i, j) not in grid:
                    grid[(i, j)] = (d, p)
                elif grid[(i, j)][0] > d:
                    grid[(i, j)] = (d, p)
                elif grid[(i, j)][0] == d:
                    grid[(i, j)] = (d, ".")

    finite_points = set(points)
    i = 0
    for j in range(0, max_y + 1):  # top border
        finite_points -= {grid[(i, j)][1]}
    i = max_x
    for j in range(0, max_y + 1):  # bottom border
        finite_points -= {grid[(i, j)][1]}
    j = 0
    for i in range(0, max_x + 1):  # left border
        finite_points -= {grid[(i, j)][1]}
    j = max_y
    for i in range(0, max_x + 1):  # right border
        finite_points -= {grid[(i, j)][1]}

    max_area = float("-inf")
    for p in finite_points:
        max_area = max(max_area, area(grid, p))
    print(max_area)


def part2():
    regions = set()
    for i in range(0, max_x + 1):
        for j in range(0, max_y + 1):
            total = 0
            for p in points:
                total += manhattan_distance(p, (i, j))
                if total >= 10_000:
                    break
            if total < 10_000:
                regions.add((i, j))

    print(len(regions))


part1()
part2()
