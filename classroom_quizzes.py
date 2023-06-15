from generate_classroom_credential import generate_classroom_credential
from helper_functions.read_ini_functions import read_quizzes_info, read_period_info
from helper_functions.post_assignment import post_assignment, change_assignment_assignees
import datetime
import re

# Read in info
config_filename = "crls_teacher_tools.ini"
# print(f"Opening up this config file now: {config_filename}")
quiz_info_dict = read_quizzes_info(config_filename)
# print(quiz_info_dict)

topic = 'Quizzes/Tests'
title = 'Quiz ' + str(quiz_info_dict['title'])
days_to_complete = 0
text = 'Good luck!'
due_date = quiz_info_dict['due_date']
# need date for day_info
assignment_counter = 0
# need ID course
# spreadsheet ID? nah
service_classroom = generate_classroom_credential()
course_id = quiz_info_dict['course_id']
course_results = service_classroom.courses().get(id=course_id).execute()
course_description = course_results['section']
points = 25
quiz_length = quiz_info_dict['quiz_length']
quiz1_id = quiz_info_dict['quiz1_id']
quiz2_id = quiz_info_dict['quiz2_id']

# quiz_list = [] + datetime.timedelta(hours=7)
column_dict = {}
column_dict['assignment_or_announcement'] = 'assignment'
column_dict['points'] = points
column_dict['topic'] = topic
column_dict['title'] = title + ' :-)'
column_dict['days_to_complete'] = 0
attachments_1 = []
p_material_1 = {
    'driveFile': {
        'driveFile': {'id': quiz1_id},
        'shareMode': 'STUDENT_COPY',
    }
}
attachments_1.append(p_material_1)
attachments_2 = []
p_material_2 = {
    'driveFile': {
        'driveFile': {'id': quiz2_id},
        'shareMode': 'STUDENT_COPY',
    }
}
attachments_2.append(p_material_2)

quiz1_assignees_list = quiz_info_dict['quiz1_assignees'].split(',')
quiz2_assignees_list = quiz_info_dict['quiz2_assignees'].split(',')
quiz1_et_assignees_list = quiz_info_dict['quiz1_et_assignees'].split(',')
quiz2_et_assignees_list = quiz_info_dict['quiz2_et_assignees'].split(',')

print(f"description {course_description}")


period_info_dict = read_period_info(config_filename)

print(due_date)

# Find out what is the quiz date
due_date_list = due_date.split('/')
year = due_date_list[2]
month = due_date_list[0]
dom = due_date_list[1]
date_obj = datetime.datetime(year=int(year), month=int(month), day=int(dom))
period_dict = {}
if date_obj.weekday() == 3 or date_obj.weekday() == 4:
    period_dict['p1'] = period_info_dict['p1cm']
    period_dict['p2'] = period_info_dict['p2cm']
    period_dict['p3'] = period_info_dict['p3cm']
    period_dict['p4'] = period_info_dict['p4cm']
else:
    period_dict['p1'] = period_info_dict['p1']
    period_dict['p2'] = period_info_dict['p2']
    period_dict['p3'] = period_info_dict['p3']
    period_dict['p4'] = period_info_dict['p4']

if re.search('[pP]1', course_description, re.X | re.M | re.S):
    start_time = period_dict['p1']
elif re.search('[pP]2', course_description, re.X | re.M | re.S):
    start_time = period_dict['p2']
elif re.search('[pP]3', course_description, re.X | re.M | re.S):
    start_time = period_dict['p3']
elif re.search('[pP]4', course_description, re.X | re.M | re.S):
    start_time = period_dict['p4']
else:
    start_time = period_dict['p4']

start_time_list = start_time.split(':')
start_time_hour = start_time_list[0]
start_time_minute = start_time_list[1]
start_time_obj = datetime.datetime(year=int(year), month=int(month), day=int(dom),
                                   hour=int(start_time_hour), minute=int(start_time_minute))
# print(period_dict)
# print(start_time_obj)

if date_obj.weekday() == 3 or date_obj.weekday() == 4:
    due_time_obj = start_time_obj + datetime.timedelta(minutes=75)
else:
    due_time_obj = start_time_obj + datetime.timedelta(minutes=85)

post_time_obj = due_time_obj - datetime.timedelta(minutes=int(quiz_length)) \
                    - datetime.timedelta(minutes=5)
post_time_obj_et = post_time_obj - datetime.timedelta(minutes=int(0.5 * int(quiz_length)))

print(due_time_obj)
print(post_time_obj)

# quiz1
assignment_id = post_assignment(topic, title, days_to_complete, text, attachments_1,
                                due_date, assignment_counter, course_description, course_id,
                                '', '', service_classroom, points, due_time_obj=due_time_obj,
                                post_time_obj=post_time_obj)
mode = change_assignment_assignees(course_id, quiz1_assignees_list, [], assignment_id, service_classroom)

# quiz2
assignment_id = post_assignment(topic, title, days_to_complete, text, attachments_2,
                                due_date, assignment_counter, course_description, course_id,
                                '', '', service_classroom, points, due_time_obj=due_time_obj,
                                post_time_obj=post_time_obj)

mode = change_assignment_assignees(course_id, quiz2_assignees_list, [], assignment_id, service_classroom)

# quiz1 et
assignment_id = post_assignment(topic, title + ' ET', days_to_complete, text, attachments_1,
                                due_date, assignment_counter, course_description, course_id,
                                '', '', service_classroom, points, due_time_obj=due_time_obj,
                                post_time_obj=post_time_obj_et)
print(quiz1_et_assignees_list)

mode = change_assignment_assignees(course_id, quiz1_et_assignees_list, [], assignment_id, service_classroom)

# quiz 2 et
assignment_id = post_assignment(topic, title + ' ET', days_to_complete, text, attachments_2,
                                due_date, assignment_counter, course_description, course_id,
                                '', '', service_classroom, points, due_time_obj=due_time_obj,
                                post_time_obj=post_time_obj_et)
print(quiz2_et_assignees_list)
mode = change_assignment_assignees(course_id, quiz2_et_assignees_list, [], assignment_id, service_classroom)

# single_id = post_assignment(assignment_announcement['topic'], assignment_announcement['title'],
#                             assignment_announcement['days_to_complete'],
#                             assignment_announcement['text'],
#                             assignment_announcement['attachments'],
#                             day_info['date'], assignment_counter, course_section,
#                             course_id, spreadsheet_id, service_sheets, service_classroom,
#                             points, )

print()
