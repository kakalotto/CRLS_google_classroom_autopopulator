# Input: date in 9/4/2018 format
# Output: True or False.  True if date given is in the past OR if it's today.  False if it's in the future


def is_in_past(p_date):
    import datetime

    numbers = p_date.split('/')
    p_month = numbers[0]
    p_day = numbers[1]
    p_year = numbers[2]

    # create a datetime object from dates given in inputs
    date_string = str(p_month) + '-' + str(p_day) + '-' + str(p_year)
    date_obj_notime = datetime.datetime.strptime(date_string, '%m-%d-%Y')

    # Create a datetime object with no time from today
    today_obj = datetime.datetime.now()
    today_string = today_obj.strftime('%m-%d-%Y')
    today_numbers = today_string.split('-')
    today_obj_notime = datetime.datetime.strptime(today_numbers[0] + '-' + today_numbers[1] + '-' + today_numbers[2],
                                                  '%m-%d-%Y')

    if today_obj_notime >= date_obj_notime:
        return True
    else:
        return False

#
# abc = is_in_past('5/2/2019')
# print(abc)
