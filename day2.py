from collections import Counter

with open("./resources/day2.txt") as f:
    lines = f.read().strip().splitlines()


def part1():
    two_count = 0
    three_count = 0
    for line in lines:
        c = Counter(line)
        if 2 in c.values():
            two_count += 1
        if 3 in c.values():
            three_count += 1

    print(two_count * three_count)


def part2():
    i = 0
    while i < len(lines):
        j = i + 1
        while j < len(lines):
            line = list(lines[i])
            other = list(lines[j])
            k = 0
            diff = 0
            while k < len(other):
                if line[k] != other[k]:
                    diff += 1
                if diff > 1:
                    break
                k += 1
            j += 1
            if diff == 1:
                k = 0
                while k < len(other):
                    if line[k] != other[k]:
                        break
                    k += 1
                print("".join(line[0:k] + line[k + 1:]))
                return
        i += 1


part1()
part2()
