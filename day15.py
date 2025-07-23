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

lines = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#   
####### 
""".strip().splitlines()


class Unit:
    def __init__(self, x, y, elf, hp, attack):
        self.x = x
        self.y = y
        self.elf = elf
        self.hp = hp
        self.attack = attack

    def is_alive(self):
        return self.hp > 0

    def __repr__(self):
        return f"{"Elf" if self.elf else "Goblin"} [{self.x},{self.y}] - {self.hp}"


def position_of(units):
    return set(map(lambda u: (u.x, u.y), units))


def sort_by_reading_order(units):
    sorted_positions = sorted(units, key=lambda u: (u.x, u.y))
    return sorted_positions


def destinations(positions):
    result = set()
    for p in positions:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next = (p[0] + dx, p[1] + dy)
            result.add(next)

    return result


def in_range(position, enemy_positions):
    return (position[0], position[1]) in destinations(enemy_positions)


def shortest_paths(unit, heros, enemies, space):
    starting_position = (unit.x, unit.y)
    heros_positions = position_of(heros)
    enemy_positions = position_of(enemies)
    free_space = space - heros_positions - enemy_positions
    if not destinations(enemy_positions) & free_space:
        return []

    q = []
    heapq.heapify(q)
    heapq.heappush(q, (0, starting_position, set(), []))
    paths = []

    while q:
        _, current_position, seen, path = heapq.heappop(q)
        if len(paths) > 0 and path and len(path) > len(paths[0]):
            break
        if current_position in seen:
            continue

        if current_position != starting_position:
            path.append(current_position)

        seen.add(current_position)
        if in_range(current_position, enemy_positions):
            if path:
                paths.append(path)

        for dx, dy in [(-1, 0), (0, 1), (0, -1), (1, 0)]:
            next = (current_position[0] + dx, current_position[1] + dy)
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
            elfs.add(Unit(row, col, True, 200, 3))
            space.add((row, col))
        elif c == 'G':
            goblins.add(Unit(row, col, False, 200, 3))
            space.add((row, col))


def print_game(elfs, goblins, space):
    elfs = position_of(elfs)
    goblins = position_of(goblins)
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


def get_with_fewest_hit_points(units):
    min_hit_point = min(units, key=lambda u: u.hp)
    units = list(filter(lambda u: u.hp == min_hit_point.hp, units))
    return sorted(units, key=lambda u: (u.hp, u.x, u.y))


print_game(elfs, goblins, space)
for _ in range(47):
    elf = set(filter(lambda u: u.is_alive(), elfs))
    goblins = set(filter(lambda u: u.is_alive(), goblins))

    units_in_range = set()
    for elf in elfs:
        for goblin in goblins:
            if in_range((elf.x, elf.y), {(goblin.x, goblin.y)}):
                units_in_range.add(elf)
                units_in_range.add(goblin)

    units_to_move = elfs | goblins
    units_to_move = units_to_move - units_in_range
    units_to_move = sort_by_reading_order(units_to_move)
    for current in units_to_move:
        if current in elfs:
            paths = shortest_paths(current, elfs, goblins, space)
            step = step_in_reading_order(paths)
            if step:
                current.x = step[0]
                current.y = step[1]
        else:
            paths = shortest_paths(current, goblins, elfs, space)
            step = step_in_reading_order(paths)
            if step:
                current.x = step[0]
                current.y = step[1]

    enemies = dict()
    for elf in elfs:
        for goblin in goblins:
            if in_range((elf.x, elf.y), {(goblin.x, goblin.y)}):
                e = enemies.get(elf, set())
                e.add(goblin)
                enemies[elf] = e
                e = enemies.get(goblin, set())
                e.add(elf)
                enemies[goblin] = e
    units_in_range = sort_by_reading_order(enemies.keys())
    for current in units_in_range:
        if not current.is_alive():
            continue

        for enemy in get_with_fewest_hit_points(enemies.get(current)):
            if not enemy.is_alive():
                continue
            enemy.hp -= current.attack
            print(current, enemy)

    elf = set(filter(lambda u: u.is_alive(), elfs))
    goblins = set(filter(lambda u: u.is_alive(), goblins))
    print_game(elfs, goblins, space)
