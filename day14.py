def part1():
    recipies = [3, 7]
    elf1 = 0
    elf2 = 1

    window = 10
    after = 920831
    while True:
        new_recipe = recipies[elf1] + recipies[elf2]
        if new_recipe >= 10:
            recipies.append(int(str(new_recipe)[0]))
            recipies.append(int(str(new_recipe)[1]))
        else:
            recipies.append(new_recipe)

        if len(recipies) >= window + after:
            print("".join(map(str, recipies[after:after + window])))
            break

        elf1 = (elf1 + recipies[elf1] + 1) % len(recipies)
        elf2 = (elf2 + recipies[elf2] + 1) % len(recipies)


def part2():
    recipies = [3, 7]
    elf1 = 0
    elf2 = 1

    after = [9, 2, 0, 8, 3, 1]
    while True:
        new_recipe = recipies[elf1] + recipies[elf2]
        if new_recipe >= 10:
            recipies.append(int(str(new_recipe)[0]))

            if len(recipies) >= len(after):
                if recipies[len(recipies) - len(after):] == after:
                    print(len(recipies) - len(after))
                    break

            recipies.append(int(str(new_recipe)[1]))
            if len(recipies) >= len(after):
                if recipies[len(recipies) - len(after):] == after:
                    print(len(recipies) - len(after))
                    break
        else:
            recipies.append(new_recipe)

            if len(recipies) >= len(after):
                if recipies[len(recipies) - len(after):] == after:
                    print(len(recipies) - len(after))
                    break

        elf1 = (elf1 + recipies[elf1] + 1) % len(recipies)
        elf2 = (elf2 + recipies[elf2] + 1) % len(recipies)


part1()
part2()
