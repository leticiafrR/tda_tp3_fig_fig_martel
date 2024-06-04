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

            auxiliar_and_vars[i][k] = [pulp.LpVariable(f"Group_{i}_and_of_[{k}-{j}]", cat="Binary") for j in range(benders_count)]

            n = 2 # And de dos binarios
            for j in range(benders_count): # Definicion del and
                problem += n * auxiliar_and_vars[i][k][j] <= pulp.lpSum([S[i][k], S[i][j]])
                problem += (n - 1) + auxiliar_and_vars[i][k][j] >= pulp.lpSum([S[i][k], S[i][j]])

    # Ejemplo para una sumatoria de 3 elementos al cuadrado de este caso: ai = constante, xi = binario
    # (a1*x1 + a2*x2 + a3*x3)^2 <=> 
    # (a1*x1 + a2*x2 + a3*x3) * (a1*x1 + a2*x2 + a3*x3) <=>
    # ((a1*x1 * a1*x1) + (a1*x1 * a2*x2) + (a1*x1 * a3*x3)) + ((a2*x2 * a1*x1) + (a2*x2 * a2*x2) + (a2*x2 * a3*x3)) + ((a3*x3 * a1*x1) + (a3*x3 * a2*x2) + (a3*x3 * a3*x3)) <=>
    # ((a1*a1 * x1*x1) + (a1*a2 * x1*x2) + (a1*a3 * x1*x3)) + ((a2*a1 * x2*x1) + (a2*a2 * x2*x2) + (a2*a3 * x2*x3)) + ((a3*a1 * x3*x1) + (a3*a2 * x3*x2) + (a3*a3 * x3*x3)) <=>
    # Notemos que xi*xj se puede interpretar como: xi_and_xj pues si al menos una de las 2 es 0, el resultado es 0, caso contrario, 1
    # ((a1*a1 * x1_and_x1) + (a1*a2 * x1_and_x2) + (a1*a3 * x1_and_x3)) + ((a2*a1 * x2_and_x1) + (a2*a2 * x2_and_x2) + (a2*a3 * x2_and_x3)) + ((a3*a1 * x3_and_x1) + (a3*a2 * x3_and_x2) + (a3*a3 * x3_and_x3))
    problem += pulp.lpSum([pulp.lpSum([(auxiliar_and_vars[i][k][j] * (benders_skills[k][1] * benders_skills[j][1])) for k in range(benders_count) for j in range(benders_count)]) for i in range(groups_count)])
    
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
