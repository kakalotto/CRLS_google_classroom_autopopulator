def quarter_dates(*, fy=False, p_filename=''):
    """
    quarter_date returns the ranges that I care about, given where I am now.
    Returns:
    datetime objects  of the first day of current quarter and last day that matters (list of datetimes)
    """
    import configparser
    import datetime

    config = configparser.ConfigParser()
    if p_filename:
        config.read(p_filename)
    else:
        config.read("crls_teacher_tools.ini")

    if 'QUARTERS' in config:
        quarters = config['QUARTERS']
        q1 = quarters['q1']
        q2 = quarters['q2']
        q3 = quarters['q3']
        q4 = quarters['q4']
        summer = quarters['summer']
    else:
        raise ValueError("In your ini file, need to have a section called QUARTERS")

    q1_list = q1.split('/')
    q2_list = q2.split('/')
    q3_list = q3.split('/')
    q4_list = q4.split('/')
    summer_list =  summer.split('/')

    q1 = datetime.datetime(int(q1_list[0]), int(q1_list[1]), int(q1_list[2]))
    q2 = datetime.datetime(int(q2_list[0]), int(q2_list[1]), int(q2_list[2]))
    q3 = datetime.datetime(int(q3_list[0]), int(q3_list[1]), int(q3_list[2]))
    q4 = datetime.datetime(int(q4_list[0]), int(q4_list[1]), int(q4_list[2]))
    summer = datetime.datetime(int(summer_list[0]), int(summer_list[1]), int(summer_list[2]))
    today = datetime.datetime.now()
    one_day = datetime.timedelta(days=1)
    if fy:
        return [q1, summer - one_day]
    else:
        if q3 > today:
            return [q1, q3 - one_day]
        else:
            return [q3, summer - one_day]


def which_quarter_today(*, p_filename=''):
    """
    Tells me what quarter I'm int oday
    Returns:
    datetime object of the first day of current quarters
    """
    import configparser
    import datetime

    config = configparser.ConfigParser()
    if p_filename:
        config.read(p_filename)
    else:
        config.read("crls_teacher_tools.ini")

    if 'QUARTERS' in config:
        quarters = config['QUARTERS']
        q1 = quarters['q1']
        q2 = quarters['q2']
        q3 = quarters['q3']
        q4 = quarters['q4']
    else:
        raise ValueError("In your ini file, need to have a section called QUARTERS")

    q1_list = q1.split('/')
    q2_list = q2.split('/')
    q3_list = q3.split('/')
    q4_list = q4.split('/')
    q1 = datetime.datetime(int(q1_list[0]), int(q1_list[1]), int(q1_list[2]))
    q2 = datetime.datetime(int(q2_list[0]), int(q2_list[1]), int(q2_list[2]))
    q3 = datetime.datetime(int(q3_list[0]), int(q3_list[1]), int(q3_list[2]))
    q4 = datetime.datetime(int(q4_list[0]), int(q4_list[1]), int(q4_list[2]))

    today = datetime.datetime.now()
    if q2 > today > q1:
        return q1
    elif q3 > today > q2:
        return q2
    elif q4 > today > q3:
        return q3
    else:
        return q4


def which_quarter_today_string():
    """
    Tells me what quarter I'm int oday in string (i.e. Q1, Q2, Q3, Q4)
    Returns: String of which quarter it is ('Q1', 'Q2', 'Q3', or 'Q4')
    """
    import configparser
    import datetime

    config = configparser.ConfigParser()
    config.read("crls_teacher_tools.ini")

    if 'QUARTERS' in config:
        quarters = config['QUARTERS']
        q1 = quarters['q1']
        q2 = quarters['q2']
        q3 = quarters['q3']
        q4 = quarters['q4']
        summer = quarters['summer']
    else:
        raise ValueError("In your ini file, need to have a section called QUARTERS")

    q1_list = q1.split('/')
    q2_list = q2.split('/')
    q3_list = q3.split('/')
    q4_list = q4.split('/')
    q1 = datetime.datetime(int(q1_list[0]), int(q1_list[1]), int(q1_list[2]))
    q2 = datetime.datetime(int(q2_list[0]), int(q2_list[1]), int(q2_list[2]))
    q3 = datetime.datetime(int(q3_list[0]), int(q3_list[1]), int(q3_list[2]))
    q4 = datetime.datetime(int(q4_list[0]), int(q4_list[1]), int(q4_list[2]))
    today = datetime.datetime.now()
    if q2 > today > q1:
        return 'Q1'
    elif q3 > today > q2:
        return 'Q2'
    elif q4 > today > q3:
        return 'Q3'
    else:
        return 'Q4'
