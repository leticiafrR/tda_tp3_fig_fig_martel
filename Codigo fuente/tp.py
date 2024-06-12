import time
from reader import *
from bt import *
from lp import *

def greedy_resolution(bender_skills, cant_groups):
    bender_skills = sorted(bender_skills, key=lambda x : x[1], reverse=True)
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

    start_time = time.time()

    #arr = greedy_resolution(benders_skills, groups_count)
    #coefficient = (arr[1], arr[2])
    #groups = arr[0]

    #coefficient, groups = backtracking_algotithm(benders_skills, groups_count)
    coefficient, groups = backtracking_greedy_algotithm(benders_skills, groups_count)
    #coefficient, groups = lp_algorithm(benders_skills, groups_count)

    end_time = time.time()

    print(coefficient)
    print(groups)

    time_ms = round((end_time - start_time) * 1000, 6)
    print(time_ms, "ms")


if __name__ == "__main__":
    main()



