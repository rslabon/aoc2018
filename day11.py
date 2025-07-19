max_x = 300
max_y = 300


def power_level(x, y, serial_number):
    rack_id = x + 1 + 10
    power = rack_id * (y + 1)
    power += serial_number
    power *= rack_id
    spower = str(power)
    if len(spower.strip()) < 3:
        power = 0
    else:
        power = int(spower[-3])
    return power - 5


serial_number = 6303
grid = []
for y in range(max_y):
    row = []
    grid.append(row)
    for x in range(max_x):
        row.append(power_level(x, y, serial_number))


def power_square(grid, x, y, square_size):
    power = 0
    for j in range(y, y + square_size):
        for i in range(x, x + square_size):
            power += grid[i][j]
    return power


def part1():
    square_size = 3
    max_power = float("-inf")
    max_power_x = None
    max_power_y = None
    for y in range(max_y - square_size - 1):
        for x in range(max_x - square_size - 1):
            power = power_square(grid, x, y, square_size)
            if power > max_power:
                max_power = power
                max_power_x = x + 1
                max_power_y = y + 1

    print(f"{max_power_y},{max_power_x}")


def part2():
    max_power = float("-inf")
    max_power_x = None
    max_power_y = None
    max_power_square_size = None
    no_change = 3
    for square_size in range(1, max_x + 1):
        prev = max_power
        for y in range(max_y - square_size - 1):
            for x in range(max_x - square_size - 1):
                power = power_square(grid, x, y, square_size)
                if power > max_power:
                    max_power = power
                    max_power_x = x + 1
                    max_power_y = y + 1
                    max_power_square_size = square_size
                    no_change = 3

        if prev == max_power:
            no_change -= 1
            if no_change == 0:
                break

    print(f"{max_power_y},{max_power_x},{max_power_square_size}")


part1()
part2()
