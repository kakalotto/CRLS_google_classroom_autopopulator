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
        p_all_classes[gc7] = aspen7
    if gc8 and aspen8:
        p_all_classes[gc8] = aspen8

    return p_all_classes


def read_quizzes_info(p_filename):
    import configparser
    config = configparser.ConfigParser()
    config.read(p_filename)


    if 'QUIZZES' in config:
        gc_class = config.get('QUIZZES', 'gc_class', fallback='')
        title = config.get('QUIZZES', 'title', fallback='')
        due_date = config.get('QUIZZES', 'due_date', fallback='')

        period = config.get('QUIZZES', 'period', fallback=1)
        quiz1_id = config.get('QUIZZES', 'quiz1_id', fallback='')
        quiz2_id = config.get('QUIZZES', 'quiz2_id', fallback=quiz1_id)
        quiz1_assignees = config.get('QUIZZES', 'quiz1_assignees', fallback='')
        quiz2_assignees = config.get('QUIZZES', 'quiz2_assignees', fallback='')
        quiz1_et_assignees =  config.get('QUIZZES', 'quiz1_et_assignees', fallback='')
        quiz2_et_assignees =  config.get('QUIZZES', 'quiz2_et_assignees', fallback='')
        course_id = config.get('QUIZZES', 'course_id', fallback='')
        quiz_length = config.get('QUIZZES', 'quiz_length', fallback='')
    else:
        raise ValueError("Need to have a file called: " +
                         str(p_filename) +
                         "\nThis file needs to have a DEFAULT section with variables gc_class1, and so on")
    quiz_info = {}
    quiz_info['gc_class'] = gc_class
    quiz_info['title'] = title
    quiz_info['due_date'] = due_date
    quiz_info['period'] = period
    quiz_info['quiz1_id'] = quiz1_id
    quiz_info['quiz2_id'] = quiz2_id
    quiz_info['quiz1_assignees'] = quiz1_assignees
    quiz_info['quiz2_assignees'] = quiz2_assignees
    quiz_info['quiz1_et_assignees'] = quiz1_et_assignees
    quiz_info['quiz2_et_assignees'] = quiz2_et_assignees

    quiz_info['course_id'] = course_id
    quiz_info['quiz_length'] = quiz_length
    return quiz_info

def read_period_info(p_filename):
    import configparser
    config = configparser.ConfigParser()
    config.read(p_filename)

    if 'PERIODS' in config:
        p1 = config.get('PERIODS', 'p1', fallback='')
        p2 = config.get('PERIODS', 'p2', fallback='')
        p3 = config.get('PERIODS', 'p3', fallback='')
        p4 = config.get('PERIODS', 'p4', fallback='')
        p1cm = config.get('PERIODS', 'p1cm', fallback='')
        p2cm = config.get('PERIODS', 'p2cm', fallback='')
        p3cm = config.get('PERIODS', 'p3cm', fallback='')
        p4cm = config.get('PERIODS', 'p4cm', fallback='')
    else:
        raise ValueError("Need to have a file called: " +
                         str(p_filename) +
                         "\nThis file needs to have a DEFAULT section with variables gc_class1, and so on")
    period_info = {}
    period_info['p1'] = p1
    period_info['p2'] = p2
    period_info['p3'] = p3
    period_info['p4'] = p4
    period_info['p1cm'] = p1cm
    period_info['p2cm'] = p2cm
    period_info['p3cm'] = p3cm
    period_info['p4cm'] = p4cm
    return period_info

