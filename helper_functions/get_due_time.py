# Input: p_days_to_complete (integer) days to complete assignment, p_section is the string in Google classroom
#        corresponding to section.  This function assumes something P1, P2, P3, P4
#        Note, does not get due DATE, only due TIME.
# Output: A list.  list[hour, minute] of due time.


def get_due_time(p_days_to_complete, p_section):
    import re

    p1 = re.search('P1', p_section, re.X | re.M | re.S)  # 8:10
    p2 = re.search('P2', p_section, re.X | re.M | re.S)  # 9:58
    p3 = re.search('P3', p_section, re.X | re.M | re.S)  # 11:58
    p4 = re.search('P4', p_section, re.X | re.M | re.S)  # 1:10

    # All times are -4 (UTC TO EDT converter)
    p_hours = 0
    p_minutes = 0
    if int(p_days_to_complete) == 0:
        p_hours = 18
        p_minutes = 29
    else:
        if p1:
            p_hours = 13
            p_minutes = 10
        if p2:
            p_hours = 14
            p_minutes = 53
        if p3:
            p_hours = 16
            p_minutes = 51
        if p4:
            p_hours = 18
            p_minutes = 11
    return [p_hours, p_minutes]

# abc = get_due_time(5, '18/19, FY, P4')
# print(abc)
