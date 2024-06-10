import random
import sys

MAX_RAND_VALUE = 999
NOT_CONSTANT = -1
CONTEXT = "# La primera linea indica la cantidad de grupos a formar, las siguientes son de la forma 'nombre maestro, habilidad'"
BENDERS = [
    "Yue",
    "Rafa",
    "Pakku",
    "Siku",
    "Wei", 
    "Eska",
    "Misu",
    "Katara",
    "Sangok",
    "Amon",
    "Sura",
    "Hama", 
    "Desna",
    "Yakone"
]

def generate_benders(cant, const_skill = NOT_CONSTANT):
    benders = []
    already_in = set()
    for _ in range(cant):
        benders.append(generate_bender(const_skill, already_in))
    return benders

def generate_bender(skill, already_in):

    bender = BENDERS[random.randint(0, len(BENDERS) - 1)]

    while bender in already_in:
        bender += "'"
    already_in.add(bender)

    if skill == NOT_CONSTANT:
        skill = random.randint(1, MAX_RAND_VALUE)
    
    return (bender, skill)

def get_constant(const_arg):
    const_b = NOT_CONSTANT

    if len(const_arg) >= 1:
        split = const_arg[0].split("=")
        if split[0] == "b":
            const_b = int(split[1])

    return const_b

def main():
    filename = sys.argv[1]
    count = int(sys.argv[2])
    groups_count = int(sys.argv[3])

    const_b = get_constant(sys.argv[4:])
    benders = generate_benders(count, const_b)

    with open(filename, 'w') as file:
        file.write(CONTEXT)
        file.write("\n" + str(groups_count))
        for bender in benders:
            file.write("\n" + str(bender[0]) + ", " + str(bender[1]))
    file.close()

if __name__ == "__main__":
    main()