import heapq

lines = """
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########
""".strip().splitlines()


def sort_by_reading_order(positions):
    sorted_positions = sorted(positions, key=lambda p: (p[0], p[1]))
    return sorted_positions


def in_range(current, enemies):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        next = (current[0] + dx, current[1] + dy)
        if next in enemies:
            return True
    return False


def shortest_path(current, heros, enemies, space):
    q = []
    heapq.heapify(q)
    heapq.heappush(q, (0, current, set(), []))
    free_space = space - heros - enemies

    paths = []

    while q:
        _, c, seen, path = heapq.heappop(q)
        if c in seen:
            continue

        seen.add(c)
        path.append(c)
        if in_range(c, enemies):
            if len(paths) > 0 and path and len(path[1:]) > len(paths[0]):
                break
            paths.append(path[1:])

        for dx, dy in [(-1, 0), (0, 1), (0, -1), (1, 0)]:
            next = (c[0] + dx, c[1] + dy)
            if not next in free_space:
                continue
            if next in seen:
                continue
            heapq.heappush(q, (len(path), next, set(seen), path[:]))

    print(paths)
    return paths


elfs = set()
goblins = set()
space = set()
for row, line in enumerate(lines):
    for col, c in enumerate(line):
        if c == '.':
            space.add((row, col))
        elif c == 'E':
            elfs.add((row, col))
            space.add((row, col))
        elif c == 'G':
            goblins.add((row, col))
            space.add((row, col))


def print_game(elfs, goblins, space):
    for row in range(len(lines)):
        for col in range(len(lines[0])):
            if (row, col) in elfs:
                print('E', end='')
            elif (row, col) in goblins:
                print('G', end='')
            elif (row, col) in space:
                print('.', end='')
            else:
                print('#', end='')
        print()
    print()


print_game(elfs, goblins, space)
for _ in range(3):
    all = elfs | goblins
    all = sort_by_reading_order(all)
    for current in all:
        if current in elfs:
            path = shortest_path(current, elfs, goblins, space)
            if path:
                elfs.remove(current)
                elfs.add(path[0])
        else:
            path = shortest_path(current, goblins, elfs, space)
            if path:
                goblins.remove(current)
                goblins.add(path[0])

    print_game(elfs, goblins, space)
