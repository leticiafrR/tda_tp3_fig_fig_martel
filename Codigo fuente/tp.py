import sys
import pulp # sudo apt install pip | pip install pulp

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

def lp_algorithm(benders_skills, groups_count):
    S = []
    benders_count = len(benders_skills)

    for i in range(groups_count):
        S.append([])
        for j in range(benders_count):
            S[i].append(pulp.LpVariable("S_" + str(i) + ", " + str(j), cat="Binary"))

    problem = pulp.LpProblem("benders", pulp.LpMinimize)

    for i in range(groups_count):
        problem += pulp.LpAffineExpression([(S[i][j], benders_skills[j][1]) for j in range(benders_count)]) >= 1 # Aseguro que en cada grupo haya al menos un maestro


    for j in range(benders_count):
        problem += pulp.lpSum([S[i][j] for i in range(groups_count)]) <= 1 # Aseguro que no se repitan los binarios en diferentes grupos

    problem += pulp.lpSum([S[i][j] for i in range(groups_count) for j in range(benders_count)]) == benders_count # Aseguro que se usen todos los maestros

    auxiliar_and_vars = []
    
    for i in range(groups_count):
        auxiliar_and_vars.append([])

        for k in range(benders_count):
            auxiliar_and_vars[i].append([])

            # Mejor solo para indexar
            auxiliar_and_vars[i][k] = [None] * benders_count

            n = 2
            for j in range(k + 1, benders_count):
                auxiliar_and_vars[i][k][j] = pulp.LpVariable(f"Group_{i}_and_of_[{k}.{j}]", cat="Binary")

                problem += n * auxiliar_and_vars[i][k][j] <= pulp.lpSum([S[i][k], S[i][j]])
                problem += (n - 1) + auxiliar_and_vars[i][k][j] >= pulp.lpSum([S[i][k], S[i][j]])
            

    problem += pulp.lpSum([(pulp.lpSum([(S[i][j] * (benders_skills[j][1] ** 2)) for j in range(benders_count)]) + (2 * pulp.lpSum([((benders_skills[k][1] * benders_skills[j][1]) * auxiliar_and_vars[i][k][j]) for k in range(benders_count) for j in range(k + 1, benders_count)]))) for i in range(groups_count)])
    
    problem.solve()

    # Resultados
    r = []
    for i in range(groups_count):
        r.append([])
        for yi in S[i]:
            r[i].append(pulp.value(yi))

    print("Binarios: " + str(r))

    groups = []
    for group_values in r:
        group = []
        for i in range(len(group_values)):
            if group_values[i] == 1:
                group.append(benders_skills[i][0])
        groups.append(group)

    print("Grupos: " + str(groups))
    print("Coeficiente: " + str(problem.objective.value()))
    return r

def main():

    benders_skills, groups_count = read_benders()
    lp_algorithm(benders_skills, groups_count)

if __name__ == "__main__":
    main()
