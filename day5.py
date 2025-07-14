polymers = "dabAcCaCBAcCcaDA"

with open("./resources/day5.txt") as f:
    polymers = f.read().strip()


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.previous = None

    def append(self, other_node):
        self.next = other_node
        other_node.previous = self
        return other_node

    def remove(self):
        next = self.next
        previous = self.previous
        if previous:
            previous.next = next
        if next:
            next.previous = previous

        self.next = None
        self.previous = None

    def __repr__(self):
        return f"[{self.value}]"


def reduce(polymers):
    start = None
    current = None
    for p in polymers:
        if not current:
            current = Node(p)
            start = current
        else:
            current = current.append(Node(p))

    left = start
    right = left.next
    deleted = 0
    while left != right and left and right:
        if left.value.lower() == right.value.lower() and left.value != right.value:
            d1, d2 = left, right
            if not left.previous:
                left = right.next
                right = left.next if left else None
            elif not right.next:
                right = left.previous
                left = right.previous if right else None
            else:
                left = left.previous
                right = right.next
            d1.remove()
            d2.remove()
            deleted += 2
        else:
            left = left.next
            right = right.next

    return deleted


def remove(line, c):
    return line.replace(c.lower(), "").replace(c.upper(), "")


def part1():
    print(len(polymers) - reduce(polymers))


def part2():
    min_length = float("inf")
    for char in range(ord('a'), ord('z') + 1):
        new_polymer = remove(polymers, chr(char))
        min_length = min(len(new_polymer) - reduce(new_polymer), min_length)
    print(min_length)


part1()
part2()
