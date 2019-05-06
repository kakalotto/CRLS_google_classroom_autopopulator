# Inputs:
# Output: assignment ID (int)


def post_assignment(p_topic, p_title, p_days_to_complete, p_text, p_attachments, p_date, p_offset,
                    p_course_description,
                    p_course_id, p_spreadsheet_id, p_service_sheet, p_service_classroom):

    import googleapiclient

    from helper_functions.get_due_date import get_due_date
    from helper_functions.get_due_time import get_due_time
    from helper_functions.date_to_ISO8601 import date_to_iso8601
    from helper_functions.get_topic_ids import get_topic_ids

    # Misc. data formatting
    days = p_date.split('/')
    year = days[2]
    month = days[0]
    dom = days[1]

    # Get due date
    post_day = str(month) + '-' + str(dom) + '-' + str(year)
    due_date_obj = get_due_date(post_day, p_days_to_complete, p_spreadsheet_id, p_service_sheet)

    # get topic IDs
    topic_dict = get_topic_ids(p_course_id, p_service_classroom)

    # Get due time (searched course description for P1, P2, P3, P4)
    [due_hour, due_minute] = get_due_time(p_days_to_complete, p_course_description)
    due_date_obj = due_date_obj.replace(hour=due_hour, minute=due_minute)

    # get scheduled time.  Stagger entries so not all at once.
    new_scheduled_time = date_to_iso8601(month, dom, year, p_offset)

    if p_topic not in topic_dict.keys():
        raise Exception("The topic you want to post this under {}, is not in the list of topics for the class.\n"
                        "Please add this topic into the class, or else change the topic of the assignment"
                        .format(p_topic))
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
    }
    try:
        assignment = p_service_classroom.courses().courseWork().create(courseId=p_course_id, body=assignment).execute()
        assignment_id = assignment.get('id')
    except googleapiclient.errors.HttpError:
        raise Exception("'Request contains an invalid argument' - is the topic you want for this assignment one that "
                        "exists in this class within Google classroom?")
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
