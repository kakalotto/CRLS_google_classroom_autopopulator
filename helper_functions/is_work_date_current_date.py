# Input: announcement['scheduledTime'] which is ISO8601 format, this_date is format (9/5/2019)
#        and is date create_assignments_announcements is currently looking at
# Output: True, announcement date is same as the current date that the program is looking at


def is_work_date_current_date(p_announcement_date, this_date):

    import re

    from helper_functions.date_to_ISO8601 import date_to_iso8601

    announcement_date = re.sub(r'T.+$', '', p_announcement_date, re.X | re.M | re.S)
    numbers = this_date.split('/')
    today_date = date_to_iso8601(numbers[0], numbers[1], numbers[2], 0)
    today_date = re.sub(r'T.+$', '', today_date, re.X | re.M | re.S)

    if announcement_date == today_date:
        return True
    else:
        return False


