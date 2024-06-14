from reader import *
from bt import *
from lp import *
from greedy import *

def backtracking_greedy_algotithm(benders_skills, groups_count):
    data = greedy_resolution_data(benders_skills, groups_count)
    return backtracking_algotithm(benders_skills, groups_count, data[1], data[2])

def main():
    execute(backtracking_algotithm)

if __name__ == "__main__":
    main()



