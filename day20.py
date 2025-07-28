class Node:
    def __init__(self):
        self.value = ""
        self.children = []

    def leaf(self):
        if len(self.children) == 0:
            return [self]

        result = []
        for child in self.children:
            result += child.leaf()

        return result

    def __repr__(self):
        return f"Node({self.value})"


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


# def xxx():
#     lines = """
#     ESSWWN E
#     ESSWWN NNENN EESS WNSE SSS
#     ESSWWN NNENN EESS SSS
#     ESSWWN NNENN WWWSSSSE SW
#     ESSWWN NNENN WWWSSSSE NNNE
#     """.strip().splitlines()
#
#     grid = {(0, 0): "X"}
#     for line in lines:
#         x, y = 0, 0
#         for c in line:
#             if c == "E":
#                 grid[(x + 1, y)] = "|"
#                 grid[(x + 2, y)] = "."
#                 x += 2
#             elif c == "W":
#                 grid[(x - 1, y)] = "|"
#                 grid[(x - 2, y)] = "."
#                 x -= 2
#             elif c == "N":
#                 grid[(x, y - 1)] = "-"
#                 grid[(x, y - 2)] = "."
#                 y -= 2
#             elif c == "S":
#                 grid[(x, y + 1)] = "-"
#                 grid[(x, y + 2)] = "."
#                 y += 2
#
#         grid[(0, 0)] = "X"
#         print_grid(grid)
#
#     return grid


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
                inner_node = Node()
                current.children.append(inner_node)
                pattern = pattern[end_index + 1:]
                parse_node(inner_pattern, inner_node, current)
                for child in current.children:
                    if not child.value and not child.children:
                        current.children.remove(child)
                if pattern:
                    rest_node = Node()
                    tmp_parent = Node()
                    tmp_parent.children.append(rest_node)
                    parse_node(pattern, rest_node, tmp_parent)
                    for leaf in current.leaf():
                        leaf.children += tmp_parent.children
                    pattern = []
            elif pattern and pattern[0] == ')':
                pattern.pop(0)
        else:
            if not current.value and not current.children:
                parent.children.remove(current)
            for alternative_pattern in alternatives:
                sibling = Node()
                parent.children.append(sibling)
                parse_node(alternative_pattern, sibling, parent)
            return


def fill_grid(grid, node, x=0, y=0):
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


def print_grid(grid):
    minx = min(map(lambda k: k[0], grid.keys()))
    maxx = max(map(lambda k: k[0], grid.keys()))
    miny = min(map(lambda k: k[1], grid.keys()))
    maxy = max(map(lambda k: k[1], grid.keys()))
    grid[(0,0)] = "X"
    for row in range(minx - 1, maxx + 2):
        for col in range(miny - 1, maxy + 2):
            if (col, row) not in grid:
                print("#", end="")
            else:
                print(grid[(col, row)], end="")
        print()
    print()


pattern = "ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN"
pattern = "ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))"
pattern = "WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))"
pattern = "W(S|N)(EE|WW)(S|N)"
# with open("./resources/day20.txt") as f:
#     pattern = f.read().strip()
#     pattern = pattern[1:-1]

root = Node()
parse_node(list(pattern), root, None)
print("PARSED!!!!")
grid = {(0, 0): "X"}
fill_grid(grid, root)
print("FILLED!!!!")
print_grid(grid)
