# Input: month (int), day of month (int), year (int)
# Output: Day and time in ISO8601 format.
# Example:  inputs 9, 4, 2018
#           output: 09-04-2018T12:00:00Z


def date_to_iso8601(p_month, p_dom, p_year, p_offset):
    if int(p_month) < 10:
        p_month_string = '0' + str(p_month)
    else:
        p_month_string = p_month
    if int(p_dom) < 10:
        p_dom_string = '0' + str(p_dom)
    else:
        p_dom_string = p_dom
    if p_offset > 59:
        raise ValueError("p_offset is too high ({}).  Did you have more than 60 assignments in a lesson?\n"
                         "Max 59 assignments per lesson.".format(p_offset))
    if p_offset < 10:
        p_offset_string = '0' + str(p_offset)
    else:
        p_offset_string = str(p_offset)
    daytime_iso8601 = str(p_year) + '-' + p_month_string + '-' + p_dom_string + 'T12:00:' + p_offset_string + 'Z'
    return daytime_iso8601

#
# abc = date_to_iso8601(5, 3, 2018, 8)
# print(abc)
