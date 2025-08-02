DEBUG = True


def addr(registers, A, B, C):
    before = registers[:]
    registers[C] = registers[A] + registers[B]
    if DEBUG:
        print(f"ADD into {C} = {before[A]}[R={A}] + {before[B]}[R={B}] = {registers[C]}")
        # if A == 0 or B == 0:
        #     raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def addi(registers, A, B, C):
    before = registers[:]
    registers[C] = registers[A] + B
    if DEBUG:
        print(f"ADD into {C} = {before[A]}[R={A}] + {B} = {registers[C]}")
        if C == 5:
            print(f"IP={registers[5]}")


def mulr(registers, A, B, C):
    before = registers[:]
    registers[C] = registers[A] * registers[B]
    if DEBUG:
        print(f"MUL into {C} = {before[A]}[R={A}] * {before[B]}[R={B}] = {registers[C]}")
        # if A == 0 or B == 0:
        #     raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def muli(registers, A, B, C):
    before = registers[:]
    registers[C] = registers[A] * B
    if DEBUG:
        print(f"MUL into {C} = {before[A]}[R={A}] * {B} = {registers[C]}")
        # if A == 0:
        #     raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def banr(registers, A, B, C):
    before = registers[:]
    registers[C] = registers[A] & registers[B]
    if DEBUG:
        print(f"AND into {C} = {before[A]}[R={A}] & {before[B]}[R={B}] = {registers[C]}")
        # if A == 0 or B == 0:
        #     raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def bani(registers, A, B, C):
    before = registers[:]
    registers[C] = registers[A] & B
    if DEBUG:
        print(f"AND into {C} = {before[A]}[R={A}] & {B} = {registers[C]}")
        # if A == 0:
        #     raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def borr(registers, A, B, C):
    before = registers[:]
    registers[C] = registers[A] | registers[B]
    if DEBUG:
        print(f"OR into {C} = {before[A]}[R={A}] | {before[B]}[R={B}] = {registers[C]}")
        # if A == 0 or B == 0:
        #     raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def bori(registers, A, B, C):
    before = registers[:]
    registers[C] = registers[A] | B
    if DEBUG:
        print(f"OR into {C} = {before[A]}[R={A}] | {B} = {registers[C]}")
        # if A == 0:
        #     raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def setr(registers, A, B, C):
    before = registers[:]
    registers[C] = registers[A]
    if DEBUG:
        print(f"SET into {C} = {before[A]}[R={A}]")
        # if A == 0:
        #     raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def seti(registers, A, B, C):
    registers[C] = A
    if DEBUG:
        print(f"SET into {C} = {A}")
        if C == 5:
            print(f"IP={registers[5]}")


def gtir(registers, A, B, C):
    before = registers[:]
    registers[C] = 1 if A > registers[B] else 0
    if DEBUG:
        print(f"{C} = if {A} > {before[B]}[R={B}] 1 else 0 = {registers[C]}")
        # if B == 0:
        #     raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def gtri(registers, A, B, C):
    before = registers[:]
    registers[C] = 1 if registers[A] > B else 0
    if DEBUG:
        print(f"{C} = if {before[A]}[R={A}] > {B} 1 else 0 = {registers[C]}")
        # if A == 0:
        #     raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def gtrr(registers, A, B, C):
    before = registers[:]
    registers[C] = 1 if registers[A] > registers[B] else 0
    if DEBUG:
        print(f"{C} = if {before[A]}[R={A}] > {before[B]}[R={B}] 1 else 0 = {registers[C]}")
        # if A == 0 or B == 0:
        #     raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def eqir(registers, A, B, C):
    before = registers[:]
    registers[C] = 1 if A == registers[B] else 0
    if DEBUG:
        print(f"{C} = if {A} == {before[B]}[R={B}] 1 else 0 = {registers[C]}")
        # if B == 0:
        #     raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def eqri(registers, A, B, C):
    before = registers[:]
    registers[C] = 1 if registers[A] == B else 0
    if DEBUG:
        print(f"{C} = if {before[A]}[R={A}] == {B} 1 else 0 = {registers[C]}")
        # if A == 0:
        #     raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def eqrr(registers, A, B, C):
    before = registers[:]
    registers[C] = 1 if registers[A] == registers[B] else 0
    if DEBUG:
        print(f"{C} = if {before[A]}[R={A}] == {before[B]}[R={B}] 1 else 0 = {registers[C]}")
        # if A == 0 or B == 0:
        #     raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


executed = 0


def execute(instructions, registers):
    ip_instruction = instructions[0]
    _, bound = ip_instruction.split(" ")
    bound = int(bound)
    ip = 0
    instructions = instructions[1:]

    after_check = False
    total = 0
    while 0 <= ip < len(instructions):
        registers[bound] = ip
        instruction = instructions[ip]
        op_name, *args = instruction.split(" ")
        before = registers[:]
        if DEBUG: print(instruction)
        args = map(int, args)

        if op_name == "addr":
            addr(registers, *args)
        if op_name == "addi":
            addi(registers, *args)
        if op_name == "mulr":
            mulr(registers, *args)
        if op_name == "muli":
            muli(registers, *args)
        if op_name == "banr":
            banr(registers, *args)
        if op_name == "bani":
            bani(registers, *args)
        if op_name == "borr":
            borr(registers, *args)
        if op_name == "bori":
            bori(registers, *args)
        if op_name == "setr":
            setr(registers, *args)
        if op_name == "seti":
            seti(registers, *args)
        if op_name == "gtir":
            gtir(registers, *args)
        if op_name == "gtri":
            gtri(registers, *args)
        if op_name == "gtrr":
            gtrr(registers, *args)
        if op_name == "eqir":
            eqir(registers, *args)
        if op_name == "eqri":
            eqri(registers, *args)
        if op_name == "eqrr":
            eqrr(registers, *args)
            if registers[3] == 1 and registers[2] == registers[0]:
                after_check = True

        # print(f"ip={ip} {before} {instruction} {registers}")

        ip = registers[bound] + 1
        total += 1

        if total > 2000 and not after_check:
            return 0

    return total


with open("./resources/day21.txt") as f:
    instructions = [line.strip() for line in f.readlines()]


def check(i):
    registers = [i, 0, 0, 0, 0, 0]
    return execute(instructions, registers)


# DEBUG = True
DEBUG = False

def simulate():
    seen = set()
    last = None

    r2 = 0
    while True:
        r4 = r2 | 65536
        r2 = 6718165

        while True:
            r2 = (((r2 + (r4 & 255)) & 16777215) * 65899) & 16777215
            if r4 < 256:
                break
            r4 //= 256

        if r2 in seen:
            return last
        seen.add(r2)
        last = r2


def part1():
    print(check(30842))


def part2():
    print(simulate()) # copilot help


part1()
part2()
