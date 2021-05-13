def read_quarter_info(p_filename):
    import configparser
    import datetime
    config = configparser.ConfigParser()
    config.read(p_filename)

    if 'QUARTERS' in config:
        quarters = config['QUARTERS']
        q1 = quarters['q1']
        q2 = quarters['q2']
        q3 = quarters['q3']
        q4 = quarters['q4']
        summer = quarters['summer']
    else:
        raise ValueError("Need to have a file called: " + str(p_filename) + "\n"
                         "This file needs to have a QUARTERS section with variables q1, q2, q3, and q4")

    q1_list = q1.split('/')
    q1 = datetime.datetime(int(q1_list[0]), int(q1_list[1]), int(q1_list[2]))
    q2_list = q2.split('/')
    q2 = datetime.datetime(int(q2_list[0]), int(q2_list[1]), int(q2_list[2]))
    q3_list = q3.split('/')
    q3 = datetime.datetime(int(q3_list[0]), int(q3_list[1]), int(q3_list[2]))
    q4_list = q4.split('/')
    q4 = datetime.datetime(int(q4_list[0]), int(q4_list[1]), int(q4_list[2]))
    summer_list = summer.split('/')
    summer = datetime.datetime(int(summer_list[0]), int(summer_list[1]), int(summer_list[2]))

    return [q1, q2, q3, q4, summer]


def read_classes_info(p_filename):
    import configparser
    config = configparser.ConfigParser()
    config.read(p_filename)

    p_all_classes = {}

    if 'DEFAULT' in config:
        gc1 = config.get('DEFAULT', 'gc_class1', fallback='')
        gc2 = config.get('DEFAULT', 'gc_class2', fallback='')
        gc3 = config.get('DEFAULT', 'gc_class3', fallback='')
        gc4 = config.get('DEFAULT', 'gc_class4', fallback='')
        gc5 = config.get('DEFAULT', 'gc_class5', fallback='')
        gc6 = config.get('DEFAULT', 'gc_class6', fallback='')
        gc7 = config.get('DEFAULT', 'gc_class7', fallback='')
        gc8 = config.get('DEFAULT', 'gc_class8', fallback='')
    else:
        raise ValueError("Need to have a file called: " +
                         str(p_filename) +
                         "\nThis file needs to have a DEFAULT section with variables gc_class1, and so on")

    if 'DEFAULT' in config:
        aspen1 = config.get('DEFAULT', 'aspen_class1', fallback='')
        aspen2 = config.get('DEFAULT', 'aspen_class2', fallback='')
        aspen3 = config.get('DEFAULT', 'aspen_class3', fallback='')
        aspen4 = config.get('DEFAULT', 'aspen_class4', fallback='')
        aspen5 = config.get('DEFAULT', 'aspen_class5', fallback='')
        aspen6 = config.get('DEFAULT', 'aspen_class6', fallback='')
        aspen7 = config.get('DEFAULT', 'aspen_class7', fallback='')
        aspen8 = config.get('DEFAULT', 'aspen_class8', fallback='')
    else:
        raise ValueError("Need to have a file called: " +
                         str(p_filename) +
                         "\nThis file needs to have a DEFAULT section with variables aspen1, and so on")

    if gc1 and aspen1:
        p_all_classes[gc1] = aspen1
    if gc2 and aspen2:
        p_all_classes[gc2] = aspen2
    if gc3 and aspen3:
        p_all_classes[gc3] = aspen3
    if gc4 and aspen4:
        p_all_classes[gc4] = aspen4
    if gc5 and aspen5:
        p_all_classes[gc5] = aspen5
    if gc6 and aspen6:
        p_all_classes[gc6] = aspen6
    if gc7 and aspen7:
        p_all_classes[gc7] = aspen6
    if gc8 and aspen8:
        p_all_classes[gc8] = aspen6

    return p_all_classes


def read_mailer_info(p_filename):
    import configparser
    config = configparser.ConfigParser()
    config.read(p_filename)

    if 'MAILER' in config:
        p_message1 = config.get('MAILER', 'message1', fallback='')
        p_message2 = config.get('MAILER', 'message2', fallback='')
    else:
        raise ValueError("Need to have a file called: " +
                         str(p_filename) +
                         "\nThis file needs to have a "
                         "MAILER section with variables message1, message2, test_run, etc...")
    p_send_email = config.getboolean('MAILER', 'send_email', fallback=False)
    p_cc = config.get('MAILER', 'cc', fallback='')

    p_message = p_message1 + '\n\n' + p_message2

    return [p_message, p_send_email, p_cc]
