license = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

with open("./resources/day8.txt") as f:
    license = f.read().strip()


class Node:
    def __init__(self):
        self.children = []
        self.metadata = []
        self.value = None

    def total_metadata(self):
        total = sum(self.metadata)
        for child in self.children:
            total += child.total_metadata()
        return total

    def get_value(self):
        if self.value is None:
            if not self.children:
                self.value = sum(self.metadata)
            else:
                indices = [m for m in self.metadata if 0 < m <= len(self.children)]
                self.value = 0
                for i in indices:
                    self.value += self.children[i - 1].get_value()

        return self.value


def parse_node(numbers):
    num_of_children = numbers.pop(0)
    metadata_size = numbers.pop(0)
    node = Node()
    for _ in range(num_of_children):
        child = parse_node(numbers)
        node.children.append(child)
    for _ in range(metadata_size):
        node.metadata.append(numbers.pop(0))

    return node


def part1():
    root = parse_node(list(map(int, license.split(" "))))
    print(root.total_metadata())


def part2():
    root = parse_node(list(map(int, license.split(" "))))
    print(root.get_value())


part1()
part2()
