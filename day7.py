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


class Worker:
    def __init__(self, name):
        self.name = name
        self.time = 0
        self.step = None

    def is_available(self):
        return self.time == 0

    def take_step(self):
        self.time = 0
        step = self.step
        self.step = None
        return step

    def give_step(self, step, time):
        self.step = step
        self.time = time

    def __repr__(self):
        return f'{self.name} - {self.time}s - {self.step}'


times = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "I": 9,
    "J": 10,
    "K": 11,
    "L": 12,
    "M": 13,
    "N": 14,
    "O": 15,
    "P": 16,
    "Q": 17,
    "R": 18,
    "S": 19,
    "T": 20,
    "U": 21,
    "V": 22,
    "W": 23,
    "X": 24,
    "Y": 25,
    "Z": 26,
}

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


def tick(workers):
    for worker in workers:
        if worker.time > 0:
            worker.time -= 1


def get_free_worker(workers):
    for worker in workers:
        if worker.is_available():
            return worker
    return None


def get_finished_workers(workers):
    return [worker for worker in workers if worker.time == 0 and worker.step]


def has_busy_workers(workers):
    return len([worker for worker in workers if worker.step]) > 0


def traverse_with_workers(available, seen, workers, clock):
    if not available and not has_busy_workers(workers):
        return clock

    tick(workers)
    clock += 1
    for finished_worker in get_finished_workers(workers):
        step = finished_worker.take_step()
        seen.add(step)
        for next_step in step.next:
            if seen.issuperset(next_step.required):
                available = set(available) | {next_step}

    available = sorted(available, key=lambda n: n.name)
    if not available and has_busy_workers(workers):
        return traverse_with_workers(available, seen, workers, clock)

    while available:
        step = available[0]
        worker = get_free_worker(workers)
        if not worker:
            return traverse_with_workers(available, seen, workers, clock)

        available.pop(0)
        if step in seen:
            continue

        worker.give_step(step, times[step.name] + 60)

    return traverse_with_workers(available, seen, workers, clock)


def part1():
    sources = list(sorted(filter(lambda n: len(n.required) == 0, nodes.values()), key=lambda n: n.name))
    path = []
    seen = set()
    traverse(sources, path, seen)
    print("".join([n.name for n in path]))


def part2():
    sources = list(sorted(filter(lambda n: len(n.required) == 0, nodes.values()), key=lambda n: n.name))
    seen = set()
    workers = [Worker("1"), Worker("2"), Worker("3"), Worker("4"), Worker("5")]
    clock = traverse_with_workers(sources, seen, workers, -1)
    print(clock)


part1()
part2()
