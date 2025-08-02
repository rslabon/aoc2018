import random

DEBUG = True

def addr(registers, A, B, C):
    registers[C] = registers[A] + registers[B]
    if DEBUG:
        print(f"ADD into {C} = {registers[A]}[R={A}] + {registers[B]}[R={B}] = {registers[C]}")
        if A == 0 or B == 0:
            raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def addi(registers, A, B, C):
    registers[C] = registers[A] + B
    if DEBUG:
        print(f"ADD into {C} = {registers[A]}[R={A}] + {B} = {registers[C]}")
        if C == 5:
            print(f"IP={registers[5]}")


def mulr(registers, A, B, C):
    registers[C] = registers[A] * registers[B]
    if DEBUG:
        print(f"MUL into {C} = {registers[A]}[R={A}] * {registers[B]}[R={B}] = {registers[C]}")
        if A == 0 or B == 0:
            raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def muli(registers, A, B, C):
    registers[C] = registers[A] * B
    if DEBUG:
        print(f"MUL into {C} = {registers[A]}[R={A}] * {B} = {registers[C]}")
        if A == 0:
            raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def banr(registers, A, B, C):
    registers[C] = registers[A] & registers[B]
    if DEBUG:
        print(f"AND into {C} = {registers[A]}[R={A}] & {registers[B]}[R={B}] = {registers[C]}")
        if A == 0 or B == 0:
            raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def bani(registers, A, B, C):
    registers[C] = registers[A] & B
    if DEBUG:
        print(f"AND into {C} = {registers[A]}[R={A}] & {B} = {registers[C]}")
        if A == 0:
            raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def borr(registers, A, B, C):
    registers[C] = registers[A] | registers[B]
    if DEBUG:
        print(f"OR into {C} = {registers[A]}[R={A}] | {registers[B]}[R={B}] = {registers[C]}")
        if A == 0 or B == 0:
            raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def bori(registers, A, B, C):
    registers[C] = registers[A] | B
    if DEBUG:
        print(f"OR into {C} = {registers[A]}[R={A}] | {B} = {registers[C]}")
        if A == 0:
            raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def setr(registers, A, B, C):
    registers[C] = registers[A]
    if DEBUG:
        print(f"SET into {C} = {registers[A]}[R={A}]")
        if A == 0:
            raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def seti(registers, A, B, C):
    registers[C] = A
    if DEBUG:
        print(f"SET into {C} = {A}")
        if C == 5:
            print(f"IP={registers[5]}")


def gtir(registers, A, B, C):
    registers[C] = 1 if A > registers[B] else 0
    if DEBUG:
        print(f"{C} = if {A} > {registers[B]}[R={B}] 1 else 0 = {registers[C]}")
        if B == 0:
            raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def gtri(registers, A, B, C):
    registers[C] = 1 if registers[A] > B else 0
    if DEBUG:
        print(f"{C} = if {registers[A]}[R={A}] > {B} 1 else 0 = {registers[C]}")
        if A == 0:
            raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def gtrr(registers, A, B, C):
    registers[C] = 1 if registers[A] > registers[B] else 0
    if DEBUG:
        print(f"{C} = if {registers[A]}[R={A}] > {registers[B]}[R={B}] 1 else 0 = {registers[C]}")
        if A == 0 or B == 0:
            raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def eqir(registers, A, B, C):
    registers[C] = 1 if A == registers[B] else 0
    if DEBUG:
        print(f"{C} = if {A} == {registers[B]}[R={B}] 1 else 0 = {registers[C]}")
        if B == 0:
            raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def eqri(registers, A, B, C):
    registers[C] = 1 if registers[A] == B else 0
    if DEBUG:
        print(f"{C} = if {registers[A]}[R={A}] == {B} 1 else 0 = {registers[C]}")
        if A == 0:
            raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def eqrr(registers, A, B, C):
    registers[C] = 1 if registers[A] == registers[B] else 0
    if DEBUG:
        print(f"{C} = if {registers[A]}[R={A}] == {registers[B]}[R={B}] 1 else 0 = {registers[C]}")
        if A == 0 or B == 0:
            raise "XXXX"
        if C == 5:
            print(f"IP={registers[5]}")


def execute(instructions, registers):
    ip_instruction = instructions[0]
    _, bound = ip_instruction.split(" ")
    bound = int(bound)
    ip = 0
    instructions = instructions[1:]

    total = 0
    while 0 <= ip < len(instructions):
        registers[bound] = ip
        instruction = instructions[ip]
        op_name, *args = instruction.split(" ")
        before = registers[:]

        print(instruction)

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

        # print(f"ip={ip} {before} {instruction} {registers}")

        ip = registers[bound] + 1
        total += 1
        if total > 2000:
            raise RuntimeError("Too many iterations, something is wrong")

    return total


with open("./resources/day21.txt") as f:
    instructions = [line.strip() for line in f.readlines()]


def check(i):
    registers = [i, 0, 0, 0, 0, 0]
    try:
        execute(instructions, registers)
    except RuntimeError:
        return False
    else:
        return True


def xxx(start, end):
    if start >= end:
        return
    mid = start + (end - start) // 2
    print("checking", mid)
    found = check(mid)
    if found:
        print(mid)
        raise RuntimeError(mid)

    random_boolean = random.choice([True, False])
    if random_boolean:
        xxx(start, mid)
        xxx(mid + 1, end)
    else:
        xxx(mid + 1, end)
        xxx(start, mid)


# check(0, True)
# xxx(0, 5000_000_000)
DEBUG=False
print(check(30842))

