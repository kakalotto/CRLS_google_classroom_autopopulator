# Inputs:
# Output: assignment ID (int)


def post_assignment_reschedule(p_assignment, p_date, p_course_id, p_coursework_id, p_service_classroom,
                               p_spreadsheet_id, p_service_sheets):

    import re

    # import googleapiclient
    import datetime

    from helper_functions.date_to_ISO8601 import date_to_iso8601
    from helper_functions.read_in_holidays import read_in_holidays
    from helper_functions.get_due_date import get_due_date

    # Misc. data formatting get new schedule date year, month, day of month
    days = p_date.split('/')
    this_year = days[2]
    this_month = days[0]
    this_dom = days[1]

    print("original assign scheduled time")
    print(p_assignment['scheduledTime'])

    # Get old scheduled day and convert it to datetime format
    sched_day = re.sub(r'T.+$', '', p_assignment['scheduledTime'], re.X | re.M | re.S)
    numbers = sched_day.split('-')
    sched_year = numbers[0]
    sched_month = numbers[1]
    sched_dom = numbers[2]
    sched_month = re.sub(r'^0', '', sched_month, re.X | re.M | re.S)
    sched_dom = re.sub(r'^0', '', sched_dom, re.X | re.M | re.S)
    scheduled_day_obj = datetime.datetime(int(sched_year), int(sched_month), int(sched_dom))

    # Get old due date and convert to datetime format
    due_year = p_assignment['dueDate']['year']
    due_month = p_assignment['dueDate']['month']
    due_dom = p_assignment['dueDate']['day']
    due_day_obj = datetime.datetime(int(due_year), int(due_month), int(due_dom))

    # Get days to complete (do this instead of going back to original spreadsheet)
    days_to_complete_obj = due_day_obj - scheduled_day_obj
    strings = str(days_to_complete_obj).split(' ')
    days_to_complete = strings[0]  # gives a number like '4'
    days_to_complete = int(days_to_complete)
    # print("THIS MANY DAYS TO COPLETE ORIGINALLY " + str(days_to_complete))

    # Get ready to find new due date.  Find holidays
    holidays = read_in_holidays(p_spreadsheet_id, p_service_sheets)
    holidays_obj = []
    format_str = '%m/%d/%Y'
    for holiday in holidays:
        p_post_day_obj = datetime.datetime.strptime(holiday, format_str)
        holidays_obj.append(p_post_day_obj)
    # print(holidays_obj)

    counter = 0
    new_count_days = 0

    # New scheduled time calculate from this_month, dom, and year
    new_scheduled_time = date_to_iso8601(this_month, this_dom, this_year, 0)

    # Use these variables to help figure out how many days you were allowed to do original assignment
    day_obj = scheduled_day_obj
    one_day_obj = datetime.timedelta(days=1)

    # Calculate new_count_days, which is hopefully the original days_to_complete from lesson sheet
    while counter <= days_to_complete:
        # print("begin" + str(day_obj) + ' ' + str(day_obj.isoweekday()) + ' ' + str(counter) + ' ' +
        #       str(new_count_days))
        if day_obj.isoweekday() == 7 or day_obj.isoweekday() == 6:
            pass
        else:
            holiday_match = False
            for holiday_obj in holidays_obj:
                if day_obj == holiday_obj:
                    holiday_match = True
                    break
            if holiday_match is False:
                new_count_days += 1
        day_obj += one_day_obj
        counter += 1
    new_count_days -= 1  # counted one extra for day of assignment itself.
    # print("END!" + str(new_count_days))

    # Given new posting date and days_to_complete, calculate the new due date
    p_date = re.sub(r'/', '-', p_date, re.X | re.M | re.S)
    new_due_date_obj = get_due_date(p_date, int(new_count_days), p_spreadsheet_id, p_service_sheets)

    # print(new_due_date_obj)
    # print(new_scheduled_time)
#    raise Exception("stalling now")
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
