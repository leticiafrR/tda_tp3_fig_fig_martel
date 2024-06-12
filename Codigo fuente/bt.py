import math

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