from day16 import addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr

instructions = """
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
""".strip().splitlines()

with open("./resources/day19.txt") as f:
    instructions = f.read().strip().splitlines()


def execute(instructions, registers):
    ip_instruction = instructions[0]
    _, bound = ip_instruction.split(" ")
    bound = int(bound)
    ip = 0
    instructions = instructions[1:]

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

        print(f"ip={ip} {before} {instruction} {registers}")

        ip = registers[bound] + 1


def part1():
    registers = [0, 0, 0, 0, 0, 0]
    execute(instructions, registers)
    print(registers[0])


def part2():
    # copilot help :-)
    target = 10551350  # value from 5 register
    num_of_devisors = 0

    # number of divisors of given number
    for i in range(1, int(target ** 0.5) + 1):
        if target % i == 0:
            num_of_devisors += i
            if i != target // i:
                num_of_devisors += target // i

    print(num_of_devisors)


part1()
part2()
