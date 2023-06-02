# Inputs:
# Output: assignment ID (int)


def post_assignment(p_topic, p_title, p_days_to_complete, p_text, p_attachments, p_date, p_offset,
                    p_course_description,
                    p_course_id, p_spreadsheet_id, p_service_sheet, p_service_classroom, p_points, *,
                    due_time_obj='', post_time_obj=''):
    import re
    import googleapiclient
    from datetime import timedelta
    from helper_functions.get_due_date import get_due_date
    from helper_functions.classroom_functions import get_due_time
    from helper_functions.date_to_ISO8601 import date_to_iso8601
    from helper_functions.get_topic_ids import get_topic_ids
    import datetime

    # Misc. data formatting
    days = p_date.split('/')
    year = int(days[2])
    month = int(days[0])
    dom = int(days[1])

    # Get due date
    post_day = str(month) + '-' + str(dom) + '-' + str(year)
    if p_spreadsheet_id:
        due_date_obj = get_due_date(post_day, p_days_to_complete, p_spreadsheet_id, p_service_sheet)
    else:
        due_date_obj = datetime.datetime(year=year, month=month, day=dom)
    # due_date_obj = due_date_obj  # - timedelta(days=1)

    # get topic IDs
    topic_dict = get_topic_ids(p_course_id, p_service_classroom)

    # Get due time (searched course description for P1, P2, P3, P4)
    if not due_time_obj:
        [due_hour, due_minute] = get_due_time(p_days_to_complete, p_course_description)
        due_hour = int(due_hour)
        due_hour += 7
    else:
        due_time_obj = due_time_obj + datetime.timedelta(hours=4)
        due_hour = due_time_obj.hour
        due_minute = due_time_obj.minute
    due_date_obj = due_date_obj.replace(hour=int(due_hour), minute=int(due_minute))
    print(f"due date obj! in post {due_date_obj}")
    # get scheduled time.  Stagger entries so not all at once.
    new_scheduled_time = date_to_iso8601(month, dom, year, p_offset)
    # print(new_scheduled_time)
    if post_time_obj:
        post_time_obj = post_time_obj + datetime.timedelta(hours=4)
        new_scheduled_time = re.sub('T.*?$','', new_scheduled_time, re.X | re.M | re. S)
        post_time_hour = str(post_time_obj.hour)
        if len(post_time_hour) == 1:
            post_time_hour = '0' + post_time_hour
        post_time_minute = str(post_time_obj.minute)
        if len(post_time_minute) == 1:
            post_time_minute = '0' + post_time_minute
        new_scheduled_time = new_scheduled_time + 'T' + post_time_hour + ':' + post_time_minute + ':00Z'
    if p_topic not in topic_dict.keys():
        raise Exception("The topic you want to post this under: {}, is not in the list of topics for the class.\n"
                        "Please add this topic into the class, or else change the topic of the assignment.\n"
                        "If you think the topic is actually there, maybe you put a space in front of it.\n"
                        "In the courses tab, the topics are separated by commas, no spaces in between."
                        .format(p_topic,))
    assignment = {
        'title': p_title,
        'description': p_text,
        'materials': p_attachments,
        'dueDate': {"year": due_date_obj.year,
                    "month": due_date_obj.month,
                    "day": due_date_obj.day,
                    },
        'dueTime': {"hours": due_date_obj.hour,
                    "minutes": due_date_obj.minute,
                    "seconds": 0},
        'topicId': topic_dict[p_topic],
        'scheduledTime': new_scheduled_time,
        'workType': 'ASSIGNMENT',
        'state': 'DRAFT',
        'maxPoints': p_points,
    }
    try:
        print("In post_assignment, posting this " + str(assignment))
        assignment = p_service_classroom.courses().courseWork().create(courseId=p_course_id, body=assignment).execute()
        assignment_id = assignment.get('id')
        print("posting this assignment" + str(assignment))
    except googleapiclient.errors.HttpError:
        raise Exception("'Request contains an invalid argument' - is the topic you want for this assignment one that "
                        "exists in this class within Google classroom?\n"
                        "Alternatively, if there is a message 'materials: Duplicate materials are not allowed', you"
                        "probably have two of the same link on your lesson plan.\n"
                        "Alternatively, did you update your b1 cell, classroom ID?")
    return assignment_id

#
# from generate_classroom_credential import generate_classroom_credential
# from generate_sheets_credential import generate_sheets_credential
#
# service_classroom = generate_classroom_credential()
# service_sheet = generate_sheets_credential()
# offset = 1
# abc = post_assignment('AP_testing', 'test assignment', 5, 'do this assignment or else', [], '5/5/2019', offset,
#                     'S1, P2',
#                       36512536321, '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA', service_sheet, service_classroom)

# course_id = 36500789911  # test_APCSP_Computer_Principles
# abc = post_assignment(1, 'MCAS GOOD LUCK', '5/28/2019', course_id, service_classroom)
# print(abc)

def change_assignment_assignees(p_course_id, p_students_to_add, p_students_to_remove,
                                p_coursework_id, p_service_classroom):
    ModifyIndividualStudentsOptions = {
            "addStudentIds": p_students_to_add,
            "removeStudentIds": p_students_to_remove
        }
    assigneeMode = {
        "assigneeMode": "INDIVIDUAL_STUDENTS",
        "modifyIndividualStudentsOptions": ModifyIndividualStudentsOptions
    }
    assigneeMode = p_service_classroom.courses().courseWork().modifyAssignees(courseId=p_course_id,
                                                                              id=p_coursework_id,
                                                                              body=assigneeMode).execute()
    return assigneeMode

# def change_assignee_mode(course_id, assignment_title, assignment_desc, students_this_is_for, students_this_isnt_for, p_version, p_dueDate, p_todaysDate, p_todayTime, regMin):
#     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     service = build('classroom', 'v1', credentials=creds)
#     try:
#         print("Hello starting change!")
#         ModifyIndividualStudentsOptions = {
#             "addStudentIds": [
#                 students_this_is_for
#             ],
#             "removeStudentIds": [
#                 students_this_isnt_for
#             ]
#         }
#         assigneeMode = {
#             "assigneeMode": "INDIVIDUAL_STUDENTS",
#             "modifyIndividualStudentsOptions": ModifyIndividualStudentsOptions
#
#         }
#         courseworkId = classroom_create_coursework(588321485718, p_version, p_dueDate, p_todaysDate, p_todayTime, regMin).get('id')
#         print(f"This is the courseworkID {courseworkId}")
#         assigneeMode = service.courses().courseWork().modifyAssignees(courseId=course_id, id=courseworkId, body=assigneeMode).execute()
#         return assigneeMode
#     except HttpError as error:
#         print(f"An error occurred: {error}")
#         return error