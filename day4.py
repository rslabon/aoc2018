import re
from datetime import datetime

lines = """
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
""".strip().splitlines()

with open('./resources/day4.txt', 'r') as f:
    lines = f.read().strip().splitlines()

date_format = "%Y-%m-%d %H:%M"

entries = []
for line in lines:
    timestamp, text = re.findall(r"\[(.+)] (.+)", line)[0]
    dt = datetime.strptime(timestamp, date_format)
    entries.append((dt, text))

entries.sort(key=lambda e: e[0])

guards = []
events = []
for (timestamp, text) in entries:
    if "begins shift" in text:
        events = []
        id = re.findall(r"Guard #(\d+) begins shift", text)[0]
        events.append((timestamp, "start"))
        guards.append((id, events))
    elif "falls asleep" in text:
        events.append((timestamp, "sleep"))
    elif "wakes up" in text:
        events.append((timestamp, "wakes"))

total_sleep_minutes = dict()
stats = dict()
for id, events in guards:
    prev_type = "start"
    start = None
    end = None
    for event in events:
        dt, type = event
        if prev_type == type:
            continue
        prev_type = type
        if type == "sleep":
            start = dt
            end = None
        elif type == "wakes" and start:
            end = dt
            duration = (end - start).total_seconds() // 60
            total_sleep_minutes[id] = total_sleep_minutes.get(id, 0) + duration
            for minute in range(start.minute, end.minute):
                minute_occurrences = stats.get(id, dict())
                minute_occurrences[minute] = minute_occurrences.get(minute, 0) + 1
                stats[id] = minute_occurrences
            start = None


def part1():
    max_id = None
    max_sleep = float("-inf")
    for id, minutes in total_sleep_minutes.items():
        if minutes > max_sleep:
            max_id = id
            max_sleep = minutes

    max_minute = None
    max_occurrences = float("-inf")
    for minute, occurrences in stats[max_id].items():
        if occurrences > max_occurrences:
            max_occurrences = occurrences
            max_minute = minute

    print(int(max_id) * max_minute)


def part2():
    max_occurrences = float("-inf")
    max_id = None
    max_minute = None
    for id, minute_occurrences in stats.items():
        for minute, occurrences in minute_occurrences.items():
            if occurrences > max_occurrences:
                max_occurrences = occurrences
                max_id = id
                max_minute = minute

    print(int(max_id) * max_minute)


part1()
part2()
