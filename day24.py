import re
import sys

lines = """    
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""".strip()

with open('./resources/day24.txt', 'r') as f:
    lines = f.read().strip()


class Group:
    def __init__(self, army, nr, units, hit_points, attack_damage, attack_type, initiative, weaknesses, immunities):
        self.army = army
        self.nr = nr
        self.units = units
        self.hit_points = hit_points
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities

    def effective_power(self):
        return self.units * self.attack_damage

    def selection_priority(self):
        return (-self.effective_power(), -self.initiative)

    def is_dead(self):
        return self.units <= 0

    def receive_damage(self, damage):
        max_damage = self.units * self.hit_points
        before = self.units
        if damage >= max_damage:
            self.units = 0
            return before
        else:
            self.units -= int(damage / self.hit_points)
            return before - self.units

    def compute_attack_damage(self, enemy_group):
        if self.is_dead() or enemy_group.is_dead():
            return 0
        damage = self.effective_power()
        if self.attack_type in enemy_group.weaknesses:
            damage *= 2
        elif self.attack_type in enemy_group.immunities:
            damage = 0
        return damage

    def __repr__(self):
        return f"{self.army} Group {self.nr}"


def select_target(group, groups):
    enemy_groups = list(filter(lambda g: g.army != group.army and g.units > 0, groups))
    result = []
    for enemy_group in enemy_groups:
        damage = group.compute_attack_damage(enemy_group)
        if damage <= 0:
            continue
        result.append((damage, enemy_group))
    result = sorted(result, key=lambda x: (-x[0], -x[1].effective_power(), -x[1].initiative))
    if result:
        return result[0][1]


def parse_groups():
    blocks = lines.split("\n\n")
    groups = set()
    army = None
    for block in blocks:
        for i, line in enumerate(block.splitlines()):
            if i == 0:
                army = line.replace(":", "").strip()
                continue
            units, hit_points, details, attack_damage, attack_type, initiative = re.findall(
                r"(\d+) units each with (\d+) hit points (\(.+\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)",
                line)[0]
            units = int(units)
            hit_points = int(hit_points)
            attack_damage = int(attack_damage)
            initiative = int(initiative)
            weaknesses = []
            immunities = []
            if details:
                parts = details.strip()[1:-1].split("; ")
                for part in parts:
                    if part.startswith("weak to "):
                        weaknesses = part[len("weak to "):].split(", ")
                    elif part.startswith("immune to "):
                        immunities = part[len("immune to "):].split(", ")

            groups.add(
                Group(army, i, units, hit_points, attack_damage, attack_type, initiative, weaknesses, immunities))

    return groups


def fight(groups):
    while True:
        selection = dict()
        selected = set()
        for group in sorted(groups, key=lambda g: g.selection_priority()):
            target = select_target(group, groups - selected)
            if target:
                selected.add(target)
                selection[group] = target

        if not selection:
            return -1

        attack = False
        for group in sorted(selection.keys(), key=lambda g: -g.initiative):
            enemy_group = selection[group]
            damage = group.compute_attack_damage(enemy_group)
            if group.units <= 0 or enemy_group.units <= 0:
                continue
            killed = enemy_group.receive_damage(damage)
            if killed > 0:
                attack = True

        if not attack:
            return -1

        dead_groups = [group for group in groups if group.is_dead()]
        for group in dead_groups:
            groups.remove(group)

        armies = set(map(lambda g: g.army, groups))
        if len(armies) == 1:
            return sum([g.units for g in groups])


def left_units_after_immune_won(boost):
    groups = parse_groups()
    for group in groups:
        if "Immune" in group.army:
            group.attack_damage += boost
    left = fight(groups)
    if left > 0 and "Immune" in groups.pop().army:
        return left

    return 0


def part1():
    groups = parse_groups()
    print(fight(groups))


def part2():
    step = 10000
    start = 1
    end = sys.maxsize
    left = None
    while True:
        for i in range(start, end, step):
            left = left_units_after_immune_won(i)
            if left > 0:
                end = i
                break
            else:
                start = i

        if step == 1:
            print(left)
            break

        step //= 10


# part1()
part2()
