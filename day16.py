def addr(registers, A, B, C):
    registers[C] = registers[A] + registers[B]


def addi(registers, A, B, C):
    registers[C] = registers[A] + B


def mulr(registers, A, B, C):
    registers[C] = registers[A] * registers[B]


def muli(registers, A, B, C):
    registers[C] = registers[A] * B


def banr(registers, A, B, C):
    registers[C] = registers[A] & registers[B]


def bani(registers, A, B, C):
    registers[C] = registers[A] & B


def borr(registers, A, B, C):
    registers[C] = registers[A] | registers[B]


def bori(registers, A, B, C):
    registers[C] = registers[A] | B


def setr(registers, A, B, C):
    registers[C] = registers[A]


def seti(registers, A, B, C):
    registers[C] = A


def gtir(registers, A, B, C):
    registers[C] = 1 if A > registers[B] else 0


def gtri(registers, A, B, C):
    registers[C] = 1 if registers[A] > B else 0


def gtrr(registers, A, B, C):
    registers[C] = 1 if registers[A] > registers[B] else 0


def eqir(registers, A, B, C):
    registers[C] = 1 if A == registers[B] else 0


def eqri(registers, A, B, C):
    registers[C] = 1 if registers[A] == B else 0


def eqrr(registers, A, B, C):
    registers[C] = 1 if registers[A] == registers[B] else 0


operations = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

sample_blocks = """
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
""".split("\n\n")

# with open("./resources/day16.txt") as f:
#     block1, block2 = f.read().split("\n\n\n\n")

# sample_blocks = block1.split("\n\n")

samples = []
for sample_block in sample_blocks:
    before, instruction, after = sample_block.strip().splitlines()
    before = before.replace("Before: ", "").replace("[", "").replace("]", "").strip()
    before = list(map(int, before.split(", ")))
    instruction = list(map(int, instruction.split()))
    after = after.replace("After: ", "").replace("[", "").replace("]", "").strip()
    after = list(map(int, after.split(", ")))
    samples.append((before, instruction, after))


def part1():
    three_opcodes = 0
    for before, instruction, after in samples:
        matches = 0
        for operation in operations:
            if matches >= 3:
                break
            registers = before[:]
            operation(registers, *instruction[1:])
            if registers == after:
                matches += 1
        if matches >= 3:
            three_opcodes += 1

    print(three_opcodes)


def match_opcodes(samples):
    opcodes = {}
    operations_to_check = operations[:]
    while operations_to_check:
        for before, instruction, after in samples:
            matches = []
            for operation in operations_to_check:
                registers = before[:]
                operation(registers, *instruction[1:])
                if registers == after:
                    matches += [operation]
            if len(matches) == 1:
                operation = matches[0]
                opcodes[instruction[0]] = operation
                operations_to_check.remove(operation)

    return opcodes


def part2():
    opcodes = match_opcodes(samples)
    program_lines = block2.strip().splitlines()
    program_lines = [list(map(int, line.split())) for line in program_lines]
    registers = [0, 0, 0, 0]
    for program_line in program_lines:
        opcode = program_line[0]
        operation = opcodes[opcode]
        operation(registers, *program_line[1:])

    print(registers[0])


# part1()
# part2()
