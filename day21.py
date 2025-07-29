from day16 import addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr


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
        if total >= 100:
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

    xxx(start, mid - 1)
    xxx(mid + 1, end)


for i in range(1000_000_000):
    print("checking", i)
    if check(i):
        print(i)
        break
