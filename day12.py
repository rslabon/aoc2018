block1, block2 = """
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
""".strip().split("\n\n")

with open("./resources/day12.txt") as f:
    block1, block2 = f.read().strip().split("\n\n")

state = block1.replace("initial state: ", "")
margin = 50
state = "." * margin + state + "." * margin
patterns = dict()
for line in block2.splitlines():
    pattern, s = line.split(" => ")
    patterns[pattern] = s


def part1(state):
    for _ in range(20):
        idx = 0
        new_state = list("." * len(state))
        while idx < len(state) - 5:
            p = "".join(state[idx: idx + 5])
            new_state[idx + 2] = patterns[p]
            idx += 1
        state = "".join(new_state)

    total = 0
    for i, c in enumerate(state):
        if c == "#":
            total += i - margin

    print(total)


def part2(state):
    generations = 50000000000
    for _ in range(generations):
        idx = 0
        prev = state
        new_state = list("." * len(state))
        while idx < len(state) - 5:
            p = "".join(state[idx: idx + 5])
            new_state[idx + 2] = patterns.get(p, ".")
            idx += 1
        new_state = new_state[1:] + ["."]
        state = "".join(new_state)
        if prev == state:
            break

    total = 0
    for i, c in enumerate(state):
        if c == "#":
            total += generations + i - margin

    print(total)


part1(state)
part2(state)
