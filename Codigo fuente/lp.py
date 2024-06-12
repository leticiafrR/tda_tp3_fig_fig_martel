import pulp # sudo apt install pip | pip install pulp

def lp_algorithm(benders_skills, groups_count):
    S = []
    benders_count = len(benders_skills)

    for i in range(groups_count):
        S.append([])
        for k in range(benders_count):
            S[i].append(pulp.LpVariable("S_" + str(i) + ", " + str(k), cat="Binary"))

    problem = pulp.LpProblem("benders", pulp.LpMinimize)

    for i in range(groups_count):
        problem += pulp.LpAffineExpression([(S[i][j], benders_skills[j][1]) for j in range(benders_count)]) >= 1 # Aseguro que en cada grupo haya al menos un maestro

    for k in range(benders_count):
        problem += pulp.lpSum([S[i][k] for i in range(groups_count)]) <= 1 # Aseguro que no se repitan los binarios en diferentes grupos

    problem += pulp.lpSum([S[i][j] for i in range(groups_count) for j in range(benders_count)]) == benders_count # Aseguro que se usen todos los maestros

    auxiliar_and_vars = []
    
    for i in range(groups_count):
        auxiliar_and_vars.append([])

        for j in range(benders_count):
            auxiliar_and_vars[i].append([])

            n = 2 # And de dos binarios
            for k in range(benders_count):
                if k == j:
                    auxiliar_and_vars[i][j].append(S[i][j]) # Caso and de una misma variable
                    continue
                
                if k < j:
                    auxiliar_and_vars[i][j].append(auxiliar_and_vars[i][k][j]) # Caso en el que tenemos un and repetido, (x1 and x2) = (x2 and x1)
                    continue

                auxiliar_and_vars[i][j].append(pulp.LpVariable(f"Group_{i}_and_of_[{j}-{k}]", cat="Binary")) # Creación del and

                problem += n * auxiliar_and_vars[i][j][k] <= pulp.lpSum([S[i][j], S[i][k]])
                problem += (n - 1) + auxiliar_and_vars[i][j][k] >= pulp.lpSum([S[i][j], S[i][k]])

    # Ejemplo para una sumatoria de 3 elementos al cuadrado de este caso: ai = constante, xi = binario
    # (a1*x1 + a2*x2 + a3*x3)^2 <=> 
    # (a1*x1 + a2*x2 + a3*x3) * (a1*x1 + a2*x2 + a3*x3) <=>
    # ((a1*x1 * a1*x1) + (a1*x1 * a2*x2) + (a1*x1 * a3*x3)) + ((a2*x2 * a1*x1) + (a2*x2 * a2*x2) + (a2*x2 * a3*x3)) + ((a3*x3 * a1*x1) + (a3*x3 * a2*x2) + (a3*x3 * a3*x3)) <=>
    # ((a1*a1 * x1*x1) + (a1*a2 * x1*x2) + (a1*a3 * x1*x3)) + ((a2*a1 * x2*x1) + (a2*a2 * x2*x2) + (a2*a3 * x2*x3)) + ((a3*a1 * x3*x1) + (a3*a2 * x3*x2) + (a3*a3 * x3*x3)) <=>
    # Notemos que xi*xj se puede interpretar como: xi_and_xj pues si al menos una de las 2 es 0, el resultado es 0, caso contrario, 1
    # ((a1*a1 * x1_and_x1) + (a1*a2 * x1_and_x2) + (a1*a3 * x1_and_x3)) + ((a2*a1 * x2_and_x1) + (a2*a2 * x2_and_x2) + (a2*a3 * x2_and_x3)) + ((a3*a1 * x3_and_x1) + (a3*a2 * x3_and_x2) + (a3*a3 * x3_and_x3))
    problem += pulp.lpSum([pulp.lpSum([(auxiliar_and_vars[i][j][k] * (benders_skills[j][1] * benders_skills[k][1])) for j in range(benders_count) for k in range(benders_count)]) for i in range(groups_count)])
    
    #problem.solve()
    problem.solve(pulp.PULP_CBC_CMD(msg=0))
    
    # Resultados
    binary_results = []
    for i in range(groups_count):
        binary_results.append([])
        for yi in S[i]:
            binary_results[i].append(pulp.value(yi))

    groups = []
    for group_binary_values in binary_results:
        group = []
        for i in range(len(group_binary_values)):
            if group_binary_values[i] == 1:
                group.append(benders_skills[i][0])
        groups.append(group)

    coefficient = int(problem.objective.value())
    return coefficient, groups