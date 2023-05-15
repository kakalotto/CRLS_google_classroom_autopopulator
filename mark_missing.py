def mark_missing(p_gc_classname, p_aspen_classname, *,
                 username='', password='', p_config_filename='crls_teacher_tools.ini',
                 p_ignore_noduedate=False, p_use_stored_gc_students=False):
    from generate_ro_classroom_credential import generate_ro_classroom_credential
    from helper_functions.aspen_functions import generate_driver, aspen_login, goto_assignments_this_quarter, \
        goto_scores_this_quarter, get_student_ids_from_aspen, get_assignments_and_assignment_ids_from_aspen, \
        input_assignments_into_aspen
    from helper_functions.quarters import which_quarter_today, which_quarter_today_string, which_next_quarter
    from helper_functions.classroom_functions import get_assignments_from_classroom, class_name_2_id, \
        get_student_profiles, get_assignment_scores_from_classroom, scrub_assignment_scores_student_id, \
        verify_due_date_exists
    from helper_functions.db_functions import create_connection, execute_sql, query_db


    # Get current quarter's start date, get gc assignments,
    print("Marking missing for this classroom's grades:" + str(p_gc_classname) +
          " in this aspen class " + str(p_aspen_classname))
    today_quarter_obj = which_quarter_today(p_filename=p_config_filename)
    next_quarter_obj = which_next_quarter(p_filename=p_config_filename)

    service_classroom = generate_ro_classroom_credential()
    course_id = class_name_2_id(service_classroom, p_gc_classname)
    courseworks = get_assignments_from_classroom(service_classroom, course_id, today_quarter_obj,
                                                 p_next_quarter_start_obj=next_quarter_obj)

    print(courseworks)
    db_filename = 'database_gc_grades_put_in_aspen_' + p_aspen_classname + '.db'
    db_conn = create_connection(db_filename)

    # Get student profiles
    print("Getting student profiles")
    gc_student_profiles = {}
    if p_use_stored_gc_students is False:
        gc_student_profiles = get_student_profiles(service_classroom, course_id)
        print("Here are Google classroom student profiles")
        print(gc_student_profiles)

        sql = 'DELETE FROM "gc_students"'
        execute_sql(db_conn, sql)
        for id in gc_student_profiles:
            sql = 'INSERT INTO "gc_students" VALUES ( "' + id + '", "' + gc_student_profiles[id] + '" );'
            execute_sql(db_conn, sql)
    else:
        print("Using stored student profiles")
        sql = 'SELECT * FROM "gc_students";'
        rows = query_db(db_conn, sql)
        for row in rows:
            gc_student_profiles[row[0]] = row[1]
        if len(gc_student_profiles) == 0:
            raise ValueError(p_gc_classname + " has zero students according to the database.  Run this program"
                                              "with the use_stored_gc_students=0 first")
    num_gc_students = len(gc_student_profiles)
