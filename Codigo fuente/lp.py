import pulp
from executer import *

def lp_algorithm(benders_skills, groups_count):
    S = []
    benders_count = len(benders_skills)

    for i in range(groups_count):
        S.append([])
        for k in range(benders_count):
            S[i].append(pulp.LpVariable("S_" + str(i) + ", " + str(k), cat="Binary"))

    problem = pulp.LpProblem("benders", pulp.LpMinimize)

    for k in range(benders_count):
        problem += pulp.lpSum([S[i][k] for i in range(groups_count)]) == 1

    auxiliar_and_vars = []
    
    for i in range(groups_count):
        auxiliar_and_vars.append([])

        for j in range(benders_count):
            auxiliar_and_vars[i].append([])

            n = 2
            for k in range(benders_count):
                if k == j:
                    auxiliar_and_vars[i][j].append(S[i][j])
                    continue
                
                if k < j:
                    auxiliar_and_vars[i][j].append(auxiliar_and_vars[i][k][j])
                    continue

                auxiliar_and_vars[i][j].append(pulp.LpVariable(f"Group_{i}_and_of_[{j}-{k}]", cat="Binary"))

                problem += n * auxiliar_and_vars[i][j][k] <= pulp.lpSum([S[i][j], S[i][k]])
                problem += (n - 1) + auxiliar_and_vars[i][j][k] >= pulp.lpSum([S[i][j], S[i][k]])

    problem += pulp.lpSum([pulp.lpSum([(auxiliar_and_vars[i][j][k] * (benders_skills[j][1] * benders_skills[k][1])) for j in range(benders_count) for k in range(benders_count)]) for i in range(groups_count)])
    
    problem.solve(pulp.PULP_CBC_CMD(msg=0))
    
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
                group.append(benders_skills[i])
        groups.append(group)

    coefficient = int(problem.objective.value())
    return coefficient, groups

def main():
    execute(lp_algorithm)

if __name__ == "__main__":
    main()
