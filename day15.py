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


def destinations(enemies):
    result = set()
    for e in enemies:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next = (e[0] + dx, e[1] + dy)
            result.add(next)

    return result


def in_range(current, enemies):
    return current in destinations(enemies)


def shortest_paths(unit, heros, enemies, space):
    free_space = space - heros - enemies
    if not destinations(enemies) & free_space:
        return []

    q = []
    heapq.heapify(q)
    heapq.heappush(q, (0, unit, set(), []))
    paths = []

    while q:
        _, current, seen, path = heapq.heappop(q)
        if len(paths) > 0 and path and len(path) > len(paths[0]):
            break
        if current in seen:
            continue

        if current != unit:
            path.append(current)

        seen.add(current)
        if in_range(current, enemies):
            if path:
                paths.append(path)

        for dx, dy in [(-1, 0), (0, 1), (0, -1), (1, 0)]:
            next = (current[0] + dx, current[1] + dy)
            if not next in free_space:
                continue
            if next in seen:
                continue
            heapq.heappush(q, (len(path), next, set(seen), path[:]))

    return paths


def step_in_reading_order(paths):
    if not paths:
        return None

    paths = list(paths)
    last_step = min(map(lambda p: p[-1][0] * 10_000 + p[-1][1], paths))
    paths_with_last_step = list(filter(lambda p: p[-1][0] * 10_000 + p[-1][1] == last_step, paths))
    first_step = min(map(lambda p: p[0][0] * 10_000 + p[0][1], paths_with_last_step))
    return first_step // 10_000, first_step % 10_000


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
for _ in range(5):
    units_in_range = set()
    for elf in elfs:
        if in_range(elf, goblins):
            units_in_range.add(elf)
    for goblin in goblins:
        if in_range(goblin, elfs):
            units_in_range.add(goblin)

    units_to_move = elfs | goblins
    units_to_move = units_to_move - units_in_range
    units_to_move = sort_by_reading_order(units_to_move)
    for current in units_to_move:
        if current in elfs:
            paths = shortest_paths(current, elfs, goblins, space)
            step = step_in_reading_order(paths)
            if step:
                elfs.remove(current)
                elfs.add(step)
        else:
            paths = shortest_paths(current, goblins, elfs, space)
            step = step_in_reading_order(paths)
            if step:
                goblins.remove(current)
                goblins.add(step)

    units_in_range = sort_by_reading_order(units_in_range)
    for current in units_in_range:
        print(current)

    print_game(elfs, goblins, space)