def read_sheets_info(p_filename):
    import configparser
    config = configparser.ConfigParser()
    config.read(p_filename)
    p_spreadsheet_ids = []

    if 'CREATE_ASSIGNMENTS_ANNOUNCEMENTS' in config:
        spreadsheet_1 = config.get('CREATE_ASSIGNMENTS_ANNOUNCEMENTS', 'spreadsheet_id_1', fallback='')
        spreadsheet_2 = config.get('CREATE_ASSIGNMENTS_ANNOUNCEMENTS', 'spreadsheet_id_2', fallback='')
        spreadsheet_3 = config.get('CREATE_ASSIGNMENTS_ANNOUNCEMENTS', 'spreadsheet_id_3', fallback='')
        spreadsheet_4 = config.get('CREATE_ASSIGNMENTS_ANNOUNCEMENTS', 'spreadsheet_id_4', fallback='')
        spreadsheet_5 = config.get('CREATE_ASSIGNMENTS_ANNOUNCEMENTS', 'spreadsheet_id_5', fallback='')
        spreadsheet_6 = config.get('CREATE_ASSIGNMENTS_ANNOUNCEMENTS', 'spreadsheet_id_6', fallback='')
    else:
        raise ValueError("Need to have a file called: " +
                         str(p_filename) +
                         "\nThis file needs to have a CREATE_ASSIGNMENTS_ANNOUNCEMENTS section "
                         "with variables spreadsheet_id_1, and so on")
    if spreadsheet_1:
        p_spreadsheet_ids.append(spreadsheet_1)
    if spreadsheet_2:
        p_spreadsheet_ids.append(spreadsheet_2)
    if spreadsheet_3:
        p_spreadsheet_ids.append(spreadsheet_3)
    if spreadsheet_4:
        p_spreadsheet_ids.append(spreadsheet_4)
    if spreadsheet_5:
        p_spreadsheet_ids.append(spreadsheet_5)
    if spreadsheet_6:
        p_spreadsheet_ids.append(spreadsheet_6)
    print(f"Here are all the spreadsheet IDs {p_spreadsheet_ids}")
    return p_spreadsheet_ids


