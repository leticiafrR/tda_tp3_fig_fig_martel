from executer import *

def greedy_resolution_data(bender_skills, cant_groups):
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

def greedy_resolution(benders_skills, cant_groups):
    data = greedy_resolution_data(benders_skills, cant_groups)
    return data[1], data[0]

def main():
    execute(greedy_resolution)

if __name__ == "__main__":
    main()
