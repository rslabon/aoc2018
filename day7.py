import re

lines = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""".strip().splitlines()

with open("./resources/day7.txt") as f:
    lines = f.read().strip().splitlines()


class Step:
    def __init__(self, name):
        self.name = name
        self.required = set()
        self.next = set()

    def add_step(self, other_node):
        self.next.add(other_node)
        other_node.required.add(self)

    def __repr__(self):
        return f'{self.name}'


nodes = dict()

for line in lines:
    first, second = re.findall(r"Step (\w+) must be finished before step (\w+) can begin.", line)[0]
    first_node = nodes.get(first, Step(first))
    second_node = nodes.get(second, Step(second))
    nodes[first] = first_node
    nodes[second] = second_node
    first_node.add_step(second_node)


def traverse(available, path, seen):
    available = sorted(available, key=lambda n: n.name)
    if not available:
        return

    step = available.pop(0)
    if step in seen:
        return

    seen.add(step)
    path.append(step)

    for next_step in step.next:
        if seen.issuperset(next_step.required):
            available = set(available) | {next_step}
    traverse(available, path, seen)


def part1():
    sources = list(sorted(filter(lambda n: len(n.required) == 0, nodes.values()), key=lambda n: n.name))
    path = []
    seen = set()
    traverse(sources, path, seen)
    print("".join([n.name for n in path]))


part1()
