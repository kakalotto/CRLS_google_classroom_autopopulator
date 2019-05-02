# Input: month (int), day of month (int), year (int)
# Output: Day and time in ISO8601 format.
# Example:  inputs 9, 4, 2018
#           output: 09-04-2018T12:00:00Z


def date_to_iso8601(p_month, p_dom, p_year):
    if int(p_month) < 10:
        p_month_string = '0' + str(p_month)
    else:
        p_month_string = p_month
    if int(p_dom) < 10:
        p_dom_string = '0' + str(p_dom)
    else:
        p_dom_string = p_dom
    daytime_iso8601 = str(p_year) + '-' + p_month_string + '-' + p_dom_string + 'T12:00:00Z'
    return daytime_iso8601


# abc = date_to_ISO8601(9, 3, 2018)
# print(abc)
