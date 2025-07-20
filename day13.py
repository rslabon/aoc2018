from enum import Enum

lines = """
/->-\\        
|   |  /----\\
| /-+--+-\\  |
| | |  | v  |
\\-+-/  \\-+--/
  \\------/   
""".strip().splitlines()

lines = """
/>-<\\  
|   |  
| /<+-\\
| | | v
\\>+</ |
  |   ^
  \\<->/
""".strip().splitlines()

with open("./resources/day13.txt") as f:
    lines = f.read().splitlines()


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    STRAIGHT = 4


class Cart:
    def __init__(self, row, col, dir):
        self.col = col
        self.row = row
        self.dir = dir
        self.intersection = Direction.LEFT

    def move(self, grid):
        if self.dir == Direction.LEFT:
            self.col -= 1
        if self.dir == Direction.RIGHT:
            self.col += 1
        if self.dir == Direction.UP:
            self.row -= 1
        if self.dir == Direction.DOWN:
            self.row += 1

        current = grid[(self.row, self.col)]

        if current == "/" and self.dir == Direction.UP:
            self.dir = Direction.RIGHT
        elif current == "/" and self.dir == Direction.LEFT:
            self.dir = Direction.DOWN
        elif current == "/" and self.dir == Direction.RIGHT:
            self.dir = Direction.UP
        elif current == "/" and self.dir == Direction.DOWN:
            self.dir = Direction.LEFT

        elif current == "\\" and self.dir == Direction.UP:
            self.dir = Direction.LEFT
        elif current == "\\" and self.dir == Direction.RIGHT:
            self.dir = Direction.DOWN
        elif current == "\\" and self.dir == Direction.DOWN:
            self.dir = Direction.RIGHT
        elif current == "\\" and self.dir == Direction.LEFT:
            self.dir = Direction.UP

        elif current == "+" and self.dir == Direction.LEFT and self.intersection == Direction.LEFT:
            self.dir = Direction.DOWN
            self.intersection = Direction.STRAIGHT
        elif current == "+" and self.dir == Direction.LEFT and self.intersection == Direction.RIGHT:
            self.dir = Direction.UP
            self.intersection = Direction.LEFT

        elif current == "+" and self.dir == Direction.RIGHT and self.intersection == Direction.LEFT:
            self.dir = Direction.UP
            self.intersection = Direction.STRAIGHT
        elif current == "+" and self.dir == Direction.RIGHT and self.intersection == Direction.RIGHT:
            self.dir = Direction.DOWN
            self.intersection = Direction.LEFT

        elif current == "+" and self.dir == Direction.UP and self.intersection == Direction.LEFT:
            self.dir = Direction.LEFT
            self.intersection = Direction.STRAIGHT
        elif current == "+" and self.dir == Direction.UP and self.intersection == Direction.RIGHT:
            self.dir = Direction.RIGHT
            self.intersection = Direction.LEFT

        elif current == "+" and self.dir == Direction.DOWN and self.intersection == Direction.LEFT:
            self.dir = Direction.RIGHT
            self.intersection = Direction.STRAIGHT
        elif current == "+" and self.dir == Direction.DOWN and self.intersection == Direction.RIGHT:
            self.dir = Direction.LEFT
            self.intersection = Direction.LEFT

        elif current == "+" and self.intersection == Direction.STRAIGHT:
            self.intersection = Direction.RIGHT

    def __repr__(self):
        return f"Cart({self.col}, {self.row}, {self.dir})"


def parse():
    grid = dict()
    carts = []
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if not c.strip():
                continue
            if c == "v":
                carts.append(Cart(row, col, Direction.DOWN))
            elif c == "^":
                carts.append(Cart(row, col, Direction.UP))
            elif c == ">":
                carts.append(Cart(row, col, Direction.RIGHT))
            elif c == "<":
                carts.append(Cart(row, col, Direction.LEFT))
            grid[(row, col)] = c

    return grid, carts


def part1():
    grid, carts = parse()
    while True:
        carts = sorted(carts, key=lambda c: (c.col, c.row))
        current = set([(cart.row, cart.col) for cart in carts])
        for cart in carts:
            current.remove((cart.row, cart.col))
            cart.move(grid)
            if (cart.row, cart.col) in current:
                print(f"{cart.col},{cart.row}")
                return
            else:
                current.add((cart.row, cart.col))


def part2():
    grid, carts = parse()
    crashed = set()
    while True:
        carts = set(carts) - crashed
        carts = sorted(carts, key=lambda c: (c.col, c.row))
        current = set([(cart.row, cart.col) for cart in carts])
        for cart in carts:
            if len(carts) == 1:
                print(f"{cart.col},{cart.row}")
                return
            current.remove((cart.row, cart.col))
            cart.move(grid)
            if (cart.row, cart.col) in current:
                crashed |= set([c for c in carts if (c.row, c.col) == (cart.row, cart.col)])
            else:
                current.add((cart.row, cart.col))


part1()
part2()
