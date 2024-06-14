import sys

def read_benders():
    filename = sys.argv[1:]
    benders_skills = []
    if len(filename) == 1:
        with open(filename[0]) as file:
            for line in file:
                line = line.strip()

                if line.isnumeric():
                    groups_count = int(line)
                    continue

                bender_skill = line.split(",")
                if len(bender_skill) == 2 and bender_skill[1].strip().isnumeric():
                    benders_skills.append((bender_skill[0], int(bender_skill[1])))

                    
    return benders_skills, groups_count

def execute(func):
    benders_skills, groups_count = read_benders()

    coefficient, groups = func(benders_skills, groups_count)
    print("Coeficiente:", coefficient)
    print("Grupos:", groups)
