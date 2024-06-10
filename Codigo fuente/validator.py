def validate_np (partitions,b ):
    skills = 0
    for partition in partitions:
        skills_group = 0
        for _,skill in partition:
            skills_group += skill
        skills += (skills_group**2)
        if skills > b:
            return False
    return True
