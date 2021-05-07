def classroom_grades_to_aspen(p_gc_classname, p_aspen_classname, *, content_knowledge_completion=False,
                              ignore_ungraded=False,
                              username='', password=''):
    from generate_classroom_credential import generate_classroom_credential
    from helper_functions.aspen_functions import generate_driver, aspen_login, goto_assignments, \
        goto_assignments_this_quarter, goto_scores, \
        add_assignments, \
        check_new_aspen_names, convert_assignment_name, get_assignments_and_assignment_ids_from_aspen
    from helper_functions.quarters import which_quarter_today, which_quarter_today_string
    from helper_functions.classroom_functions import get_assignments_from_classroom, class_name_2_id, \
        get_student_profiles, get_assignment_scores_from_classroom, verify_due_date_exists, verify_points_exists, \
        scrub_assignment_scores_student_id
    from helper_functions.db_functions import create_connection, execute_sql, query_db
    import time
    import re

    # Get current quarter's start date, get gc assignments,
    today_quarter_obj = which_quarter_today()
    service_classroom = generate_classroom_credential()
    course_id = class_name_2_id(service_classroom, p_gc_classname)
#    courseworks = get_assignments_from_classroom(service_classroom, course_id, today_quarter_obj)

    # Get student profiles
#    student_profiles = get_student_profiles(service_classroom, course_id)
#    print("Here are student profiles")
#   for student in student_profiles:
#        print(student)

    # Use gc assignments and student profiles to figure out which scores I potentially want to record.
#    gc_assignment_scores_student_id = get_assignment_scores_from_classroom(service_classroom, student_profiles,
#                                                                           courseworks, course_id)
#    print("Original assignments, students, and IDs")
#    print(gc_assignment_scores_student_id)

    # Get the DB stuff and clean the data
    # db_filename = 'classroom_grades_to_aspen_' + p_aspen_classname + '.db'
    # db_conn = create_connection(db_filename)
    # sql = 'CREATE TABLE IF NOT EXISTS recorded_scores (id varchar(60) PRIMARY KEY, assignment varchar(60),' \
    #       'name varchar(60), score integer NOT NULL );'
    # execute_sql(db_conn, sql)
    # sql = 'SELECT * FROM recorded_scores;'
    # rows = query_db(db_conn, sql)
    # gc_assignment_scores_student_id = scrub_assignment_scores_student_id(gc_assignment_scores_student_id, rows)
    # print("scrubbed assignments, students, and IDs")
    # print(gc_assignment_scores_student_id)
    #

    # Logon to Aspen
    driver = generate_driver()
    aspen_login(driver, username=username, password=password)

    # Get this quarter's assignments from aspen
    quarter = which_quarter_today_string()
    goto_assignments_this_quarter(driver, p_aspen_classname, quarter)
    assignments_and_ids = get_assignments_and_assignment_ids_from_aspen(driver)
    print("here are the assignments and IDs")
    print(assignments_and_ids)

    # Put in the scores
    goto_scores(driver, p_aspen_classname )


    print("done!")

    time.sleep(5)

    raise ValueError("quitting on purpose")
