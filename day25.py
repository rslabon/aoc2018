lines = """
0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0
""".strip().splitlines()

with open("./resources/day25.txt") as f:
    lines = f.read().strip().splitlines()

points = []
for line in lines:
    vals = line.strip().split(",")
    if len(vals) == 4:
        points.append(tuple(int(v) for v in vals))


def manhatann_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2]) + abs(p1[3] - p2[3])


i = 0
constellations = set()
while i < len(points):
    j = i + 1
    while j < len(points):
        distance = manhatann_distance(points[i], points[j])
        if distance <= 3:
            constellations.add(frozenset({i, j}))
        else:
            constellations.add(frozenset({i}))
            constellations.add(frozenset({j}))

        j += 1
    i += 1

i = 0
while i < len(points):
    to_merge = [c for c in constellations if i in c]
    remain = [c for c in constellations if i not in c]
    merge = set()
    for v in to_merge:
        merge |= v
    constellations = []
    if merge:
        constellations.append(merge)
    if remain:
        constellations.extend(remain)
    i += 1

print(len(constellations))
