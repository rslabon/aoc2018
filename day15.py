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

lines1 = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""".strip().splitlines()

# zle
lines2 = """
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
""".strip().splitlines()

lines3 = """
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
""".strip().splitlines()

lines4 = """
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
""".strip().splitlines()

lines5 = """
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
""".strip().splitlines()

with open("resources/day15.txt") as f:
    lines = f.read().strip().splitlines()


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
        return f"{"E" if self.elf else "G"} ({self.hp}) [{self.x},{self.y}]"


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


def next_step(unit, heros, enemies, space):
    start = (unit.x, unit.y)
    heros_positions = position_of(heros)
    enemy_positions = position_of(enemies)
    targets = destinations(enemy_positions)
    free_space = space - heros_positions - enemy_positions
    q = []
    heapq.heapify(q)
    heapq.heappush(q, (0, start))
    prev = dict()
    cost = dict()
    prev[start] = None
    cost[start] = 0

    while q:
        _, (x, y) = heapq.heappop(q)
        if (x, y) in targets:
            current = (x, y)
            path = [current]
            while current:
                current = prev[current]
                if current:
                    path.append(current)
            return path[-2]

        for next in [(x + 1, y + 0), (x + 0, y + 1), (x + 0, y - 1), (x - 1, y + 0)]:
            if next not in free_space:
                continue
            if next not in cost or cost[(x, y)] + 1 < cost[next]:
                cost[next] = cost[(x, y)] + 1
                prev[next] = (x, y)
                heapq.heappush(q, (cost[next], next))

    return None


def step_in_reading_order(paths):
    if not paths:
        return None

    paths = list(paths)
    last_step = min(map(lambda p: p[-1][0] * 10_000 + p[-1][1], paths))
    paths_with_last_step = list(filter(lambda p: p[-1][0] * 10_000 + p[-1][1] == last_step, paths))
    first_step = min(map(lambda p: p[0][0] * 10_000 + p[0][1], paths_with_last_step))
    return first_step // 10_000, first_step % 10_000


def parse(lines):
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

    return elfs, goblins, space


def get_alive_with_fewest_hit_points(units):
    live_units = list(filter(lambda u: u.is_alive(), units))
    if not live_units:
        return None
    min_hit_point = min(live_units, key=lambda u: u.hp)
    min_hp_live_units = list(filter(lambda u: u.hp == min_hit_point.hp, live_units))
    return sort_by_reading_order(min_hp_live_units)[0]


def get_surrounded_by(current, enemies):
    x = current.x
    y = current.y
    enemy_positions = dict(map(lambda e: ((e.x, e.y), e), enemies))
    current_enemies = []
    for dx, dy in [(-1, 0), (0, 1), (0, -1), (1, 0)]:
        if (x + dx, y + dy) in enemy_positions:
            current_enemies.append(enemy_positions.get((x + dx, y + dy)))

    return current_enemies


def play_game(elfs, goblins, space):
    number_elfs_at_start = len(elfs)
    round = 0
    while True:
        elfs = set(filter(lambda u: u.is_alive(), elfs))
        goblins = set(filter(lambda u: u.is_alive(), goblins))
        units = elfs | goblins
        units = sort_by_reading_order(units)
        for current in units:
            if not current.is_alive():
                continue
            units = set(filter(lambda u: u.is_alive(), units))
            heros = set(filter(lambda u: current.elf == u.elf, units))
            enemies = set(filter(lambda u: current.elf != u.elf, units))
            if len(enemies) == 0:
                outcome = round * (sum(map(lambda u: u.hp, heros)) + sum(map(lambda u: u.hp, enemies)))
                live_elfs = set(filter(lambda u: u.is_alive(), elfs))
                return outcome, len(live_elfs) == number_elfs_at_start

            if not get_surrounded_by(current, enemies):
                step = next_step(current, heros, enemies, space)
                if step:
                    current.x = step[0]
                    current.y = step[1]
            targets = get_surrounded_by(current, enemies)
            target = get_alive_with_fewest_hit_points(targets)
            if target:
                target.hp -= current.attack

        round += 1


def find_outcome(lines):
    elfs, goblins, space = parse(lines)
    return play_game(elfs, goblins, space)


assert find_outcome(lines1)[0] == 27730
assert find_outcome(lines2)[0] == 36334
assert find_outcome(lines3)[0] == 27755
assert find_outcome(lines4)[0] == 28944
assert find_outcome(lines5)[0] == 18740


def part1():
    print(find_outcome(lines)[0])


def part2():
    attack = 4
    while True:
        elfs, goblins, space = parse(lines)
        for elf in elfs:
            elf.attack = attack

        outcome, every_elf_survive = play_game(elfs, goblins, space)
        if every_elf_survive:
            print(outcome)
            break
        attack += 1


part1()
part2()