def read_mailer_info(p_filename):
    import configparser
    config = configparser.ConfigParser()
    config.read(p_filename)

    if 'MAILER' in config:
        p_send_email = config.getboolean('MAILER', 'send_email', fallback=False)
        p_mailclass1 = config.get('MAILER', 'mailclass1', fallback='')
        p_mailclass2 = config.get('MAILER', 'mailclass2', fallback='')
        p_mailclass3 = config.get('MAILER', 'mailclass3', fallback='')
        p_mailclass4 = config.get('MAILER', 'mailclass4', fallback='')
        p_mailclass5 = config.get('MAILER', 'mailclass5', fallback='')
        p_mailclass6 = config.get('MAILER', 'mailclass6', fallback='')
        p_mailclass7 = config.get('MAILER', 'mailclass7', fallback='')
        p_mailclass8 = config.get('MAILER', 'mailclass8', fallback='')
        p_teachercc1 = config.get('MAILER', 'teachercc1', fallback='')
        p_teachercc2 = config.get('MAILER', 'teachercc2', fallback='')
        p_teachercc3 = config.get('MAILER', 'teachercc3', fallback='')
        p_teachercc4 = config.get('MAILER', 'teachercc4', fallback='')
        p_teachercc5 = config.get('MAILER', 'teachercc5', fallback='')
        p_teachercc6 = config.get('MAILER', 'teachercc6', fallback='')
        p_teachercc7 = config.get('MAILER', 'teachercc7', fallback='')
        p_teachercc8 = config.get('MAILER', 'teachercc8', fallback='')
        p_message1 = config.get('MAILER', 'message1', fallback='')
        p_message2 = config.get('MAILER', 'message2', fallback='')
        p_message3 = config.get('MAILER', 'message3', fallback='')
        p_message4 = config.get('MAILER', 'message4', fallback='')
        p_message5 = config.get('MAILER', 'message5', fallback='')
        p_message6 = config.get('MAILER', 'message6', fallback='')
        p_message7 = config.get('MAILER', 'message7', fallback='')
        p_message8 = config.get('MAILER', 'message8', fallback='')
        p_student1 = config.get('MAILER', 'email1', fallback='')
        p_student2 = config.get('MAILER', 'email2', fallback='')
        p_student3 = config.get('MAILER', 'email3', fallback='')
        p_student4 = config.get('MAILER', 'email4', fallback='')
        p_student5 = config.get('MAILER', 'email5', fallback='')
        p_student6 = config.get('MAILER', 'email6', fallback='')
        p_student7 = config.get('MAILER', 'email7', fallback='')
        p_student8 = config.get('MAILER', 'email8', fallback='')
        p_student9 = config.get('MAILER', 'email9', fallback='')
        p_student10 = config.get('MAILER', 'email10', fallback='')
        p_student11 = config.get('MAILER', 'email11', fallback='')
        p_student12 = config.get('MAILER', 'email12', fallback='')
        p_student13 = config.get('MAILER', 'email13', fallback='')
        p_student14 = config.get('MAILER', 'email14', fallback='')
        p_student15 = config.get('MAILER', 'email15', fallback='')
        p_student16 = config.get('MAILER', 'email16', fallback='')
        p_student17 = config.get('MAILER', 'email17', fallback='')

        p_guardian1 = config.get('MAILER', 'guardian1', fallback='')
        p_guardian2 = config.get('MAILER', 'guardian2', fallback='')
        p_guardian3 = config.get('MAILER', 'guardian3', fallback='')
        p_guardian4 = config.get('MAILER', 'guardian4', fallback='')
        p_guardian5 = config.get('MAILER', 'guardian5', fallback='')
        p_guardian6 = config.get('MAILER', 'guardian6', fallback='')
        p_guardian7 = config.get('MAILER', 'guardian7', fallback='')
        p_guardian8 = config.get('MAILER', 'guardian8', fallback='')
        p_guardian9 = config.get('MAILER', 'guardian9', fallback='')
        p_guardian10 = config.get('MAILER', 'guardian10', fallback='')
        p_guardian11 = config.get('MAILER', 'guardian11', fallback='')
        p_guardian12 = config.get('MAILER', 'guardian12', fallback='')
        p_guardian13 = config.get('MAILER', 'guardian13', fallback='')
        p_guardian14 = config.get('MAILER', 'guardian14', fallback='')
        p_guardian15 = config.get('MAILER', 'guardian15', fallback='')
        p_guardian16 = config.get('MAILER', 'guardian16', fallback='')
        p_guardian17 = config.get('MAILER', 'guardian17', fallback='')

    else:
        raise ValueError("Need to have a file called: " +
                         str(p_filename) +
                         "\nThis file needs to have a "
                         "MAILER section with variables mailclass1, send_email, etc...")

    p_mailclasses= [p_mailclass1, p_mailclass2, p_mailclass3, p_mailclass4, p_mailclass5, p_mailclass6, p_mailclass7,
                    p_mailclass8]
    p_teachercc = [p_teachercc1, p_teachercc2, p_teachercc3, p_teachercc4, p_teachercc5, p_teachercc6,
                  p_teachercc7, p_teachercc8]
    p_messages = [p_message1, p_message2, p_message3, p_message4, p_message5, p_message6, p_message7, p_message8]
    p_student_cc = {p_student1: p_guardian1, p_student2: p_guardian2, p_student3: p_guardian3, p_student4: p_guardian4,
                    p_student5: p_guardian5, p_student6: p_guardian6, p_student7: p_guardian7, p_student8: p_guardian8,
                    p_student9: p_guardian9, p_student10: p_guardian10, p_student11: p_guardian11,
                    p_student12: p_guardian12, p_student13: p_guardian13, p_student14: p_guardian14,
                    p_student15: p_guardian15, p_student16: p_guardian16, p_student17: p_guardian17}
    print(f"Here is the studentCC's {p_student_cc}")
    return [p_mailclasses, p_teachercc, p_messages, p_student_cc, p_send_email, ]


def config_string_to_dict(p_string):
    p_list = p_string.split(',')
    return p_list


