def classroom_grades_to_aspen(p_gc_classname, p_aspen_classname,*, content_knowledge_completion=False,
                              ignore_ungraded=False,
                              username='', password=''):
    from generate_classroom_credential import generate_classroom_credential
    from helper_functions.aspen_functions import generate_driver, aspen_login, goto_assignment, add_assignments, \
        check_new_aspen_names, convert_assignment_name, get_assignments_from_aspen
    from helper_functions.quarters import which_quarter_today
    from helper_functions.classroom_functions import get_assignments_from_classroom, class_name_2_id, \
        verify_due_date_exists, verify_points_exists, scrub_courseworks
    from helper_functions.db_functions import create_connection, execute_sql, query_db
    import time
    import re

    # Get current quarter's start date, get gc assignments,
    today_quarter_obj = which_quarter_today()
    service_classroom = generate_classroom_credential()
    course_id = class_name_2_id(service_classroom, p_gc_classname)
    courseworks = get_assignments_from_classroom(service_classroom, course_id, today_quarter_obj)

    # Logon to Aspen
    driver = generate_driver()
    aspen_login(driver, username=username, password=password)
    goto_assignment(driver, p_aspen_classname)
    print("done!")