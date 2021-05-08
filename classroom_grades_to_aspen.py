def classroom_grades_to_aspen(p_gc_classname, p_aspen_classname, *, content_knowledge_completion=False,
                              username='', password=''):
    from generate_classroom_credential import generate_classroom_credential
    from helper_functions.aspen_functions import generate_driver, aspen_login,  goto_assignments_this_quarter, \
        goto_scores_this_quarter, get_student_ids_from_aspen, get_assignments_and_assignment_ids_from_aspen, \
        input_assignments_into_aspen
    from helper_functions.quarters import which_quarter_today, which_quarter_today_string
    from helper_functions.classroom_functions import get_assignments_from_classroom, class_name_2_id, \
        get_student_profiles, get_assignment_scores_from_classroom, scrub_assignment_scores_student_id
    from helper_functions.db_functions import create_connection, execute_sql, query_db
    import time

    # Get current quarter's start date, get gc assignments,
    today_quarter_obj = which_quarter_today()
    service_classroom = generate_classroom_credential()
    course_id = class_name_2_id(service_classroom, p_gc_classname)
    courseworks = get_assignments_from_classroom(service_classroom, course_id, today_quarter_obj)

    print("Here are the gc assignments")
    for coursework in courseworks:
        print(coursework['title'])
    # Get student profiles
    gc_student_profiles = get_student_profiles(service_classroom, course_id)
    print("Here are gc student profiles")
    print(gc_student_profiles)

    # Use gc assignments and student profiles to figure out which scores I potentially want to record.
    gc_assignment_scores_student_id = get_assignment_scores_from_classroom(service_classroom, gc_student_profiles,
                                                                           courseworks, course_id)
    print("Here are the original gc assignments, students, and IDs")
    print(gc_assignment_scores_student_id)

    # Get the DB stuff and clean the data
    db_filename = 'classroom_grades_to_aspen_' + p_aspen_classname + '.db'
    db_conn = create_connection(db_filename)
    sql = 'CREATE TABLE IF NOT EXISTS recorded_scores (id varchar(60) PRIMARY KEY, assignment varchar(60),' \
          'name varchar(60), score integer NOT NULL );'
    execute_sql(db_conn, sql)
    sql = 'SELECT * FROM recorded_scores;'
    rows = query_db(db_conn, sql)
    gc_assignment_scores_student_id = scrub_assignment_scores_student_id(gc_assignment_scores_student_id, rows)
    print("Here are the scrubbed gc assignments, students, and IDs")
    print(gc_assignment_scores_student_id)

    # Logon to Aspen
    driver = generate_driver()
    aspen_login(driver, username=username, password=password)

    # Get this quarter's assignments from aspen
    quarter = which_quarter_today_string()
    goto_assignments_this_quarter(driver, p_aspen_classname, quarter)
    aspen_assignments = get_assignments_and_assignment_ids_from_aspen(driver)
    print("here are the aspen assignments and IDs")
    print(aspen_assignments)

    # Put in the scores
    goto_scores_this_quarter(driver, p_aspen_classname, quarter)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    aspen_students = get_student_ids_from_aspen(driver)
    print("here are the  aspen student IDs")
    print(aspen_students)
    input_assignments_into_aspen(driver, gc_assignment_scores_student_id, aspen_students,
                                 aspen_assignments,
                                 content_knowledge_completion, db_conn)
    print("all done!")
    time.sleep(3)
    input("Press any key to continue")

