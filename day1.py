with open("./resources/day1.txt") as f:
    lines = f.read().strip().splitlines()


def part1():
    total = 0
    for line in lines:
        total += int(line)

    print(total)


def part2():
    seen = set()
    total = 0
    seen.add(total)
    index = 0
    while True:
        value = int(lines[index])
        total += value
        if total in seen:
            print(total)
            break
        seen.add(total)
        index = (index + 1) % len(lines)


part1()
part2()
