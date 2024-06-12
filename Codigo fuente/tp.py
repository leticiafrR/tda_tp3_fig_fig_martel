import sys
import pulp # sudo apt install pip | pip install pulp
import math
import time

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

def get_coefficient(groups):
    sum_sqr_groups = 0
    for group in groups:
        sum_group = 0
        for bender in group:
            sum_group += bender[1]
        sum_sqr_groups += sum_group ** 2
    return sum_sqr_groups

def get_group_sum(group):
    return sum([bender[1] for bender in group])

def get_max_group_sum(groups):
    max_sum = 0
    for group in groups:
        group_sum = get_group_sum(group)
        if group_sum > max_sum:
            max_sum = group_sum

    return max_sum

def has_a_greater_group_sum(partial_result, max_group_sum):
    for group in partial_result:
        if get_group_sum(group) > max_group_sum:
            return True
    return False

def group_rec(benders_skills, n, index, partial_result, groups_result, min_coefficient, max_group_sum):

    if has_a_greater_group_sum(partial_result, max_group_sum):
        return min_coefficient, max_group_sum
    
    coefficient = get_coefficient(partial_result)

    if len(partial_result) == n and index == len(benders_skills) and coefficient <= min_coefficient: # Reemplazo, tengo una mejor cota

        max_group_sum = get_max_group_sum(partial_result)

        for i in range(len(partial_result)):
            groups_result[i].clear()
            groups_result[i].extend(partial_result[i])
            
        return coefficient, max_group_sum

    if index == len(benders_skills) or coefficient > min_coefficient:
        return min_coefficient, max_group_sum

    for i in range(len(partial_result)):
        partial_result[i].append(benders_skills[index])
        min_coefficient, max_group_sum = group_rec(benders_skills, n, index + 1, partial_result, groups_result, min_coefficient, max_group_sum)
        partial_result[i].pop()
    
    if len(partial_result) < n:
        partial_result.append([benders_skills[index]])
        min_coefficient, max_group_sum = group_rec(benders_skills, n, index + 1, partial_result, groups_result, min_coefficient, max_group_sum)
        partial_result.pop()
    return min_coefficient, max_group_sum

def backtracking_algotithm(benders_skills, groups_count, min_coefficient = math.inf, max_group_sum = math.inf):

    benders_skills = sorted(benders_skills, key=lambda x : x[1], reverse=True)

    groups_result = []
    
    for _ in range(groups_count):
        groups_result.append([])
    
    coefficient, _ = group_rec(benders_skills, groups_count, 0, [], groups_result, min_coefficient, max_group_sum)

    return coefficient, groups_result

def greedy_resolution(bender_skills, cant_groups):
    groups=[[] for _ in range(cant_groups)]
    joint_skills = [0]*cant_groups
    i_strong_group = 0
    for bender in bender_skills:
        _,skill = bender
        i_weak_group = joint_skills.index(min(joint_skills))
        groups[i_weak_group].append(bender)
        joint_skills[i_weak_group] += skill
        if joint_skills[i_weak_group] > joint_skills[i_strong_group]:
            i_strong_group = i_weak_group
    coefficient = sum(s**2 for s in joint_skills)
    return [groups , coefficient , joint_skills[i_strong_group]]

def backtracking_greedy_algotithm(benders_skills, groups_count):
    arr = greedy_resolution(benders_skills, groups_count)
    return backtracking_algotithm(benders_skills, groups_count, arr[1], arr[2])

def main():
    benders_skills, groups_count = read_benders()
    #arr = greedy_resolution(benders_skills, groups_count)
    coefficient, groups = backtracking_algotithm(benders_skills, groups_count)
    #coefficient, groups = backtracking_greedy_algotithm(benders_skills, groups_count)
    #coefficient, groups = lp_algorithm(benders_skills, groups_count)

    print(coefficient)
    print(groups)

if __name__ == "__main__":
    main()



