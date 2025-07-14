polymers = "dabAcCaCBAcCcaDA"

with open("./resources/day5.txt") as f:
    polymers = f.read().strip()


def reduce(polymers):
    stack = []
    for p in polymers:
        if not stack:
            stack.append(p)
            continue
        elif stack[-1].lower() == p.lower() and stack[-1] != p:
            stack.pop()
        else:
            stack.append(p)

    return len(stack)


def remove(line, c):
    return line.replace(c.lower(), "").replace(c.upper(), "")


def part1():
    print(reduce(polymers))


def part2():
    min_length = float("inf")
    for char in range(ord('a'), ord('z') + 1):
        new_polymer = remove(polymers, chr(char))
        min_length = min(reduce(new_polymer), min_length)
    print(min_length)


part1()
part2()
