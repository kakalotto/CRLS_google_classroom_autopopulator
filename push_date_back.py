import re
import datetime
from generate_sheets_credential import generate_sheets_credential
from generate_classroom_credential import generate_classroom_credential

from helper_functions.sheets_functions import read_in_holidays
from helper_functions.get_due_time import get_due_time

# stuff is from post_assignment_reschedule


COURSE_ID = 263541763318
SPREADSHEET_ID = '1ZenTcQlCQhbYvBvPOVq8XIB2FQgseIGHH4gTBTcw-KY'
days_to_move = 1
after_this_date_obj = datetime.datetime(2021,1,20)


one_day_obj = datetime.timedelta(days=1)
service_classroom = generate_classroom_credential()
service_sheet = generate_sheets_credential()
course_results = service_classroom.courses().get(id=COURSE_ID).execute()
course_section = course_results['section']


holidays = read_in_holidays(SPREADSHEET_ID, service_sheet)
holidays_obj = []
format_str = '%m/%d/%Y'
for holiday in holidays:
    p_post_day_obj = datetime.datetime.strptime(holiday, format_str)
    holidays_obj.append(p_post_day_obj)


[due_hour, due_minute]  = get_due_time(3, course_section)
print(due_hour, due_minute)
assignments = service_classroom.courses().courseWork().list(courseId=COURSE_ID).execute()
if 'courseWork' in assignments:
    assignments_list = assignments['courseWork']

    for assignment in assignments_list:
        due_year = assignment['dueDate']['year']
        due_month = assignment['dueDate']['month']
        due_day = assignment['dueDate']['day']
        assignment_due_obj = datetime.datetime(due_year, due_month, due_day)
        new_assignment_due_obj = assignment_due_obj
        if assignment_due_obj > after_this_date_obj:
            print("due {}".format(assignment_due_obj))
            print("after this {}".format(after_this_date_obj))

            print(assignment)
            coursework_id = assignment['id']
            counter = 0
            while counter < days_to_move:
                new_assignment_due_obj += one_day_obj
                if new_assignment_due_obj.isoweekday() == 7 or new_assignment_due_obj.isoweekday() == 6:
                    continue
                else:
                    holiday_match = False
                    for holiday_obj in holidays_obj:
                        if new_assignment_due_obj == holiday_obj:
                            holiday_match = True
                            break
                    if holiday_match is False:
                        counter += 1
            if assignment['dueTime']:

                update = {'dueDate': {"year": new_assignment_due_obj.year,
                                      "month": new_assignment_due_obj.month,
                                      "day": new_assignment_due_obj.day,
                                      },
                          'dueTime': {"hours": due_hour,
                                      "minutes": due_minute,
                                      "seconds": 0},
                          }
                print('update' + str(update))
                assignment = service_classroom.courses().courseWork().patch(courseId=COURSE_ID,
                                                                              id=coursework_id,
                                                                              updateMask='dueDate,'
                                                                                         'dueTime,',
                                                                              body=update).execute()
            else:
                update = {'dueDate': {"year": new_assignment_due_obj.year,
                                      "month": new_assignment_due_obj.month,
                                      "day": new_assignment_due_obj.day,
                                      },
                          'dueTime': {"hours":  4,
                                      "minutes": 59,
                                      "seconds": 0},
                          }
                print('update' + str(update))
            assignment = service_classroom.courses().courseWork().patch(courseId=COURSE_ID,
                                                                        id=coursework_id,
                                                                        updateMask='dueDate,'
                                                                                   'dueTime,',
                                                                        body=update).execute()


assignments = service_classroom.courses().courseWork().list(courseId=COURSE_ID, courseWorkStates = 'DRAFT' ).execute()
if 'courseWork' in assignments:
    assignments_list = assignments['courseWork']

    for assignment in assignments_list:
        due_year = assignment['dueDate']['year']
        due_month = assignment['dueDate']['month']
        due_day = assignment['dueDate']['day']
        assignment_due_obj = datetime.datetime(due_year, due_month, due_day)
        new_assignment_due_obj = assignment_due_obj
        if assignment_due_obj > after_this_date_obj:
            print("due {}".format(assignment_due_obj))
            print("after this {}".format(after_this_date_obj))

            print(assignment)
            coursework_id = assignment['id']
            counter = 0
            while counter < days_to_move:
                new_assignment_due_obj += one_day_obj
                if new_assignment_due_obj.isoweekday() == 7 or new_assignment_due_obj.isoweekday() == 6:
                    continue
                else:
                    holiday_match = False
                    for holiday_obj in holidays_obj:
                        if new_assignment_due_obj == holiday_obj:
                            holiday_match = True
                            break
                    if holiday_match is False:
                        counter += 1
            if assignment['dueTime']:

                update = {'dueDate': {"year": new_assignment_due_obj.year,
                                      "month": new_assignment_due_obj.month,
                                      "day": new_assignment_due_obj.day,
                                      },
                          'dueTime': {"hours": due_hour,
                                      "minutes": due_minute,
                                      "seconds": 0},
                          }
                print('update' + str(update))
                assignment = service_classroom.courses().courseWork().patch(courseId=COURSE_ID,
                                                                            id=coursework_id,
                                                                            updateMask='dueDate,'
                                                                                       'dueTime,',
                                                                            body=update).execute()
            else:
                update = {'dueDate': {"year": new_assignment_due_obj.year,
                                      "month": new_assignment_due_obj.month,
                                      "day": new_assignment_due_obj.day,
                                      },
                          'dueTime': {"hours": 4,
                                      "minutes": 59,
                                      "seconds": 0},
                          }
                print('update' + str(update))
            assignment = service_classroom.courses().courseWork().patch(courseId=COURSE_ID,
                                                                        id=coursework_id,
                                                                        updateMask='dueDate,'
                                                                                   'dueTime,',
                                                                        body=update).execute()


