import re

lines = """
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
""".strip().splitlines()

with open("./resources/day3.txt") as f:
    lines = f.read().strip().splitlines()

rectangles = []
for line in lines:
    id, col, row, width, height = re.findall(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line)[0]
    row, col = int(row), int(col)
    width, height = int(width), int(height)
    rectangles.append((id, row, col, width, height))


def part1():
    occurrences = dict()
    for id, row, col, width, height in rectangles:
        i = 0
        while i < height:
            j = 0
            while j < width:
                o = occurrences.get((row + i, col + j), 0) + 1
                occurrences[(row + i, col + j)] = o
                j += 1
            i += 1

    overlaps = 0
    for _, occurrences in occurrences.items():
        if occurrences > 1:
            overlaps += 1
    print(overlaps)


def part2():
    not_overlaps = set()
    occurrences = dict()
    for id, row, col, width, height in rectangles:
        not_overlaps.add(id)
        i = 0
        while i < height:
            j = 0
            while j < width:
                o = occurrences.get((row + i, col + j), set()) | {id}
                occurrences[(row + i, col + j)] = o
                if len(o) > 1:
                    not_overlaps -= o
                j += 1
            i += 1

    print(not_overlaps)


part1()
part2()
