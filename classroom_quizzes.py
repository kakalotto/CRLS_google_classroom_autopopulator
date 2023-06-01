from generate_classroom_credential import generate_classroom_credential
from helper_functions.read_ini_functions import read_quizzes_info
from helper_functions.post_assignment import post_assignment


# Read in info
config_filename = "crls_teacher_tools.ini"
print(f"Opening up this config file now: {config_filename}")
quiz_info_dict = read_quizzes_info(config_filename)
print(quiz_info_dict)

topic = 'Quizzes/Tests'
title = 'Quiz ' + str(quiz_info_dict['title'])
days_to_complete = 0
text = 'Good luck!'
attachments = quiz_info_dict['quiz1_link']
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

 # id = post_assignment(topic, title, days_to_complete, text, attachments,
 #                     due_date, assignment_counter, course_description, course_id,
 #                     '', '', service_classroom, points)
# single_id = post_assignment(assignment_announcement['topic'], assignment_announcement['title'],
#                             assignment_announcement['days_to_complete'],
#                             assignment_announcement['text'],
#                             assignment_announcement['attachments'],
#                             day_info['date'], assignment_counter, course_section,
#                             course_id, spreadsheet_id, service_sheets, service_classroom,
#                             points, )

print()