import re
from helper_functions.aspen_functions import generate_driver, aspen_login, add_assignments, \
    check_new_aspen_names, get_assignments_from_aspen, goto_assignments
from helper_functions.classroom_functions import scrub_courseworks
from helper_functions.quarters import which_quarter_today
from helper_functions.db_functions import execute_sql, query_db, create_connection
from helper_functions.skills_functions import date_to_classroom_due_date, date_to_classroom_creation_date

today_quarter_obj = which_quarter_today()
dates = ['9/3/2024',
         '9/4/2024',
         '9/5/2024',
         '9/6/2024',
         '9/9/2024',
         '9/10/2024',
         '9/11/2024',
         '9/12/2024',
         '9/13/2024',
         '9/16/2024',
         '9/17/2024',
         '9/18/2024',
         '9/19/2024',
         '9/20/2024',
         '9/23/2024',
         '9/24/2024',
         '9/25/2024',
         '9/26/2024',
         '9/27/2024',
         '9/30/2024',
         '10/1/2024',
         '10/2/2024',
         '10/4/2024',
         '10/7/2024',
         '10/8/2024',
         '10/9/2024',
         '10/10/2024',
         '10/11/2024',
         '10/15/2024',
         '10/16/2024',
         '10/17/2024',
         '10/18/2024',
         '10/21/2024',
         '10/22/2024',
         '10/23/2024',
         '10/24/2024',
         '10/25/2024',
         '10/28/2024',
         '10/29/2024',
         '10/30/2024',
         '10/31/2024',
         '11/1/2024',
         '11/4/2024',
         '11/6/2024',
         '11/7/2024',
         '11/8/2024',
         '11/12/2024',
         '11/13/2024',
         '11/14/2024',
         '11/15/2024',
         '11/18/2024',
         '11/19/2024',
         '11/20/2024',
         '11/21/2024',
         '11/22/2024',
         '11/25/2024',
         '11/26/2024',
         '11/27/2024',
         '12/2/2024',
         '12/3/2024',
         '12/4/2024',
         '12/5/2024',
         '12/6/2024',
         '12/9/2024',
         '12/10/2024',
         '12/11/2024',
         '12/12/2024',
         '12/13/2024',
         '12/16/2024',
         '12/17/2024',
         '12/18/2024',
         '12/19/2024',
         '12/20/2024',
         '12/23/2024',
         '1/3/2025',
         '1/6/2025',
         '1/7/2025',
         '1/8/2025',
         '1/9/2025',
         '1/10/2025',
         '1/13/2025',
         '1/14/2025',
         '1/15/2025',
         '1/16/2025',
         '1/17/2025'
         ]
assignments_list = [
    [2, 3, 4, 5],
    [6, 7, 8],
    [9, 10, 11, 12],
    [13,14, 15, 16],
    [17, 18, 19],
    [20, 21, 22, 23],
    [25, 26, 27],
    [28, 29, 30, 31],
    [32, 33, 34,],
    [35, 36, 37],
    [38, 39, 40, 41, 42],
]

content_knowledge_completion = False
default_category = None
p_style = "no_due_dates"
# [43, 44, 45, 46, 47, 48, 49, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58],
# [59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75],
# [76, 77, 78, 79, 80, 81, 82, 83, 84, 85]
# rotation_change = [
#     2,
#     6,
#     9,
#     13,
#     17,
#     20,
#     24,
#     28,
#     32,
#     35,
#     38,
#     43,
#     59,
#     75,
# ]

aspen_username = 'ewu@cpsd.us'
aspen_password = '***REMOVED***'
course_letter = 'L'
course_prefix = 'T120'
# T120L-I-001

# Aspen

