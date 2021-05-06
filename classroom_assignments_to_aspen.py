

def classroom_assignments_to_aspen(p_gc_classname, p_aspen_classname,*, content_knowledge_completion=False,
                                   ignore_ungraded=False,
                                   username='', password=''):
    from generate_classroom_credential import generate_classroom_credential
    from helper_functions.aspen_functions import generate_driver, aspen_login, goto_assignment, add_assignments, \
        check_new_aspen_names
    from helper_functions.quarters import which_quarter_today
    from helper_functions.classroom_functions import get_assignments_from_classroom, class_name_2_id, \
        verify_due_date_exists, verify_points_exists
    from helper_functions.db_functions import create_connection, execute_sql, query_db
    import datetime
    import time

    # Get current quarter's start date
    today_quarter_obj = which_quarter_today()
    service_classroom = generate_classroom_credential()
    course_id = class_name_2_id(service_classroom, p_gc_classname)
    courseworks = get_assignments_from_classroom(service_classroom, course_id, today_quarter_obj)
    check_new_aspen_names(courseworks, content_knowledge_completion)
    verify_due_date_exists(courseworks)
    if ignore_ungraded is False:
        verify_points_exists(courseworks)
    else:
        print("We are ignoring assignments without a maxpoint value in Google classroom.")
    print("Here are the list of assignments we are putting in:")
    for coursework in courseworks:
        print(coursework['title'])
    print()


    # DB stuff; create connection, add table if not there, select all, remove duplicates from coursework
    print("Opening up the sqlite DB, which has info about classes that have already been put in Aspen.\n"
          "If you need something to edit this manually: https://sqlitebrowser.org/")
    db_filename = 'classroom_assignments_to_aspen' + p_gc_classname + '.db'
    db_conn = create_connection(db_filename)
    sql = 'CREATE TABLE IF NOT EXISTS aspen_assignments (id varchar(60) PRIMARY KEY);'
    execute_sql(db_conn, sql)
    sql = 'SELECT * FROM aspen_assignments;'
    rows = query_db(db_conn, sql)
    print(rows)
    new_courseworks = []
    for coursework in courseworks:
        found = False
        if coursework['title'] in rows:
            found = True
        if found is False:
            new_courseworks.append(coursework)
    courseworks = new_courseworks

    print(courseworks)
    # Aspen
    driver = generate_driver()
    aspen_login(driver, username=username, password=password)
    goto_assignment(driver,p_aspen_classname)
    add_assignments(driver, courseworks, content_knowledge_completion, db_conn)

    time.sleep(5)
