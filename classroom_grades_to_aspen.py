def classroom_grades_to_aspen(p_gc_classname, p_aspen_classname, *, content_knowledge_completion=False,
                              username='', password='', p_config_filename='crls_teacher_tools.ini',
                              p_ignore_noduedate=False):
    from generate_ro_classroom_credential import generate_ro_classroom_credential
    from helper_functions.aspen_functions import generate_driver, aspen_login,  goto_assignments_this_quarter, \
        goto_scores_this_quarter, get_student_ids_from_aspen, get_assignments_and_assignment_ids_from_aspen, \
        input_assignments_into_aspen
    from helper_functions.quarters import which_quarter_today, which_quarter_today_string
    from helper_functions.classroom_functions import get_assignments_from_classroom, class_name_2_id, \
        get_student_profiles, get_assignment_scores_from_classroom, scrub_assignment_scores_student_id, \
        verify_due_date_exists
    from helper_functions.db_functions import create_connection, execute_sql, query_db
    import time

    # Get current quarter's start date, get gc assignments,
    print("Transferring this classroom's grades:" + str(p_gc_classname) +
          " to this aspen class " + str(p_aspen_classname))
    today_quarter_obj = which_quarter_today(p_filename=p_config_filename)
    service_classroom = generate_ro_classroom_credential()
    course_id = class_name_2_id(service_classroom, p_gc_classname)
    courseworks = get_assignments_from_classroom(service_classroom, course_id, today_quarter_obj)

    print("Here are the Google classroom assignments from this quarter or with no due date")
    for coursework in courseworks:
        print(coursework['title'])

    # Crash out if there is no due date for assignment unless p_ignore_noduedaste is True.
    courseworks = verify_due_date_exists(courseworks, p_ignore_noduedate)
    print("\nHere are the Google classroom assignments that we will try to process")
    for coursework in courseworks:
        print(coursework['title'])


    # Get student profiles
    gc_student_profiles = get_student_profiles(service_classroom, course_id)
    print("Here are Google classroom student profiles")
    print(gc_student_profiles)
    num_gc_students = len(gc_student_profiles
                          )
    # Use gc assignments and student profiles to figure out which scores I potentially want to record.
    print("Using student profiles to find potential grades to put into Aspen")
    gc_assignment_scores_student_id = get_assignment_scores_from_classroom(service_classroom, gc_student_profiles,
                                                                           courseworks, course_id)
    print("Here are the original Google classroom assignments, students, and IDs")
    for key in gc_assignment_scores_student_id:
        print(f"{key}         {gc_assignment_scores_student_id[key]}")

    # Get the DB stuff and clean the data
    db_filename = 'database_gc_grades_put_in_aspen_' + p_aspen_classname + '.db'
    db_conn = create_connection(db_filename)
    # sql = 'CREATE TABLE IF NOT EXISTS recorded_scores (id varchar(60) PRIMARY KEY, assignment varchar(60),' \
    #       'name varchar(60), score integer NOT NULL );'
    sql = 'CREATE TABLE IF NOT EXISTS  "recorded_scores" ("id"	varchar(60), "assignment"	varchar(60), ' \
          '"name"	varchar(60), "score" integer NOT NULL, PRIMARY KEY("id","score"));'
    execute_sql(db_conn, sql)

    # sql = 'ALTER TABLE recorded_scores DROP PRIMARY KEY '
    # execute_sql(db_conn, sql)
    # sql = 'ALTER TABLE  recorded_scores  ADD CONSTRAINT PK_CUSTID PRIMARY KEY (id, score);'
    # execute_sql(db_conn, sql)
    sql = 'SELECT * FROM recorded_scores;'
    rows = query_db(db_conn, sql)
    gc_assignment_scores_student_id = scrub_assignment_scores_student_id(gc_assignment_scores_student_id, rows)
    print("Here are the scrubbed Google classroom assignments, students, and IDs (removing ones that have already "
          "been put in the database)")
    for key in gc_assignment_scores_student_id:
        print(f"{key}         {gc_assignment_scores_student_id[key]}")

    # Logon to Aspen
    if len(gc_assignment_scores_student_id) != 0:
        print("Opening up Aspen now")
        driver = generate_driver()
        aspen_login(driver, username=username, password=password)

        # Get this quarter's assignments from aspen
        print("Getting this quarter's assignments from Aspen")
        quarter = which_quarter_today_string()
        goto_assignments_this_quarter(driver, p_aspen_classname, quarter)
        aspen_assignments = get_assignments_and_assignment_ids_from_aspen(driver)
        print("Here are the aspen assignments and IDs from this quarter:")
        for key in aspen_assignments:
            print(f"{key}       {aspen_assignments[key]}")

        # Put in the scores
        students_done = False
        while students_done is False:
            print("Getting the Aspen student ID's")
            goto_scores_this_quarter(driver, p_aspen_classname, quarter)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            aspen_students = get_student_ids_from_aspen(driver)
            print("here are the  aspen student IDs")
            for key in aspen_students:
                print(f"{key}        {aspen_students[key]}")
            if len(aspen_students) + 6 > num_gc_students:
                students_done = True

        print("Putting in the grades now")
        input_assignments_into_aspen(driver, gc_assignment_scores_student_id, aspen_students,
                                     aspen_assignments,
                                     content_knowledge_completion, db_conn)
        print("All done!")
        driver.close()
    else:
        print("No assignments to input grades for for this class.  Next!\n\n\n")



