from collections import deque


class Node:
    def __init__(self):
        self.value = ""
        self.children = []
        self.leafs = []

    def leaf(self):
        if len(self.children) == 0:
            return [self]

        result = []
        for child in self.children:
            result += child.leaf()

        return result

    def __repr__(self):
        return f"Node({self.value})"


def leaf(node, seen=set()):
    if node.leafs:
        return node.leafs

    if node in seen:
        return []
    seen.add(node)

    if len(node.children) == 0:
        node.leafs = [node]
        return [node]

    result = []
    for child in node.children:
        result += leaf(child, seen)

    node.leafs = result

    return result


def find_closing_index(pattern):
    if not pattern:
        return None
    s = 0
    for i, c in enumerate(pattern):
        if c == "(":
            s += 1
        elif c == ")":
            s -= 1
        if s == 0:
            return i

    return None


def split_pattern(pattern):
    if not pattern:
        return []
    s = 0
    splits = []
    last_split = 0
    for i, c in enumerate(pattern):
        if c == "(":
            s += 1
        elif c == ")":
            s -= 1
        if s == 0 and c == "|":
            splits.append(pattern[last_split:i])
            last_split = i + 1

    if last_split >= 0:
        splits.append(pattern[last_split:])

    return splits


def parse_node(pattern, current, parent):
    while pattern:
        alternatives = split_pattern(pattern)
        if len(alternatives) == 1:
            if pattern[0] in ["E", "W", "S", "N"]:
                direction = pattern.pop(0)
                current.value += direction
            elif pattern and pattern[0] == '(':
                end_index = find_closing_index(pattern)
                if end_index is None:
                    raise RuntimeError(f"Invalid pattern: {pattern}")
                inner_pattern = pattern[1:end_index]
                pattern = pattern[end_index + 1:]
                parse_node(inner_pattern, None, current)
                if pattern:
                    rest_node = Node()
                    tmp_parent = Node()
                    tmp_parent.children.append(rest_node)
                    parse_node(pattern, rest_node, tmp_parent)
                    for leaf in current.leaf():
                        leaf.children += tmp_parent.children
                    pattern = []
            if not current.value and current.children:
                parent.children.remove(current)
                parent.children += current.children
        else:
            for alternative_pattern in alternatives:
                sibling = Node()
                parent.children.append(sibling)
                parse_node(alternative_pattern, sibling, parent)
            return


def fill_grid(grid, node, x=0, y=0, seen=set()):
    if node in seen:
        return
    seen.add(node)

    for d in node.value:
        if d == "E":
            grid[(x + 1, y)] = "|"
            grid[(x + 2, y)] = "."
            x += 2
        elif d == "W":
            grid[(x - 1, y)] = "|"
            grid[(x - 2, y)] = "."
            x -= 2
        elif d == "N":
            grid[(x, y - 1)] = "-"
            grid[(x, y - 2)] = "."
            y -= 2
        elif d == "S":
            grid[(x, y + 1)] = "-"
            grid[(x, y + 2)] = "."
            y += 2
    for child in node.children:
        fill_grid(grid, child, x, y)


def manhatan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_furthest_with_max_doors(grid):
    q = deque([(0, 0, set(), 0, 0)])
    stats = dict()
    while q:
        x, y, seen, doors, rooms = q.popleft()
        if (x, y) not in stats and grid[(x, y)] == ".":
            stats[(x, y)] = ((x, y), rooms, doors)
        elif (x, y) in stats and doors > stats[(x, y)][-1]:
            stats[(x, y)] = ((x, y), rooms, doors)

        if (x, y) in seen:
            continue
        seen.add((x, y))
        if (x, y) not in grid:
            continue
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            xx = x + dx
            yy = y + dy
            if (xx, yy) not in grid:
                continue
            if (xx, yy) in seen:
                continue
            if grid[(xx, yy)] in ["|", "-"]:
                door = 1
                room = 0
            else:
                door = 0
                room = 1
            q.append((xx, yy, set(seen), doors + door, rooms + room))

    sorted_stats = sorted(map(lambda x: (x[1][-1], manhatan_distance((0, 0), x[0])), stats.items()), reverse=True)
    return sorted_stats[0][0]


def print_grid(grid):
    minx = min(map(lambda k: k[0], grid.keys()))
    maxx = max(map(lambda k: k[0], grid.keys()))
    miny = min(map(lambda k: k[1], grid.keys()))
    maxy = max(map(lambda k: k[1], grid.keys()))
    grid[(0, 0)] = "X"
    for y in range(miny - 1, maxy + 2):
        for x in range(minx - 1, maxx + 2):
            if (x, y) not in grid:
                print("#", end="")
            else:
                print(grid[(x, y)], end="")
        print()
    print()


# pattern = "ENWWW(NEEE|SSE(EE|N))"
# pattern = "ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN"
# pattern = "ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))"
# pattern = "WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))"
# pattern = "W(S|N)(EE|WW)(S|N)"
with open("./resources/day20.txt") as f:
    pattern = f.read().strip()
    pattern = pattern[1:-1]


def part1():
    root = Node()
    parse_node(list(pattern), root, None)
    grid = {(0, 0): "X"}
    fill_grid(grid, root)
    print(find_furthest_with_max_doors(grid))
    # print_grid(grid)


part1()