for rotation_number in range(1, 12):
    course_number = course_prefix + course_letter + '-I-00' + str(rotation_number)
    print(f"Course number xxx {course_number}")
    assignment_numbers = assignments_list[rotation_number - 1]
    assignment_names = ['day_' + str(assignment_number) for assignment_number in assignment_numbers ]
    print("Here is the list of assignments we are putting in xxx:")
    print(assignment_names)
    courseworks = []
    for assignment_name in assignment_names:
        day_number = re.sub(r'day_', '', assignment_name )
        day_number = int(day_number) - 1
        coursework = {}
        coursework['title'] = assignment_name
        coursework['state'] = 'Published'
        date = dates[day_number]
        creation_time = date_to_classroom_creation_date(date)
        coursework['creationTime'] = creation_time
        coursework['scheduledTime'] = creation_time

        due_date = date_to_classroom_due_date(date)
        print(due_date)
        coursework['dueDate'] = due_date
        coursework['maxPoints'] = 100
        courseworks.append(coursework)
    print("Printing out all courseworks")
    for coursework in courseworks:
        print(coursework)
    print("Opening up the sqlite DB, which has info about classes that have already been put in Aspen.\n"
          "If you need something to edit this manually: https://sqlitebrowser.org/")
    db_filename = 'database_gc_assignments_put_in_aspen_' + course_number + '.db'
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
    if len(courseworks) == 0:
        print("No assignments to enter into Aspen!")
    else:
        print("classroom _assignments_to_aspen Here are the final courseworks!")
        for course in courseworks:
            print(course['title'])
        driver = generate_driver()
        aspen_login(driver, username=aspen_username, password=aspen_password)
        goto_assignments(driver, course_number)
        aspen_assignments = get_assignments_from_aspen(driver)
        courseworks = scrub_courseworks(courseworks, 'Aspen', aspen_assignments, content_knowledge_completion)

        print("The Final list of courses we are going to try to put in is this:")
        for coursework in courseworks:
            print(coursework['title'])
        add_assignments(driver, courseworks, content_knowledge_completion, db_conn, default_category, style)
        driver.close()

    #
    # driver = generate_driver()
    # aspen_login(driver, username=aspen_username, password=aspen_password)
    # goto_assignments(driver, course_number)
    # aspen_assignments = get_assignments_from_aspen(driver)

#




#
#
# {'courseId': '705341860037',
# 'id': '705357370557',
# 'title': 'Electroboom',
# 'description': '𝐎𝐁𝐉𝐄𝐂𝐓𝐈𝐕𝐄𝐒:\n1.d Demonstrate appropriate use of safety procedures and tools.\n1.e Explain the dangers of Electrostatic Discharge (ESD).\n1.f List the tools to protect against ESD.\n1.g Demonstrate appropriate use of ESD safety tools.\n\n𝐑𝐔𝐁𝐑𝐈𝐂: (10 points)\n- Watch the video (10 points)\n\nWe will watch this video in class together.  Click "submit" when complete.\nhttps://www.youtube.com/watch?v=RtlYi1yLTVQ\n\n',
# 'state': 'PUBLISHED',
#  'alternateLink': 'https://classroom.google.com/c/NzA1MzQxODYwMDM3/a/NzA1MzU3MzcwNTU3/details',
# 'creationTime': '2024-09-02T12:12:14.707Z',
# 'updateTime': '2024-09-05T12:00:18.708Z',
# 'dueDate': {'year': 2024, 'month': 9, 'day': 6},
#  'dueTime': {'hours': 16, 'minutes': 10},
# 'maxPoints': 10,
# 'workType': 'ASSIGNMENT',
# 'submissionModificationMode': 'MODIFIABLE_UNTIL_TURNED_IN',
#  'assignment': {'studentWorkFolder': {
#                                  'id': '1eYhOQMeaxU5NflIBm0CHQChNn5o_iULmrkJpnt067r0oqK6SkvURAw3EaUokPvtC5snghCLl',
#                                 'title': 'Electroboom',
#                                'alternateLink': 'https://drive.google.com/drive/folders/1eYhOQMeaxU5NflIBm0CHQChNn5o_iULmrkJpnt067r0oqK6SkvURAw3EaUokPvtC5snghCLl'}}
#
# 'assigneeMode': 'ALL_STUDENTS',
# 'creatorUserId': '110067882309555165220',
# 'topicId': '705341948484'}
# {
#   "courseId": string,
#   "id": string,
#   "title": string,
#   "description": string,
#   "materials": [
#     {
#       object (Material)
#     }
#   ],
#   "state": enum (CourseWorkState),
#   "alternateLink": string,
#   "creationTime": string,
#   "updateTime": string,
#   "dueDate": {
#     object (Date)
#   },
#   "dueTime": {
#     object (TimeOfDay)
#   },
#   "scheduledTime": string,
#   "maxPoints": number,
#   "workType": enum (CourseWorkType),
#   "associatedWithDeveloper": boolean,
#   "assigneeMode": enum (AssigneeMode),
#   "individualStudentsOptions": {
#     object (IndividualStudentsOptions)
#   },
#   "submissionModificationMode": enum (SubmissionModificationMode),
#   "creatorUserId": string,
#   "topicId": string,
#   "gradeCategory": {
#     object (GradeCategory)
#   },
#   "previewVersion": enum (PreviewVersion),
#
#   // Union field details can be only one of the following:
#   "assignment": {
#     object (Assignment)
#   },
#   "multipleChoiceQuestion": {
#     object (MultipleChoiceQuestion)
#   }
#   // End of list of possible types for union field details.
#   "gradingPeriodId": string
# }
#