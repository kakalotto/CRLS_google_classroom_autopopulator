def quarter_dates(*, fy=False):
    """
    quarter_date returns the ranges that I care about, given where I am now.
    Returns:
    datetime objects  of the first day of current quarter and last day that matters (list of datetimes)
    """
    from datetime import datetime, timedelta
    import helper_functions.constants as constants
    q1 = constants.Q1
    q2 = constants.Q2
    q3 = constants.Q3
    q4 = constants.Q4
    summer = constants.summer

    today = datetime.now()
    if fy:
        return [q1, summer - timedelta(days=1)]
    else:
        if q3 > today:
            return [q1, q3 - timedelta(days=1)]
        else:
            return [q3, summer - timedelta(days=1)]


def which_quarter_today():
    """
    Tells me what quarter I'm int oday
    Returns:
    datetime object of the first day of current quarter and last day that matters
    """
    import datetime
    import helper_functions.constants as constants
    q1 = constants.Q1
    q2 = constants.Q2
    q3 = constants.Q3
    q4 = constants.Q4

    today = datetime.datetime.now()
    if q2 > today > q1:
        return q1
    elif q3 > today > q2:
        return q2
    elif q4 > today > q3:
        return q3
    else:
        return q4
