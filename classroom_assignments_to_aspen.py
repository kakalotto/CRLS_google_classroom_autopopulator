

def classroom_assignments_to_aspen(p_gc_classname, p_aspen_classname, *, content_knowledge_completion=False,
                                   ignore_ungraded=False,
                                   username='', password='', default_category='', ignore_noduedate=False):
    # from generate_classroom_credential import generate_classroom_credential
    from helper_functions.aspen_functions import generate_driver, aspen_login, add_assignments, \
        check_new_aspen_names, get_assignments_from_aspen, goto_assignments
    from helper_functions.quarters import which_quarter_today
    from helper_functions.classroom_functions import get_assignments_from_classroom, class_name_2_id, \
        verify_due_date_exists, verify_points_exists, scrub_courseworks
    from helper_functions.db_functions import create_connection, execute_sql, query_db
    import time
    import re
    from generate_classroom_aspen_tools_credentials import generate_classroom_aspen_tools_credentials


    # Get current quarter's start date, get gc assignments,
    today_quarter_obj = which_quarter_today()
    [service_classroom, service_sheets, service_doc] = generate_classroom_aspen_tools_credentials()

    # service_classroom = generate_classroom_credential()
    course_id = class_name_2_id(service_classroom, p_gc_classname)
    courseworks = get_assignments_from_classroom(service_classroom, course_id, today_quarter_obj)
    # for coursework in courseworks:
    #     print(coursework)
    print(f"The name of the class is this: {p_gc_classname}")
    if p_gc_classname == 'AP Computer Science Principles':
        return

    # Print out for testing purposes1
    # print("initial courses")
    # for coursework in courseworks:
    #     print(coursework)
    # print()

    # Crash out if there are conflict of names that would go into Aspen
    print("Checking for name conflict in Aspen")
    check_new_aspen_names(courseworks, content_knowledge_completion)

    print("Getting rid of smileyfaces")
    new_courseworks = []
    for coursework in courseworks:
        if re.search(r':-\)', coursework['title']):
            print("Skipping this assignment has a smiley face by it:" + str(coursework['title']))
            continue
        else:
            new_courseworks.append(coursework)
    courseworks = new_courseworks

    # Crash out if there is no due date for assignment
    print("Crashing if no due date for assignment")
    courseworks = verify_due_date_exists(courseworks, ignore_noduedate)


    # Crash out if there are no points for any assignment
    print("Crashing if no points for assignment")
    if ignore_ungraded is False:
        verify_points_exists(courseworks)
    else:
        print("We are ignoring assignments without a maxpoint value in Google classroom.")

    # DB stuff; create connection, add table if not there, select all, remove duplicates from coursework
    print("Here is the list of assignments we are putting in:")

    print("Opening up the sqlite DB, which has info about classes that have already been put in Aspen.\n"
          "If you need something to edit this manually: https://sqlitebrowser.org/")
    db_filename = 'database_gc_assignments_put_in_aspen_' + p_gc_classname + '.db'
    db_conn = create_connection(db_filename)
    print("connection created")
    sql = 'CREATE TABLE IF NOT EXISTS aspen_assignments (id varchar(60) PRIMARY KEY, date varchar(60));'
    # sql = 'CREATE TABLE IF NOT EXISTS aspen_assignments (id varchar(60) PRIMARY KEY);'

    execute_sql(db_conn, sql)
    sql = 'SELECT * FROM aspen_assignments;'
    style = ''
    rows = query_db(db_conn, sql)
    if rows and len(rows[0]) == 1:
        print("classroom_assignments_to_aspen: old style")
        previous_assignments = [x[0] for x in rows]
        style = 'no_due_dates'
    else:
        print("classroom_assignments_to_aspen: new style")
        previous_assignments = []
        for row in rows:
            previous_assignments.append([row[0], row[1]])
        style = 'due_dates'
    print(f"fff previous_assignments are here, extracted from the DB!! {previous_assignments}")

#    raise Exception("testing")
    courseworks = scrub_courseworks(courseworks, 'The assignment database', previous_assignments,
                                    content_knowledge_completion)

    # Print out for testing purposes
    # print("clasroom_assignments_to_aspen, post scrub all courseworks")
    # for coursework in courseworks:
    #      print(coursework['title'])

    if len(courseworks) == 0:
        print("No assignments to enter into Aspen!")
    else:
        print("classroom _assignments_to_aspen Here are the final courseworks!")
        for course in courseworks:
            print(course['title'])
        # Aspen
        driver = generate_driver()
        aspen_login(driver, username=username, password=password)
        goto_assignments(driver, p_aspen_classname)
        aspen_assignments = get_assignments_from_aspen(driver)
        courseworks = scrub_courseworks(courseworks, 'Aspen', aspen_assignments, content_knowledge_completion)

        print("The Final list of courses we are going to try to put in is this:")
        for coursework in courseworks:
            print(coursework['title'])
        add_assignments(driver, courseworks, content_knowledge_completion, db_conn, default_category, style)
        driver.close()
