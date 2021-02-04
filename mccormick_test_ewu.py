from mccormick_test import create_oss_sheet

# Fill out all these
student_name = 'Eric Wu'
template_link = ''
advisory_zoom_link = 'https://zoom.us/j/9332367963?pwd=WElmWmc0dHBqSjY2MDFpaWJsbEFsdz09'
cm_zoom_link = 'https://zoom.us/j/93032197658?pwd=ZGdJbTlTcDF6RVdPSnFKeVhucExndz09'
period1_course_id = '164978129388'
period2_course_id = ''
period3_course_id = '164899277959'
period4_course_id = '164965412687'

course_ids = [period1_course_id, period2_course_id, period3_course_id, period4_course_id]



create_oss_sheet(name=student_name, advisory_link=advisory_zoom_link,cm_link=cm_zoom_link, course_ids=course_ids)