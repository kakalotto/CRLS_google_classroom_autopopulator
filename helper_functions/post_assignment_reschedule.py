# Inputs:
# Output: assignment ID (int)


def post_assignment_reschedule(p_assignment, p_date, p_course_id, p_coursework_id, p_service_classroom,
                               p_service_sheet):

    import re

    import googleapiclient
    import datetime

    from helper_functions.date_to_ISO8601 import date_to_iso8601

    # Misc. data formatting
    days = p_date.split('/')
    this_year = days[2]
    this_month = days[0]
    this_dom = days[1]

    print("assign scheduled time")
    print(p_assignment['scheduledTime'])
    sched_day = re.sub(r'T.+$', '', p_assignment['scheduledTime'], re.X | re.M | re.S)
    numbers = sched_day.split('-')
    sched_year = numbers[0]
    sched_month = numbers[1]
    sched_dom = numbers[2]
    sched_month = re.sub(r'^0', '', sched_month, re.X | re.M | re.S)
    sched_dom = re.sub(r'^0', '', sched_dom, re.X | re.M | re.S)
    scheduled_day_obj = datetime.datetime(int(sched_year), int(sched_month), int(sched_dom))

    due_year = p_assignment['dueDate']['year']
    due_month = p_assignment['dueDate']['month']
    due_dom = p_assignment['dueDate']['day']
    due_day_obj = datetime.datetime(int(due_year), int(due_month), int(due_dom))

    days_to_complete_obj = due_day_obj - scheduled_day_obj
    strings = days_to_complete_obj.split(' ')
    days_to_complete = strings[0]
    print("THIS MANY DAYS TO COPLETE ORIGINALLY")


    new_scheduled_time = date_to_iso8601(this_month, this_dom, this_year, 0)
    new_scheduled_time_obj = datetime.datetime(int(this_year), int(this_month), int(this_dom))

    new_due_date_obj = new_scheduled_time_obj + days_to_complete_obj

    print(days_to_complete_obj)
    print(new_due_date_obj)
    print(new_scheduled_time)
    raise Exception("stalling now")
    update = {'dueDate': {"year": new_due_date_obj.year,
                          "month": new_due_date_obj.month,
                          "day": new_due_date_obj.day,
                          },
              'dueTime': {"hours": p_assignment['dueTime']['hours'],
                          "minutes": p_assignment['dueTime']['minutes'],
                          "seconds": 0},
              'scheduledTime': new_scheduled_time,
              }
    assignment = p_service_classroom.courses().courseWork().patch(courseId=p_course_id,
                                                                  id=p_coursework_id,
                                                                  updateMask='dueDate,'
                                                                             'dueTime,'
                                                                             'scheduledTime',
                                                                  body=update).execute()
    assignment_id = assignment.get('id')
    return assignment_id

    # try:
    #     assignment = p_service_classroom.courses().courseWork().create(courseId=p_course_id, body=assignment)
    # .execute()
    #     assignment_id = assignment.get('id')
    # except googleapiclient.errors.HttpError:
    #     raise Exception("'Request contains an invalid argument' - is the topic you want for this assignment one that "
    #                     "exists in this class within Google classroom?")
    # return assignment_id

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
