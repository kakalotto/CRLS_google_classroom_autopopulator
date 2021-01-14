# Input: first day of school year(in format 9/4/2018) and list of dates that are off - holidays + snow days
# (not counting weekends), also in same format (i.e. 3/21/2019).
# Output: List of dates for the school year, datetime format


def generate_school_dates(p_first_day, p_days_off):
    import dateutil.parser
    import datetime

    # Convert days off to datetime format, put in new list days_off_datetime
    days_off_datetime = []
    for date in p_days_off:
        days_off_datetime.append(dateutil.parser.parse(date))

    # Create blank list of all the school days, in datetime format.
    p_school_dates_datetime = []

    # Start with day one in datetime format.  Add one day at a time.
    # Check to see if this day is a weekend of if it's in the days off.
    # If it's not in one of those, then keep this day by adding it to the p_school_dates_datetime list.
    current_day_datetime = dateutil.parser.parse(p_first_day)

    one_day = datetime.timedelta(days=1)

    # Check to see if first day is 180 days different from first holiday.   If so, exit with error
    if current_day_datetime + 180 * one_day < days_off_datetime[0] \
            or current_day_datetime - 180 * one_day > days_off_datetime[0]:
        raise Exception('day 1 {} is more than 180 days different from first holiday {}.   Check your years and dates in '
                        'First day of school and Holidays columns in Calendar sheet '
                        .format(current_day_datetime, days_off_datetime[0]))

    while len(p_school_dates_datetime) != 180:
        if current_day_datetime.isoweekday() == 7 or current_day_datetime.isoweekday() == 6 \
                or current_day_datetime in days_off_datetime:
            pass
        else:
            p_school_dates_datetime.append(current_day_datetime)
        current_day_datetime += one_day

    # All done! Return the list days of school in datetime format.
    return p_school_dates_datetime


# dates = generate_school_dates('9/4/2018', ['9/3/2018', '9/19/2018', '10/8/2018', '11/12/2018', '11/22/2018',
#                                             '11/23/2018', '12/24/2018', '12/25/2018', '12/26/2018', '12/27/2018',
#                                             '12/28/2018', '12/31/2018', '1/1/2019', '1/21/2019', '2/18/2019',
#                                             '2/19/2019', '2/20/2019', '2/21/2019', '2/22/2019', '4/15/2019',
#                                             '4/16/2019',
#                                             '4/17/2019', '4/18/2019', '4/19/2019', '5/27/2019', '6/5/2019',
#                                             '3/4/2019'])
# print(dates)