def read_return_perfect_info(p_filename):
    import configparser
    config = configparser.ConfigParser()
    config.read(p_filename)
    classes_dict = {}

    if 'RETURN_PERFECT' in config:
        gc_1 = config.get('RETURN_PERFECT', 'gc_class1', fallback='')
        assignments_1 = config.get('RETURN_PERFECT', 'assignments1', fallback='')
        gc_2 = config.get('RETURN_PERFECT', 'gc_class2', fallback='')
        assignments_2 = config.get('RETURN_PERFECT', 'assignments2', fallback='')
        gc_3 = config.get('RETURN_PERFECT', 'gc_class3', fallback='')
        assignments_3 = config.get('RETURN_PERFECT', 'assignments3', fallback='')
        gc_4 = config.get('RETURN_PERFECT', 'gc_class4', fallback='')
        assignments_4 = config.get('RETURN_PERFECT', 'assignments4', fallback='')
        gc_5 = config.get('RETURN_PERFECT', 'gc_class5', fallback='')
        assignments_5 = config.get('RETURN_PERFECT', 'assignments5', fallback='')
        gc_6 = config.get('RETURN_PERFECT', 'gc_class6', fallback='')
        assignments_6 = config.get('RETURN_PERFECT', 'assignments6', fallback='')


    else:
        raise ValueError("Need to have a file called: " +
                         str(p_filename) +
                         "\nThis file needs to have a RETURN_PERFECT section "
                         "with variables gc_1 assignments_1, and so on")
    if gc_1:
        classes = config_string_to_dict(assignments_1)
        classes_dict[gc_1] = classes
    if gc_2:
        classes = config_string_to_dict(assignments_2)
        classes_dict[gc_2] = classes
    if gc_3:
        classes = config_string_to_dict(assignments_3)
        classes_dict[gc_3] = classes
    if gc_4:
        classes = config_string_to_dict(assignments_4)
        classes_dict[gc_4] = classes
    if gc_5:
        classes = config_string_to_dict(assignments_5)
        classes_dict[gc_5] = classes
    if gc_6:
        classes = config_string_to_dict(assignments_6)
        classes_dict[gc_6] = classes

    return classes_dict


def read_return_screenshot_assignments(p_filename):
    import configparser
    config = configparser.ConfigParser()
    config.read(p_filename)
    classes_dict = {}

    if 'RETURN_SCREENSHOT_ASSIGNMENTS' in config:
        gc_1 = config.get('RETURN_SCREENSHOT_ASSIGNMENTS', 'gc_class1', fallback='')
        assignments_1 = config.get('RETURN_SCREENSHOT_ASSIGNMENTS', 'assignments1', fallback='')
        gc_2 = config.get('RETURN_SCREENSHOT_ASSIGNMENTS', 'gc_class2', fallback='')
        assignments_2 = config.get('RETURN_SCREENSHOT_ASSIGNMENTS', 'assignments2', fallback='')
        gc_3 = config.get('RETURN_SCREENSHOT_ASSIGNMENTS', 'gc_class3', fallback='')
        assignments_3 = config.get('RETURN_SCREENSHOT_ASSIGNMENTS', 'assignments3', fallback='')
        gc_4 = config.get('RETURN_SCREENSHOT_ASSIGNMENTS', 'gc_class4', fallback='')
        assignments_4 = config.get('RETURN_SCREENSHOT_ASSIGNMENTS', 'assignments4', fallback='')
        gc_5 = config.get('RETURN_SCREENSHOT_ASSIGNMENTS', 'gc_class5', fallback='')
        assignments_5 = config.get('RETURN_SCREENSHOT_ASSIGNMENTS', 'assignments5', fallback='')
        gc_6 = config.get('RETURN_SCREENSHOT_ASSIGNMENTS', 'gc_class6', fallback='')
        assignments_6 = config.get('RETURN_SCREENSHOT_ASSIGNMENTS', 'assignments6', fallback='')
        gc_7 = config.get('RETURN_SCREENSHOT_ASSIGNMENTS', 'gc_class7', fallback='')
        assignments_7 = config.get('RETURN_SCREENSHOT_ASSIGNMENTS', 'assignments7', fallback='')

    else:
        raise ValueError("Need to have a file called: " +
                         str(p_filename) +
                         "\nThis file needs to have a RETURN_SCREENSHOT_ASSIGNMENTS section "
                         "with variables gc_1 assignments_1, and so on")
    if gc_1:
        classes = config_string_to_dict(assignments_1)
        classes_dict[gc_1] = classes
    if gc_2:
        classes = config_string_to_dict(assignments_2)
        classes_dict[gc_2] = classes
    if gc_3:
        classes = config_string_to_dict(assignments_3)
        classes_dict[gc_3] = classes
    if gc_4:
        classes = config_string_to_dict(assignments_4)
        classes_dict[gc_4] = classes
    if gc_5:
        classes = config_string_to_dict(assignments_5)
        classes_dict[gc_5] = classes
    if gc_6:
        classes = config_string_to_dict(assignments_6)
        classes_dict[gc_6] = classes
    if gc_7:
        classes = config_string_to_dict(assignments_7)
        classes_dict[gc_7] = classes
    return classes_dict
