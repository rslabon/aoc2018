class Marble:
    def __init__(self, nr):
        self.nr = nr
        self.next = None
        self.prev = None

    def add_next(self, next):
        self.next = next.next
        next.next = self
        self.prev = next
        self.next.prev = self

    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.next = None
        self.prev = None

    def left(self, n):
        current = self
        while n > 0:
            current = current.prev
            n -= 1
        return current

    def __repr__(self):
        return f"{self.nr}"


def play(num_of_players, end_marble):
    scores = []
    for _ in range(num_of_players):
        scores.append(0)
    nr = 0
    current_marble = Marble(nr)
    current_marble.next = current_marble
    current_marble.prev = current_marble
    player = -1
    while nr < end_marble:
        player = (player + 1) % num_of_players
        nr += 1
        if nr % 23 == 0:
            scores[player] += nr
            to_remove = current_marble.left(7)
            scores[player] += to_remove.nr
            current_marble = to_remove.next
            to_remove.remove()
        else:
            marble = Marble(nr)
            current_marble = current_marble.next
            marble.add_next(current_marble)
            current_marble = marble

    return max(scores)


def part1():
    print(play(458, 71307))


def part2():
    print(play(458, 71307 * 100))


part1()
part2()
